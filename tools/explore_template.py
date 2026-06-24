import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import json, gzip, base64

    return base64, gzip, json, mo


@app.cell(hide_code=True)
def _(base64, gzip, json):
    # Full tree embedded once (gzip+base64). Rendered lazily: only the children
    # of the node you are currently on are ever materialised, so you can drill to
    # any depth without loading or rendering all ~288k concepts at once.
    _BLOB = "__BLOB__"
    _data = json.loads(gzip.decompress(base64.b64decode(_BLOB)))
    domains = _data["domains"]                 # 13 top-domain labels
    dom_root = _data["dom_root"]               # notation of each domain's root concept
    rows = _data["rows"]                       # [notation,label,broader,depth,domidx,ndesc,nsrc]
    totals = _data["totals"]
    domain_summary = _data["domain_summary"]
    depth_hist = _data["depth_hist"]
    examples = _data["examples"]
    featured = _data["featured"]

    by_id = {r[0]: r for r in rows}            # notation -> row
    children = {}                              # notation -> list of child rows
    for _r in rows:
        if _r[2] is not None:
            children.setdefault(_r[2], []).append(_r)
    nchild = {k: len(v) for k, v in children.items()}  # notation -> # direct children

    disp = lambda s: s.title()
    return (
        by_id,
        children,
        depth_hist,
        disp,
        dom_root,
        domain_summary,
        domains,
        examples,
        featured,
        nchild,
        totals,
    )


@app.cell(hide_code=True)
def _(mo, totals):
    mo.md(
        f"""
        # ⚖️ Open Legal Issue Taxonomy (OLIT)

        An interactive look at a SKOS controlled vocabulary of
        **{totals['concepts']:,} legal-issue concepts**, organised under
        **{totals['domains']} top-level domains** and grounded in
        **{totals['sources']:,} source classifications**. Each concept has a stable,
        permanent identifier at `https://w3id.org/legal-taxonomy/concept/{{notation}}`.

        *Browse the whole tree below — pick a domain and drill in as deep as you like
        (all the way to depth {totals['maxdepth']}). Each step only loads the branch
        you open.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, totals):
    mo.hstack(
        [
            mo.stat(value=f"{totals['concepts']:,}", label="Concepts", bordered=True),
            mo.stat(value=str(totals["domains"]), label="Top domains", bordered=True),
            mo.stat(value=f"{totals['sources']:,}", label="Source links", bordered=True),
            mo.stat(value=str(totals["maxdepth"]), label="Max depth", bordered=True),
        ],
        justify="start",
        gap=1,
    )
    return


@app.cell(hide_code=True)
def _(disp, domain_summary, mo):
    _mx = max(d["concepts"] for d in domain_summary)

    def _bar(d):
        _pct = 100 * d["concepts"] / _mx
        return (
            '<div style="display:flex;align-items:center;gap:10px;margin:3px 0;'
            'font-family:system-ui,sans-serif;font-size:12.5px">'
            f'<div style="width:300px;text-align:right;color:#343a40">{disp(d["domain"])[:46]}</div>'
            '<div style="flex:1;background:#f1f3f5;border-radius:4px;overflow:hidden">'
            f'<div style="width:{_pct}%;min-width:3px;height:16px;'
            'background:linear-gradient(90deg,#4263eb,#74c0fc)"></div></div>'
            f'<div style="width:64px;color:#495057">{d["concepts"]:,}</div></div>'
        )

    _bars = "".join(_bar(d) for d in sorted(domain_summary, key=lambda x: -x["concepts"]))
    mo.md("### Concepts by legal domain\n\n<div>" + _bars + "</div>")
    return


@app.cell(hide_code=True)
def _(depth_hist, mo):
    _mx = max(c for _, c in depth_hist)

    def _bar(d, c):
        _pct = 100 * c / _mx
        return (
            '<div style="display:flex;align-items:center;gap:10px;margin:3px 0;'
            'font-family:system-ui,sans-serif;font-size:12.5px">'
            f'<div style="width:70px;text-align:right;color:#343a40">depth {d}</div>'
            '<div style="flex:1;background:#f1f3f5;border-radius:4px;overflow:hidden">'
            f'<div style="width:{_pct}%;min-width:3px;height:14px;background:#20c997"></div></div>'
            f'<div style="width:64px;color:#495057">{c:,}</div></div>'
        )

    _bars = "".join(_bar(d, c) for d, c in depth_hist)
    mo.md(
        "### How deep the tree goes\n\nConcept count at each level of nesting "
        "(depth 1 = the broad domains, deeper = more specific issues).\n\n<div>"
        + _bars + "</div>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## 🔎 Browse the taxonomy

        Pick a domain, then click any row to drill into it. Use **↑ Up one level** or
        the breadcrumb to climb back. Rows are sorted by how many concepts sit beneath
        them, so the biggest branches come first.
        """
    )
    return


