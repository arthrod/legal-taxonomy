# LinkedIn article (native long-form): publish after Post 1, before or with Post 3

TITLE: The Missing Map of American Law

SUBTITLE: We have the world's best legal classification system. We just can't use it.

---

Every legal AI product you have ever demoed has a taxonomy problem, and most of them are hiding it behind a dropdown.

Ask the vendor how documents get classified and you will hear about embeddings and fine-tuning and agents. Ask to see the list of categories those documents get classified into, and you will usually find 25 to 40 practice areas, written by a product manager in an afternoon, versioned nowhere, mapped to nothing. Contract review tools that cannot tell securities enforcement from securities offerings. Matter intake systems where "Regulatory" is one bucket. The models got a thousand times better in three years. The category lists did not.

This is strange, because law is the field that invented rigorous classification of ideas, and we know exactly what good looks like. We built it over a century ago. And in the largest legal market in the world, roughly 396 billion dollars in 2024, the state of the map is quietly a disaster.

## The cathedral behind the paywall

The story starts smaller than you would guess. In 1876, John B. West, a 24-year-old who had been peddling law books to Minnesota lawyers, launched an eight-page weekly called The Syllabi: the state's court decisions, reported faster than the official reports could manage. Lawyers paid, because knowing what courts just held is the job. The newsletter became the North Western Reporter, then the National Reporter System, and West Publishing found itself sitting on an unclassified mountain of American case law.

Then, between 1897 and 1906, its editors did something slightly insane: they classified all of it into a single tree. West had bought the subscriber list of a competing digest and, more importantly, hired its author, John A. Mallory, who spent years perfecting the classification. Seven grand divisions at the top: persons, property, contracts, torts, crime, remedies, government. Beneath them, the West Key Number System grew to what it is today: 400+ topics, roughly 100,000 numbered points of law, maintained continuously by human editors ever since. Every reported case, sorted into the same structure, for over a century. It is one of the great intellectual artifacts of American law, and I mean that without irony.

Notice what the origin story actually is: a private solution to a public information failure. The courts produced the law but no usable map of it, so a book salesman built the map and, quite reasonably, charged admission. In 1906 that was the best possible outcome. The problem is that in 2026 it is still the arrangement.

Now try to build on it.

You cannot cite a key number as a stable, resolvable identifier on the open web. You cannot tag your own document corpus with key numbers and publish that dataset. You cannot map your DMS categories to it, train a public model on it, or run a benchmark against it. It is proprietary, which is Thomson Reuters' right, and I am not writing to complain about a company declining to donate a crown jewel. I am writing because the rest of us behave as if the gap it leaves does not exist.

Here is the test I apply to any classification system that wants to be infrastructure: can a stranger link to one of your concepts, resolve it, and use it in their own system without asking permission? The Key Number System fails not because it is bad but because it is closed. Nearly everything else in legal tech fails because it is shallow.

## The open world had one answer, then two

The open alternative was supposed to be SALI's Legal Matter Standard Specification: 18,000+ tags covering areas of law, legal services, industries, and the machinery of the business of law. MIT licensed, with real adoption since 2022. For a moment, legal tech had a Schelling point.

Then, in late 2024, it fractured. Contributors raised governance concerns about the nonprofit. The ALEA Institute forked the MIT-licensed specification into a new project. Cease-and-desist letters followed in January 2025, a rebrand to FOLIO in March 2025, and as of this writing I can find no public resolution. SALI, for its part, has kept building, with an LMSS v3 release process underway. I have no inside knowledge of the dispute and this article takes no side on it.

Two lessons survive whichever account you believe.

First, the MIT license worked. When the institution stumbled, the work product remained legally portable. Every hour those volunteers contributed stayed usable by everyone, which is precisely what open licensing is for. If you contribute to a standard, the license is not paperwork. It is the standard's life insurance.

Second, fragmentation is the tax everyone pays for governance failure. Vendors that adopted the standard now field a question that should not exist: which one? Standards live on network effects, and a fork cuts the network in half on day one.

## The boring part was solved in 2009

Here is what makes the whole situation genuinely funny, in the way that only infrastructure problems are funny. The technical problem of publishing a shared vocabulary was solved seventeen years ago, by a W3C standard so simple it is almost rude.

SKOS, the Simple Knowledge Organization System, became a W3C Recommendation in August 2009. The core data model is about five properties. A concept gets a permanent URI. A preferred label. An opaque notation so the ID survives relabeling. A broader link to its parent. Membership in a scheme. That is it. No description logic, no reasoner, no committee meetings about whether a lease is a subclass of a conveyance.

Libraries run their subject headings on it. Museums publish collections with it. The European Union maintains EuroVoc, its multilingual thesaurus, in SKOS across more than 20 languages, and every member state's systems can point at the same concept URIs.

