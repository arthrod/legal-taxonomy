import sqlite3, re, collections, csv, json, os
SP=os.environ["SP"]
db=sqlite3.connect("legal-taxonomy.db")
rows=db.execute("SELECT notation,pref_label,broader,depth,top_domain FROM concepts WHERE broader IS NOT NULL").fetchall()
src=dict(db.execute("SELECT notation,COUNT(*) FROM sources GROUP BY notation").fetchall())
kids=dict(db.execute("SELECT broader,COUNT(*) FROM concepts WHERE broader IS NOT NULL GROUP BY broader").fetchall())
label={n:l for n,l,b,d,t in rows}

STOP={"AND","OR","THE","OF","A","AN","IN","TO","FOR","ON","WITH","&","UNDER","BY"}
def norm(s):
    s=re.sub(r"[^A-Za-z0-9 ]"," ",s.upper())
    out=[]
    for t in s.split():
        if t in STOP: continue
        if len(t)>3 and t.endswith("S") and not t.endswith("SS"): t=t[:-1]
        out.append(t)
    return tuple(sorted(out))

bychild=collections.defaultdict(list)
for n,l,b,d,t in rows: bychild[b].append((n,l,t))

def pick_canonical(group):
    # group: list of (notation,label). winner = max sources, then max children, then shortest label, then lowest notation
    return sorted(group, key=lambda x:(-src.get(x[0],0), -kids.get(x[0],0), len(x[1]), x[0]))[0]

tier1=[]            # rows for csv
collapsed={}        # loser_notation -> winner_notation (tier1)
remaining=collections.defaultdict(list)  # parent -> surviving (notation,label) after tier1
for b,ch in bychild.items():
    keymap=collections.defaultdict(list)
    for n,l,t in ch: keymap[norm(l)].append((n,l))
    survivors=[]
    for key,grp in keymap.items():
        if len(grp)>1:
            win=pick_canonical(grp)
            survivors.append((win[0],win[1]))
            losers=[g for g in grp if g[0]!=win[0]]
            for ln,ll in losers: collapsed[ln]=win[0]
            tier1.append({
                "parent":b,"parent_label":label.get(b,""),
                "winner_notation":win[0],"winner_label":win[1],
                "winner_sources":src.get(win[0],0),"winner_children":kids.get(win[0],0),
                "losers":";".join(f"{ln}={ll}" for ln,ll in losers),
                "n_losers":len(losers),"norm_key":" ".join(key),
            })
        else:
            survivors.append((grp[0][0],grp[0][1]))
    if len(survivors)>=2:
        remaining[b]=survivors

# Tier1 CSV
with open(f"{SP}/tier1_merges.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(tier1[0].keys()))
    w.writeheader(); w.writerows(tier1)

# Tier2 batches: parents with >=2 distinct surviving siblings -> LLM clustering
batches=[]
for b,sv in remaining.items():
    if len(sv)<2: continue
    items=[{"notation":n,"label":l,"sources":src.get(n,0),"children":kids.get(n,0)} for n,l in sv]
    batches.append({"parent":b,"parent_label":label.get(b,""),"siblings":items})
with open(f"{SP}/tier2_batches.jsonl","w") as f:
    for x in batches: f.write(json.dumps(x)+"\n")

print("Tier1 merge groups:",len(tier1))
print("Tier1 losers (removable rows):",sum(t["n_losers"] for t in tier1))
print("Tier2 parents to LLM-cluster:",len(batches))
print("Tier2 total siblings to scan:",sum(len(b['siblings']) for b in batches))
import statistics
sizes=[len(b['siblings']) for b in batches]
print("Tier2 sibling-count: max",max(sizes),"median",int(statistics.median(sizes)))
