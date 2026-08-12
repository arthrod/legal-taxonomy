# LinkedIn post series: testing the waters for the taxonomy launch
# Three posts, ship in order, roughly 2 to 4 days apart.
# None of them names the project. The work is the hook.

---

## POST 1: The map you cannot link to

MAIN POST:

The best map of American law was started by a 24-year-old book peddler in 1876. It is still the best one we have. And you are not allowed to link to it.

John B. West's eight-page weekly, The Syllabi, promised Minnesota decisions faster than the official reports. It grew into the National Reporter System, and between 1897 and 1906 his editors classified all of American case law into one tree: the Key Number System. Today, 400+ topics, roughly 100,000 numbered points of law, curated by hand ever since.

Here is the problem. Try to use it as infrastructure.

You cannot cite a key number as a stable URI. You cannot tag your own documents with it and publish the dataset. You cannot fine-tune a model on it or build a public benchmark against it. It lives inside a subscription, and the license ends where your product begins.

So every legal AI company rebuilds the same thing badly: a "practice areas" dropdown with 30 entries, versioned nowhere. I have reviewed vendor taxonomies that classify all of securities law under "Corporate." The 1906 editors would weep.

Now zoom out. The United States is the largest legal market in the world, roughly 400 billion dollars a year, and its only issue-level map of the law is a trade secret. Europe mints an open identifier for every judgment. We mint a login screen. For the biggest market on earth, that is not a quirk. It is a disaster.

Honest reading: West's editors add judgment no automated system matches, and Thomson Reuters owes nobody its crown jewel. The gap is not their fault. It is still a gap.

Links in comments. Question for the in-house and KM crowd: what do you actually tag matters and documents with today, and who maintains it?

COMMENT:

Background reading:
- West Key Number System overview: [Thomson Reuters link placeholder]
- Stanford Law guide to the Key Number System: [link placeholder]

Plain English: a legal taxonomy is a controlled list of concepts (issues, areas, doctrines) with stable IDs and a hierarchy, so different systems can agree on what a document is about. "Stable URI" means an identifier that lives at a web address anyone can resolve, forever.

Nitty-gritty: John B. West started selling law books in St. Paul in the early 1870s and launched The Syllabi in 1876. The classification scheme in roughly its modern shape was built 1897 to 1906, in large part by John A. Mallory, a digest competitor whose subscriber list West bought before hiring the man himself. The original scheme had seven grand divisions: persons, property, contracts, torts, crime, remedies, government. Today it sits behind Westlaw. KeyCite, which people sometimes confuse with it, is the citator (good law / bad law), not the taxonomy. The Europe reference is ECLI, the European Case Law Identifier, an open standard for citing judgments across member states.

Market figure: US legal services generated roughly 396 billion dollars in 2024 (Grand View Research), the largest legal market in the world.

VISUAL SUGGESTIONS:

1876 | THE SYLLABI LAUNCHES | a 24-year-old's newsletter becomes the map of US law
100,000 | KEY NUMBERS | issue-level granularity, built and curated by hand
$396B | US LEGAL MARKET, 2024 | the largest in the world, mapped by a trade secret

---

## POST 2: The open standard that forked

MAIN POST:

Legal tech finally got one open taxonomy standard. Then it split into two, and the story is a governance case study I would assign in a law school class.

SALI's Legal Matter Standard Specification: 18,000+ tags for areas of law, services, industries. MIT licensed. Real adoption since 2022. The closest thing the industry had to a shared vocabulary.

In August 2024, contributors raised concerns about the nonprofit's governance, including its Delaware corporate status. In September 2024, the ALEA Institute forked the MIT-licensed spec into a new project. In January 2025, SALI sent cease-and-desist letters. In March 2025, the fork rebranded as FOLIO. As of this writing I can find no public resolution, and SALI has continued shipping LMSS v3 on its own track.

To be clear about what I know: ALEA published its account in an open letter, SALI disputes the fork's legitimacy, and I have no inside knowledge. I am not taking a side on the facts.

The engineering lesson does not depend on whose account you believe. The MIT license did exactly what open licenses are for: when the institution wobbled, the work survived. Whatever else was lost, the tags were not.

The cost is real too. Vendors now ask "which standard?" where a year earlier there was one answer. Fragmentation is the tax on governance failure, and in the largest legal market in the world, everyone pays it.

Honest reading: forks are also how open ecosystems heal. Two active projects beat one paused one.

Links in comments. Question: if your firm depends on a standard, what governance would actually make you trust it? Foundation, consortium, W3C process, or just a license and a git history?

COMMENT:

Sources:
- ALEA's open letter, "What's Happening with SALI, SOLI, and FOLIO?": https://openlegalstandard.org/whats-happening-with-sali-soli-folio/
- Law.com coverage of the dispute (Mar 2025): [link placeholder]
- SALI LMSS: https://sali.org / FOLIO: https://openlegalstandard.org

Both projects are worth your attention regardless of the dispute. The point of this post is the mechanism, not the verdict.

VISUAL SUGGESTIONS:

18,000+ | TAGS IN THE STANDARD | MIT licensed, which is why the fork was lawful
2 | COMPETING OPEN STANDARDS | where 12 months earlier there was one
5 | MONTHS OF ATTEMPTED MEETINGS | before the first cease-and-desist, per ALEA's account

---

## POST 3: The boring technology that already solved this

MAIN POST:

The hard technical problem of publishing a legal taxonomy was solved in 2009, by a standard most lawyers have never heard of, in about five properties.

