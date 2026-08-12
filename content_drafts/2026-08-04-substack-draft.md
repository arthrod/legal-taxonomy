TITLE: skos:Concept or owl:Class? A fight about legal taxonomies that nobody is having
SUBTITLE: West built the map in 1906, the open standard forked in 2025, and the W3C solved the plumbing in 2009. So where is the thing?

---

Run this and look at what comes back:

```
curl -sI "https://legal.thomsonreuters.com/en/products/westlaw" | head -1
```

That resolves fine, because it is a marketing page. Now try to construct a URL for a specific West key number, say the one for reformation of contracts for mutual mistake. You cannot, because there isn't one. The most granular classification of American law ever built, roughly 100,000 numbered points of law under 400+ topics, has no public addressing scheme at all. It is a map you can only look at through one company's window, and the window has a EULA.

This post is about the three-body problem of legal taxonomies: the closed one that is deep, the open ones that are shallow and currently in a standoff, and the seventeen-year-old W3C standard sitting quietly in the corner that could carry the whole thing. By the end I want to convince you of two claims: that an open, issue-level legal vocabulary is the missing dependency under most of legal AI, and that the correct data model for it is the boring one.

## The deep one is closed

The history is better than the punchline, so indulge me for three paragraphs.

In 1876, John B. West was a 24-year-old selling law books to Minnesota lawyers out of St. Paul, listening to the same complaint on every call: by the time the official state reports published a decision, it was old news. So he started an eight-page weekly called The Syllabi, promising "prompt and reliable intelligence" on what the Minnesota courts had just held. It sold. The newsletter became the North Western Reporter, the reporter became the National Reporter System, and within a generation a book peddler's side project was the de facto publication layer for American case law. The startup playbook, complete with wedge product and platform expansion, run a century before anyone wrote it down.

Volume created the next problem: an unclassified mountain of decisions is barely more useful than no decisions. West's solution was partly acquisition. He bought the subscriber list of a competing digest and hired its author, John A. Mallory, who then spent years building the classification that mattered: seven grand divisions (persons, property, contracts, torts, crime, remedies, government) subdividing all of American law, constructed between 1897 and 1906. That scheme, extended and curated by hand ever since, is the West Key Number System.

And the design was right. Everything that makes modern retrieval hard, they hit first: granularity (a "topic" is useless, a point of law is useful), stability (numbers survive relabeling), and maintenance (law moves, the tree must move with it, without breaking old references).

Their solutions were correct. Opaque numeric identity decoupled from labels. Hierarchical addressing. Editorial curation as a permanent cost center, not a launch task. If you designed a concept scheme from scratch today you would arrive at the same invariants.

What they could not have designed for, in 1906, is the open web. There are no URIs. There is no license under which you can tag your own corpus with key numbers and share it. Interoperability with a Thomson Reuters product is a feature; interoperability with the world is not on the roadmap. Again: their asset, their right. But it means the deepest map is unusable as public infrastructure, and public infrastructure is what everything else in this post is starving for.

## The open ones are shallow, and fighting

The open world produced exactly one Schelling point: SALI's Legal Matter Standard Specification, 18,000+ tags under an MIT license, real adoption since 2022, strongest on the business-of-law axis: areas of law, services, industries, matter metadata.

Then late 2024 happened. Contributors raised governance concerns about the SALI nonprofit. The ALEA Institute forked the MIT-licensed spec (first as SOLI, September 2024). SALI answered with cease-and-desist letters (January 2025). The fork rebranded as FOLIO (March 2025) and published its account in an open letter; SALI disputes the fork's legitimacy and has continued shipping its own LMSS v3 process. As of this writing I can find no public resolution. I know some of the people involved by reputation only, I have no inside knowledge, and I am not adjudicating it from a blog post.

Two observations that survive any version of the facts.

The MIT license did its job. The moment the work was published under MIT in 2022, its survival stopped depending on any one institution's health. Fork rights are not a loophole; they are the mechanism. If you have ever contributed unpaid hours to a standard, the license is the only thing standing between your work and someone else's org chart.

