#!/usr/bin/env python3
"""Combine two models' Tier-2 results into AGREED clusters (double-safe).
A pair (x,y) is merged ONLY if BOTH models put x,y in the same cluster.
Final clusters = connected components of the agreement graph (per parent)."""
import json, sys, csv, sqlite3, os, collections
HERE=os.path.dirname(os.path.abspath(__file__))

def load(path):
    by={}
    for line in open(path):
        if not line.strip(): continue
        r=json.loads(line)
        by[r["parent"]]=r
    return by

def pairs(clusters):
    s=set()
    for c in clusters:
        m=sorted(c["members"])
        for i in range(len(m)):
            for j in range(i+1,len(m)):
                s.add((m[i],m[j]))
    return s

def components(nodes, edges):
    par={n:n for n in nodes}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for a,b in edges:
        par.setdefault(a,a); par.setdefault(b,b)
        ra,rb=f(a),f(b)
        if ra!=rb: par[ra]=rb
    comp=collections.defaultdict(list)
    for n in par: comp[f(n)].append(n)
    return [sorted(v) for v in comp.values() if len(v)>=2]

def main():
    a=load(sys.argv[1]); b=load(sys.argv[2])
    out_csv=sys.argv[3] if len(sys.argv)>3 else os.path.join(HERE,"tier2_agreed.csv")
    db=sqlite3.connect(os.path.join(HERE,"..","legal-taxonomy.db"))
    lab=dict(db.execute("SELECT notation,pref_label FROM concepts"))
    src=dict(db.execute("SELECT notation,COUNT(*) FROM sources GROUP BY notation").fetchall())
    kids=dict(db.execute("SELECT broader,COUNT(*) FROM concepts WHERE broader IS NOT NULL GROUP BY broader").fetchall())
    common=set(a)&set(b)
    only_a=set(a)-set(b); only_b=set(b)-set(a)
    rows=[]; n_clusters=0; n_losers=0
    a_pairs_tot=b_pairs_tot=agree_pairs_tot=0
    for p in sorted(common):
        pa=pairs(a[p]["clusters"]); pb=pairs(b[p]["clusters"])
        a_pairs_tot+=len(pa); b_pairs_tot+=len(pb)
        agree=pa&pb; agree_pairs_tot+=len(agree)
        if not agree: continue
        nodes={x for pr in agree for x in pr}
        for comp in components(nodes,agree):
            # canonical: max sources, max children, shortest label, lowest notation
            win=sorted(comp,key=lambda n:(-src.get(n,0),-kids.get(n,0),len(lab.get(n,"")),n))[0]
            losers=[n for n in comp if n!=win]
            n_clusters+=1; n_losers+=len(losers)
            rows.append({
                "parent":p,"parent_label":lab.get(p,""),
                "winner_notation":win,"winner_label":lab.get(win,""),
                "winner_sources":src.get(win,0),"winner_children":kids.get(win,0),
                "losers":";".join(f"{n}={lab.get(n,'')}" for n in losers),
                "n_losers":len(losers),
            })
    with open(out_csv,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"parents in A={len(a)} B={len(b)} common={len(common)} onlyA={len(only_a)} onlyB={len(only_b)}")
    print(f"pairwise merges: A={a_pairs_tot} B={b_pairs_tot} AGREED(both)={agree_pairs_tot}")
    print(f"agreement rate vs A: {agree_pairs_tot/max(a_pairs_tot,1):.1%}  vs B: {agree_pairs_tot/max(b_pairs_tot,1):.1%}")
    print(f"AGREED clusters={n_clusters} removable_losers={n_losers}")
    print(f"-> {out_csv}")

if __name__=="__main__": main()
