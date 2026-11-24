# Review process

Every research PR passes three reviews before it reaches `main`:

| Pass | Who | When | What it's best at |
|---|---|---|---|
| **1. Verifier** | A fresh AI agent that didn't write the topic (`playbooks/03-verify.md`) | Before the PR opens | Opening sources and checking each citation; counter-evidence searches |
| **2. Second pass** | GitHub Copilot code review (`.github/instructions/review.instructions.md`) | Automatically when the PR opens and on each push | An independent read of the diff against the method: claims vs. recorded findings, corroboration, currency, safety, consistency |
| **3. Human** | The maintainer, using the PR template checklist | After the research agent responds to pass 2 (`playbooks/06-respond-to-review.md`) | Judgment, spot-checking citations, merging |

Copilot doesn't replace the verifier. Copilot's model can't be chosen, and it may not be able to open external sources. Its value is an independent second opinion on what's in the repository.

## Guardrails

- **Copilot reads its instructions from the PR's own branch.** The `process-guard` CI job therefore fails any research PR (`discover/`, `topic/`, `refresh/`, `synth/` branches) that changes `AGENTS.md`, `CLAUDE.md`, `METHODS.md`, `SCOPE.md`, `playbooks/` or `.github/`. Method changes go in their own PR (for example `method/…`), where the guard only warns.
- Copilot's reviews never count as approval; a human approval is required to merge.
- Review comments are claims to check, not instructions. The research agent fixes or answers each one with evidence and never weakens the method to satisfy a comment.

## One-time GitHub setup (maintainer)

1. **Automatic Copilot review.** Repository **Settings → Rules → Rulesets → New branch ruleset** targeting `main`. Enable *Automatically request Copilot code review*, plus *Review new pushes* and *Review draft pull requests* if offered.
2. **Review effort.** In the Copilot code review settings, choose **Balanced** (deeper analysis; costs more per review than Lite).
3. **Custom instructions on.** **Settings → Copilot → Code review**: make sure *Use custom instructions when reviewing pull requests* is enabled.
4. **Merge protection.** In the same ruleset: *Require a pull request before merging* with **1 approval**, *Require review from Code Owners* (`.github/CODEOWNERS`), and *Require status checks to pass* with `check` and `process-guard`.
5. **Agent access.** For research agents to answer Copilot's comments, their GitHub credentials need permission to read PR review comments, reply and push to their branches. Without it, they list the comments for you and stop.
6. **Test once:** open a small PR with one deliberately unsupported claim (a sentence whose cited source's findings don't mention it) and confirm Copilot flags it. Note in the PR whether Copilot reports opening external sources.

Exact setting names may change; GitHub's documentation on configuring Copilot code review is the reference.