@app.cell(hide_code=True)
def _(disp, dom_root, domains, mo):
    get_path, set_path = mo.state([dom_root[0]])

    domain_dd = mo.ui.dropdown(
        options={disp(domains[i]): dom_root[i] for i in range(len(domains))},
        value=disp(domains[0]),
        label="**Jump to domain**",
        on_change=lambda nid: set_path([nid]) if nid else None,
    )
    up_btn = mo.ui.button(
        label="↑ Up one level",
        on_change=lambda _v: set_path(get_path()[:-1] or get_path()),
    )
    top_btn = mo.ui.button(
        label="⟲ Domain top",
        on_change=lambda _v: set_path(get_path()[:1] or get_path()),
    )
    return domain_dd, get_path, set_path, top_btn, up_btn


@app.cell(hide_code=True)
def _(by_id, children, disp, domain_dd, get_path, mo, nchild, top_btn, up_btn):
    cur_path = get_path()
    cur_node = cur_path[-1]
    _row = by_id[cur_node]
    _kids = children.get(cur_node, [])

    _crumb = " › ".join(disp(by_id[n][1]) for n in cur_path)
    _uri = f"https://w3id.org/legal-taxonomy/concept/{cur_node}"
    _header = mo.md(
        f"**{disp(_row[1])}**  ·  id [`{cur_node}`]({_uri})  ·  depth {_row[3]}  ·  "
        f"**{_row[5]:,}** concepts below  ·  **{_row[6]:,}** sources"
    )

    if _kids:
        _data = [
            {
                "id": r[0],
                "concept": disp(r[1]),
                "children": nchild.get(r[0], 0),
                "concepts below": r[5],
                "sources": r[6],
            }
            for r in sorted(_kids, key=lambda r: -r[5])
        ]
        drill_table = mo.ui.table(
            _data,
            selection="single",
            page_size=15,
            label=f"**{len(_kids)} sub-concepts** — click a row to drill in",
        )
        _body = drill_table
    else:
        drill_table = None
        _body = mo.callout(
            mo.md(
                f"**{disp(_row[1])}** is a leaf — no narrower concepts. "
                f"Its permanent id resolves at [{_uri}]({_uri})."
            ),
            kind="success",
        )

    _view = mo.vstack(
        [
            mo.hstack([domain_dd, up_btn, top_btn], justify="start", gap=0.75, align="end"),
            mo.md(f"**Path:** {_crumb}"),
            _header,
            _body,
        ]
    )
    _view
    return cur_node, cur_path, drill_table


@app.cell(hide_code=True)
def _(cur_path, drill_table, get_path, set_path):
    # React to a row selection by drilling in. marimo tables expose selection via
    # `.value` (read reactively here) rather than an on_change callback.
    if drill_table is not None and drill_table.value:
        _cid = drill_table.value[0]["id"]
        if get_path() == cur_path and _cid != cur_path[-1]:
            set_path(cur_path + [_cid])
    return


@app.cell(hide_code=True)
def _(disp, examples, featured, mo):
    _rows = "".join(
        f'<tr><td style="padding:3px 16px 3px 0">{disp(e["label"])}</td>'
        f'<td style="text-align:right;color:#4263eb;font-weight:600">{e["parents"]}</td></tr>'
        for e in examples
    )
    _samples = ", ".join(f"_{disp(p)}_" for p in featured["sample_parents"])
    mo.md(
        f"""
        ## 🧭 One issue, many homes

        The same legal idea legitimately recurs under different parents — and that is
        intentional. **{disp(featured['label'])}** appears under **{featured['parents']}
        different parents**, each a distinct concept (e.g. {_samples}, …). Identity is
        the parent context, not the label alone — which is why every node has its own
        permanent id.

        **Labels appearing under the most distinct parents:**

        <table style="font-family:system-ui,sans-serif;font-size:13px">
        <tr><th style="text-align:left">Label</th><th style="text-align:right"># parents</th></tr>
        {_rows}
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## 📦 Get the data

        - **Per-concept pages:** every concept resolves at
          `https://w3id.org/legal-taxonomy/concept/{notation}`
        - **Full vocabulary (SKOS / Turtle):** [legal-taxonomy.ttl](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.ttl)
        - **Full vocabulary (JSON-LD):** [legal-taxonomy.jsonld](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.jsonld)
        - **SQLite database (all 287k concepts + source links):** [legal-taxonomy.db.gz](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.db.gz)
        - **Project:** [github.com/arthrod/legal-taxonomy](https://github.com/arthrod/legal-taxonomy)

        *This notebook embeds the full tree (depth 7) and expands one branch at a time,
        so you can browse every concept offline without loading them all at once.*
        """
    )
    return


if __name__ == "__main__":
    app.run()
