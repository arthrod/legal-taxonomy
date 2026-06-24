#!/usr/bin/env python3
"""Generate a static HTML page for every OLIT concept.

Reads `legal-taxonomy.db.gz` (at the repo root) and writes one page per
`skos:Concept` so that each permanent URI dereferences on GitHub Pages:

    https://w3id.org/legal-taxonomy/concept/{notation}
        -> https://arthrod.github.io/legal-taxonomy/concept/{notation}

Output (under the repo root):
    concept/{notation}.html      one flat file per concept   (LAYOUT="flat")
    concept/index.html           index of the 13 top domains
    concept/_assets/concept.css  shared stylesheet

Flat files are used deliberately: GitHub Pages serves the extensionless
`/concept/{notation}` request directly with HTTP 200, whereas the
`{notation}/index.html` layout adds a 301 redirect to the trailing slash.

Usage:
    python3 tools/gen_concept_pages.py [flat|dir]
"""
import gzip
import html
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_GZ = os.path.join(REPO, "legal-taxonomy.db.gz")
OUT = os.environ.get("OLIT_OUT") or os.path.join(REPO, "concept")

LAYOUT = sys.argv[1] if len(sys.argv) > 1 else "flat"  # "flat" | "dir"
BASE = "/legal-taxonomy"                       # site path base (same on w3id + github.io)
SCHEME_URI = "https://w3id.org/legal-taxonomy/scheme/olit"
MAX_CHILDREN = 250      # cap rendered child links (a few domains have ~1200)
MAX_SOURCES = 50        # cap rendered source ids (max 271)

e = html.escape


def rel_prefix():
    return "" if LAYOUT == "flat" else "../"


def link_to(notation):
    return f"{rel_prefix()}{notation}" + ("" if LAYOUT == "flat" else "/")


def out_path(notation):
    if LAYOUT == "flat":
        return os.path.join(OUT, f"{notation}.html")
    return os.path.join(OUT, notation, "index.html")


def open_db():
    """Decompress legal-taxonomy.db.gz to a temp file and open it read-only."""
    tmp = tempfile.NamedTemporaryFile(prefix="olit-", suffix=".db", delete=False)
    with gzip.open(DB_GZ, "rb") as f:
        shutil.copyfileobj(f, tmp)
    tmp.close()
    return tmp.name


