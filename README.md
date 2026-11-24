# Cardiometabolic Nutrition

An open, AI-maintained, human-reviewed body of diet research for adults managing a common cluster of conditions: **high blood pressure, prediabetes or early type 2 diabetes, and high LDL cholesterol or triglycerides**, often alongside overweight and the medications usually prescribed for them. Who exactly is covered, with lab ranges, is defined in [`SCOPE.md`](SCOPE.md).

The research is written for people, not journals: longer and deeper than a fact sheet, plainer than a review article, and every claim is traceable to a verified source.

> **Educational material, not medical advice.** Nothing here replaces your clinician or a registered dietitian. Medication decisions, including doses, belong to your prescriber.

## How it works: two tiers

| Tier | What it is | Who changes it | Contains |
|---|---|---|---|
| **1. This repository (upstream)** | Shared, preference-neutral research for everyone in scope | AI agents propose by pull request; a human reviewer merges | `SCOPE.md`, `METHODS.md`, `research/`, `references/`, playbooks, templates, tools |
| **2. Your private copy** | This repository plus a `personal/` folder holding your profile and the guide built from it | You and your AI assistant | `personal/profile.md`, `personal/guide/`, saved recipes and restaurant orders |

Research flows one way: upstream research + your profile → your personal guide. When the upstream research changes, you pull it, and your assistant rebuilds the parts of your guide that depend on what changed, telling you what changed and why.

**Upstream never contains personal data, and personal copies never edit upstream research.** That separation is what keeps your updates conflict-free and the shared research neutral.

## Status: clean room

This repository deliberately starts with **no research, no topic list and no seeded conclusions**. It contains only the cohort definition, the evidence method, and instructions that let an AI agent discover the relevant topics, research them, verify the citations and propose the results for human review. See [`docs/EVALUATION.md`](docs/EVALUATION.md) for how to test whether that works.

## For maintainers and contributors

1. Read [`AGENTS.md`](AGENTS.md), [`SCOPE.md`](SCOPE.md) and [`METHODS.md`](METHODS.md).
2. Point an AI agent at [`playbooks/00-orchestrate.md`](playbooks/00-orchestrate.md). The pipeline is: **discover → research → verify → synthesize**, one pull request per step or topic. Each research PR then gets an automatic second-pass review from GitHub Copilot, which the research agent answers ([`docs/REVIEW-PROCESS.md`](docs/REVIEW-PROCESS.md)).
3. Review each pull request with the checklist in [`.github/pull_request_template.md`](.github/pull_request_template.md). Merging to `main` is the human gate.
4. `python tools/check.py` validates sources, topics and the topic map; CI runs it on every pull request.

## For individuals

1. **Make a private copy; do not fork publicly.** GitHub forks of a public repository are public, and your profile would be too. Create an empty private repository, then:
   ```bash
   git clone https://github.com/<owner>/cardiometabolic-nutrition.git my-diet
   cd my-diet
   git remote rename origin upstream
   git remote add origin https://github.com/<you>/my-diet-private.git
   git push -u origin main
   ```
   Or simply keep a local clone with no remote of your own.
2. Run `python tools/setup_personal.py` (add `--track` only if your remote is private). It creates `personal/` from `templates/personal/`.
3. Ask your AI assistant to follow [`playbooks/10-personal-setup.md`](playbooks/10-personal-setup.md). It interviews you, fills in your profile, checks you're in scope, and builds your guide.
4. To get research updates: `git pull upstream main`, then ask the assistant to "rebuild my guide" ([`playbooks/11-personal-guide.md`](playbooks/11-personal-guide.md)).

`personal/` is listed in `.gitignore` so it can't be pushed by accident from a public clone.

## Layout

```
SCOPE.md            Who this is for: cohort, lab ranges, exclusions (human-owned)
METHODS.md          Evidence hierarchy, corroboration, grading, citation rules (human-owned)
AGENTS.md           Rules for every AI agent, both tiers
research/
  INDEX.md          Generated index of topics (tools/check.py --write-index)
  _plan/            Topic map, discovery log
  topics/           One in-depth analysis per topic
  changelog.md
references/
  sources/          One YAML file per source, stable slug IDs
  authorities.yaml  Bodies whose guidance is weighed, with jurisdiction
playbooks/          Step-by-step instructions for each kind of agent work
templates/          Topic, source and personal-folder templates
schemas/            JSON Schemas for the YAML files and profile fields
tools/              check.py (validation, index), setup_personal.py
docs/               Evaluation plan, design notes
```
