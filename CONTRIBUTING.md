# Contributing

Most content here is written by AI agents following `AGENTS.md` and the playbooks, and reviewed by humans. You can contribute in three ways:

1. **Request a topic or flag new evidence:** open an issue with the *Topic request* template. Never include personal health data.
2. **Run the pipeline:** point an AI agent at `playbooks/00-orchestrate.md` on a branch and open the resulting pull requests. Include the search log and verification report.
3. **Review:** pick an open PR, read Copilot's second-pass review and the agent's replies, work through the reviewer checklist, and spot-check citations yourself. You can also leave notes in a topic's `## Reviewer notes` section; agents answer them in the next update.

Changes to `SCOPE.md` or `METHODS.md` need a maintainer's approval and a short rationale in the PR.

Before opening any PR: `pip install pyyaml jsonschema && python tools/check.py --write-index`.