Law's contribution to this ecosystem, the field that runs on citation and precedent and careful hierarchies of authority, is close to nothing at the granularity that matters.

## The rest of the world is not waiting

Widen the lens past the US and the picture gets uncomfortable.

Europe mints an open identifier for every judgment (ECLI, the European Case Law Identifier) and every piece of legislation (ELI), so any system in any member state can point at the same decision the same way, for free. The free-access-to-law movement has been publishing case law openly for three decades: AustLII in Australia since 1995, BAILII in the UK and Ireland, CanLII in Canada, funded by the profession itself. These are jurisdictions that treated legal findability as public infrastructure and built the boring plumbing accordingly.

Now the US. The largest legal market in the world by a wide margin. The jurisdiction whose case law the rest of the common-law world reads. And its only issue-level map of the law is a trade secret, while the Legal Services Corporation reports that 92 percent of low-income Americans' civil legal problems receive no or insufficient legal help.

I want to be careful with that juxtaposition, because a taxonomy does not represent anyone in housing court. Classification is one layer of the access-to-justice stack, not the whole of it. But it is a load-bearing layer. Every court self-help portal, every legal aid triage tool, every pro bono routing system needs to answer "what kind of problem is this" before it can do anything else, and today each one builds that answer from scratch, badly, because the good answer is paywalled. The people with Westlaw get the map. The people building tools for everyone else get the dropdown.

A country that runs the world's biggest legal market on a closed map, while its peers publish theirs as open infrastructure, is not being prudent. It is being complacent, and the complacency compounds annually.

## What is actually missing

Put the two halves of the landscape side by side and the hole has a precise shape.

FOLIO and LMSS are strongest where the business of law lives: matter types, services, industries, players. Call it the metadata layer, and at 18,000+ concepts it is a real achievement. But when your question is "what point of law is this document actually about," you need the other axis, the one West spent a century refining: issue-level depth, on the order of 100,000 concepts, where "SECURITIES REGULATION" is not a tag but a neighborhood with streets and house numbers.

Open, at that depth, with resolvable identifiers and a license you can build a business on: that thing does not exist.

And the maddening part is that the raw material for it is sitting in the public domain. Pre-1930 treatises and encyclopedias, whose copyrights have expired. American Law Institute drafts from the 1920s. Government works that were never copyrightable at all. Collectively: millions of section headings and tables of contents, structured by the finest legal editors of their eras, machine-readable for the first time in history because we finally have machines that read.

Nobody's permission is required. That is the sentence I keep coming back to. The deepest classification work in American legal history is either locked (West) or contested (the standards fight) or waiting in books old enough that they belong to everyone.

## Something has to be done

I will be honest about the hard parts, because they are why this has not happened already. A section heading is not a concept; turning one into the other takes judgment at scale. Deduplication across hundreds of sources is brutal, and the failure mode is subtle: merge too eagerly and you destroy meaning, merge too timidly and you have a pile, not a taxonomy. And an open vocabulary that nobody curates is just a snapshot with a license; the Key Number System's real moat is not the 100,000 numbers, it is the century of maintenance.

But none of those are reasons the thing cannot exist. They are the engineering requirements for it. Solved problems in other fields, waiting for someone in ours to take them seriously.

I have been pulling on this thread for longer than I intended to admit in public. What I can say today is that the ingredients check out: the sources are open, the standard is boring and proven, and the identifiers can be made permanent with tools that already exist.

More soon. In the meantime, I want the argument. If you think the metadata layer is enough and issue-level depth is a librarian's fetish, tell me why. If you think nothing open can stay curated, tell me what governance would fix it. And if you have ever shipped a product with a 30-item practice area dropdown, you are not the villain of this article. You are its audience.

---

## OPEN QUESTIONS FOR ARTHUR (updated)

0. New facts added in this revision, all in the shared evidence log: 1876 Syllabi origin, Mallory subscriber-list story, seven divisions, 396 billion dollar 2024 US market (Grand View Research), LSC 2022 justice gap (92 percent), ECLI/ELI, AustLII 1995. The access-to-justice section explicitly disclaims that a taxonomy fixes housing court; that beat is doing real defamation-proofing and hype-proofing work, keep it.

## OPEN QUESTIONS FOR ARTHUR (original)

1. Same SALI/FOLIO temperature question as the post series. The article version is one notch cooler (no Delaware detail, no whistleblower name). Confirm you want it that cool.
2. "125 years ago" dates from the 1897 to 1906 construction. Consistent with Post 1; change both or neither.
3. The closer names three invitations to argue. If you want the article to convert to newsletter signups instead, replace the last paragraph with a pointer to the Substack.

## EVIDENCE LOG

Same log as 2026-08-04-linkedin-posts.md. No numbers appear here that are not in that log. OLIT itself is deliberately absent; the "ingredients check out" paragraph is the only hook and discloses nothing not already public in the sources themselves.
