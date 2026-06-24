#!/usr/bin/env python3
"""Apply majority-agreed merges to a SQLite DB. SAFE ORDER (children-first, deepest-first):
 for each loser L -> winner W:  (1) re-parent L's children to W  (2) move L's sources to W
 (3) deprecate L (keep row + URI) and record replaced_by=W.
Never deletes; never deprecates a concept before its children are re-parented.
Usage: apply_merges.py <db> <majority.csv>   (operate on a COPY for dry runs)"""
import sys, csv, sqlite3, collections
db_path=sys.argv[1]; csv_path=sys.argv[2]
con=sqlite3.connect(db_path); cur=con.cursor()
# ensure replaced_by column
cols=[r[1] for r in cur.execute("PRAGMA table_info(concepts)")]
if "replaced_by" not in cols:
    cur.execute("ALTER TABLE concepts ADD COLUMN replaced_by TEXT")
depth=dict(cur.execute("SELECT notation,depth FROM concepts"))
live_parent=dict(cur.execute("SELECT notation,broader FROM concepts"))

# load clusters; expand losers
groups=[]
for r in csv.DictReader(open(csv_path)):
    losers=[]
    for tok in r["losers"].split(";"):
        if "=" in tok: losers.append(tok.split("=",1)[0])
    if losers: groups.append((r["parent"],r["winner_notation"],losers))
# deepest-first by parent depth (process child-level merges before higher levels)
groups.sort(key=lambda g:-depth.get(g[0],0))

n_merge=0; n_reparent=0; n_src=0; loser_set=set(); win_of={}
cur.execute("BEGIN")
for parent,W,losers in groups:
    for L in losers:
        if L==W: continue
        n_reparent+=cur.execute("UPDATE concepts SET broader=? WHERE broader=?",(W,L)).rowcount
        n_src+=cur.execute("UPDATE sources SET notation=? WHERE notation=?",(W,L)).rowcount
        cur.execute("UPDATE concepts SET deprecated=1, replaced_by=? WHERE notation=? AND deprecated=0",(W,L))
        loser_set.add(L); win_of[L]=W; n_merge+=1
con.commit()

# follow replaced_by chains so children never point at a deprecated winner-that-was-also-merged
chain_fixes=0
cur.execute("BEGIN")
repl=dict((n,w) for n,w in cur.execute("SELECT notation,replaced_by FROM concepts WHERE replaced_by IS NOT NULL"))
def final(x,seen=None):
    seen=seen or set()
    while x in repl and x not in seen: seen.add(x); x=repl[x]
    return x
for L,W in list(repl.items()):
    fw=final(W)
    if fw!=W:
        cur.execute("UPDATE concepts SET broader=? WHERE broader=?",(fw,L))  # already moved to L? no
# re-point any live concept whose broader is a deprecated loser, to that loser's final winner
bad=cur.execute("""SELECT c.notation,c.broader FROM concepts c JOIN concepts p ON c.broader=p.notation
                   WHERE c.deprecated=0 AND p.deprecated=1""").fetchall()
for child,par in bad:
    cur.execute("UPDATE concepts SET broader=? WHERE notation=?",(final(par),child)); chain_fixes+=1
con.commit()

# VALIDATION
orphans=cur.execute("""SELECT COUNT(*) FROM concepts c JOIN concepts p ON c.broader=p.notation
                       WHERE c.deprecated=0 AND p.deprecated=1""").fetchone()[0]
live=cur.execute("SELECT COUNT(*) FROM concepts WHERE deprecated=0").fetchone()[0]
dep =cur.execute("SELECT COUNT(*) FROM concepts WHERE deprecated=1").fetchone()[0]
src_on_dep=cur.execute("""SELECT COUNT(*) FROM sources s JOIN concepts c ON s.notation=c.notation
                          WHERE c.deprecated=1""").fetchone()[0]
print(f"merges applied (losers deprecated): {n_merge}")
print(f"children re-parented: {n_reparent}   sources moved: {n_src}   chain re-points: {chain_fixes}")
print(f"live concepts: {live}   deprecated: {dep}")
print(f"VALIDATION  live-concept-with-deprecated-parent: {orphans} (must be 0)")
print(f"VALIDATION  source-rows-on-deprecated-concept:   {src_on_dep} (must be 0)")
con.close()
