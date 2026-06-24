#!/usr/bin/env python3
"""Phase B (FINAL TEST): use kanon-2-embedder (Isaacus, legal-domain) vectors to audit the merge set.
Q: does a legal-domain embedder change the picture?
 1) GATE every proposed merge (Tier-1 lexical + Tier-2 agreed): flag any whose internal
    cosine is low -> a merge lawyers might nitpick.
 2) DISCOVER high-cosine sibling pairs the pipeline did NOT merge -> potential misses."""
import os, json, csv, math, pickle, collections, sqlite3
HERE=os.path.dirname(os.path.abspath(__file__))
cache=pickle.load(open(os.path.join(HERE,os.environ.get("EMB_CACHE","emb_isaacus.pkl")),"rb"))
def nrm(v):
    s=math.sqrt(sum(x*x for x in v)) or 1.0; return [x/s for x in v]
VEC={k:nrm(v) for k,v in cache.items()}
def cos(a,b):
    va,vb=VEC.get(a),VEC.get(b)
    if va is None or vb is None: return None
    return sum(x*y for x,y in zip(va,vb))

db=sqlite3.connect(os.path.join(HERE,"..","legal-taxonomy.db"))
LAB=dict(db.execute("SELECT notation,pref_label FROM concepts"))

# ---- Tier-1 groups ----
t1=[]
for r in csv.DictReader(open(os.path.join(HERE,"tier1_merges.csv"))):
    mem=[(r["winner_notation"],r["winner_label"])]
    for tok in r["losers"].split(";"):
        if "=" in tok:
            n,l=tok.split("=",1); mem.append((n,l))
    t1.append((r["parent"],mem))

# ---- Tier-2 agreed clusters (both models) ----
def pairs(path):
    s=collections.defaultdict(set)
    for line in open(path):
        if not line.strip(): continue
        r=json.loads(line)
        for c in r["clusters"]:
            m=sorted(c["members"])
            for i in range(len(m)):
                for j in range(i+1,len(m)): s[r["parent"]].add((m[i],m[j]))
    return s
pa=pairs(os.path.join(HERE,"tier2.opus.jsonl")); pb=pairs(os.path.join(HERE,"tier2.gpt.jsonl"))
agreed=collections.defaultdict(set)
for p in set(pa)&set(pb):
    ag=pa[p]&pb[p]
    if ag: agreed[p]=ag
def comps(edges):
    par={}
    def f(x):
        par.setdefault(x,x)
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for a,b in edges:
        ra,rb=f(a),f(b)
        if ra!=rb: par[ra]=rb
    g=collections.defaultdict(list)
    for n in list(par): g[f(n)].append(n)
    return [v for v in g.values() if len(v)>=2]
t2=[]
for p,edges in agreed.items():
    for comp in comps(edges):
        t2.append((p,[(n,LAB.get(n,"")) for n in comp]))

def min_cos(mem):
    ns=[n for n,_ in mem]; lo=2.0; worst=None
    for i in range(len(ns)):
        for j in range(i+1,len(ns)):
            c=cos(ns[i],ns[j])
            if c is None: continue
            if c<lo: lo=c; worst=(ns[i],ns[j],c)
    return lo if worst else None, worst

def gate(groups,name):
    rows=[]
    for p,mem in groups:
        lo,worst=min_cos(mem)
        if lo is None: continue
        rows.append((lo,p,mem,worst))
    rows.sort()
    flagged=[r for r in rows if r[0]<0.75]
    print(f"\n=== {name}: {len(groups)} merge groups, {len(rows)} embeddable ===")
    import statistics
    sims=[r[0] for r in rows]
    if sims:
        print(f"  internal min-cosine: p1={sorted(sims)[len(sims)//100]:.3f} p10={sorted(sims)[len(sims)//10]:.3f} median={statistics.median(sims):.3f}")
    print(f"  merges with internal min-cos <0.75 (NITPICK REVIEW): {len(flagged)}")
    for lo,p,mem,worst in flagged[:25]:
        a,b,c=worst
        print(f"   {lo:.3f} [{p}] {LAB.get(a)}  ||  {LAB.get(b)}")
    return rows,flagged

t1_rows,t1_flag=gate(t1,"TIER-1 (lexical)")
t2_rows,t2_flag=gate(t2,"TIER-2 (LLM-agreed)")

# ---- DISCOVERY: high-cos sibling pairs NOT merged ----
merged_pairs=set()
for _,mem in t1+t2:
    ns=[n for n,_ in mem]
    for i in range(len(ns)):
        for j in range(i+1,len(ns)): merged_pairs.add(tuple(sorted((ns[i],ns[j]))))
batches=[json.loads(l) for l in open(os.path.join(HERE,"tier2_batches.jsonl")) if l.strip()]
disc=[]
for b in batches:
    ns=[x["notation"] for x in b["siblings"]]
    for i in range(len(ns)):
        for j in range(i+1,len(ns)):
            key=tuple(sorted((ns[i],ns[j])))
            if key in merged_pairs: continue
            c=cos(ns[i],ns[j])
            if c is not None and c>=0.93:
                disc.append((c,b["parent"],ns[i],ns[j]))
disc.sort(reverse=True)
print(f"\n=== DISCOVERY: high-cosine sibling pairs NOT merged by pipeline ===")
for t in (0.97,0.95,0.93):
    print(f"  cos>={t}: {sum(1 for d in disc if d[0]>=t)}")
print("  top 40 (embedder says near-dup, pipeline did not merge):")
for c,p,a,bn in disc[:40]:
    print(f"   {c:.3f} [{p}] {LAB.get(a)}  ||  {LAB.get(bn)}")

json.dump({"t1_flagged":[(r[0],r[1]) for r in t1_flag],
           "t2_flagged":[(r[0],r[1]) for r in t2_flag],
           "discovery_top":[(c,p,a,bn,LAB.get(a),LAB.get(bn)) for c,p,a,bn in disc[:500]]},
          open(os.path.join(HERE,"embed_report.json"),"w"),indent=1)
print("\n-> dedup/embed_report.json")
