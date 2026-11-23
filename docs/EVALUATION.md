# Evaluating the clean-room approach

The question being tested: **given only `SCOPE.md`, `METHODS.md` and the playbooks, can an AI agent discover, research and write diet guidance for this cohort that is as good as or better than guidance built with human-seeded topics?**

## The answer key stays outside

If you already have a hand-built or seeded version of this research (for example, a personal project), it is the **answer key**. Keep it out of the agent's reach:

- Run every upstream session with **only this repository** attached or checked out. No other folders, no project knowledge, no pasted notes.
- Don't paste topic names or conclusions into prompts. The only prompt needed is "Follow `playbooks/00-orchestrate.md`."
- Do comparisons in a **separate** session that sees both, after the clean-room output exists.

## Stages

### 1. Discovery quality (cheap; do first)

Run `01-discover.md` once. Then, in a separate session, compare its topic map with the answer key's topic list.

| Measure | How |
|---|---|
| **Recall** | Share of answer-key topics the map covers (fully, partly, missed) |
| **Novel topics** | Topics the map proposes that the answer key lacks; rate each useful / marginal / noise |
| **Shape** | Are topics sized sensibly (not one giant "diet" topic, not 80 slivers)? |
| **Priority sanity** | Are the foundational topics priority 1? |
| **Traceability** | Does every topic's rationale point to discovery-log entries backed by real sources? |
| **Scope check** | Did step 1 catch any wrong threshold in `SCOPE.md`? |

**Stability:** run discovery a second time in a fresh context (another model, if available) and diff the two maps. High overlap on priority 1–2 topics is the bar; differences in priority 3 topics are expected.

### 2. Topic quality (2–3 topics end to end)

Pick one topic the answer key covers well, one where the answer key is thin, and one fast-moving topic. Run `02-research-topic.md` and `03-verify.md` for each.

| Measure | How |
|---|---|
| **Citation accuracy** | Spot-check decisive citations yourself: exists, finding at locator, fairly represented. Target: zero fabricated sources |
| **Agreement with the answer key** | Same bottom line? Where different, which is better supported? |
| **Corroboration** | Non-US-federal authority actually present for each rule |
| **Depth at reading level** | Would a non-scientist in the cohort understand and act on it? |
| **Verifier value** | Did the fresh verifier catch real problems the researcher missed? |

### 3. Personal layer (after a few topics merge)

In a separate private copy, run `10-personal-setup.md` with a real or realistic profile, then `11-personal-guide.md`. Compare the generated guide with the answer key's guide: same practical rules? Preferences applied and marked correctly? Adjacent-zone cautions present? Then change one topic's version upstream, pull, and check the rebuild reports exactly what changed.

## What would mean the approach needs seeding after all

- Discovery repeatedly misses a topic the answer key shows is important, even after a second run.
- Topics converge on US-federal sources despite METHODS §3.
- Fabricated or misattributed citations reach PRs past the verifier.

If any of these occur, the fix is a change to the **method** (playbook steps, checks), not seeding conclusions: for example, a discovery step that mines a particular kind of document, or a stricter verifier sample.
