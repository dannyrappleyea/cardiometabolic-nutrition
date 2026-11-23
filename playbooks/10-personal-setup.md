# 10 — Set up a personal copy (personal)

**Goal:** a filled-in `personal/profile.md`, a scope check, and a first guide.

## Steps

1. **Check the copy is safe.** Run `git remote -v`. If `origin` points to a public repository (for example, an unmodified public fork), stop and tell the person their profile would be public; explain the private-copy steps in `README.md`. Confirm `personal/` exists (if not, run `python tools/setup_personal.py`).
2. **Explain in two sentences** what you'll do and the privacy defaults in `personal/AGENTS.local.md` (bands instead of exact values, generic medication names, no names, places or dates of care). Ask whether they want to keep those defaults; record the answer in `personal/AGENTS.local.md`.
3. **Interview** the person to fill in `personal/profile.md`, section by section, using the field list in `schemas/profile-fields.yaml`. Ask a few questions at a time. Accept "don't know". If they give exact values, use them for the scope check and store only what the privacy settings allow. Never infer a fact or preference; ask.
4. **Scope check** against `SCOPE.md`:
   - **Core:** say so in one line.
   - **Adjacent:** name each flag and what it means: the research applies, but on the listed points their clinician's advice comes first, and the guide will mark those lines.
   - **Out of scope:** say plainly that this research wasn't built for their situation, why it matters, and that a clinician or registered dietitian is the right source. Build no guide unless they explicitly ask; if they do, every guide page carries a banner.
   Record the zone and flags in the profile front matter (`scope_zone`, `scope_flags`).
5. **Missing data that matters.** List the "unknown" fields that published topics' personalization hooks depend on (for example, a kidney test), and suggest the person ask their clinician. Don't block on them; rules that need them use the cautious default the topic states.
6. **Build the guide** with `11-personal-guide.md`.
7. **Claude tools:** `tools/setup_personal.py` created `CLAUDE.local.md`, which loads the profile and local rules automatically. Other tools read them per `AGENTS.md` §1.
