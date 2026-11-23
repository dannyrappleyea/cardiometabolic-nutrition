# 11 — Build or rebuild the personal guide (personal)

**Inputs:** published topics in `research/topics/` (status `reviewed`, or `draft` if the person accepts unreviewed research; ask once and record the choice in `personal/AGENTS.local.md`), and `personal/profile.md`.
**Outputs:** files in `personal/guide/` (layout: `templates/personal/guide/README.md`) and `personal/guide/BUILD.yaml`.

## Principle

**Research + profile → guide.** Every guide line comes from a topic's Bottom-line rule, adjusted only by (a) that topic's personalization hooks applied to the profile's facts, and (b) the profile's preferences.

- A **stricter** preference (they want to avoid something the evidence allows): follow it and mark the line **(your choice)**.
- A **looser** preference (they want something the evidence advises against): state the evidence-based rule and the trade-off in one line, then respect the choice. Never relax medication or safety rules.
- An **adjacent-zone flag** that a topic says changes a rule: mark the line **(check with your clinician)** and say why in a clause.
- Status-dependent rules (those whose hooks read a "current status" field): use the profile's Current status; if the field is missing or stale for the decision, ask.

## First build

1. Read `research/INDEX.md` and every topic to be used.
2. Write the guide files from `templates/personal/guide/`. Organize `diet-guide.md` by how the person eats (meals, shopping, eating out), not by topic. Plain language, one line per rule (rating, amount, swap) with at most a short clause of why.
3. **No source IDs or raw links in guide files.** Back each rule with a footnote naming the topic: `…[^<topic-id>]` and in `## Notes` at the end: `[^<topic-id>]: Why: research/topics/<topic-id>.md`. One footnote per topic per file.
4. Write `BUILD.yaml`: upstream commit (`git rev-parse HEAD`), date, each topic ID with the `version` used, and the profile's `updated` value.
5. Tell the person, briefly: what the guide covers, any adjacent-zone cautions, and any rules waiting on unknown profile fields.

## Rebuild (after `git pull upstream main` or a profile change)

1. Compare current topic versions with `BUILD.yaml`. List topics added, removed, or with a changed `version`; and profile fields changed since the last build.
2. Update only the guide lines that depend on those. Keep the person's saved recipes and restaurant entries, but re-check any whose verdict depends on a changed rule and say which.
3. **Tell the person what changed and why**, rule by rule, in plain language. Never change a medication-related line silently.
4. Update `BUILD.yaml`.

## Rating scale for foods in guides

🟢🟢 daily core · 🟢 often · 🟡 moderate · 🟠 limit · 🔴 avoid. The rating must follow from the topic's rules; say "(your choice)" when a preference moved it.
