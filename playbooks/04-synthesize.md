# 04 — Synthesize across topics (upstream)

Run after a batch of topic PRs merges. Branch: `synth/<YYYY-MM-DD>`.

**Goal:** the topics read as one coherent body of research.

## Steps

1. **Conflicts.** Compare every Bottom-line rule across topics. Find rules that contradict, that state the same quantity differently (for example, two different daily amounts for the same thing), or that leave a gap where one topic assumes another covers it. For each, decide which topic is the canonical home of that rule; the other topic should refer to it, not restate it. Fixing a rule's substance is a topic update (`02-research-topic.md`), not synthesis: open an issue or a topic PR.
2. **Dependencies.** Update `depends_on` in the topic map and topic front matter to match how the topics actually rely on each other.
3. **Shared numbers.** If several topics depend on a common set of daily targets, make sure one topic owns them and the others cite that topic.
4. **Personalization fields.** Check that every field used in a topic's hooks exists in `schemas/profile-fields.yaml`, and that no two fields mean the same thing.
5. **Coverage.** Re-run the coverage table from `01-discover.md` step 9 against published topics. Add missing topics to the topic map as `proposed`.
6. **Index.** `python tools/check.py --write-index`.
7. **Changelog.** One line per change.
8. **PR** listing each conflict found and how it was resolved, and any topic issues opened.
