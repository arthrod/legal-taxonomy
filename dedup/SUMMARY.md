# OLIT sibling-deduplication — run summary

**Result:** 287,715 → **247,929 live** + **39,786 deprecated** (13.8% reduction). Integrity: **ALL PASS**.
Nothing deleted — losers are `deprecated=1` with `replaced_by` → winner; all URIs still resolve.
Backup of pre-dedup DB: `legal-taxonomy.db.bak`.

## Rules honored
- **Same label, different parent = KEPT.** `DAMAGES` survives 186× under 186 distinct parents; 28k+ labels legitimately repeat across parents, untouched. Only *siblings* (same parent) were ever merged.
- **Near-synonym siblings = MERGED.** e.g. `HUSBAND AND WIFE` absorbed `MARITAL RELATIONS`, `MARITAL RELATIONSHIPS`, `MARRIAGE AND SPOUSAL RELATIONSHIP`, +4 more.

## Method — 6-model ensemble vote (no single model trusted)
Voters: claude-opus-4-8, gpt-5.4 (Pioneer→OpenRouter), glm-5.2, deepseek-v4-pro, minimax-m3, nemotron-3-ultra-550b (OpenRouter). Each clustered every parent's siblings independently.
Merge applied where **≥3 of 6 agree** (half the ensemble) OR **all 3 named Chinese models agree**, plus lexical (word-order/plural) and orthographic (cos≥0.97, e.g. offences/offenses) tiers. Of 157k raw suggestions, 84k were lone-wolf (single model) and dropped.

Antonym guard (recognition≠nonrecognition), deepest-first ordering, children-re-parented-before-deprecate, and a lexical closure loop (cascades from collided children) were all applied. Legal embedder (Isaacus kanon-2-embedder) used to flag/validate, not gate.

## Verification
`python3 dedup/ensure_solid.py legal-taxonomy.db 287715` → 8/8 checks PASS
(totals conserved, no orphans, 13 tops intact, all reach a live root, no cycles, depth invariant, every deprecated resolves to a live winner, no dup siblings remain).

## Known residual (for review)
- `SPOUSAL RELATIONSHIPS` vs `HUSBAND AND WIFE` under one parent stays separate — models genuinely split (spousal may include non-marital partners). A substring hand-rule to force it wrongly merged "CIVIL ACTIONS ARISING FROM MARITAL RELATIONSHIPS", so it was reverted.
- minimax-m3 completed 25,084/25,961 parents (budget hit $0); union voting covered the rest via the other 5 models.

## NOT done (needs approval — outward-facing)
Regenerate `dumps/`, `legal-taxonomy.ttl/.jsonld`, the 287k `concept/*.html` (`tools/gen_concept_pages.py`), re-gzip `legal-taxonomy.db.gz`, and commit. Held pending Arthur's go-ahead.
