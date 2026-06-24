#!/usr/bin/env python3
"""N-model agreement for Tier-2. Usage: tier2_agree3.py <minvotes> <out.csv> <f1> <f2> [f3...]
A sibling pair is merged if it co-clusters in >= minvotes models. Final clusters =
connected components of the surviving-pair graph, per parent. minvotes=len(files) => unanimous."""
import json, sys, csv, sqlite3, os, collections, itertools
HERE=os.path.dirname(os.path.abspath(__file__))
def load(path):
    by={}
    for line in open(path):
        if line.strip():
            r=json.loads(line); by[r["parent"]]=r   # last wins (dedup dup parent lines)
    return by
def pairs(clusters):
    s=set()
    for c in clusters:
        m=sorted(c["members"])
        for a,b in itertools.combinations(m,2): s.add((a,b))
    return s
def comps(nodes,edges):
    par={n:n for n in nodes}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for a,b in edges:
        par.setdefault(a,a); par.setdefault(b,b)
        ra,rb=f(a),f(b)
        if ra!=rb: par[ra]=rb
    g=collections.defaultdict(list)
    for n in par: g[f(n)].append(n)
    return [sorted(v) for v in g.values() if len(v)>=2]

def main():
    minvotes=int(sys.argv[1]); out_csv=sys.argv[2]; files=sys.argv[3:]
    models=[load(f) for f in files]
    names=[os.path.basename(f).replace("tier2.","").replace(".jsonl","") for f in files]
    db=sqlite3.connect(os.path.join(HERE,"..","legal-taxonomy.db"))
    lab=dict(db.execute("SELECT notation,pref_label FROM concepts"))
    src=dict(db.execute("SELECT notation,COUNT(*) FROM sources GROUP BY notation").fetchall())
    kids=dict(db.execute("SELECT broader,COUNT(*) FROM concepts WHERE broader IS NOT NULL GROUP BY broader").fetchall())
    all_parents=set().union(*[set(m) for m in models])
    common=set(models[0])
    for m in models[1:]: common&=set(m)
    all_parents=set().union(*[set(m) for m in models])
    print(f"models={names} parents each={[len(m) for m in models]} common_to_all={len(common)} union={len(all_parents)}")
    rows=[]; nclu=0; nlose=0
    votes_hist=collections.Counter()
    for p in sorted(all_parents):
        present=[m for m in models if p in m]   # union-based: vote only over models that ran this parent
        ps=[pairs(m[p]["clusters"]) for m in present]
        allpairs=set().union(*ps) if ps else set()
        keep=set()
        for pr in allpairs:
            v=sum(1 for s in ps if pr in s); votes_hist[v]+=1
            if v>=minvotes: keep.add(pr)
        if not keep: continue
        nodes={x for pr in keep for x in pr}
        for comp in comps(nodes,keep):
            win=sorted(comp,key=lambda n:(-src.get(n,0),-kids.get(n,0),len(lab.get(n,"")),n))[0]
            losers=[n for n in comp if n!=win]
            nclu+=1; nlose+=len(losers)
            rows.append({"parent":p,"parent_label":lab.get(p,""),
                "winner_notation":win,"winner_label":lab.get(win,""),
                "winner_sources":src.get(win,0),"winner_children":kids.get(win,0),
                "losers":";".join(f"{n}={lab.get(n,'')}" for n in losers),"n_losers":len(losers)})
    with open(out_csv,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"vote histogram (pairs by #models agreeing): {dict(sorted(votes_hist.items()))}")
    print(f"minvotes>={minvotes}: clusters={nclu} removable_losers={nlose}")
    print(f"-> {out_csv}")

if __name__=="__main__": main()
