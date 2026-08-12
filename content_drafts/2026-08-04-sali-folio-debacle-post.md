# Detailed standalone post: the SALI/SOLI/FOLIO debacle
# Runs as either a LinkedIn article or a Substack post. If it runs on Substack,
# it can replace the shorter "open ones are shallow, and fighting" section in the
# main Substack draft with a link to this piece.
# Temperature: middle. Every contested fact is attributed, nothing is asserted as
# my own finding, and the analysis stays on licensing and governance mechanics,
# where a lawyer can stand. The hotter and colder dials are flagged at the end.

TITLE: The fork heard round the legal industry

SUBTITLE: What the SALI and FOLIO standoff teaches about open licenses, boring corporate hygiene, and why "open" is a legal conclusion, not a vibe

---

Legal tech had exactly one shared taxonomy standard. It now has two organizations publishing rival versions of it, months of cease-and-desist correspondence behind them, and a community quietly asking which repo to build against.

I keep bringing this story up when I write about legal taxonomies, and each time I compress it to a paragraph it loses the parts that matter most to lawyers. So here is the longer version. Two disclaimers before the timeline, because this one is still warm.

First, I have no inside knowledge. Everything below comes from published sources: ALEA's open letter of March 20, 2025, the public repositories, SALI's own site, and trade press coverage. Where a fact comes from one side's account, I say so.

Second, this is a dispute between organizations I respect, populated by people who collectively donated thousands of hours to giving our industry a common language. Nothing here is a verdict on anyone. The interesting part is not who wins. The interesting part is what the mechanics teach the rest of us.

## The cast and the timeline

SALI, the Standards Advancement for the Legal Industry alliance, spent years building the Legal Matter Standard Specification: 18,000+ tags covering areas of law, services, industries, and the machinery of legal matters. Real adoption since 2022. Law firms mapped intake systems to it. Vendors shipped integrations. It was becoming what standards people call a Schelling point: the answer you pick because you expect everyone else to pick it.

Then, per ALEA's open letter: in August 2024, Damien Riehl, one of the standard's most prolific contributors, approached the ALEA Institute with concerns about SALI's corporate governance. The letter says ALEA reviewed public records and found, among other things, Delaware filings indicating SALI's corporate status had been void since 2020, no Illinois registration despite operations there, and discrepancies in IRS filings. It also says SALI leadership acknowledged issues and announced a "pause" of activities.

I want to be precise about epistemic status here: these are allegations published in an open letter by one party to a dispute, supported by screenshots of public records that I have not independently pulled. SALI has not, to my knowledge, published a detailed point-by-point public response. Treat them accordingly.

What is not disputed: in September 2024, ALEA forked the specification into a project called SOLI. On January 13, 2025, SALI sent cease-and-desist letters. On January 17, Michael Bommarito opened a public notice on SALI's own LMSS repository, issue #28, titled "ACTION REQUIRED: Notice of License Dispute and Potential DMCA Action." In March 2025, the fork rebranded as FOLIO, the Federated Open Legal Information Ontology, and published its account of the whole affair. Law.com's coverage that month framed the core question crisply: is the standard protected intellectual property, or an open resource anyone may build on?

Since then, both projects have kept shipping. SALI has an LMSS v3 release process underway with a public viewer. FOLIO publishes an OWL ontology of 18,000+ concepts under CC BY, plus an API, a Python library, and an MCP server. As of this writing, issue #28 remains open with no reply from SALI, and I can find no public resolution of the underlying dispute.

## What SALI has actually said, and where it said it

SALI has published no detailed rebuttal of ALEA's open letter that I can find. But calling SALI silent would be wrong. Its position exists in public, stated indirectly, and once you assemble the pieces it is coherent.

Piece one, the cease-and-desist letters themselves. Per Bommarito's account in issue #28, SALI's letters claim that the LMSS XML and related IP are licensed under CC BY-ND, not under the MIT license stated in the repository's own LICENSE file. Note the ND. NoDerivatives. If that is the operative license, derivative works are prohibited, and a fork is not a right, it is an infringement.