But the fork also cut the network in half. A standard is only worth what everyone else's adoption makes it worth, and "which of the two open standards do you support" is now a real question vendors have to answer. The dispute may resolve; the fragmentation cost has already been paid.

And here is the technical point that gets lost under the drama: even a unified, healthy FOLIO-slash-LMSS would not close the gap this post is about. 18,000 concepts of mostly matter metadata is a different animal from 100,000 points of law. One tells you the matter is "Securities: Enforcement, Financial Services industry." The other tells you the document is about the reliance element of a 10b-5 claim against a non-trading defendant. Retrieval, routing, conflict checks, benchmark labels: the interesting applications live at the second granularity.

## The boring standard already won everywhere else

SKOS became a W3C Recommendation on August 18, 2009. Here is a complete, publishable concept in it:

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<https://example.org/concept/041237> a skos:Concept ;
  skos:notation "041237" ;
  skos:prefLabel "REFORMATION FOR MUTUAL MISTAKE"@en ;
  skos:broader <https://example.org/concept/041201> ;
  skos:inScheme <https://example.org/scheme/legal> .
```

Five properties. Identity lives in the opaque notation, not the label, so you can fix a typo without breaking a decade of references, which is the same trick West figured out in 1906. The URI resolves to a page a human can read and a client can parse. Hierarchy is one hop at a time via skos:broader. Deprecation has an answer too: owl:deprecated plus dct:isReplacedBy means a retired concept keeps resolving and tells you where it went, so published annotations never rot.

This is not exotic. Library subject headings, museum collections, and the EU's EuroVoc thesaurus (20+ languages, every member state pointing at the same URIs) all run on exactly this. The pattern has been in production for longer than most legal tech companies have existed.

## Everyone else built the plumbing. The biggest market did not.

Here is where the story stops being funny and starts being a policy failure.

Other jurisdictions decided legal findability is public infrastructure and standardized accordingly. Europe has ECLI, an open identifier scheme for case law, so a judgment in Rotterdam and a judgment in Vienna are citable the same way by any system, for free; ELI does the same for legislation; Akoma Ntoso gives legislative documents a shared open XML vocabulary. The free-access-to-law movement got there even earlier and from the bottom up: AustLII publishing Australian case law openly since 1995, BAILII and CanLII following, the latter funded by the Canadian profession itself as a matter of course.

Now hold that against the United States: the largest legal market in the world, roughly 396 billion dollars in 2024, the jurisdiction whose case law the rest of the common-law world actually reads. Its issue-level map is a trade secret. Its open standards for matter metadata are mid-fork. And per the Legal Services Corporation's 2022 study, 92 percent of low-income Americans' civil legal problems receive no or insufficient legal help.

The honest version of the access-to-justice link, because I refuse to hand-wave it: a SKOS file has never represented anyone in an eviction. Classification is one layer of the stack. But it is the routing layer. Court self-help portals, legal aid intake, pro bono matching, the triage tools that decide whether your problem is "landlord-tenant: habitability" or "consumer debt: garnishment" before any human sees it: all of them need a shared answer to "what kind of legal problem is this," and in the US there is no open one at usable depth, so every project rebuilds a worse private one. The people who can pay for Westlaw get the century-old map. The tools serving the other 92 percent get a dropdown someone wrote at a hackathon.

For the biggest legal market on earth, that arrangement is not conservative. It is a slow-motion disaster, and it is invisible precisely because everyone inside it has stopped noticing the plumbing is missing.

## The fight nobody is having: skos:Concept vs owl:Class

FOLIO made a defensible and interesting choice: it is an OWL ontology. Its 18,000+ things are classes with IRIs, and OWL gives you machinery SKOS refuses to: subclass reasoning, property restrictions, consistency checking. If your goal is representing legal knowledge, classes are seductive.

I think classes are the wrong primitive for an issue-level taxonomy, and since nobody else seems to want to have this argument in public, let me start it.

When you say `owl:Class`, you are making an ontological commitment: there exists a set of individuals, and membership in the set has truth conditions. "MOTOR VEHICLE" as a class is fine; a Honda is or is not one. But what are the individuals of "REFORMATION FOR MUTUAL MISTAKE"? Documents about it? Disputes involving it? Arguments invoking it? Pick any answer and rdfs:subClassOf starts lying to you. Is every instance of a child issue necessarily an instance of the parent issue? Under West-style trees, a narrower key number is not a logical subset of its parent, it is an editorial subdivision of a discussion. The hierarchy means "filed under," not "is a."

SKOS was designed for exactly this epistemic humility. skos:broader explicitly does not entail subsumption, does not require transitivity, and carries no instance semantics. It asserts what a legal index actually knows: this concept is organized under that one, in this scheme, per these editors. That is not a weakness. It is the accurate representation of what a century of legal classification practice has actually been doing.

There is also a brutal practical asymmetry. An OWL ontology at 100,000+ classes with real axioms is a curation and reasoning liability; every axiom is a promise someone must keep as law drifts. A SKOS scheme at that scale is just a very large, very useful index, and index maintenance is a solved editorial workflow. The metadata layer, where FOLIO lives, genuinely benefits from OWL's rigor. The issue layer needs the opposite trade: maximal coverage, minimal ontological debt.

Reasonable people disagree here, including people who have built more ontology than I have. The comment section exists for a reason.

## The raw material is public domain, which changes everything

The standard objection at this point: fine, but where would 100,000 open concepts come from? Paying editors to redo West's century is a nine-figure fantasy, and scraping anything proprietary is both wrong and a lawsuit.

The answer has been sitting in the stacks the whole time. American legal literature before 1930 is public domain: the great treatises, the encyclopedias, the digests of their day. ALI proposed drafts from the 1920s. Federal government works, which were never copyrightable at all. These are not marginal sources; they are the same editorial tradition West grew out of, written by the most careful legal taxonomists who ever lived, and their tables of contents and section headings encode millions of classification decisions.

Until recently that material was practically inert, because extracting a concept hierarchy from a few hundred scanned treatises was a lifetime of manual labor. It is not anymore. Reading section headings at scale, normalizing them, and placing them in a tree is exactly the kind of judgment-at-volume that current models, carefully supervised and checked against each other, are actually good at. The copyright status means the output can be genuinely open, CC-BY open, with no proprietary taint anywhere in the chain, provided you enforce that rule in the pipeline rather than in the README.

Honest limits, because there are several. A 1926 heading needs mapping, not copying; "TELEGRAPHS AND TELEPHONES" is not how anyone bills in 2026, and a pipeline that cannot distinguish live doctrine from historical curiosity produces a museum, not a tool. Deduplication at six figures is vicious, with a failure mode in each direction: merge "DAMAGES" under contracts with "DAMAGES" under torts and you have destroyed meaning, refuse to merge anything and you have a word list. And the deep question, the one West answered with a permanent editorial staff, is maintenance: an open vocabulary nobody curates is a snapshot with a license, and snapshots rot.

Those are engineering requirements, not impossibilities. Each one has a shape I recognize from systems that exist.

## Something has to be done

Add it up. The depth exists but is closed. The open standards are shallow at the issue level and split into two camps. Peer jurisdictions publish open legal identifiers as a matter of routine while the biggest legal market on earth runs on a trade secret and a justice gap. The publishing standard has been boring, proven, and free since 2009. The source material is public domain and finally machine-readable. Permanent identifier infrastructure (w3id.org and friends) is a solved problem run by volunteers.

Every ingredient for an open, issue-level, SKOS-native map of American law is lying on the table, and the field that invented systematic legal citation is the only one that has not picked its ingredients up.

I have been pulling on this thread for a while now, long enough to have opinions about deduplication ensembles and deprecation semantics that I did not plan to acquire. What I have seen convinces me the thing can exist, at the granularity that matters, under a license that lets you build on it without asking anyone.

More on that soon. First I want the fight: tell me why concepts should be classes, or why the metadata layer is enough, or why open curation always rots. Bring receipts. I intend to.

---

## OPEN QUESTIONS FOR ARTHUR

1. The 10b-5 reliance example and the "reformation for mutual mistake" example are illustrative, invented for the post, and not claimed to be actual key numbers. Confirm you are comfortable with clearly-illustrative examples, or I will rework around real public classifications (e.g. from a public-domain digest).
2. The skos:Concept vs owl:Class section takes your side of the argument explicitly and firmly. It is the spiciest part of the piece and also its best comment bait. Confirm the framing matches the position you actually hold, since you will have to defend it in the comments.
3. "Nine-figure fantasy" for redoing West's editorial century is a rhetorical estimate, not a sourced number. Keep, soften, or cut.
4. The turtle example uses example.org URIs so nothing about OLIT leaks. When you launch, a follow-up post can replace it with a real resolving concept, which will be a satisfying callback.
5. The dispute section says "suing each other" in the subtitle for punch, but the body only documents cease-and-desist letters, not filed litigation. Recommend changing the subtitle to "forked in 2025" (done in the title line above; the phrase "currently suing each other" also appears once in the intro, soften to "currently in a standoff" unless you have confirmed litigation).

## EVIDENCE LOG

- West Key Number System: 400+ topics, roughly 100,000 key numbers, classification built 1897 to 1906, curated since; West acquired by Thomson late 1990s. Sources: Thomson Reuters pages, Stanford Law research guide, Wikipedia (West American Digest System).
- Origins: John B. West, law book salesman in St. Paul from the early 1870s, launched The Syllabi (eight-page weekly) in 1876 at age 24, promising "prompt and reliable intelligence" on Minnesota decisions; grew into North Western Reporter then National Reporter System. West bought John A. Mallory's Complete Digest subscriber list; Mallory joined West and perfected the American Digest classification; seven original divisions (persons, property, contracts, torts, crime, remedies, government). Sources: Lawbook Exchange description of The Syllabi reprint, Riesenfeld Rare Books blog (U. Minn. Law Library), FundingUniverse and Encyclopedia.com West Group histories, Encyclopedia.com "Key Numbers".
- US legal services market: USD 396.1 billion in 2024, largest in the world. Source: Grand View Research, US legal services market outlook.
- Justice gap: 92 percent of low-income Americans' civil legal problems received no or insufficient legal help; 74 percent of low-income households experienced at least one civil legal problem in the prior year. Source: Legal Services Corporation, 2022 Justice Gap Report (justicegap.lsc.gov).
- Open legal identifiers elsewhere: ECLI (case law) and ELI (legislation), EU open standards; Akoma Ntoso, OASIS open XML standard for legislative documents; AustLII publishing openly since 1995; BAILII, CanLII (profession-funded) similar. Well-established; spot-check AustLII date before publishing.
- SKOS: W3C Recommendation 18 August 2009; core properties as described; owl:deprecated / dct:isReplacedBy deprecation pattern is standard SKOS/OWL practice.
- SALI LMSS: 18,000+ tags, MIT license, adoption since 2022, LMSS v3 process with public viewer. Sources: sali.org, lmss.io, Law.com (2025-03-21).
- FOLIO: OWL ontology, ~18,000+ classes, CC BY 4.0, ALEA Institute; SOLI fork September 2024; C&Ds January 13, 2025; FOLIO rebrand March 14, 2025; open letter March 20, 2025 (openlegalstandard.org). No public resolution found as of 2026-08-04.
- EuroVoc: EU SKOS thesaurus, 20+ languages (verify exact count before publishing).
- Public-domain basis (pre-1930 treatises, 1920s ALI drafts, 17 U.S.C. § 105 government works) mirrors OLIT's actual NOTICE.md source policy without disclosing the project, its name, or its numbers.
- Deliberately absent: OLIT name, concept counts (247,929 / 39,786 / 287,715), 739 sources, 13 domains, six-model ensemble, w3id namespace. All held for launch.
