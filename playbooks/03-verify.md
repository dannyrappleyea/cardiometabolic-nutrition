# 03 — Verify a topic (upstream, fresh agent)

You did **not** write this topic and have not seen its drafting. Your job is to find what's wrong before a human spends time on it. Be skeptical; a clean report is fine, a rubber stamp is not.

**Input:** branch `topic/<id>`. **Output:** a verification report (Markdown, for the PR description). Don't edit the topic; the researcher fixes it.

## Checks

1. **Mechanical:** `python tools/check.py` passes.
2. **Citations exist and say what's claimed.** For every decisive source and a random sample of at least 10 other citations (or all, if fewer):
   - Open the source yourself (DOI, PMID or URL). Does it exist, and do the title, authors and year match the source file?
   - Does the cited finding appear at the recorded locator, and does the topic's sentence represent it fairly (population, size of effect, direction, certainty)?
   - Report each as ✅ supported · ⚠️ overstated/understated · ❌ not found or contradicted.
3. **Bottom line traceability.** Each rule is supported by the evidence sections and its stated confidence matches METHODS §4.
4. **Corroboration.** Each rule meets METHODS §3 (≥2 independent authorities, ≥1 non-US-federal), or says why not.
5. **Counter-evidence.** Run at least two searches designed to find evidence against the main rules (recent meta-analyses, regulator reviews, critiques). Report anything material the topic missed.
6. **Currency and depth.** Search for a newer edition of every decisive guideline and drug label yourself; don't rely on the source's `edition_check`. Is any rule resting on a tier-1 source that was only read as a summary or landing page? Any source with a verification date more than 12 months old on a fast-moving question?
7. **Population limits.** Does the topic apply any source to people it excludes, or present a conditional recommendation as a strong one?
8. **Scope and safety.** No dose advice. Medication facts trace to labels or Tier 1 guidelines. Adjacent-cohort cautions cover the SCOPE §4 flags that plausibly matter. Nothing harmful for an out-of-scope reader without a warning.
9. **Neutrality.** No personal preferences, tastes or brand promotion.
10. **Copying.** No passage copied from a source; at most one short quote per source.
11. **Readability.** Terms defined; absolute numbers given; a non-scientist could act on the Bottom line.

## Report format

```
## Verification report — <topic-id> (verifier: <model/agent>, <YYYY-MM-DD>)
Result: PASS | PASS WITH NOTES | FAIL
### Citation checks
| Citation | Claim (short) | Result | Note |
### Issues (must fix)
### Suggestions (optional)
### Counter-evidence searches
```

FAIL if any ❌ on a decisive source, any rule without support, any dose advice, or a superseded guideline driving a rule.
