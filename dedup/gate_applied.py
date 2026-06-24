#!/usr/bin/env python3
"""Isaacus (kanon-2-embedder) gate over APPLIED merges in the live DB.
 1) Every deprecated->winner merge: cosine(loser,winner); flag low ones (nitpick review).
 2) Discovery: high-cosine LIVE sibling pairs still NOT merged (semantic round-2 candidates)."""
import sqlite3, pickle, math, os, collections, statistics, json
HERE=os.path.dirname(os.path.abspath(__file__))
VEC=pickle.load(open(os.path.join(HERE,"emb_isaacus.pkl"),"rb"))
def nrm(v):
    s=math.sqrt(sum(x*x for x in v)) or 1.0; return [x/s for x in v]
V={k:nrm(v) for k,v in VEC.items()}
def cos(la,lb):
    a,b=V.get(la),V.get(lb)
    return None if a is None or b is None else sum(x*y for x,y in zip(a,b))
con=sqlite3.connect(os.path.join(HERE,"..","legal-taxonomy.db"))
lab=dict(con.execute("SELECT notation,pref_label FROM concepts"))
# 1) applied merges
merges=con.execute("SELECT notation,replaced_by FROM concepts WHERE deprecated=1 AND replaced_by IS NOT NULL").fetchall()
sims=[]; low=[]
for L,W in merges:
    c=cos(lab[L],lab[W])
    if c is None: continue
    sims.append(c)
    if c<0.75: low.append((c,lab[L],lab[W]))
sims.sort(); low.sort()
print(f"=== APPLIED MERGES audited by kanon-2-embedder: {len(sims)} ===")
print(f"  cosine min={sims[0]:.3f} p1={sims[len(sims)//100]:.3f} p10={sims[len(sims)//10]:.3f} median={statistics.median(sims):.3f}")
for t in (0.90,0.85,0.80,0.75,0.70):
    print(f"  merges cos>={t}: {sum(1 for s in sims if s>=t)} ({sum(1 for s in sims if s>=t)/len(sims):.1%})")
print(f"  merges below 0.75 (nitpick review): {len(low)}")
for c,a,b in low[:20]: print(f"    {c:.3f}  {a}  ->  {b}")
# 2) discovery among live siblings
rows=con.execute("SELECT notation,broader FROM concepts WHERE deprecated=0 AND broader IS NOT NULL").fetchall()
by=collections.defaultdict(list)
for n,b in rows: by[b].append(n)
disc=[]
for b,ch in by.items():
    if len(ch)<2 or len(ch)>400: continue
    for i in range(len(ch)):
        for j in range(i+1,len(ch)):
            c=cos(lab[ch[i]],lab[ch[j]])
            if c is not None and c>=0.93: disc.append((c,b,lab[ch[i]],lab[ch[j]]))
disc.sort(reverse=True)
print(f"\n=== DISCOVERY: high-cosine LIVE sibling pairs NOT merged (semantic round-2 candidates) ===")
for t in (0.97,0.95,0.93): print(f"  cos>={t}: {sum(1 for d in disc if d[0]>=t)}")
for c,b,a,bn in disc[:25]: print(f"   {c:.3f} [{b}] {a}  ||  {bn}")
json.dump({"applied":len(sims),"low_cos":[(c,a,b) for c,a,b in low],
           "discovery_top":[(c,b,a,bn) for c,b,a,bn in disc[:300]]},
          open(os.path.join(HERE,"gate_report.json"),"w"),indent=1)
print("\n-> dedup/gate_report.json")
