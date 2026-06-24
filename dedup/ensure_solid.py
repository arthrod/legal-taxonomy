#!/usr/bin/env python3
"""Post-dedup integrity verification. Confirms the taxonomy is still solid.
Usage: ensure_solid.py <db> [original_total]"""
import sys, sqlite3, collections
db=sys.argv[1]; orig_total=int(sys.argv[2]) if len(sys.argv)>2 else None
con=sqlite3.connect(db); cur=con.cursor()
has_rb="replaced_by" in [r[1] for r in cur.execute("PRAGMA table_info(concepts)")]
rb_sel="COALESCE(replaced_by,'')" if has_rb else "''"
rows=cur.execute(f"SELECT notation,broader,depth,top_domain,deprecated,{rb_sel} FROM concepts").fetchall()
by={r[0]:r for r in rows}
live={n for n,b,d,td,dep,rb in rows if dep==0}
dep ={n for n,b,d,td,dep,rb in rows if dep==1}
broader={n:b for n,b,d,td,dp,rb in rows}
depth={n:d for n,b,d,td,dp,rb in rows}
repl={n:rb for n,b,d,td,dp,rb in rows if rb}
fails=[]; checks=[]
def chk(name,cond,detail=""):
    checks.append((name,cond,detail))
    if not cond: fails.append(f"{name}: {detail}")

# 1 totals conserved (nothing deleted)
chk("totals conserved (live+dep==orig)", orig_total is None or len(rows)==orig_total,
    f"rows={len(rows)} orig={orig_total}")
# 2 no live concept points at a deprecated/ missing parent
bad_parent=[n for n in live if broader[n] and (broader[n] not in by or by[broader[n]][4]==1)]
chk("no live concept with dead/deprecated parent", not bad_parent, f"{len(bad_parent)} e.g.{bad_parent[:5]}")
# 3 exactly 13 live top concepts (broader NULL)
tops=[n for n in live if not broader[n]]
chk("live top concepts == 13", len(tops)==13, f"got {len(tops)}")
# 4 every live concept reaches a top within depth limit (no broken/cyclic chain)
def root_ok(n):
    seen=set(); x=n; steps=0
    while broader.get(x):
        if x in seen: return False  # cycle
        seen.add(x); x=broader[x]; steps+=1
        if steps>50: return False
        if x not in by or by[x][4]==1: return False  # hits missing/deprecated
    return x in live  # ended at a live top
unreachable=[n for n in live if not root_ok(n)]
chk("all live concepts reach a live root (no cycles/breaks)", not unreachable, f"{len(unreachable)} e.g.{unreachable[:5]}")
# 5 depth consistency: depth == actual chain length
def chain_depth(n):
    x=n; d=0
    while broader.get(x): x=broader[x]; d+=1
        # guard
    return d
bad_depth=[(n,depth[n],depth[broader[n]]) for n in live
           if broader.get(n) and broader[n] in depth and depth[n]!=depth[broader[n]]+1]
chk("depth invariant (child.depth==parent.depth+1)", not bad_depth, f"{len(bad_depth)} e.g.{bad_depth[:5]}")
# 6 deprecated concepts resolve via replaced_by to a LIVE concept
def resolve(n):
    seen=set(); x=n
    while x in repl and x not in seen: seen.add(x); x=repl[x]
    return x
bad_repl=[n for n in dep if not repl.get(n) or resolve(n) not in live]
chk("every deprecated concept resolves to a live winner", not bad_repl, f"{len(bad_repl)} e.g.{bad_repl[:5]}")
# 7 no sources on deprecated concepts
son=cur.execute("""SELECT COUNT(*) FROM sources s JOIN concepts c ON s.notation=c.notation WHERE c.deprecated=1""").fetchone()[0]
chk("no source links on deprecated concepts", son==0, f"{son} rows")
# 8 no remaining exact-duplicate live siblings (same parent, same norm label)
import re
def norm(s):
    s=re.sub(r"[^a-z0-9 ]"," ",s.lower())
    return " ".join(sorted(t for t in s.split()))
sib=collections.defaultdict(set); dupsib=0
lab=dict(cur.execute("SELECT notation,pref_label FROM concepts WHERE deprecated=0"))
kids=collections.defaultdict(list)
for n in live: kids[broader[n]].append(n)
for p,ch in kids.items():
    seen={}
    for n in ch:
        k=norm(lab[n])
        if k in seen: dupsib+=1
        seen[k]=n
chk("no exact-duplicate live siblings remain", dupsib==0, f"{dupsib} dup-sibling pairs")

print(f"=== INTEGRITY REPORT for {db} ===")
print(f"rows={len(rows)} live={len(live)} deprecated={len(dep)}")
for name,cond,detail in checks:
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if not cond else ""))
print("\nRESULT:", "ALL PASS ✅" if not fails else f"{len(fails)} FAILURES ❌")
sys.exit(0 if not fails else 1)