Piece two, SALI's website, and here the archaeology matters, so I did it. For years, SALI's "Using the LMSS" page carried the dual-license theory in plain text: "The public can access and use an XML implementation of our latest LMSS standard in our GitHub repository, available under the MIT License. SALI's standard specification and associated documentation are licensed under the CC BY ND license." Plus the mission statement: "any SALI-licensed materials cannot be used to create competing standards."

The Wayback Machine dates that paragraph precisely, and the timing is the most exculpatory fact in this piece for SALI. It appeared between January and May 2022, within days of the GitHub repo's initial MIT commit on May 27, 2022, and then sat unchanged, down to a typo ("LSSS"), through every flashpoint of the dispute: untouched in August 2024 when the concerns were raised, untouched in January 2025 when the letters went out, untouched at the March 2025 rebrand. Whatever the CC BY-ND theory is, it is not a position improvised after the fork. The MIT license file and the CC BY-ND webpage were born the same week and were simply never reconciled, for years, by anyone.

Piece three, the present tense, which turns out to be the most interesting layer. Sometime before April 11, 2026, SALI redesigned its site. The Using the LMSS page and the FAQ are gone, both 404. The current canonical statement, at sali.org/explore-the-standard, reads: "The choice of the CC BY ND license is intended to facilitate widespread adoption and use of SALI standards while preserving canonical reference versions. This means that SALI-licensed materials cannot be used to create competing standards or distributed derivatives. But all stakeholders ... can freely incorporate SALI into their systems and adapt it for their internal use."

Read the deltas like a redline, because that is what it is. The MIT acknowledgment: deleted. The GitHub link: gone from the site entirely; the public entry point is now a hosted viewer. The prohibition: broadened from "competing standards" to "competing standards or distributed derivatives." The concession: a new internal-use adaptation carve-out. SALI never argued its position in public, but it quietly amended its position in place, and the amended version is cleaner, broader, and no longer admits that any part of the work was ever MIT.

Piece four, conduct on the repo. On March 24, 2025, ten days after the FOLIO rebrand, a SALI-side commit updated the repository's LICENSE copyright line to read "SALI Alliance™," trademark symbol included. The file remains bare MIT to this day, with no commits since. And SALI has kept building LMSS v3, which is its most eloquent statement of all: we are the standard, carry on.

So SALI's position, reconstructed from its public footprint across time: the specification is CC BY-ND and no one may derive a competing standard from it; the MIT grant, once described as covering the XML implementation, is now not described at all; and the repository that still says MIT sits unlinked from the site that no longer mentions it.

## The part lawyers should find fascinating

Now the fight has an actual shape, and it is a beautiful one: where does an "XML implementation" end and a "specification" begin, when the repository is the only public artifact and the XML is the spec's entire expression?

ALEA's side of that line is simple. The repo has said MIT since its initial commit in May 2022. MIT grants everyone the right to copy, modify, and redistribute, including in ways the steward hates. A fork of an MIT repo is not a loophole; it is the license working as designed. On that narrow point the ground is famously solid: the modern software stack sits on forks of MIT and BSD code.

SALI's side is subtler than it first looks. Dual licensing by artifact type is a real and legitimate pattern; W3C and OASIS distinguish specification documents from schema files all the time. If the taxonomy's structure is a copyrightable work distinct from its serialization, a CC BY-ND wrapper on the former is at least an arguable position, and the archive shows SALI has held some version of it since the week the repo went up. The failure is executional, and it is the least dramatic failure imaginable: the marketing page and the LICENSE file said different things from day one, and for over two years nobody with authority reconciled them. Not malice, not retrofit. Just two documents, drafted in the same week, never read side by side until people with lawyers needed them to agree. Every attorney reading this has seen the corporate version of that story; this is what it looks like when it happens to an industry standard.