SKOS. Simple Knowledge Organization System. A W3C Recommendation since August 2009. A concept gets a permanent URI, a label, a notation, a parent, and a scheme. Libraries run on it. Museums run on it. The EU publishes EuroVoc with it in 20+ languages.

So why does law not have an open issue-level vocabulary built on it?

Not for lack of pieces. FOLIO has 18,000+ concepts under CC BY, strongest on matter metadata. West has the issue-level depth, roughly 100,000 points of law, none of it open. Between them sits the gap: nothing open at Key Number granularity, with resolvable URIs and a license you can build on.

Other jurisdictions stopped waiting. Europe mints open identifiers for judgments (ECLI) and legislation (ELI); AustLII, BAILII, and CanLII have published case law openly since the 1990s. The largest legal market in the world keeps its only issue-level map behind a subscription, while 92 percent of low-income Americans' civil legal problems get little or no legal help. You cannot triage what you cannot label, and the labels are paywalled. A disaster hiding in plain sight.

The raw material for fixing it sits in the public domain: pre-1930 treatises, ALI drafts from the 1920s, government works. Millions of section headings, waiting for machines that finally read.

Honest reading: a heading is not a concept, deduplication at that scale is brutal, and an open tree nobody curates rots. Publishing triples is the easy 10 percent.

I have been pulling on this thread for a while. More soon.

Links in comments. Question for the ontology folks: issue-level legal concepts as skos:Concept or owl:Class? I have a strong opinion and I suspect some of you have the opposite one.

COMMENT:

Full build story coming on the blog: [substack link placeholder]

- SKOS spec (W3C, 2009): https://www.w3.org/TR/skos-reference/
- FOLIO: https://openlegalstandard.org
- EuroVoc, the EU's SKOS vocabulary: [link placeholder]

Plain English: SKOS is a tiny W3C standard for publishing controlled vocabularies as linked data. Each concept is a web address that resolves to something readable by humans and machines. "Issue-level" means the granularity of a point of law you would argue, not a practice area you would bill to. ECLI and ELI are the EU's open identifier standards for judgments and legislation. The 92 percent figure is from the Legal Services Corporation's 2022 Justice Gap report: [link placeholder].

VISUAL SUGGESTIONS:

2009 | SKOS BECAME A W3C REC | the tech has been ready for 17 years
92% | CIVIL LEGAL PROBLEMS UNMET | low-income Americans, LSC 2022, little or no legal help
~100,000 | ISSUE-LEVEL CONCEPTS | the depth law needs, currently closed

---

## OPEN QUESTIONS FOR ARTHUR

1. Post 2 states the SALI/FOLIO facts from ALEA's open letter with attribution and an explicit "no inside knowledge" beat. You know the players; dial the temperature up or down as you see fit. The safest version cuts the Delaware detail and says only "governance concerns."
2. Post 1 now opens on the 1876 Syllabi origin story, so the dating question is moot. The Mallory subscriber-list detail in the comment is sourced to company histories (FundingUniverse, Encyclopedia.com); it is colorful, verify comfort level before shipping.
3. Post 3 ends with the skos:Concept vs owl:Class bait. The Substack draft argues the SKOS side. If you would rather keep that powder dry for launch, swap the closer for the governance question from Post 2.
4. "I have reviewed vendor taxonomies that classify all of securities law under Corporate" is written from your general experience; confirm it is true for you or I will soften it to "I have seen."

## EVIDENCE LOG

- West Key Number System: 400+ topics, nearly 100,000 key numbers; classification built 1897 to 1906; West Publishing acquired by Thomson in the late 1990s. Sources: Thomson Reuters marketing pages, Stanford Law School research guide, Wikipedia (West American Digest System).
- Origins: John B. West sold law books in St. Paul from the early 1870s; launched The Syllabi, an eight-page weekly, in 1876 at age 24; it evolved into the National Reporter System. John A. Mallory's Complete Digest subscriber list was purchased by West; Mallory then joined West and was crucial in perfecting the American Digest classification. Original scheme had seven primary divisions: persons, property, contracts, torts, crime, remedies, government. Sources: Lawbook Exchange (The Syllabi reprint description), Riesenfeld Rare Books blog (U. Minn.), FundingUniverse/Encyclopedia.com West Group histories, Encyclopedia.com "Key Numbers".
- US legal services market: USD 396.1 billion revenue in 2024, largest in the world (Grand View Research, US legal services market outlook).
- Justice gap: 92 percent of low-income Americans' civil legal problems received no or insufficient legal help; 74 percent of low-income households had at least one civil legal problem in the prior year. Source: Legal Services Corporation, 2022 Justice Gap Report.
- Open identifiers elsewhere: ECLI (European Case Law Identifier) and ELI (European Legislation Identifier), EU open standards; free-access-to-law movement institutions AustLII (1995), BAILII, CanLII publishing case law openly since the 1990s/2000s.
- SKOS: W3C Recommendation, 18 August 2009 (skos-reference).
- FOLIO: ~18,000+ concepts/classes, OWL file, CC BY 4.0, stewarded by ALEA Institute; forked from MIT-licensed SALI LMSS as SOLI in September 2024; cease-and-desist letters January 13, 2025; rebranded FOLIO March 14, 2025. Source: openlegalstandard.org open letter (March 20, 2025), alea-institute/FOLIO GitHub README.
- SALI LMSS: 18,000+ tags, MIT license, adopted since 2022; SALI shipping LMSS v3 process with public viewer. Sources: sali.org, lmss.io, Law.com (March 21, 2025).
- No public resolution of the dispute found as of 2026-08-04 (searched).
- EuroVoc: EU multilingual SKOS vocabulary, 20+ languages (well-established).
