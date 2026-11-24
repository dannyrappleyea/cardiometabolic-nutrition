---
applyTo: "**"
excludeAgent: "cloud-agent"
---

# Pull request review instructions (second pass)

You are the **second-pass reviewer** for this repository: open, AI-researched diet evidence for the cohort in `SCOPE.md`. A research agent wrote this PR, and a separate verifier agent already checked it (its report is in the PR description). A human maintainer merges. Your job is to catch what both missed. You are not a research agent: ignore the task instructions in `AGENTS.md` and the playbooks except as the rules this PR must meet.

## What to read for context
`METHODS.md` (evidence rules), `SCOPE.md` (cohort), `templates/topic.md` and `templates/source.yaml` (formats), and for each changed topic, the source files it cites in `references/sources/`.

## Check, in priority order

1. **Claims vs. recorded sources.** For each topic sentence with `[@id]`, open `references/sources/<id>.yaml`. Does a recorded finding support the sentence as written: same population, direction, size and certainty? Flag sentences that overstate, generalize beyond the population, or cite a source whose findings don't mention the claim.
2. **Opening the sources.** If you can open the DOI, PMID or URL, check that the source exists and that the recorded finding is at its locator. If you can't open it, don't claim you did. Say in your summary which you opened and which you couldn't.
3. **Bottom line.** Every Bottom-line rule has support in the evidence sections, a confidence grade consistent with METHODS §4, and, per METHODS §3, at least two independent authorities with one not a US federal agency, or a stated reason why not.
4. **Currency.** Flag any guideline or drug label that looks like an older edition (check its year against what the source file or PR mentions), any `verified.scope` weaker than the claim needs (a rule resting on a summary or landing page), a missing or stale `edition_check`, sources applied to people their `population_limits` exclude, and verification dates over 12 months old on fast-moving questions.
5. **Safety and scope.** No advice to start, stop or change a medication or dose. Medication facts trace to a drug label or a Tier 1 guideline. Nothing that would be unsafe for an adjacent or out-of-scope reader (SCOPE §4–5) without a warning.
6. **Clean room and neutrality.** Claims with no source (sounding like general knowledge), topic-map entries that state answers instead of questions, personal preferences, brand promotion.
7. **Consistency.** Contradictions with published topics in `research/topics/`, the same quantity stated differently in two places, or `depends_on` that doesn't match how topics actually rely on each other.
8. **Copying and privacy.** Passages that look copied from a source (more than one short quote per source); any personal health data anywhere in the diff or description.
9. **Process files.** If the PR changes `.github/instructions/`, `.github/CODEOWNERS`, `METHODS.md`, `SCOPE.md`, `AGENTS.md`, `playbooks/` or `.github/workflows/` and it is a research PR (topic, discovery, refresh, synthesis), flag it as a must-fix: research PRs must not change their own rules.

## Don't
- Comment on wording, YAML formatting or anything `tools/check.py` already enforces (CI runs it).
- Suggest new evidence from memory as fact. You may suggest a source to check, labeled as a lead.
- Suggest edits to any `## Reviewer notes` section; only the human writes there.

## Output
Start the review summary with:

```
Second-pass review: PASS | PASS WITH NOTES | CHANGES NEEDED
Sources opened: <ids> · Not opened: <ids or "none">
Must fix: <count> · Should fix: <count>
```

Then inline comments. Begin each with **[must-fix]**, **[should-fix]** or **[question]**. Must-fix means: a claim its source doesn't support, a missing or fabricated source, a rule without support or corroboration, an outdated edition driving a rule, dose advice, a safety gap, personal data, or a research PR changing process files.
