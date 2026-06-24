# Open Legal Issue Taxonomy (OLIT)

A SKOS controlled vocabulary of **247,929 active legal-issue concepts** organised under
**13 top-level legal domains**, with stable, permanent identifiers. A further **39,786
near-duplicate concepts have been merged and deprecated** (retained as resolvable URIs) by a
six-model ensemble de-duplication pass — see [Status & provenance](#status--provenance).

- **Browse / data site:** https://arthrod.github.io/legal-taxonomy/
- **Interactive explorer:** https://arthrod.github.io/legal-taxonomy/explore/ *(in-browser notebook — no install)*
- **Permanent identifier base:** `https://w3id.org/legal-taxonomy/` *(live via [w3id PR #6235](https://github.com/perma-id/w3id.org/pull/6235) — 302-redirects to the GitHub Pages site)*

## Identifiers

| Thing | Pattern |
|-------|---------|
| Concept | `https://w3id.org/legal-taxonomy/concept/{notation}` (e.g. `…/concept/000054`) |
| Concept scheme | `https://w3id.org/legal-taxonomy/scheme/olit` |

Each concept is a `skos:Concept`. Identity is the opaque `skos:notation`, decoupled
from the label — a concept keeps its ID even if it is relabelled or moved.

Every concept URI **resolves to a human-readable HTML page** (breadcrumb up to its
top domain, broader/narrower links, source counts) — e.g.
[`…/concept/010089`](https://w3id.org/legal-taxonomy/concept/010089) — in addition to
appearing in the bulk RDF dumps below.

## Download the data

| File | Format | Contents |
|------|--------|----------|
| [`legal-taxonomy.ttl`](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.ttl) | SKOS / Turtle | full vocabulary (scheme + all concepts) |
| [`legal-taxonomy.jsonld`](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.jsonld) | JSON-LD | full vocabulary |
| [`scheme.ttl`](https://arthrod.github.io/legal-taxonomy/scheme.ttl) | Turtle | the `skos:ConceptScheme` + 13 top concepts |
| [`dumps/`](https://arthrod.github.io/legal-taxonomy/dumps/) | Turtle | concepts split by top-level domain |
| [`legal-taxonomy.db.gz`](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.db.gz) | SQLite (gzip) | all 287,715 concepts (247,929 active + 39,786 deprecated) + 156k source links, queryable |

GitHub Pages serves `.ttl` as `text/turtle` and `.jsonld` as `application/ld+json`,
so Linked Data clients can consume the URLs directly.

## SKOS shape

```
skos:Concept        a concept (a legal issue in its parent's context)
skos:notation       the opaque, permanent code (e.g. "000054")
skos:prefLabel      the preferred label (@en)
skos:broader        the parent concept
skos:topConceptOf   the 13 top-level domains
skos:inScheme       the concept scheme
owl:deprecated      set on retired (merged) concepts — their URIs stay resolvable
dct:isReplacedBy    on a deprecated concept, points to the live concept it merged into
skos:historyNote    records the merge ("Deduplicated 2026-06: merged into c:…")
```

Deprecated concepts keep their `skos:notation`, `skos:prefLabel`, and `skos:inScheme`, but are
dropped from the live `skos:broader` hierarchy — so the active tree contains only live concepts,
while every retired URI still dereferences and tells you (via `dct:isReplacedBy`) where to go.

## Status & provenance

Concepts are derived from an aggregation of legal-source classifications. The tree is
**stable and addressable**. A de-duplication pass merged near-synonymous **sibling** concepts
(same parent only — a label repeated under *different* parents is a distinct concept and is kept;
e.g. `DAMAGES` survives under 186 different parents). Merges were decided by a **six-model
ensemble** (claude-opus-4-8, gpt-5.4, glm-5.2, deepseek-v4-pro, minimax-m3, nemotron-3-ultra-550b):
a sibling pair is merged only when **≥ half the models agree** (or all three of glm/minimax/deepseek
agree), plus word-order/plural and orthographic equivalence. Retired concepts are deprecated
(`owl:deprecated`) and linked to their replacement (`dct:isReplacedBy`), **never deleted**, so
published URIs never break.

## Regenerating the concept pages

The per-concept HTML pages under `concept/` are generated from
`legal-taxonomy.db.gz`:

```
python3 tools/gen_concept_pages.py
```

This writes `concept/{notation}.html` for every concept — flat files so
`/concept/{notation}` resolves with a direct `200` on GitHub Pages — plus a
`concept/` index and the shared stylesheet. Re-run it after any curation pass
that changes the SQLite snapshot.

The RDF artifacts (`legal-taxonomy.ttl`, `legal-taxonomy.jsonld`, `scheme.ttl`, `dumps/`)
are regenerated from the same `legal-taxonomy.db` by `python3 tools/gen_rdf.py`, which
emits the `owl:deprecated` / `dct:isReplacedBy` / `skos:historyNote` triples for merged
concepts. The de-duplication tooling itself lives under `dedup/` (six-model ensemble vote,
apply, lexical closure, and an integrity verifier — `dedup/SUMMARY.md` has the details).

## Maintainer

Arthur S. Rodrigues — arthursrodrigues@gmail.com — GitHub: [@arthrod](https://github.com/arthrod)
