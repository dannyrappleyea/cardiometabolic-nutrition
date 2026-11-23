# 01 — Discover topics and authorities (upstream)

**Goal:** from `SCOPE.md` alone, find out which dietary questions matter most for the cohort, and which authorities' guidance should be weighed. Output a topic map for human approval. **Write no conclusions**: the map lists questions, not answers.

Branch: `discover/<YYYY-MM-DD>`.

## Ground rules

- Start from the cohort, not from what you believe the answer is. Your prior knowledge can suggest search terms; every topic must be justified by something you opened in this session (log it).
- Prefer breadth first. It's cheaper to reject a proposed topic in review than to miss one.
- Log as you go in `research/_plan/discovery-log.md`: each search or document consulted, what it surfaced, and which topics it led to (log entry IDs `D1`, `D2`, …).

## Steps

1. **Verify the scope.** For each threshold in `SCOPE.md` (§3–5), find the current guideline that defines it and check the number. Record each as a source file. List any disagreement under "Proposed scope corrections" in the PR description; don't edit `SCOPE.md`.
2. **Find the authorities.** Identify the professional societies, national bodies and international organizations that publish current guidance on each condition domain in SCOPE §3, across several jurisdictions (US, Canada, UK, EU, Australia–New Zealand, WHO or others). Record them in `references/authorities.yaml` with jurisdiction, type and the documents found. Note which are US federal agencies.
3. **Mine the guidelines.** For each domain, open the current guideline(s) and their nutrition or lifestyle sections. List every dietary lever, food, nutrient, pattern, target or caution they address. These become candidate topics.
4. **Enumerate medication classes** commonly used by the cohort (from the same guidelines), and for each, check its label for food, beverage, supplement or nutrient interactions and eating-related effects. Each class with a dietary implication becomes a candidate topic (or part of one).
5. **Find what people in the cohort need to decide in daily life.** Look at patient-education materials from the authorities in step 2 and at official national dietary guidelines for the practical decisions they help people make: what to buy, cook, order when eating out, drink, and do on special occasions, and when to eat. Add candidates for whatever they raise.
6. **Look for live controversies and fast-moving areas**: recent systematic reviews, regulator safety reviews, and places where authorities disagree. Add candidates and note them as `watch: true`.
7. **Look for the targets and measurement questions** a person needs (what numbers diet is trying to move, by how much diet can move them, daily nutrient targets for the cohort). Add candidates.
8. **Cluster and shape.** Merge candidates into topics that each back one coherent set of rules: not so broad that a topic exceeds 3,500 words, not so narrow that two topics always change together. Give each topic:
   - an ID (`<area>-<subject>`, lowercase, hyphens, no numbers),
   - 3–8 concrete questions it must answer,
   - a one-paragraph rationale citing the log entries that justify it,
   - `kind`, `priority` (1 = foundational, needed by many others; 2 = important; 3 = useful), and `depends_on`.
9. **Coverage self-check.** For each SCOPE §3 domain and each §4 flag, confirm at least one topic addresses it, or note why none should. For each medication class from step 4, confirm a topic covers its food interactions.
10. **Write** `research/_plan/topic-map.yaml` (schema: `schemas/topic-map.schema.json`), with every topic `status: proposed`. Run `python tools/check.py`.
11. **Open the PR** with: topic count by priority, the coverage table from step 9, proposed scope corrections, and the questions you couldn't resolve.

## For a second, independent discovery run

To test stability, a maintainer may run discovery again in a fresh context on branch `discover/<date>-b` **without access to the first map**. A third agent then diffs the two maps (topics in both, in one only, differently shaped) and the maintainer merges the union they approve.