Then the counter-escalation, which deserves its own paragraph because it inverts the whole story. In issue #28, Bommarito and Riehl announced that effective January 18, 2025, they revoked the license to their own contributions, enumerated by commit and pull request, including translation work covering thousands of concepts, and warned that a DMCA takedown might follow. Their theory: the project never had a Contributor License Agreement, so SALI holds no explicit license to contributed work. Sit with the symmetry. SALI says the fork infringes the original. The contributors say the original infringes them. The no-CLA argument is aggressive in its own right, since contributing to an MIT repo is conventionally understood as licensing inbound under the same terms out, and MIT grants are generally treated as irrevocable once relied upon. But conventional understanding is not a signed instrument, and that is precisely the hole a CLA exists to close.

And notice what nobody disputed, because the parties' own conduct maps the boundary perfectly: trademarks. MIT conveys copyright permissions, not the right to the steward's name. The fork launched as SOLI, one letter from SALI; the letters arrived; the project rebranded to FOLIO explicitly to, in its words, eliminate trademark confusion. Everyone behaved as if the content was contestable and the brand was not. That intuition is roughly the law, and it is why serious open projects separate the mark from the content on day one.

One more exhibit for the completists, because the git history preserves a small drama in three commits. August 23, 2024, as the dispute was gestating: the LICENSE copyright line in SALI's repo was changed from "sali-legal" to "soli-legal," by a contributor then still holding commit access. March 13, 2025, the day before the FOLIO rebrand: the same contributor changed it back. March 24, 2025: SALI's side stamped it "SALI Alliance™." I offer no interpretation of any of these edits beyond the observation that both camps clearly understood a single line of a LICENSE file to be worth fighting over, and that a fair reader can find something to wince at in each direction.

There is a third instrument in play that nobody signed: the corporate law layer. ALEA's letter leans hard on SALI's alleged Delaware void status, citing Chancery authority for the proposition that a void corporation is treated as if it never existed. I will not pretend to adjudicate SALI's status from a blog post. But the general point survives any version of the facts: a standards body is a legal person, and its capacity to hold IP, grant licenses, enforce rights, and be accountable to contributors runs through the most boring machinery in our profession. Franchise taxes. Registered agents. Annual reports. The stuff associates are embarrassed to bill for is the stuff the whole edifice stands on.

## The lesson is not "pick a side"

If you run or rely on a shared standard, this episode hands you a due diligence checklist that costs one associate-afternoon: What entity holds the IP, and is it in good standing where it claims to exist? What license, exactly, and is it stated identically in the repo, the site, and the bylaws? Who can change it? Is the trademark held separately from the content license? What happens to the work if the steward stalls, and does the license let the community route around a dead or captured institution?

The MIT license answered that last question for LMSS, and that is the quiet success buried in this mess: when the institution wobbled, the work survived. Every contributed hour remained usable by everyone. If you have ever donated nights and weekends to a standard, understand that the license, not the org chart, is what protects your contribution.

But the fragmentation tax is real and everyone in the largest legal market in the world is paying it. Adoption conversations that used to take one meeting now begin with "which standard?" Network effects are the entire value of a taxonomy, and a fork cuts the network in half on day one, whichever side deserves the blame.

Two active projects beat one paused one. One healthy one would have beaten both.

## Why I keep telling this story

Because it is the strongest evidence I know for a claim I have been circling in this series: the legal industry's classification problem is not a technology problem. The W3C solved vocabulary publishing in 2009. The public domain is full of raw material. What keeps failing is the institutional layer: the proprietary map stays closed, and the open map fractured over governance basics that any of its own member firms would have flagged in a client's data room.

Getting that layer right is a design problem, and it is designable. License clarity from day one. Marks separated from content. An entity that files its annual reports. Continuity by construction rather than by fork.

More on what that could look like soon.

If you were closer to the SALI or FOLIO side of this than I am and I have any fact above wrong, correct me in the comments and I will amend with credit. That offer is the whole point of writing in public.

---

## SUGGESTED REPLY to Michael Bommarito's comment on the live Post 2

