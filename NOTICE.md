# NOTICE — Open Legal Issue Taxonomy (OLIT)

## Licensing

- **Vocabulary and data** — the concept scheme, concepts, labels, notations, hierarchy,
  mappings, RDF/JSON-LD/SQLite artifacts, HTML concept pages, and documentation in this
  repository — are licensed under
  **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**
  (see [`LICENSE`](LICENSE)).
- **Code** — the scripts under `tools/` and `dedup/` — is licensed under the
  **[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)**
  (see [`LICENSE-CODE`](LICENSE-CODE)).

## Attribution

When reusing the vocabulary, please attribute:

> Rodrigues, Arthur S. *Open Legal Issue Taxonomy (OLIT)*. 2026.
> https://w3id.org/legal-taxonomy/ — CC BY 4.0.

Machine-readable license and attribution statements are embedded in the
`skos:ConceptScheme` (`scheme.ttl`, `legal-taxonomy.ttl`, `legal-taxonomy.jsonld`)
via `dct:license`, `cc:attributionName`, and `cc:attributionURL`.

## Sources

OLIT was synthesized from the section headings and tables of contents of **739 legal
works**, classified one heading at a time with full per-item provenance (source
identifier, sha256, edition, year, and legal basis, recorded in the build data):

- **≈87–90% United States public domain** — treatises and encyclopedias published on or
  before 1930, American Law Institute proposed drafts of the 1920s, and U.S. government
  works (17 U.S.C. § 105) such as Federal Judicial Center monographs;
- **≈10–13% openly licensed teaching materials** — Harvard H2O open casebooks and CALI
  eLangdell titles (predominantly CC BY-NC-SA), used with per-item license records;
- **no content from any proprietary legal database** (Westlaw, Lexis, Bloomberg Law, or
  similar) was used at any stage; this exclusion is an enforced rule of the build
  pipeline.

**Position on NC-licensed sources:** concept labels in this vocabulary are normalized
short phrases and structural facts derived from source headings; they are not
substantial reproductions of any source. Item records referencing CC BY-NC-SA sources
contain only identifiers and pointers, never source text. The NonCommercial condition
of those sources therefore does not attach to this vocabulary. The full text of the
sources is not distributed here.

## FOLIO (applies to FOLIO-anchored editions)

FOLIO-anchored editions of this taxonomy (the dual-root v2/v3 digest artifacts, where
published) incorporate and map to concepts from the **Federated Open Legal Information
Ontology (FOLIO)**, used under CC BY 4.0 — publisher/steward: ALEA Institute and FOLIO
contributors (https://github.com/alea-institute/FOLIO, namespace
`https://folio.openlegalstandard.org/`). Local mappings, issue records, labels,
hierarchies, deduplication decisions, and scope notes are the work of this project and
are not part of upstream FOLIO. Builds pin the exact FOLIO snapshot; the v2/v3 build
manifest records OWL artifact sha256
`44657b4ed844f5f9c9c48869184606b4fc671471a8263d79d241de87809fa239`.
The plain SKOS vocabulary in this repository (v1 lineage) does not include FOLIO
content.

## No endorsement

Use of the named sources, FOLIO, the ALEA Institute, Harvard H2O, or CALI does not
imply endorsement by any of them. This vocabulary is an independent work; it is not
affiliated with, and does not reproduce, any commercial legal classification system.

## Maintainer

Arthur S. Rodrigues — arthursrodrigues@gmail.com — GitHub
[@arthrod](https://github.com/arthrod)
