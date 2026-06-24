import sqlite3,pickle,os,collections,json
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
VEC=pickle.load(open(os.path.join(HERE,"emb_isaacus.pkl"),"rb"))
labels=list(VEC); idx={l:i for i,l in enumerate(labels)}
M=np.array([VEC[l] for l in labels],dtype=np.float32)
M/=np.linalg.norm(M,axis=1,keepdims=True)+1e-9
con=sqlite3.connect(os.path.join(HERE,"..","legal-taxonomy.db"))
lab=dict(con.execute("SELECT notation,pref_label FROM concepts"))
rows=con.execute("SELECT notation,broader FROM concepts WHERE deprecated=0 AND broader IS NOT NULL").fetchall()
by=collections.defaultdict(list)
for n,b in rows: by[b].append(n)
disc=[]
for b,ch in by.items():
    if len(ch)<2: continue
    rid=[idx.get(lab[n]) for n in ch]
    keep=[(n,i) for n,i in zip(ch,rid) if i is not None]
    if len(keep)<2: continue
    sub=M[[i for _,i in keep]]
    S=sub@sub.T
    for a in range(len(keep)):
        for bb in range(a+1,len(keep)):
            c=float(S[a,bb])
            if c>=0.93: disc.append((c,b,lab[keep[a][0]],lab[keep[bb][0]]))
disc.sort(reverse=True)
print(f"DISCOVERY high-cosine LIVE sibling pairs NOT merged: total>=0.93 = {len(disc)}")
for t in (0.98,0.97,0.95,0.93): print(f"  cos>={t}: {sum(1 for d in disc if d[0]>=t)}")
print("top 30:")
for c,b,a,bn in disc[:30]: print(f"   {c:.3f} [{b}] {a}  ||  {bn}")
json.dump([(c,b,a,bn) for c,b,a,bn in disc[:500]],open(os.path.join(HERE,"discovery.json"),"w"),indent=1)
