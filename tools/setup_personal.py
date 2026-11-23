#!/usr/bin/env python3
"""Create the personal/ folder from templates/personal/ (personal copies only).

  python tools/setup_personal.py          # create personal/ and CLAUDE.local.md
  python tools/setup_personal.py --track  # also let git track personal/ (PRIVATE repos only)

Never overwrites existing personal files.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "personal"
PERSONAL = ROOT / "personal"
CLAUDE_LOCAL = ROOT / "CLAUDE.local.md"
GITIGNORE = ROOT / ".gitignore"


def remotes() -> str:
    try:
        return subprocess.run(["git", "remote", "-v"], cwd=ROOT, capture_output=True, text=True).stdout
    except FileNotFoundError:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", action="store_true",
                    help="remove personal/ from .gitignore so it is committed (private repos only)")
    args = ap.parse_args()

    created = []
    for src in TEMPLATE.rglob("*"):
        dest = PERSONAL / src.relative_to(TEMPLATE)
        if src.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        elif not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            created.append(dest.relative_to(ROOT))

    if not CLAUDE_LOCAL.exists():
        CLAUDE_LOCAL.write_text("@personal/AGENTS.local.md\n@personal/profile.md\n", encoding="utf-8")
        created.append(CLAUDE_LOCAL.relative_to(ROOT))

    for c in created:
        print(f"created {c}")
    if not created:
        print("personal/ already set up; nothing overwritten.")

    if args.track:
        print("\nYou asked to track personal/ in git. Only do this if every remote is PRIVATE:")
        print(remotes() or "  (no remotes)")
        if input("Type 'private' to confirm: ").strip().lower() != "private":
            print("Not changed.")
            return 1
        lines = GITIGNORE.read_text(encoding="utf-8").splitlines()
        kept = [l for l in lines if l.strip() not in ("/personal/", "/CLAUDE.local.md")]
        GITIGNORE.write_text("\n".join(kept) + "\n", encoding="utf-8")
        print(".gitignore updated: personal/ and CLAUDE.local.md will now be committed.")
    else:
        print("\npersonal/ is git-ignored. Next: ask your assistant to follow playbooks/10-personal-setup.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
