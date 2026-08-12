# Survey post: taxonomies vs ontologies and the full state of the art
# Substack-length deep dive. Slots into the series after the SKOS post and the
# SALI/FOLIO debacle piece; it is the "map of the maps" entry. No launch reveal.

TITLE: Everyone loves a taxonomy. Nobody wants to feed one.
SUBTITLE: Why trees of legal concepts feel natural, why they die anyway, and an honest map of every legal classification system that matters

---

Ask a lawyer to define "ontology" and you get a pause, then something about philosophy class. Ask the same lawyer to sketch the areas of law on a whiteboard and you get a tree in ninety seconds: contracts here, torts there, wait, does insurance go under both? That instinct, and that "wait," are the entire subject of this post.

I have been writing about legal classification for a few weeks now: the West Key Number System you cannot link to, the SALI and FOLIO standards fight, the case for boring SKOS. Several people asked some version of the same question: what actually exists in this space, and why is it all either closed, shallow, or dead? Fair. This is the survey post. First the concepts, then the graveyard tour.

## Taxonomy and ontology, without the seminar

A taxonomy is a tree of concepts. Each concept has a label, a parent, maybe some synonyms. The only relationship that matters is broader and narrower, and that relationship promises very little: "filed under," not "logically entailed by." The Dewey Decimal System is a taxonomy. So is your DMS folder structure. So is the issue outline you made for the bar exam.

An ontology is a much bigger commitment. Classes with membership conditions, properties connecting them, axioms constraining what can be true, and a reasoner that draws inferences you did not explicitly state. An ontology does not just say "Security Deposit is filed under Landlord-Tenant." It wants to say a security deposit is a payment, made by a tenant to a landlord, held under conditions, refundable on events, and it wants a machine to deduce consequences from that.

Here is why taxonomies feel natural: they are how humans already think. Cognitive science has known since the 1970s that people organize the world into rough hierarchies with fuzzy edges and prototype members, not into logically clean classes. A robin is a better "bird" than a penguin, and every lawyer knows a better and worse example of "breach of fiduciary duty." Legal training amplifies this. Issue spotting, the foundational skill we beat into 1Ls, is literally classification: read the mess, name the doctrines it implicates. Lawyers are professional taxonomists who have never used the word.

Ontologies, by contrast, demand the one thing law refuses to supply: stable truth conditions. What are the necessary and sufficient conditions of "constructive discharge"? The honest answer is a forty-page circuit split, and an OWL axiom cannot hold a circuit split. This is not a knock on ontologies; where the domain cooperates (molecules, financial instruments, legislative document structure), they are magnificent. Law's subject matter mostly does not cooperate.

## So why is the natural thing so hard to build?

If taxonomies match how lawyers think, building one should be easy. Three problems say otherwise, and each one is a small career.

Problem one: there is no view from nowhere. Every tree encodes a reader. A litigator's tree puts "sanctions" near the trunk; a transactional lawyer barely has the branch. Consumer-facing taxonomies need "my landlord won't return my deposit" where lawyer-facing ones need "surety's subrogation rights." Neither is wrong. A taxonomy is an opinion about what matters, frozen into structure, and opinions have owners.

Problem two: humans do not agree, even with themselves. Classic indexing studies going back to the 1960s keep finding the same embarrassment: give two trained indexers the same document and the same vocabulary, and they agree on the assigned terms less than half the time. Give the same indexer the same document twice, months apart, and consistency is still shaky. Now scale that to a tree with tens of thousands of nodes and ask where "DAMAGES" goes. Under contracts? Torts? Remedies? The correct answer, all three, breaks the comforting fiction of a single tree and welcomes you to polyhierarchy, where maintenance costs compound.

