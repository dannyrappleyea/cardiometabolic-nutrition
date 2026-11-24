# 05 — Refresh (upstream)

Triggered by: a topic's `next_check` date passing; a new edition of a guideline cited as decisive; a regulator action or trial named in a topic's "Re-check when" list; a reviewer note; or an issue labeled `topic-request` or `evidence-update`.

Branch: `refresh/<topic-id>-<YYYY-MM>`.

## Steps

1. List what triggered the refresh and which topics it touches (search the sources' `topics` field and topic citations for the affected source IDs).
2. For each topic: open the new evidence, record it as sources, and decide whether any Bottom-line rule changes.
3. **No rule change:** update the source files, `reviewed` and `next_check` dates, and the watch list. Keep `version`.
4. **Rule change:** follow `02-research-topic.md` §4–6 for the changed sections, increment `version`, and run `03-verify.md`. The PR description must state old rule → new rule → why (METHODS §8).
5. Mark replaced sources `status: superseded` with `superseded_by`, and update `edition_check` on the ones you re-checked. Never delete source files.
6. Answer any Reviewer notes; log how in `research/changelog.md`.

## Standing calendar

The discovery run records, in `research/_plan/topic-map.yaml` under `calendar`, when each decisive guideline publishes its next edition. Check that list monthly.
