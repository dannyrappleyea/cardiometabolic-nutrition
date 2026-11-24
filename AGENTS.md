# AGENTS.md — rules for AI agents

> Read this file, then `SCOPE.md` and `METHODS.md`, before any task. Then open the playbook for the task (table below). These rules apply to every AI tool; Claude tools load this file through `CLAUDE.md`.

## 0. Reviewing a pull request?

If your task is to **review** a pull request (for example, GitHub Copilot code review), you are not a research agent. Follow `.github/instructions/review.instructions.md` and use the rest of this file, `METHODS.md` and `SCOPE.md` only as the rules the PR must meet.

## 1. Which mode are you in?

| If… | Mode | You serve |
|---|---|---|
| `personal/profile.md` does **not** exist | **Upstream** | The shared research. Everyone in scope is your reader |
| `personal/profile.md` exists | **Personal** | One person. Read `personal/profile.md` and `personal/AGENTS.local.md` before any task |

In personal mode the person may also ask for upstream-style research; treat it as a personal question unless they explicitly ask you to prepare an upstream contribution (`playbooks/13-propose-upstream.md`).

## 2. Who owns what

| Path | Owner | Upstream agents | Personal agents |
|---|---|---|---|
| `SCOPE.md`, `METHODS.md` | Human maintainer | Propose by PR only | Read only |
| `AGENTS.md`, `playbooks/`, `templates/`, `schemas/`, `tools/` | Maintainer | Propose by PR | Read only |
| `.github/` (review instructions, CI, CODEOWNERS) | Maintainer | Propose in a method-change PR only, never in a research PR | Read only |
| `research/`, `references/` | Upstream agents, merged by a human | Write (on a branch) | **Read only**; never edit (keeps `git pull upstream` conflict-free) |
| Topic `## Reviewer notes` sections | Human reviewer | Never edit | Never edit |
| `personal/profile.md` | The person | **Never read** | Edit only on a stated fact or preference |
| `personal/` (everything else) | The person's assistant | **Never read** | Write |

## 3. Non-negotiable rules (both modes)

1. **Never advise starting, stopping or changing a medication or its dose.** Route those questions to the prescriber. Food–drug interaction facts come from the label or Tier 1 guidelines.
2. **Every factual health claim written to a file traces to a verified source** in `references/sources/` (METHODS §5). Never cite from memory.
3. **Clean room** (METHODS §1): prior knowledge points where to look; it is not evidence. No seeded topics or imported conclusions.
4. **Research is preference-neutral.** Preferences live only in `personal/profile.md` and are applied in `personal/guide/`.
5. **No personal data upstream.** No profiles, lab values, medication lists, names, places or dates of care in any upstream file, issue or pull request, even anonymized.
6. **Stay inside `SCOPE.md`.** In personal mode, if the profile falls in the adjacent or out-of-scope zone, say so plainly (SCOPE §2).
7. **Paraphrase**; don't copy passages from sources.

## 4. Playbooks

| Task | Mode | Playbook |
|---|---|---|
| Run or plan the research pipeline | Upstream | `playbooks/00-orchestrate.md` |
| Discover topics and authorities | Upstream | `playbooks/01-discover.md` |
| Research and write one topic | Upstream | `playbooks/02-research-topic.md` |
| Verify a topic before PR (fresh agent) | Upstream | `playbooks/03-verify.md` |
| Cross-topic consistency and index | Upstream | `playbooks/04-synthesize.md` |
| Respond to PR review comments (Copilot or human) | Upstream | `playbooks/06-respond-to-review.md` |
| Scheduled refresh / new guideline edition | Upstream | `playbooks/05-refresh.md` |
| Set up a personal copy | Personal | `playbooks/10-personal-setup.md` |
| Build or rebuild the personal guide | Personal | `playbooks/11-personal-guide.md` |
| Questions, recipes, restaurant checks | Personal | `playbooks/12-personal-tasks.md` |
| Turn a gap found in personal use into an upstream request | Personal | `playbooks/13-propose-upstream.md` |

## 5. Canonical homes

Every fact has one canonical home; edit it first and update every derived copy in the same task.

| Kind | Canonical home | Derived copies |
|---|---|---|
| Cohort definition | `SCOPE.md` | Topic "Adjacent cohort cautions" sections; personal scope check |
| Evidence method | `METHODS.md` | Templates, `tools/check.py` limits |
| What a source says | `references/sources/<id>.yaml` | Citations in topic files |
| What the evidence supports | `research/topics/<id>.md` Bottom line | `research/INDEX.md`; personal guides |
| Profile fields topics may use | `schemas/profile-fields.yaml` | `templates/personal/profile.md`; topic personalization hooks |
| Facts and preferences about the person | `personal/profile.md` | Everything in `personal/guide/` |

## 6. Working conventions

- **Upstream work happens on branches and lands by pull request.** One PR per discovery run, per topic, per synthesis or refresh. Never push to `main`.
- Run `python tools/check.py` before opening a PR; fix every error.
- Regenerate the index with `python tools/check.py --write-index` when topic front matter changes.
- Keep `research/changelog.md` to one line per merged change.
- Dates: `YYYY-MM` in topic files; `YYYY-MM-DD` for source verification.
- When unsure whether something is in scope, a rule change, or safe, stop and ask in the PR or conversation rather than guessing.
