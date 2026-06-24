#!/usr/bin/env python3
"""Regenerate all OLIT RDF artifacts from legal-taxonomy.db (deduped), with proper SKOS/OWL
deprecation semantics so the result is standards-clean:
  live      -> skos:Concept + notation + prefLabel + broader/topConceptOf + inScheme
  deprecated-> + owl:deprecated true ; dct:isReplacedBy c:<final live winner> ; skos:historyNote
Outputs: legal-taxonomy.ttl, legal-taxonomy.jsonld, scheme.ttl, dumps/concepts-<top>-<slug>.ttl
Live hierarchy contains only live concepts (deprecated drop skos:broader -> retired)."""
import os,re,json,sqlite3,glob
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB=os.path.join(REPO,"legal-taxonomy.db")
SCHEME="https://w3id.org/legal-taxonomy/scheme/olit"
CB="https://w3id.org/legal-taxonomy/concept/"
PRE=('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n'
     '@prefix dct:  <http://purl.org/dc/terms/> .\n'
     '@prefix owl:  <http://www.w3.org/2002/07/owl#> .\n'
     '@prefix c: <https://w3id.org/legal-taxonomy/concept/> .\n\n')
def esc(s): return s.replace('\\','\\\\').replace('"','\\"')
def slug(label): return re.sub(r'[^a-z0-9]+','-',label.lower())[:40].strip('-')

con=sqlite3.connect(DB)
rows=con.execute("SELECT notation,pref_label,broader,depth,top_domain,deprecated,COALESCE(replaced_by,'') FROM concepts ORDER BY notation").fetchall()
repl={n:rb for n,l,b,d,td,dep,rb in rows if rb}
def final_winner(n):
    seen=set()
    while n in repl and n not in seen: seen.add(n); n=repl[n]
    return n
dep_of={n:dep for n,l,b,d,td,dep,rb in rows}

def ttl_block(n,l,b,d,td,dep,rb):
    out=[f'c:{n} a skos:Concept ;',f'  skos:notation "{n}" ;',f'  skos:prefLabel "{esc(l)}"@en ;']
    if dep:
        w=final_winner(n)
        out.append('  owl:deprecated true ;')
        out.append(f'  dct:isReplacedBy c:{w} ;')
        out.append(f'  skos:historyNote "Deduplicated 2026-06: merged into c:{w} ({esc(dict_label.get(w,""))})."@en ;')
    else:
        if d==1: out.append(f'  skos:topConceptOf <{SCHEME}> ;')
        elif b: out.append(f'  skos:broader c:{b} ;')
    out.append(f'  skos:inScheme <{SCHEME}> .')
    return "\n".join(out)+"\n"

dict_label={n:l for n,l,b,d,td,dep,rb in rows}
tops=[n for n,l,b,d,td,dep,rb in rows if d==1 and not dep]
# scheme.ttl
with open(os.path.join(REPO,"scheme.ttl"),"w") as f:
    f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n@prefix dct:  <http://purl.org/dc/terms/> .\n@prefix c: <https://w3id.org/legal-taxonomy/concept/> .\n\n')
    f.write(f'<{SCHEME}> a skos:ConceptScheme ;\n  dct:title "Open Legal Issue Taxonomy"@en ;\n  skos:hasTopConcept\n    '+",\n    ".join(f"c:{t}" for t in tops)+" .\n")
# full ttl
nlive=ndep=0
with open(os.path.join(REPO,"legal-taxonomy.ttl"),"w") as f:
    f.write(PRE)
    f.write(f'<{SCHEME}> a skos:ConceptScheme ;\n  dct:title "Open Legal Issue Taxonomy"@en ;\n  skos:hasTopConcept\n    '+",\n    ".join(f"c:{t}" for t in tops)+" .\n\n")
    for n,l,b,d,td,dep,rb in rows:
        f.write(ttl_block(n,l,b,d,td,dep,rb))
        if dep: ndep+=1
        else: nlive+=1
# dumps per domain
for old in glob.glob(os.path.join(REPO,"dumps","*.ttl")): os.remove(old)
bydom={}
for r in rows: bydom.setdefault(r[4],[]).append(r)
topnot={dict_label[t]:t for t in tops}
for td,rs in bydom.items():
    tn=topnot.get(td) or rs[0][0]
    fn=os.path.join(REPO,"dumps",f"concepts-{tn}-{slug(td)}.ttl")
    with open(fn,"w") as f:
        f.write(PRE)
        for r in rs: f.write(ttl_block(*r))
# json-ld (@graph)
ctx={"skos":"http://www.w3.org/2004/02/skos/core#","dct":"http://purl.org/dc/terms/","owl":"http://www.w3.org/2002/07/owl#","@vocab":"http://www.w3.org/2004/02/skos/core#"}
g=[]
for n,l,b,d,td,dep,rb in rows:
    o={"@id":CB+n,"@type":"skos:Concept","skos:notation":n,"skos:prefLabel":{"@language":"en","@value":l},"skos:inScheme":{"@id":SCHEME}}
    if dep:
        o["owl:deprecated"]=True; o["dct:isReplacedBy"]={"@id":CB+final_winner(n)}
        o["skos:historyNote"]={"@language":"en","@value":f"Deduplicated 2026-06: merged into {final_winner(n)}."}
    else:
        if d==1: o["skos:topConceptOf"]={"@id":SCHEME}
        elif b: o["skos:broader"]={"@id":CB+b}
    g.append(o)
with open(os.path.join(REPO,"legal-taxonomy.jsonld"),"w") as f:
    json.dump({"@context":ctx,"@graph":g},f,ensure_ascii=False,separators=(",",":"))
print(f"RDF regenerated: live={nlive} deprecated={ndep} tops={len(tops)} dumps={len(bydom)}")
con.close()