def main():
    t0 = time.time()
    db_path = open_db()
    try:
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
        cols = [r[1] for r in con.execute("PRAGMA table_info(concepts)")]
        rb_sel = ",replaced_by" if "replaced_by" in cols else ",NULL AS replaced_by"
        rows = con.execute(
            "SELECT notation,uri,pref_label,broader,depth,top_domain,deprecated"
            + rb_sel + " FROM concepts"
        ).fetchall()
        C = {r["notation"]: r for r in rows}
        print(f"loaded {len(C)} concepts in {time.time()-t0:.1f}s")

        children = {}
        for r in rows:
            b = r["broader"]
            if b:
                children.setdefault(b, []).append(r["notation"])
        for k in children:
            children[k].sort()

        src_count, src_sample = {}, {}
        for notation, item_id in con.execute(
            "SELECT notation,item_id FROM sources ORDER BY notation"
        ):
            src_count[notation] = src_count.get(notation, 0) + 1
            s = src_sample.setdefault(notation, [])
            if len(s) < MAX_SOURCES:
                s.append(item_id)
        con.close()
    finally:
        os.unlink(db_path)
    print(f"indexed children+sources in {time.time()-t0:.1f}s")

    css = (
        ":root{--ink:#1a1a1a;--mut:#666;--bg:#fff;--ac:#0b5d8a;--line:#e5e5e5}"
        "*{box-sizing:border-box}"
        "body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}"
        "main{max-width:820px;margin:0 auto;padding:1.5rem 1.25rem 4rem}"
        "a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}"
        ".bc{max-width:820px;margin:0 auto;padding:1rem 1.25rem 0;font-size:.85rem;color:var(--mut)}"
        ".bc a{color:var(--mut)}.bc span{color:var(--ink)}"
        ".eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.72rem;color:var(--mut);margin:.5rem 0 .25rem}"
        "h1{font-size:1.5rem;line-height:1.25;margin:.1rem 0 1rem}"
        "h2{font-size:1rem;margin:2rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--line)}"
        "dl{display:grid;grid-template-columns:max-content 1fr;gap:.3rem 1rem;margin:0}"
        "dt{color:var(--mut);font-size:.85rem}dd{margin:0}"
        "code{font:.85em ui-monospace,SFMono-Regular,Menlo,monospace;background:#f5f5f5;padding:.05em .35em;border-radius:3px}"
        "ul.cl{list-style:none;padding:0;margin:0;columns:2;column-gap:1.5rem}"
        "ul.cl li{margin:.15rem 0;break-inside:avoid}"
        ".note{color:var(--mut);font-size:.85rem;margin:.4rem 0}"
        ".dep{background:#fff6e5;border:1px solid #f0c36d;padding:.5rem .75rem;border-radius:6px;margin:1rem 0;font-size:.9rem}"
        "footer{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.82rem;color:var(--mut)}"
        "footer a{margin-right:1rem}"
        "details{margin:.3rem 0}summary{cursor:pointer;color:var(--mut)}"
        "@media(max-width:560px){ul.cl{columns:1}dl{grid-template-columns:1fr}}"
    )
    os.makedirs(os.path.join(OUT, "_assets"), exist_ok=True)
    with open(os.path.join(OUT, "_assets", "concept.css"), "w") as f:
        f.write(css)

    def ancestors(notation):
        chain, cur, guard = [], C[notation]["broader"], 0
        while cur and cur in C and guard < 12:
            chain.append(cur)
            cur = C[cur]["broader"]
            guard += 1
        return list(reversed(chain))

    n = 0
    for r in rows:
        notation = r["notation"]
        label, uri, broader = r["pref_label"], r["uri"], r["broader"]
        depth, domain, deprecated = r["depth"], r["top_domain"], r["deprecated"]
        replaced_by = r["replaced_by"]
        # follow replaced_by chain to the final live winner
        rb_final, _g = replaced_by, 0
        while rb_final and rb_final in C and C[rb_final]["deprecated"] and _g < 12:
            rb_final = C[rb_final]["replaced_by"]; _g += 1

        bc = [f'<a href="{BASE}/">OLIT</a>',
              f'<a href="{rel_prefix() or "./"}">concepts</a>']
        for a in ancestors(notation):
            bc.append(f'<a href="{link_to(a)}">{e(C[a]["pref_label"])}</a>')
        bc.append(f"<span>{e(label)}</span>")
        breadcrumb = " › ".join(bc)

        if broader and broader in C:
            broader_row = (
                f'<dt>Broader</dt><dd><a href="{link_to(broader)}">'
                f'{e(C[broader]["pref_label"])}</a> <code>{broader}</code></dd>'
            )
        else:
            broader_row = "<dt>Broader</dt><dd>— (top-level domain)</dd>"

        kids = children.get(notation, [])
        if kids:
            shown = kids[:MAX_CHILDREN]
            items = "".join(
                f'<li><a href="{link_to(k)}">{e(C[k]["pref_label"])}</a> '
                f"<code>{k}</code></li>"
                for k in shown
            )
            more = ""
            if len(kids) > MAX_CHILDREN:
                more = (
                    f'<p class="note">Showing {MAX_CHILDREN} of {len(kids)}. '
                    f'Full hierarchy in the <a href="{BASE}/explore/">explorer</a> '
                    f'and <a href="{BASE}/legal-taxonomy.ttl">data dumps</a>.</p>'
                )
            children_block = f'<ul class="cl">{items}</ul>{more}'
        else:
            children_block = '<p class="note">No narrower concepts (leaf).</p>'
        nchild = len(kids)

        nsrc = src_count.get(notation, 0)
        if nsrc:
            sample = src_sample.get(notation, [])
            ids = ", ".join(f"<code>{e(s)}</code>" for s in sample)
            extra = f" (first {len(sample)})" if nsrc > len(sample) else ""
            sources_block = (
                f"<details><summary>{nsrc} source section"
                f"{'s' if nsrc != 1 else ''}{extra}</summary>"
                f'<p class="note">{ids}</p></details>'
            )
        else:
            sources_block = '<p class="note">No source sections linked.</p>'

        if deprecated:
            if rb_final and rb_final in C:
                rb_link = (f'<a href="{link_to(rb_final)}">{e(C[rb_final]["pref_label"])}</a> '
                           f"<code>{rb_final}</code>")
                dep_banner = (
                    '<p class="dep">⚠ This concept is <strong>deprecated</strong> '
                    "(merged during de-duplication). Its URI stays resolvable for "
                    f"stability, but use <strong>{rb_link}</strong> instead.</p>"
                )
            else:
                dep_banner = (
                    '<p class="dep">⚠ This concept is <strong>deprecated</strong>. '
                    "Its URI stays resolvable, but it should not be used for new "
                    "classification.</p>"
                )
        else:
            dep_banner = ""

        jd = {
            "@context": {"skos": "http://www.w3.org/2004/02/skos/core#"},
            "@id": uri,
            "@type": "skos:Concept",
            "skos:notation": notation,
            "skos:prefLabel": {"@language": "en", "@value": label},
            "skos:inScheme": {"@id": SCHEME_URI},
        }
        if broader and broader in C:
            jd["skos:broader"] = {"@id": C[broader]["uri"]}
        if depth == 1:
            jd["skos:topConceptOf"] = {"@id": SCHEME_URI}
        if deprecated:
            jd["owl:deprecated"] = True
            jd["@context"]["owl"] = "http://www.w3.org/2002/07/owl#"
            if rb_final and rb_final in C:
                jd["@context"]["dct"] = "http://purl.org/dc/terms/"
                jd["dct:isReplacedBy"] = {"@id": C[rb_final]["uri"]}
        jsonld = json.dumps(jd, ensure_ascii=False, separators=(",", ":"))

        doc = (
            "<!doctype html><html lang=en><head><meta charset=utf-8>"
            '<meta name=viewport content="width=device-width,initial-scale=1">'
            f"<title>{e(label)} · OLIT {notation}</title>"
            f'<link rel=canonical href="{uri}">'
            f'<link rel=stylesheet href="{rel_prefix()}_assets/concept.css">'
            f'<script type="application/ld+json">{jsonld}</script></head><body>'
            f'<nav class="bc">{breadcrumb}</nav><main>'
            f'<p class="eyebrow">Open Legal Issue Taxonomy · concept</p>'
            f"<h1>{e(label)}</h1>{dep_banner}"
            "<dl>"
            f"<dt>Notation</dt><dd><code>{notation}</code></dd>"
            f'<dt>URI</dt><dd><a href="{uri}"><code>{e(uri)}</code></a></dd>'
            f"<dt>Domain</dt><dd>{e(domain)}</dd>"
            f"<dt>Depth</dt><dd>{depth}</dd>"
            f"{broader_row}"
            "</dl>"
            f"<section><h2>Narrower concepts ({nchild})</h2>{children_block}</section>"
            f"<section><h2>Sources ({nsrc})</h2>{sources_block}</section>"
            "<footer>"
            f'<a href="{BASE}/">Home</a>'
            f'<a href="{BASE}/explore/">Explorer</a>'
            f'<a href="{BASE}/legal-taxonomy.ttl">TTL</a>'
            f'<a href="{BASE}/legal-taxonomy.jsonld">JSON-LD</a>'
            f'<a href="{BASE}/scheme.ttl">Scheme</a>'
            "</footer></main></body></html>"
        )

        p = out_path(notation)
        if LAYOUT == "dir":
            os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(doc)
        n += 1
        if n % 25000 == 0:
            print(f"  {n} pages... ({time.time()-t0:.1f}s)")

    tops = sorted([r["notation"] for r in rows if r["depth"] == 1])
    tli = "".join(
        f'<li><a href="{t}{"" if LAYOUT=="flat" else "/"}">'
        f'{e(C[t]["pref_label"])}</a> <code>{t}</code></li>'
        for t in tops
    )
    landing = (
        "<!doctype html><html lang=en><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        "<title>Concepts · Open Legal Issue Taxonomy</title>"
        f'<link rel=stylesheet href="_assets/concept.css"></head><body>'
        f'<nav class="bc"><a href="{BASE}/">OLIT</a> › <span>concepts</span></nav><main>'
        f'<p class="eyebrow">Open Legal Issue Taxonomy</p><h1>Concepts</h1>'
        f"<p>{len(C):,} legal-issue concepts under 13 top-level domains. "
        f"Each concept resolves at <code>{BASE}/concept/{{notation}}</code>.</p>"
        f'<section><h2>Top-level domains (13)</h2><ul class="cl">{tli}</ul></section>'
        "<footer>"
        f'<a href="{BASE}/">Home</a><a href="{BASE}/explore/">Explorer</a>'
        f'<a href="{BASE}/legal-taxonomy.ttl">TTL</a>'
        "</footer></main></body></html>"
    )
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(landing)

    print(f"DONE: {n} concept pages + landing + css in {time.time()-t0:.1f}s")
    print(f"layout={LAYOUT} out={OUT}")


if __name__ == "__main__":
    main()
