# 01 — Discover topics and authorities (upstream)

**Goal:** from `SCOPE.md` alone, find out which dietary questions matter most for the cohort, and which authorities' guidance should be weighed. Output a topic map for human approval. **Write no conclusions**: the map lists questions, not answers.

Branch: `discover/<YYYY-MM-DD>`. Files this run writes: `research/_plan/topic-map.yaml`, `scope-check.yaml`, `coverage.yaml`, `discovery-log.md`, `references/authorities.yaml`, and `references/sources/`.

## Ground rules

- Start from the cohort, not from what you believe the answer is. Your prior knowledge can suggest search terms; every topic and question must be justified by something you **opened** in this session.
- **Snippets are leads, not support.** A search-result snippet can suggest what to open next or a `watch` item. It never justifies a topic or a question on its own. If an idea comes from prior knowledge or a snippet, open a source for it or mark it in the rationale as a search suggestion.
- Prefer breadth first. It's cheaper to reject a proposed topic in review than to miss one.
- **Log as you go** in `research/_plan/discovery-log.md`, one row per search or document (`D1`, `D2`, …). Record **Access** honestly (`full`, `partial`, `section`, `abstract`, `summary`, `landing-page`, or `snippet`). Keep candidate names in the document's own wording, and map them to topic IDs in the last column.
- **Read long documents in parts.** If a fetch is truncated, keep reading until you reach the sections you need, and record what you read in the source's `verified.sections_read`.
- **Check every guideline and drug label is current** before recording it (METHODS §5): search the authority's site (or Drugs@FDA/DailyMed for labels) for a newer edition and fill in `edition` and `edition_check`. If you learn a newer edition exists, open and record it; never leave `result: newer-not-recorded` without saying why in the PR.
- **Record each source's population limits** (`population_limits`): who it excludes, what it doesn't cover, and whether its recommendations are conditional or weak.

## Steps

1. **Verify the scope.** Write one row in `research/_plan/scope-check.yaml` for **every** threshold in `SCOPE.md` §3–5, copied as SCOPE states it, whether or not you can check it. For each, find the current guideline that defines it, record that source, and set `status: verified`, `disagrees` (with `proposed`) or `unverified`. Prefer the source that actually defines the threshold; a summary or journal scan alone leaves it `unverified`. Don't propose a change from a threshold used for a different purpose (for example, a drug-treatment threshold for a diet boundary). Don't edit `SCOPE.md`.
2. **Find the authorities.** Identify the professional societies, national bodies and international organizations that publish current guidance on each condition domain in SCOPE §3, across several jurisdictions (US, Canada, UK, EU, Australia–New Zealand, WHO or others). Record them in `references/authorities.yaml` with jurisdiction, type, domains and the documents found. Note which are US federal agencies. **Jurisdiction floor:** for each SCOPE §3 domain, open at least one non-US guideline; list any jurisdiction you couldn't cover under `gaps` in `coverage.yaml`.
3. **Mine the guidelines.** For each SCOPE §3 domain, read **at least one current guideline's nutrition or lifestyle section in full** (`verified.scope: full`, `partial` or `section`, with `sections_read`), not just a summary. Set the source's `domains`. List every dietary lever, food, nutrient, pattern, target or caution it addresses. These become candidate topics.
4. **Enumerate medication classes** commonly used by the cohort (from the same guidelines). For each class, open the **current** label of at least one commonly prescribed member, preferring the reference listed drug's label from Drugs@FDA or DailyMed over repackager copies. Record its `edition` (supplement number and date) and `edition_check`, and note food, beverage, supplement or nutrient interactions and eating-related effects. Each class with a dietary implication becomes a candidate topic (or part of one).
5. **Find what people in the cohort need to decide in daily life.** Look at patient-education materials from the authorities in step 2 and at official national dietary guidelines for the practical decisions they help people make: what to buy, cook, order when eating out, drink, and do on special occasions, and when to eat. Add candidates for whatever they raise.
6. **Look for live controversies and fast-moving areas**: recent systematic reviews, regulator safety reviews, and places where authorities disagree. Before describing a disagreement, check each side's `population_limits`: a guideline that excludes a group doesn't disagree about that group. Add candidates and mark them `watch: true`.
7. **Look for the targets and measurement questions** a person needs (what numbers diet is trying to move, by how much diet can move them, daily nutrient targets for the cohort). Add candidates.
8. **Cluster and shape.** Merge candidates into topics that each back one coherent set of rules: not so broad that a topic exceeds 3,500 words, not so narrow that two topics always change together. **Each question has one canonical topic;** where two topics need it, one asks it and the other lists that topic in `depends_on`. Give each topic:
   - an ID (`<area>-<subject>`, lowercase, hyphens, no numbers),
   - 3–8 concrete questions it must answer,
   - a one-paragraph rationale citing the log entries that justify it (every cited `D#` also in `discovered_via`; at least two opened rows),
   - `kind`, `priority` and `depends_on`,
   - `safety: true` if getting it wrong could harm someone (for example, food–drug interactions).

   **Priority:** 1 = foundational (other topics depend on it) **or** safety-critical (`safety: true`); 2 = important; 3 = useful. A question about a group SCOPE excludes is a scope boundary, not a question: state it in the rationale instead.
9. **Coverage self-check.** Write `research/_plan/coverage.yaml`: every SCOPE §3 domain, every §4 flag, every medication class from step 4, and **every food group, beverage or food category named in the opened guidelines' eating-pattern recommendations** (with `named_in` source IDs) maps to topic IDs, or has a note saying why no topic is needed. List known gaps.
10. **Write** `research/_plan/topic-map.yaml` (schema: `schemas/topic-map.schema.json`), with every topic `status: proposed`. Run `python tools/check.py`: fix every error, and fix or explain every warning in the PR.
11. **Open the PR** with: topic count by priority; the scope-check table (threshold → status → source), with corrections proposed and anything unverified called out; a coverage summary with gaps; the check warnings you chose not to fix and why; and the questions you couldn't resolve.

## For a second, independent discovery run

To test stability, a maintainer may run discovery again in a fresh context on branch `discover/<date>-b` **without access to the first map**. A third agent then diffs the two maps (topics in both, in one only, differently shaped) and the maintainer merges the union they approve.
