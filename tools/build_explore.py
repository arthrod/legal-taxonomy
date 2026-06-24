#!/usr/bin/env python3
"""Rebuild the marimo "explore" app with the FULL taxonomy tree embedded.

The app embeds the whole tree (every concept: id, label, parent, depth, plus
subtree concept/source counts) as a gzip+base64 blob and expands one branch at
a time, so a reader can drill to any depth (7) entirely in-browser/offline.

Pipeline:
  1. read legal-taxonomy.db.gz, compute the `_data` payload + counts,
  2. inject it into tools/explore_template.py (the readable notebook),
  3. URL-encode the notebook and swap the <marimo-code> block in
     explore/index.html — reusing the already-deployed marimo WASM runtime and
     all custom branding/assets (no marimo re-export needed).

Usage:
  python3 tools/build_explore.py build <out.py>   # write the built notebook (for testing)
  python3 tools/build_explore.py inject            # build + swap into explore/index.html
"""
import base64
import gzip
import json
import os
import re
import sqlite3
import sys
import tempfile
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_GZ = os.path.join(REPO, "legal-taxonomy.db.gz")
TEMPLATE = os.path.join(REPO, "tools", "explore_template.py")
INDEX = os.path.join(REPO, "explore", "index.html")


def load_rows():
    tmp = tempfile.NamedTemporaryFile(prefix="olit-", suffix=".db", delete=False)
    with gzip.open(DB_GZ, "rb") as f:
        tmp.write(f.read())
    tmp.close()
    try:
        con = sqlite3.connect(tmp.name)
        rows = con.execute(
            "SELECT notation,pref_label,broader,depth,top_domain FROM concepts"
        ).fetchall()
        src = con.execute("SELECT notation,count(*) FROM sources GROUP BY notation").fetchall()
        nsrc_total = con.execute("SELECT count(*) FROM sources").fetchone()[0]
        con.close()
    finally:
        os.unlink(tmp.name)
    return rows, dict(src), nsrc_total


def build_data():
    rows, src_direct, nsrc_total = load_rows()

    # domains (depth==1), ordered by notation
    tops = sorted([r for r in rows if r[3] == 1], key=lambda r: r[0])
    domains = [r[1] for r in tops]
    dom_root = [r[0] for r in tops]
    dom_idx = {r[4]: i for i, r in enumerate(tops)}  # top_domain label -> index

    children = {}
    for r in rows:
        if r[2] is not None:
            children.setdefault(r[2], []).append(r[0])

    # subtree rollups: process deepest depth first so children precede parents
    desc = {r[0]: 0 for r in rows}   # descendant concept count
    ssrc = {r[0]: src_direct.get(r[0], 0) for r in rows}  # subtree source count
    for r in sorted(rows, key=lambda r: -r[3]):
        n = r[0]
        if r[2] is not None:
            p = r[2]
            desc[p] += 1 + desc[n]
            ssrc[p] += ssrc[n]

    out_rows = [
        [r[0], r[1], r[2], r[3], dom_idx[r[4]], desc[r[0]], ssrc[r[0]]]
        for r in rows
    ]

    # domain summary (concepts per top domain) + depth histogram
    dom_count = {}
    depth_count = {}
    for r in rows:
        dom_count[r[4]] = dom_count.get(r[4], 0) + 1
        depth_count[r[3]] = depth_count.get(r[3], 0) + 1
    domain_summary = [{"domain": d, "concepts": dom_count[d]} for d in dom_count]
    depth_hist = [[d, depth_count[d]] for d in sorted(depth_count)]

    # "one issue, many homes": labels appearing under the most distinct parents
    label_parents = {}
    for r in rows:
        if r[2] is not None:
            label_parents.setdefault(r[1], set()).add(r[2])
    ranked = sorted(label_parents.items(), key=lambda kv: -len(kv[1]))
    examples = [{"label": lbl, "parents": len(ps)} for lbl, ps in ranked[:8]]
    by_id = {r[0]: r for r in rows}
    top_lbl, top_parents = ranked[0]
    seen, sample_parents = set(), []
    for p in sorted(top_parents):
        pl = by_id[p][1]
        if pl not in seen:
            seen.add(pl)
            sample_parents.append(pl)
        if len(sample_parents) >= 4:
            break
    featured = {
        "label": top_lbl,
        "parents": len(top_parents),
        "sample_parents": sample_parents,
    }

    return {
        "domains": domains,
        "dom_root": dom_root,
        "rows": out_rows,
        "totals": {
            "concepts": len(rows),
            "domains": len(domains),
            "sources": nsrc_total,
            "maxdepth": max(depth_count),
        },
        "domain_summary": domain_summary,
        "depth_hist": depth_hist,
        "examples": examples,
        "featured": featured,
    }


def build_notebook_source():
    data = build_data()
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    blob = base64.b64encode(gzip.compress(raw, 9)).decode("ascii")
    template = open(TEMPLATE, encoding="utf-8").read()
    src = template.replace("__BLOB__", blob)
    print(
        f"data: {len(data['rows'])} nodes | blob {len(blob)/1048576:.2f} MB base64 "
        f"({len(raw)/1048576:.1f} MB raw)",
        file=sys.stderr,
    )
    return src


def inject(src):
    html = open(INDEX, encoding="utf-8").read()
    encoded = urllib.parse.quote(src, safe="")
    new_html, n = re.subn(
        r"(<marimo-code[^>]*>)(.*?)(</marimo-code>)",
        lambda m: m.group(1) + encoded + m.group(3),
        html,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"expected exactly 1 <marimo-code> block, found {n}")
    open(INDEX, "w", encoding="utf-8").write(new_html)
    print(f"injected new notebook into {INDEX} ({len(new_html)/1048576:.2f} MB)", file=sys.stderr)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "inject"
    if cmd == "build":
        out = sys.argv[2]
        open(out, "w", encoding="utf-8").write(build_notebook_source())
        print(f"wrote built notebook -> {out}", file=sys.stderr)
    elif cmd == "inject":
        inject(build_notebook_source())
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
