# Methods — how evidence is found, judged and written

> **Human-owned.** Agents follow this file exactly and propose changes by pull request only.

## 1. Clean-room rule

- The repository starts with no topics or conclusions. Agents **discover** what matters for the cohort in `SCOPE.md`; nothing is seeded.
- An agent's prior knowledge may suggest **where to look**. It is never evidence. Every factual claim in a topic file must come from a source the agent **opened in the current session** and recorded in `references/sources/`.
- Agents must not import content, topic lists or conclusions from other diet repositories, personal copies of this repository, or earlier drafts outside this repository. Upstream agents never read `personal/`.
- Discovery is logged (`research/_plan/discovery-log.md`) so a reviewer can see how each topic was found.
- **Snippets are leads, not evidence.** A search-result snippet may suggest what to open or a watch item; it never justifies a topic, a question or a claim on its own.

## 2. Evidence hierarchy

| Tier | Source type | Weight |
|---|---|---|
| **1** | Current clinical practice guidelines from professional societies or national/international health bodies | Highest; graded synthesis of all evidence |
| **2** | Systematic reviews, meta-analyses, scientific statements, umbrella reviews | Very high |
| **3** | Large randomized controlled trials | High for the question tested |
| **4** | Prospective cohort studies, Mendelian randomization | Moderate; association, not cause (MR: supportive of cause, with caveats) |
| **5** | Mechanistic, animal, cell or short-term biomarker studies | Hypothesis-generating only |
| **6** | Plain-language explainers from reputable health institutions; official food-composition or regulatory databases | For explanation and data, not for rules |
| **R** | Regulatory documents and drug labels | Authoritative for what a product is, its approved use and its label warnings |
| **M** | Manufacturer material (company sites, patents, product FAQs) | Lowest trust; product composition or process only, never a health claim; always `background` |
| ✗ | News, blogs, influencers, podcasts, single unreplicated studies, preprints | Not a basis for any rule. Preprints and news may go on a watch list as pointers |

- Disease-specific guidelines outrank general dietary guidelines for this cohort.
- Label every Tier 4–5 finding "observational" or "early evidence" in the text.
- Note industry funding and conflicts of interest in the source file.

## 3. Corroboration

A rule in a topic's **Bottom line** needs agreement from **at least two independent authorities, at least one of which is not a US federal agency** (FDA, CDC, NIH, USDA, HHS). Independence means different organizations, not two documents from the same body or its joint-authored family. US federal guidance can shift for non-scientific reasons; when it departs from professional-society or international consensus, follow the consensus and record the disagreement in the topic's "Where authorities agree and differ" table.

If only one authority addresses a question, say so, lower the confidence, and add the gap to the topic's watch list.

The authorities weighed are discovered, not preset: they are recorded in `references/authorities.yaml` with their jurisdiction and type.

**Jurisdiction floor:** discovery opens at least one non-US guideline for each condition domain in SCOPE §3, and records any jurisdiction it couldn't cover as a gap.

**Check who a source covers before calling it a disagreement.** A guideline that excludes a group (for example, people with diabetes) or makes only a conditional recommendation doesn't contradict a guideline written for that group. Record each source's `population_limits`.

## 4. Confidence grading

Each Bottom-line rule and each topic carries one of:

| Grade | Meaning |
|---|---|
| **High** | Consistent RCT or guideline evidence in this or a closely matching population; further research is unlikely to change it |
| **Moderate** | Good evidence with some inconsistency, indirectness or reliance on cohorts; could change |
| **Low** | Limited, indirect or mostly observational; likely to change |
| **Very low** | Expert opinion or mechanism only; stated so the reader knows it is a judgment |

Where a rule rests on a numeric range, state where the range comes from (a guideline value, a trial's dose, or a judgment).

## 5. Citation and verification

- Cite in topic files with `[@source-id]` after the claim. One claim may carry several IDs.
- Every source file must record **how it was verified**: full text fetched, abstract fetched, DOI resolved, or official landing page fetched, with the date. A source with no verification record fails CI.
- Never cite from memory. If a source can't be opened, it can't be cited; put it on the watch list instead.
- Record findings in the source file as **paraphrased notes with a locator** (section, table or page). Topic files cite those findings.
- **Paraphrase.** At most one short direct quote (under 15 words) per source, and only when the exact wording matters.
- **Record how much you read** (`verified.scope`: full, partial, section, abstract, summary or landing page; `sections_read`). Read long documents in parts rather than stopping at a truncation. If you only know a document through another one (a journal summary, a press release), record that in `read_via`. A tier-1 guideline read only as a summary or landing page can't be decisive for a reviewed topic.
- **Check editions.** Before recording a guideline or drug label, search for a newer edition (the authority's site; Drugs@FDA or DailyMed for labels) and record `edition` and `edition_check`. If a newer edition exists, record and use it. Mark the older source `superseded`, or say which parts still stand. Record the page that shows the latest edition (`evidence_url`); a search that happens not to surface a newer file does not show currency. Check the issuing body's own list of statements or guidelines, since a newer document on the same subject may carry a new title. If the latest edition can't be established, record `not-determined`, not `current`.
- Drug facts come from the current label or Tier 1 guidelines only. Prefer the reference listed drug's label over repackager or distributor copies, and record which copy was used (`label_role`). If the reference listed drug is discontinued, use the FDA reference standard or the most recently revised label for the same active ingredient.
- Re-verify a source older than 12 months before relying on it for a changed rule, and always for fast-moving areas (new drugs, new guideline editions, regulator safety reviews of food ingredients).

## 6. Topic files

- **Length:** 1,200–3,500 words from "Bottom line" through "Re-check when". Aim for completeness at a person's reading level, not academic exhaustiveness. Split a topic that needs more.
- **Decisive sources:** ≤15 per topic. Sources reviewed but not decisive are recorded as `background` so they aren't re-researched.
- **Preference-neutral:** conclusions describe what the evidence supports for the cohort, as ranges where the evidence allows. Tastes and personal choices never appear; they are applied in personal guides.
- **Personalization hooks:** each topic lists which profile fields (from `schemas/profile-fields.yaml`) change its rules and how. Personal guides apply these mechanically. A topic may not invent a profile field; propose new fields in the same pull request.
- **Medication safety:** topics may say a food–drug interaction exists and what the label says; they never advise starting, stopping or changing a dose.
- Format: `templates/topic.md`. One topic per file; filename = topic ID.

## 7. Sources

- One YAML file per source in `references/sources/`, named `<id>.yaml`. Format: `templates/source.yaml`; schema: `schemas/source.schema.json`.
- **IDs are stable slugs** (`<org-or-first-author>-<short-title>-<year>`, lowercase, hyphens). Never rename or reuse one. Mark replaced sources `status: superseded` with `superseded_by`.
- The `reviewer_read` flag is set only by the human reviewer.

## 8. Changes to rules

Any pull request that changes a Bottom-line rule must say, in its description, the old rule, the new rule and the evidence that moved it. Topic `version` increments on every rule change so personal guides can detect it.

## 9. Human review

Merging to `main` is the review gate. The reviewer may also leave notes in a topic's **Reviewer notes** section; agents never edit that section, must answer each note in the next update of that topic, and record how in `research/changelog.md`. Reviewer critique is a strong signal but is still checked against evidence; an agent that disagrees says so in the pull request.
