# 00 — Orchestrate the research pipeline (upstream)

You are the **orchestrator**. You plan, delegate and assemble; you don't write topic content yourself. If your tool can run sub-agents in parallel (for example Claude Code's Agent tool), use them as described. If not, run the roles yourself one at a time, but **always run verification in a fresh context** that did not write the topic.

## Pipeline

```
SCOPE.md + METHODS.md
      │
      ▼
 01 discover ──► PR: topic map + authorities + discovery log ──► human approves topics
      │
      ▼ (for each approved topic, in dependency order, parallel where independent)
 02 research-topic ──► 03 verify (fresh agent) ──► PR: topic + its sources
      │
      ▼
 Copilot second-pass review ──► 06 respond to review ──► human merges
      │
      ▼ (after a batch of topics merges)
 04 synthesize ──► PR: cross-topic fixes, index, changelog ──► human merges
      │
      ▼ (on schedule or trigger)
 05 refresh
```

## Steps

1. **Read state.** `research/_plan/topic-map.yaml`, `research/INDEX.md`, `research/changelog.md`, open PRs and issues labeled `topic-request`.
2. **If the topic map is empty or older than 12 months**, run discovery (`01-discover.md`) and stop at its PR. Don't research topics until a human has approved the map (topics with `status: approved`).
3. **Pick a batch.** Up to 5 approved topics whose `depends_on` topics are already published, highest priority first. Mark them `in-progress` on their branches, not on `main`.
4. **Delegate research.** One researcher per topic, each on branch `topic/<id>`, given: this repository, the topic's map entry, and `02-research-topic.md`. Researchers do not see each other's drafts.
5. **Delegate verification.** For each finished draft, a fresh verifier with `03-verify.md`. Send failures back to the researcher with the verifier's report; at most two rounds, then open the PR as draft with the unresolved items listed.
6. **Open one PR per topic** using the PR template, ready for review (not draft), so Copilot's automatic review starts. Include the researcher's search log and the verifier's report in the description.
7. **Second pass.** When Copilot's review arrives, the researcher handles it with `06-respond-to-review.md`. Copilot is a second reviewer, not a replacement for step 5: always run the fresh verifier first. If Copilot doesn't review within an hour, note it in the PR and continue; the human reviewer can request it.
8. **Source-ID collisions.** If two branches add the same source, whichever merges second rebases and reuses the existing file, merging any new findings into it.
9. **After a batch merges**, run synthesis (`04-synthesize.md`).
10. **Report** to the maintainer: PRs opened, topics blocked and why, questions for the reviewer.

## Guardrails

- Never merge. Never push to `main`.
- Research PRs never change process files (`AGENTS.md`, `METHODS.md`, `SCOPE.md`, `playbooks/`, `.github/`). Propose method changes in their own PR.
- Never edit `SCOPE.md` or `METHODS.md` except in a PR that proposes the change and explains it.
- If a researcher finds the topic is really two topics, or overlaps an existing one, stop that topic and propose a topic-map change instead.
- Budget: if a topic needs more than ~40 sources opened to reach a bottom line, stop and report; the question is probably too broad.
