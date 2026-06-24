#!/usr/bin/env python3
"""LLM-free lexical closure: after merges collide children, repeatedly merge any LIVE
token-set-duplicate siblings (word-order/plural/and-or variants) until none remain.
Children-first, deepest-first, deprecate-not-delete. Usage: iterate_lexical.py <db>"""
import sys, re, sqlite3, collections
db=sys.argv[1]; con=sqlite3.connect(db); cur=con.cursor()
STOP={"AND","OR","THE","OF","A","AN","IN","TO","FOR","ON","WITH","&","UNDER","BY"}
def norm(s):
    s=re.sub(r"[^A-Za-z0-9 ]"," ",s.upper()); out=[]
    for t in s.split():
        if t in STOP: continue
        if len(t)>3 and t.endswith("S") and not t.endswith("SS"): t=t[:-1]
        out.append(t)
    return tuple(sorted(out))
total=0
for rnd in range(1,11):
    rows=cur.execute("SELECT notation,pref_label,broader,depth FROM concepts WHERE deprecated=0 AND broader IS NOT NULL").fetchall()
    src=dict(cur.execute("SELECT notation,COUNT(*) FROM sources GROUP BY notation").fetchall())
    kids=dict(cur.execute("SELECT broader,COUNT(*) FROM concepts WHERE deprecated=0 AND broader IS NOT NULL GROUP BY broader").fetchall())
    depth={n:d for n,l,b,d in rows}
    bychild=collections.defaultdict(list)
    for n,l,b,d in rows: bychild[b].append((n,l))
    groups=[]
    for b,ch in bychild.items():
        km=collections.defaultdict(list)
        for n,l in ch: km[norm(l)].append((n,l))
        for k,g in km.items():
            if len(g)>1: groups.append((b,g))
    if not groups:
        print(f"round {rnd}: no lexical dup siblings — closure reached"); break
    # deepest first
    groups.sort(key=lambda gb:-depth.get(gb[1][0][0],0))
    merges=0; cur.execute("BEGIN")
    for b,g in groups:
        win=sorted(g,key=lambda x:(-src.get(x[0],0),-kids.get(x[0],0),len(x[1]),x[0]))[0][0]
        for n,l in g:
            if n==win: continue
            # skip if already deprecated this round (a notation can appear once per parent anyway)
            cur.execute("UPDATE concepts SET broader=? WHERE broader=?",(win,n))
            cur.execute("UPDATE sources SET notation=? WHERE notation=?",(win,n))
            cur.execute("UPDATE concepts SET deprecated=1, replaced_by=? WHERE notation=? AND deprecated=0",(win,n))
            merges+=1
    con.commit()
    total+=merges
    print(f"round {rnd}: merged {merges} lexical dup siblings")
print(f"lexical closure total merged: {total}")
# final orphan check
orph=cur.execute("""SELECT COUNT(*) FROM concepts c JOIN concepts p ON c.broader=p.notation WHERE c.deprecated=0 AND p.deprecated=1""").fetchone()[0]
print(f"orphans after closure: {orph}")
con.close()
