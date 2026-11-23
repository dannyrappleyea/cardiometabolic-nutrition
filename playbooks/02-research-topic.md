# 02 — Research and write one topic (upstream)

**Input:** one approved entry from `research/_plan/topic-map.yaml`.
**Output:** `research/topics/<id>.md` (from `templates/topic.md`), new or updated files in `references/sources/`, a search log for the PR description.
Branch: `topic/<id>`.

## 1. Prepare

- Read `SCOPE.md`, `METHODS.md`, the topic's map entry, and every published topic in its `depends_on`. Don't contradict a published topic silently: if your evidence disagrees, say so in the PR and flag it for synthesis.
- If the topic file already exists (an update), start from its "Re-check when" list, its background sources and its **Reviewer notes**. Don't redo background research it lists.
- Check `references/sources/` for sources already on file; reuse them.

## 2. Search

Work down the hierarchy (METHODS §2):

1. **Guidelines** from the authorities in `references/authorities.yaml`, current editions, at least one non-US-federal.
2. **Systematic reviews and meta-analyses** on each of the topic's questions, most recent first. Prefer those including people like the core cohort.
3. **Key RCTs** those reviews rely on, when the effect size or population matters to the rule.
4. **Cohort and Mendelian-randomization studies** only where trials are absent, labeled as such.
5. **Drug labels** for any medication interaction the topic covers.
6. **Food-composition or regulatory databases** for any numbers (amounts per serving, contents).

For each question, search for evidence **against** the emerging answer as well as for it. Note searches and what each turned up for the PR's search log.

## 3. Record sources as you read

For each source you open, create `references/sources/<id>.yaml` (`templates/source.yaml`) immediately, with the verification method and date and paraphrased findings with locators. Mark `status: decisive` only for the ≤15 the bottom line depends on; everything else is `background`. If a source can't be opened, don't cite it.

## 4. Write the topic

Follow `templates/topic.md` section by section.

- **Bottom line first, written last.** Each rule: an ID (`<topic-id>.<n>`), the rule as a range or amount where possible, confidence, and the conditions it applies under. Preference-neutral.
- **Explain at a person's level.** Define terms. Give absolute effects ("lowers systolic pressure by about 5 mmHg") alongside relative ones. Say what is association vs cause.
- **Cite every factual sentence** with `[@id]`.
- **Authorities table:** what each authority says, its year and jurisdiction. Make agreement and disagreement visible.
- **Practice section:** translate the rules into amounts, examples and swaps that work for anyone in the cohort; no personal tastes.
- **Medication interactions:** label facts only; no dose advice.
- **Personalization hooks:** for each profile field (`schemas/profile-fields.yaml`) that changes a rule, state the condition and the effect. If a needed field doesn't exist, add it to `schemas/profile-fields.yaml` and `templates/personal/profile.md` in the same PR and say so.
- **Adjacent cohort cautions:** for each SCOPE §4 flag that changes the advice, say how.
- **Watch list and re-check triggers:** named pending trials, guideline editions, regulator reviews.
- Length 1,200–3,500 words. Cut the weakest material rather than exceed it.

## 5. Check

- `python tools/check.py` passes.
- Corroboration (METHODS §3) is met for every Bottom-line rule, or the rule's confidence and text say why not.
- Re-read the Bottom line against the evidence sections: nothing in it lacks support below.

## 6. Hand off

Pass the draft to a fresh verifier (`03-verify.md`). Fix what it finds. Then add one line to `research/changelog.md`, set front matter `status: draft`, `version` (1 for new, +1 if any rule changed), and open the PR.