(He linked issue #28 and said it is unfortunate SALI chose not to clarify or resolve the concerns. He is a principal in the dispute; the reply should thank, acknowledge, and stay neutral on the merits while signaling you read the material closely.)

"Thank you for engaging directly, and for the pointer. I read #28 before replying: the CC BY-ND claim in the letters against the repo's own MIT file, the no-CLA point, and the revocation of your and Damien's contributions effective January 18. As a licensing matter the boundary question (where an XML implementation ends and a specification begins when the repo is the public artifact) is one of the most interesting open-standards fact patterns I have seen in legal tech. I am writing a longer piece on it and committed to stating both sides' positions from the public record. If I get any fact wrong, I would genuinely welcome the correction."

## OPEN QUESTIONS FOR ARTHUR

1. Temperature dials. Current setting is middle: Delaware and IRS allegations appear, but always attributed to ALEA's letter with an explicit epistemic-status paragraph. Colder: cut the itemized allegations, say only "governance concerns raised by contributors" (kills a third of the legal analysis). Hotter: name Damien Riehl's contribution hours and quote the "Where has the money gone?" line from the letter (accurate, but reads prosecutorial; not recommended under your no-conclusions-without-debate principle).
2. Riehl and Bommarito are now both named and both engaged with your live post (Bommarito commented directly). The piece describes the August 23, 2024 LICENSE edit ("sali-legal" to "soli-legal") without naming the committer in the body, though the commit metadata is public and it is Riehl. Given Bommarito is now in your comments, decide whether the git-history paragraph stays. It is verifiable and evenhanded, but it is the one passage a FOLIO partisan could read as unfriendly. The counterweight: it is also the passage that proves you are not writing a FOLIO puff piece, which after Bommarito's public engagement matters more, not less.
3. RESOLVED by your Wayback session, and the piece was rewritten accordingly. The CC BY-ND paragraph dates to the January-to-May 2022 window, contemporaneous with the repo's May 27, 2022 initial commit; unchanged (typo included) through every dispute flashpoint through Wayback's last capture of the old page (February 14, 2026). The "lawsuit seed bank" line was replaced with the never-reconciled framing your findings support. New material added on the April 2026 site overhaul: old pages 404, MIT acknowledgment deleted, "or distributed derivatives" broadening, internal-use carve-out, GitHub delinked, viewer.sali.org as public entry. One correction to my own record: my 2026-08-04 fetch of Using-the-LMSS returned the pre-redesign text even though the live site had already changed by April 11, 2026, so that fetch evidently hit stale or cached content. The evidence log now labels that quote as historical (verified via Wayback), not live. Before publishing, reload sali.org/explore-the-standard yourself and confirm the current wording one more time.
4. "I have not independently pulled" the Delaware records: ten dollars on the Delaware SOS site upgrades the epistemic status of the whole piece. Worth it at this temperature.
5. The closing correction offer is now load-bearing: Bommarito is watching the thread and the suggested reply above repeats the commitment. Only publish if you mean it.
6. The MIT irrevocability and inbound=outbound points in the counter-escalation paragraph are conventional doctrine stated at a general level, not case citations. If you want authority in the piece, Jacobsen v. Katzer for enforceability of open licenses is the standard cite, but consider whether footnoting a blog post escalates the register more than you want.

## EVIDENCE LOG

- ALEA open letter, "What's Happening with SALI, SOLI, and FOLIO?", March 20, 2025 (openlegalstandard.org): source for the August 2024 Riehl approach, the itemized governance allegations (Delaware void since 2020, Illinois registration, IRS discrepancies), the "pause," the September 2024 SOLI fork, the January 13, 2025 cease-and-desist date, the January 22 response, the March 14, 2025 FOLIO rebrand, the trademark-confusion rationale, and the Chancery citation (Rivera v. Angkor Capital, Del. Ch. Aug. 20, 2024).
- Law.com Legaltech News, March 21, 2025: frames dispute as protected IP vs open-source resource ("SALI Alliance, Former Contributors at Odds Over Rights to Legal Matter Standard"). Paywalled; framing taken from the headline and abstract.
- sali-legal/LMSS GitHub repository: MIT license; 18,000+ tags; adoption since 2022.
- SALI "Using the LMSS" page, HISTORICAL (page now 404; verified via Arthur's Wayback Machine review): dual-license paragraph verbatim: "any SALI-licensed materials cannot be used to create competing standards" and "The public can access and use an XML implementation of our latest LSSS [sic] standard in our GitHub repository, available under the MIT License. SALI's standard specification and associated documentation are licensed under the CC BY ND license." Wayback timeline: absent April 23, 2021 and January 20, 2022 (only the "competing standards" sentence existed); present by May 28, 2022 with "forthcoming GitHub repository," one day after the repo's initial commit; "forthcoming" dropped between August 27, 2023 and March 21, 2024; otherwise unchanged (typo intact) through August 5, 2024, December 28, 2024, January 18, 2025, March 24, 2025, November 17, 2025, and Wayback's last capture February 14, 2026. My earlier "fetched 2026-08-04" citation of this page returned this old text despite the live site having changed by April 11, 2026; treat that fetch as stale/cached.
- SALI FAQ page, HISTORICAL (page now 404): "Standards created by SALI Alliance ... are licensed to users under a Creative Commons license." Present since the earliest Wayback crawl, April 23, 2021, predating the GitHub repo.
- SALI current site (redesign live by April 11, 2026 per Wayback's first capture of the new page; confirmed live in Arthur's browser session): canonical license statement now at sali.org/explore-the-standard, verbatim: "The choice of the CC BY ND license is intended to facilitate widespread adoption and use of SALI standards while preserving canonical reference versions. This means that SALI-licensed materials cannot be used to create competing standards or distributed derivatives. But all stakeholders (e.g., firms and legal service providers, vendors, clients, academics) can freely incorporate SALI into their systems and adapt it for their internal use." No MIT mention; no GitHub link found in nav, footer, or that page; public entry point is viewer.sali.org. Redesign predates Bommarito's comment on Arthur's live post.
- GitHub issue sali-legal/LMSS#28, opened by mjbommar January 17, 2025, still Open as of 2026-08-04, zero comments from SALI: source for the C&D letters claiming CC BY-ND "not the MIT license stated in this repository's metadata"; the license revocation of enumerated commits/PRs effective January 18, 2025 (including translations covering ~5k concepts, PR #22); the potential DMCA notice; the no-CLA/no-CONTRIBUTORS argument; the statement that Bommarito and Riehl never received compensation nor solicited funds for the 501(c)(6).
- LICENSE file commit history (GitHub API, fetched 2026-08-04): initial commit 8a70c70 by Damien Riehl, 2022-05-27, MIT, "Copyright (c) 2022 sali-legal"; commit 9cf9697 by Damien Riehl, 2024-08-23, changed holder to "soli-legal"; commit 037e0e9 by Damien Riehl, 2025-03-13, reverted to "sali-legal"; commit 182e640 by Bert Saper, 2025-03-24, changed to "SALI Alliance™". File remains MIT today; GitHub API reports license: MIT.
- Post 2 engagement (Arthur's live LinkedIn post, 2026-08-04): Aron Ahmadia (VP Applied Science, Relativity) comment stating core contributors Riehl and Bommarito became unhappy with the governance foundation and were forced to leave the project name behind; Michael Bommarito comment linking issue #28 and stating SALI chose not to clarify or resolve governance/licensing concerns.
- SALI LMSS v3 release process and public viewer: sali.org / trade coverage.
- FOLIO: 18,000+ OWL concepts, CC BY, API, Python library, MCP server (github.com/alea-institute/FOLIO, openlegalstandard.org); Law.com, Aug 28, 2025, on planned features.
- No public resolution found as of 2026-08-04 (searched).
- US "largest legal market in the world": Grand View Research, USD 396.1 billion in 2024 (consistent with the other three drafts).
