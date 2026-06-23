# Open Legal Issue Taxonomy (OLIT)

A SKOS controlled vocabulary of **~288,000 legal-issue concepts** organised under
**13 top-level legal domains**, with stable, permanent identifiers.

- **Browse / data site:** https://arthrod.github.io/legal-taxonomy/
- **Interactive explorer:** https://arthrod.github.io/legal-taxonomy/explore/ *(in-browser notebook — no install)*
- **Permanent identifier base:** `https://w3id.org/legal-taxonomy/` *(pending [w3id PR #6235](https://github.com/perma-id/w3id.org/pull/6235); until merged, use the GitHub Pages URL above)*

## Identifiers

| Thing | Pattern |
|-------|---------|
| Concept | `https://w3id.org/legal-taxonomy/concept/{notation}` (e.g. `…/concept/000054`) |
| Concept scheme | `https://w3id.org/legal-taxonomy/scheme/olit` |

Each concept is a `skos:Concept`. Identity is the opaque `skos:notation`, decoupled
from the label — a concept keeps its ID even if it is relabelled or moved.

## Download the data

| File | Format | Contents |
|------|--------|----------|
| [`legal-taxonomy.ttl`](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.ttl) | SKOS / Turtle | full vocabulary (scheme + all concepts) |
| [`legal-taxonomy.jsonld`](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.jsonld) | JSON-LD | full vocabulary |
| [`scheme.ttl`](https://arthrod.github.io/legal-taxonomy/scheme.ttl) | Turtle | the `skos:ConceptScheme` + 13 top concepts |
| [`dumps/`](https://arthrod.github.io/legal-taxonomy/dumps/) | Turtle | concepts split by top-level domain |
| [`legal-taxonomy.db.gz`](https://arthrod.github.io/legal-taxonomy/legal-taxonomy.db.gz) | SQLite (gzip) | all 287k concepts + 156k source links, queryable |

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
owl:deprecated      set on retired concepts (their URIs stay resolvable)
```

## Status & provenance

Concepts are derived from an aggregation of legal-source classifications. The tree
is **stable and addressable**; editorial de-duplication of near-synonymous labels is
an ongoing curation pass. Retired concepts are deprecated (`owl:deprecated`), never
deleted, so published URIs never break.

## Maintainer

Arthur S. Rodrigues — arthursrodrigues@gmail.com — GitHub: [@arthrod](https://github.com/arthrod)
