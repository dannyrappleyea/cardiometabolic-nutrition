---
id: area-subject                 # = filename stem; matches the topic map
title: Plain-language title
description: One line for the index — what question this answers  # shown in research/INDEX.md
status: draft                    # draft | reviewed | stale
version: 1                       # +1 whenever any Bottom-line rule changes
confidence: moderate             # high | moderate | low | very-low (overall)
reviewed: YYYY-MM                # last agent review
next_check: YYYY-MM
human_review: not-yet            # not-yet | YYYY-MM (set by the reviewer)
depends_on: []                   # topic IDs
personalization_inputs: []       # field keys from schemas/profile-fields.yaml
sources_decisive: []             # ≤15 source IDs
sources_background: []
---

# Title

> Educational research for the cohort in `SCOPE.md`, not medical advice.

## Bottom line

| Rule | What the evidence supports | Confidence | Applies when |
|---|---|---|---|
| `area-subject.1` | The rule, as a range or amount where the evidence allows | moderate | Core cohort; see hooks |

One short paragraph on how these rules fit together. Preference-neutral: no tastes or personal choices.

## In plain terms

What this topic is about, and why it matters for blood pressure, glucose, lipids or weight in this cohort. Define every technical term used later.

## What the evidence shows

One subsection per question from the topic map. Lead with the strongest evidence. Give effect sizes in absolute terms. Label observational findings. Cite every factual sentence [@source-id].

### Question 1

### Question 2

## How sure are we

Why each rule has the confidence it does: consistency, directness to this cohort, study types, and what result would change it.

## Where authorities agree and differ

| Authority | Jurisdiction | Year | Position | Source |
|---|---|---|---|---|

## Putting it into practice

Neutral translation for anyone in the cohort: amounts, portions, examples, swaps, how to read a label. No brands unless needed to identify a product type.

## Medication interactions

For medication classes common in the cohort: what the label or Tier 1 guideline says about this topic. Never dose advice. Write "None identified" if the search found none, and say what was searched.

## Personalization hooks

| Profile field | Condition | Effect on rules |
|---|---|---|
| `field_key` | e.g., value is "unknown" | e.g., use the cautious default in rule `.2`; suggest asking a clinician |

## Adjacent cohort cautions

For each `SCOPE.md` §4 flag that changes this advice: how, and what the person should check with their clinician.

## Open questions and watch list

- Pending trials, regulator reviews, unresolved disagreements (with what would change the rules).

## Re-check when

- Concrete triggers: a named guideline's next edition, a trial readout, a regulator decision.

## References

**Decisive**
- [@source-id] — 5–10 word note on what it decides

**Background** (reviewed, not decisive; don't re-research)
- [@source-id]

## Reviewer notes

_Written by the human reviewer. Agents never edit or delete this section; respond to each note in the next update and log it in `research/changelog.md`._