Problem three, the killer: a taxonomy is a subscription, not a purchase. Law moves. Concepts split (privacy law calving into biometric, health, financial, children's), merge, go dormant, come roaring back with new names. Every change must land without breaking the identifiers already embedded in other people's systems, which means versioning discipline, deprecation semantics, and someone who shows up every quarter, forever. West's real moat was never the 100,000 key numbers. It is the century of editors who kept showing up. Creation is a project; curation is an institution. Almost everyone funds the project and starves the institution, which is why the field below reads like a graveyard with three or four survivors.

## The state of the art, honestly assessed

Commercial, deep, closed. The West Key Number System remains the reference: 400+ topics, roughly 100,000 points of law, built 1897 to 1906 and hand-curated since, proprietary to Thomson Reuters, no public identifiers. LexisNexis runs its correlate, the Legal Topics hierarchy, on the order of 16,000 topics maintained by staff attorney-taxonomists, equally closed. Bloomberg Law took a genuinely different philosophical route with Points of Law: instead of a top-down editorial tree, machine learning extracts salient legal propositions from opinions bottom-up. It is an index without a taxonomy, which neatly dodges the maintenance problem and equally neatly fails to give the industry a shared vocabulary, since extracted language is not a controlled list anyone else can adopt. Practical Law, meanwhile, organizes know-how by practice area at exactly the coarse granularity a shared standard cannot use. All of these work. None of them are infrastructure, because none of them are yours to build on.

Open, business-of-law layer. SALI's LMSS: 18,000+ tags for areas of law, services, industries, real adoption since 2022, currently mid-dispute (the fork, the CC BY-ND versus MIT fight, the still-open issue #28; I wrote that story up separately). FOLIO: the 18,000+ concept fork, CC BY, published as an OWL ontology with an API, a Python client, and an MCP server. Note the design choice hiding in that sentence: FOLIO is formally an ontology, classes rather than concepts, which buys it machinery and costs it the epistemic humility I argued for in the SKOS piece. Both projects are strongest at matter metadata, the layer that describes legal work, and thinnest at legal issues, the layer that describes law.

Open, access-to-justice layer. The one corner of the open landscape that quietly works is the least glamorous, and because it publishes a live JSON feed, I did not have to take anyone's word for it. I pulled the data.

LIST, the Legal Issues Taxonomy (formerly NSMI v2), maintained by Stanford's Legal Design Lab, descends from the legal aid community's problem codes of the early 2000s. It classifies civil legal problems as people actually experience them ("getting kicked out," not "summary process"), and it powers Spot, the issue-spotting classifier built with Suffolk's LIT Lab and used by statewide legal aid portals.

As of the June 16, 2026 snapshot: 1,301 terms across 20 top-level categories, in a five-level code scheme. The distribution tells you exactly whose problems this taxonomy is for, and that is a compliment: Housing is the largest category at 208 terms, then Family at 161 and Public Benefits at 150, while Environmental Justice holds 8. Every single term, all 1,301, carries a plain-language definition, median around 240 characters, written for intake screens rather than treatises. And the maintenance signal I care most about in this whole survey: category pages show updates from May 2026, a working group is forming, and the site publishes crosswalks, 1,367 mappings to the taxonomies legal aid already runs on (1,214 to NSMI v1, 78 to the Legal Services Corporation's codes, 68 to Legal Server's index, and a first 7 links to Wikidata). About 28 percent of terms have no crosswalk yet, which is what a living project's backlog looks like.

Since I had the data open, two design notes in the spirit of this post, offered as observations rather than complaints. First, LIST's codes are positional: HO-02-02-00-00 encodes the path to the concept, which makes codes readable at a glance and means a future reorganization has to either renumber (breaking references) or live with codes that no longer match the tree. Every taxonomy picks its poison between meaningful and opaque identifiers; LIST picked meaningful, West and SKOS practice pick opaque, and the trade is real on both sides. Second, 474 of the 1,301 terms, more than a third, have multiple parents. Polyhierarchy at that rate in a consumer-facing taxonomy is not sloppiness, it is honesty: "eviction from subsidized housing" genuinely lives in two places. But the data model records parents by name rather than by code, which works today only because no two terms currently share a name, and is the kind of quiet load-bearing assumption this post exists to point at.

None of that dents the conclusion. LIST is small, purpose-built, actually maintained, and answerable to a real user population. It is the existence proof in this survey: open legal taxonomies can live, if they have an institution and a job to do.

Academic and infrastructure layer, mostly adjacent. LKIF-Core, from the ESTRELLA project of the late 2000s, is the canonical academic legal ontology: norms, actions, agents, roles in OWL. It is foundational, cited everywhere, and used in production almost nowhere, the fate of most upper ontologies. LegalRuleML (OASIS) encodes the deontic layer, obligations and permissions and exceptions, rules rather than subjects. Akoma Ntoso, also OASIS, is the open XML standard for legislative document structure, adopted by real parliaments; it tells you what a section is, not what it is about. EuroVoc gives the EU a multilingual SKOS thesaurus across policy domains including law, in 20+ languages, with law as one domain among many rather than the point. And ECLI and ELI, the European identifier standards for judgments and legislation, are not taxonomies at all but solve the adjacent problem the US has not: open, stable, resolvable identifiers for legal things.

Lay the landscape on two axes, openness and issue-level depth, and the pattern is impossible to miss. Deep and closed: West, Lexis. Open and shallow (by design or by scope): LMSS, FOLIO, LIST, EuroVoc. Deep and open: an empty cell. It has been empty for so long that most people in legal tech have stopped seeing it as a cell at all, the way you stop seeing a missing tooth in a familiar smile.

## The uncomfortable synthesis

Put the two halves of this post together and the diagnosis writes itself. The artifact law actually needs is the humble one, a big, deep, opinionated taxonomy with stable identifiers, because that matches both how lawyers think and what retrieval systems consume. But the humble artifact carries the brutal cost structure: viewpoint fights, indexing inconsistency, and above all permanent curation, the unglamorous institutional labor that produces no papers and demos poorly. So the field keeps funding what demos well. Ontologies get conferences. Extraction models get funding rounds. Taxonomies get a shrug, because everyone assumes someone else already built the tree.

Someone did. In 1906. It is excellent, and it is not yours, and the two companies that own the deep trees have every rational reason to keep them fenced, in the largest legal market on earth.

The ingredients for the missing cell are all sitting in plain sight, and I have spent enough time with them now to know the assembly is hard in exactly the three ways this post describes, no others. More on that soon.

Tell me what I missed. Niche taxonomies, dead projects with lessons in them, jurisdictional ones I have not named. The comment section of the last post taught me more than the drafting did, and I intend to keep exploiting that.

---

## OPEN QUESTIONS FOR ARTHUR

1. The indexing-consistency claim ("agree less than half the time") is stated qualitatively from the classic information-science literature (inter-indexer consistency studies from the 1960s onward). I deliberately avoided a specific percentage because reported figures vary widely by study. If you want a citation, the standard references are Zunde and Dexter (1969) and the survey literature that followed; verify before adding.
2. LexisNexis "on the order of 16,000 topics" comes from secondary research sources describing the Legal Topics hierarchy, not from Lexis directly. Soften to "over ten thousand" if you want more margin.
3. Bloomberg Points of Law is characterized as ML-extraction without a fixed controlled vocabulary, based on ABA Journal coverage and Bloomberg's own materials. If you have hands-on experience contradicting that characterization (you evaluate these tools professionally), your firsthand version is better than my sourced one.
4. The missing-tooth line and the "graveyard with survivors" line are the two most stylized moments; cut either if the piece should run cooler.
5. RESOLVED: LIST's currency is now verified from the live API (snapshot "as of Jun 16, 2026," category page updated May 20, 2026, working group forming). The section was rewritten around the pulled data. The two design observations (positional codes, parent-by-name with 474 multi-parent terms) are original analysis of the dataset; they are stated as observations, not defects, and the "no two terms share a name" fact that makes name-refs workable was verified in the data (zero duplicate names). One caution: LIST's site footer is "All Rights Reserved" and the terms-of-use page would not render in my environment, so the piece deliberately does not call LIST "openly licensed," only "open" in the access sense. Read the terms of use in a browser before you characterize the license anywhere.
6. The closer invites niche taxonomy nominations, which sets up nicely for a follow-up post and for the launch. Intentional.

## EVIDENCE LOG

- Taxonomy/ontology distinction, prototype theory (Rosch, 1970s), issue spotting as classification: established literature, stated at textbook level.
- Inter-indexer consistency: classic findings, stated qualitatively (see open question 1).
- West Key Number System: 400+ topics, ~100,000 points of law, 1897 to 1906, proprietary. Sources: Thomson Reuters pages, Stanford Law guide (consistent with prior posts in series).
- LexisNexis Legal Topics: approximately 16,000 topics, proprietary taxonomy maintained by attorney-taxonomists. Sources: research-guide and secondary descriptions of the Lexis topic hierarchy (Georgetown Law guide on headnotes; ResearchGate description; Soutron legal metadata reference).
- Bloomberg Law Points of Law: automated/ML indexing layer over opinions. Source: ABA Journal, "Bloomberg Law trains machine to highlight legal points"; Bloomberg Law help pages.
- SALI LMSS: 18,000+ tags, adoption since 2022, license dispute and issue #28 per the debacle post's evidence log (shared).
- FOLIO: 18,000+ concepts, OWL, CC BY, API, Python library, MCP server. Sources: alea-institute/FOLIO GitHub, openlegalstandard.org.
- LIST / NSMI v2, from the live API (https://www.taxonomy.legal/api/terms, pulled this session; snapshot labeled "as of Jun 16, 2026"): 1,301 terms; 20 top-level categories; five-level positional code scheme (XX-NN-NN-NN-NN). Depth distribution: 20 at level 1, 217 at level 2, 517 at level 3, 405 at level 4, 142 at level 5. Largest categories: Housing 208, Family 161, Public Benefits 150, Courts and Lawyers 116, Money/Debt/Consumer 110. Smallest: Environmental Justice 8, Government Services 14, Veterans and Military 14, Disaster Relief 17. Definitions: 1,301 of 1,301 present, median 236 chars, mean 338. Crosswalks: 1,367 total links (NSMI v1: 1,214; Legal Services Corporation Taxonomy: 78; Legal Server Index: 68; Wikidata: 7); 367 terms (28.2 percent) have none. Multi-parent terms: 474 of 1,301 (36.4 percent); parent references are by name, not code; zero duplicate names in current data. Site: maintained by Stanford Legal Design Lab; category page "Last updated May 20, 2026"; working group forming; downloads offered as CSV, JSON, Airtable; footer "All Rights Reserved" (license text not verified, see open question 5). History: descends from early-2000s NSMI legal aid problem codes; Spot classifier (Suffolk LIT Lab) built on it; Pew supported development. Sources: taxonomy.legal (live), suffolklitlab.org, spot.suffolklitlab.org, Legal Design Lab posts.
- LKIF-Core: ESTRELLA project, OWL ontology of basic legal concepts (norms, actions, agents, time, place). Sources: Hoekstra et al., CEUR proceedings.
- LegalRuleML: OASIS standard for encoding norms (obligations, permissions, prohibitions, exceptions). Source: academic survey literature.
- Akoma Ntoso: OASIS XML standard for legislative documents, adopted by parliaments including the European Parliament. Source: academic literature, prior post's log.
- EuroVoc: EU multilingual thesaurus, SKOS, 20+ languages, law as one domain. Consistent with prior posts.
- ECLI / ELI: EU identifier standards for case law and legislation. Consistent with prior posts.
- Held back deliberately: all OLIT specifics (name, counts, sources, method).
