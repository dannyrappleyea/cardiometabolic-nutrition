# Design notes

Why the repository is shaped the way it is. For maintainers; agents follow `AGENTS.md`.

**Two tiers, one-way flow.** Upstream holds preference-neutral research; personal copies add `personal/`. Upstream agents never read `personal/`; personal agents never edit `research/` or `references/`. That makes `git pull upstream main` conflict-free and keeps personal data out of the shared repository.

**Private copies, not forks.** GitHub forks of public repositories are public. Personal copies are clones with `upstream` as a remote. `personal/` is git-ignored by default as a second line of defense, and CI fails if a personal file is ever tracked upstream.

**Clean room.** No seeded topics or conclusions. Discovery derives topics from the cohort definition and from what current guidelines and labels address, and logs how. The model's prior knowledge is allowed only as search direction; every claim needs a source opened in-session. Evaluation is in `docs/EVALUATION.md`.

**Scope is the only strong prior.** `SCOPE.md` defines the population with lab ranges and exclusions but names no diets, foods or nutrients. It is human-owned because it decides who the research is for and who could be harmed by it.

**One YAML file per source, slug IDs.** Parallel topic branches can add sources without colliding on sequential numbers, diffs stay small, and CI can validate each file against a schema. Each source records how it was verified and paraphrased findings with locators, so verifiers can check claims quickly.

**Topic files are longer than a fact sheet, shorter than a review.** 1,200–3,500 words, ≤15 decisive sources, fixed sections. Bottom-line rules have stable IDs and a `version` so personal guides can detect changes.

**Personalization hooks + a controlled field vocabulary.** Topics declare which profile fields change which rules (`schemas/profile-fields.yaml`). Personal guide builds become mostly mechanical: apply hooks to the profile's facts, then apply preferences, marked "(your choice)".

**Fresh-context verification.** The agent that writes a topic never verifies it. The human reviewer at the PR is the final gate, with a checklist that includes spot-checking citations personally.

**Generated index.** `research/INDEX.md` is built from topic front matter (`description` fields), so agents get a one-page map of the research before starting work, and it can't drift from the files.

## Possible next steps

- Scheduled refresh: a GitHub Action that runs an AI agent against `playbooks/05-refresh.md` monthly and opens PRs.
- A link checker in CI that resolves each source's DOI or URL.
- Licensing: choose a content license (for example CC BY 4.0) and a code license (for example MIT) before inviting contributors.
