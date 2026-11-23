#!/usr/bin/env python3
"""Validate the research repository and (optionally) regenerate research/INDEX.md.

Usage:
  python tools/check.py                 # validate (mode auto-detected)
  python tools/check.py --write-index   # validate, then rewrite research/INDEX.md
  python tools/check.py --mode upstream # force upstream checks (CI uses this)

Requires PyYAML. Uses jsonschema when installed (CI installs it); otherwise runs
the built-in checks only and says so.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("check.py needs PyYAML: pip install pyyaml")

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "references" / "sources"
AUTHORITIES = ROOT / "references" / "authorities.yaml"
TOPICS = ROOT / "research" / "topics"
TOPIC_MAP = ROOT / "research" / "_plan" / "topic-map.yaml"
INDEX = ROOT / "research" / "INDEX.md"
PROFILE_FIELDS = ROOT / "schemas" / "profile-fields.yaml"

WORDS_MIN, WORDS_MAX = 1200, 3500          # METHODS §6
MAX_DECISIVE = 15
CORROBORATING_TIERS = {"1", "2", "R"}
REQUIRED_HEADINGS = [
    "Bottom line", "In plain terms", "What the evidence shows", "How sure are we",
    "Where authorities agree and differ", "Putting it into practice",
    "Medication interactions", "Personalization hooks", "Adjacent cohort cautions",
    "Open questions and watch list", "Re-check when", "References", "Reviewer notes",
]
CITE_RE = re.compile(r"\[@([a-z0-9]+(?:-[a-z0-9]+)*)\]")
QUOTE_RE = re.compile(r"[\"“]([^\"”\n]{20,})[\"”]")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"ERROR   {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"warning {where}: {msg}")


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


class _StrDateLoader(yaml.SafeLoader):
    """SafeLoader that keeps dates as strings, so schemas can check their format."""


_StrDateLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def yload(text: str):
    return yaml.load(text, Loader=_StrDateLoader)


def load_yaml(path: Path, rep: Report):
    try:
        return yload(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        rep.error(rel(path), f"invalid YAML: {e}")
        return None


def schema_check(data, schema_name: str, where: str, rep: Report) -> None:
    if jsonschema is None:
        return
    schema = json.loads((ROOT / "schemas" / schema_name).read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        rep.error(where, f"schema: {loc}: {err.message}")


def split_front_matter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4:]


def body_word_count(body: str) -> int:
    """Words from '## Bottom line' up to (not including) '## References'."""
    start = body.find("## Bottom line")
    end = body.find("## References")
    if start == -1:
        return 0
    section = body[start:end if end != -1 else len(body)]
    return len(re.findall(r"\b\w[\w'’-]*\b", section))


def detect_mode() -> str:
    return "personal" if (ROOT / "personal" / "profile.md").exists() else "upstream"


def check_upstream_privacy(rep: Report) -> None:
    try:
        out = subprocess.run(
            ["git", "ls-files", "personal", "CLAUDE.local.md"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout.strip()
    except FileNotFoundError:
        return
    if out:
        for line in out.splitlines():
            rep.error(line, "personal file is tracked in the upstream repository (AGENTS.md §3.5)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["auto", "upstream", "personal"], default="auto")
    ap.add_argument("--write-index", action="store_true")
    args = ap.parse_args()
    mode = detect_mode() if args.mode == "auto" else args.mode
    rep = Report()

    # --- profile fields vocabulary ---
    pf = load_yaml(PROFILE_FIELDS, rep) or {}
    profile_fields = set((pf.get("fields") or {}).keys())

    # --- authorities ---
    auth_data = load_yaml(AUTHORITIES, rep) if AUTHORITIES.exists() else {"authorities": []}
    authorities = {}
    for a in (auth_data or {}).get("authorities") or []:
        aid = a.get("id")
        if not aid:
            rep.error(rel(AUTHORITIES), "authority without id")
        elif aid in authorities:
            rep.error(rel(AUTHORITIES), f"duplicate authority id '{aid}'")
        else:
            authorities[aid] = a

    # --- topic map ---
    tmap = load_yaml(TOPIC_MAP, rep) or {}
    schema_check(tmap, "topic-map.schema.json", rel(TOPIC_MAP), rep)
    map_ids: dict[str, dict] = {}
    for t in tmap.get("topics") or []:
        tid = t.get("id")
        if tid in map_ids:
            rep.error(rel(TOPIC_MAP), f"duplicate topic id '{tid}'")
        map_ids[tid] = t
    for tid, t in map_ids.items():
        for dep in t.get("depends_on") or []:
            if dep not in map_ids:
                rep.error(rel(TOPIC_MAP), f"'{tid}' depends on unknown topic '{dep}'")

    # --- sources ---
    sources: dict[str, dict] = {}
    for path in sorted(SOURCES.glob("*.yaml")):
        data = load_yaml(path, rep)
        if not isinstance(data, dict):
            rep.error(rel(path), "not a mapping")
            continue
        schema_check(data, "source.schema.json", rel(path), rep)
        sid = data.get("id")
        if sid != path.stem:
            rep.error(rel(path), f"id '{sid}' must equal filename '{path.stem}'")
        if sid in sources:
            rep.error(rel(path), f"duplicate source id '{sid}'")
        sources[sid] = data
        if jsonschema is None:  # minimal fallback checks
            for key in ("title", "year", "type", "tier", "jurisdiction", "status", "verified", "findings"):
                if not data.get(key):
                    rep.error(rel(path), f"missing '{key}'")
            if not (data.get("verified") or {}).get("method"):
                rep.error(rel(path), "missing verified.method")
        if data.get("authority") and data["authority"] not in authorities:
            rep.error(rel(path), f"unknown authority '{data['authority']}' (add it to authorities.yaml)")
        if data.get("tier") == "M" and data.get("status") == "decisive":
            rep.error(rel(path), "manufacturer material may only be background (METHODS §2)")
    for sid, s in sources.items():
        sup = s.get("superseded_by")
        if sup and sup not in sources:
            rep.error(f"references/sources/{sid}.yaml", f"superseded_by unknown source '{sup}'")

    # --- topics ---
    topic_meta: dict[str, dict] = {}
    cited_anywhere: set[str] = set()
    for path in sorted(TOPICS.glob("*.md")):
        where = rel(path)
        fm_text, body = split_front_matter(path.read_text(encoding="utf-8"))
        if fm_text is None:
            rep.error(where, "missing YAML front matter")
            continue
        try:
            fm = yload(fm_text) or {}
        except yaml.YAMLError as e:
            rep.error(where, f"invalid front matter: {e}")
            continue
        schema_check(fm, "topic-frontmatter.schema.json", where, rep)
        tid = fm.get("id")
        topic_meta[tid] = fm
        status = fm.get("status")
        strict = status == "reviewed"
        if tid != path.stem:
            rep.error(where, f"id '{tid}' must equal filename '{path.stem}'")
        if tid not in map_ids:
            rep.warn(where, "topic is not in research/_plan/topic-map.yaml")
        for dep in fm.get("depends_on") or []:
            if not (TOPICS / f"{dep}.md").exists():
                rep.warn(where, f"depends on '{dep}', which is not published yet")
        for field in fm.get("personalization_inputs") or []:
            if field not in profile_fields:
                rep.error(where, f"personalization input '{field}' not in schemas/profile-fields.yaml")

        headings = set(re.findall(r"^## (.+?)\s*$", body, flags=re.M))
        for h in REQUIRED_HEADINGS:
            if h not in headings:
                rep.error(where, f"missing section '## {h}'")

        words = body_word_count(body)
        if words > WORDS_MAX:
            rep.error(where, f"{words} words; limit {WORDS_MAX} (METHODS §6)")
        elif words < WORDS_MIN:
            (rep.error if strict else rep.warn)(where, f"{words} words; minimum {WORDS_MIN}")

        cited = set(CITE_RE.findall(body))
        cited_anywhere |= cited
        decisive = set(fm.get("sources_decisive") or [])
        background = set(fm.get("sources_background") or [])
        if len(decisive) > MAX_DECISIVE:
            rep.error(where, f"{len(decisive)} decisive sources; limit {MAX_DECISIVE}")
        for sid in sorted(cited | decisive | background):
            if sid not in sources:
                rep.error(where, f"cites unknown source '{sid}'")
        for sid in sorted(cited - decisive - background):
            rep.error(where, f"'{sid}' is cited but not listed in sources_decisive or sources_background")
        for sid in sorted(decisive - cited):
            rep.warn(where, f"decisive source '{sid}' is never cited in the text")
        for sid in sorted(decisive & sources.keys()):
            s = sources[sid]
            if s.get("status") == "superseded":
                rep.error(where, f"decisive source '{sid}' is superseded by '{s.get('superseded_by')}'")
            if tid not in (s.get("topics") or []):
                rep.warn(where, f"source '{sid}' does not list this topic in its 'topics'")

        # Bottom-line rule IDs
        bl = body.split("## Bottom line", 1)[-1].split("\n## ", 1)[0]
        rule_ids = re.findall(r"`([a-z0-9-]+\.\d+)`", bl)
        if not rule_ids:
            rep.error(where, "Bottom line has no rule IDs like `<topic-id>.1`")
        for r in rule_ids:
            if not r.startswith(f"{tid}."):
                rep.error(where, f"rule ID '{r}' must start with '{tid}.'")

        # Corroboration (topic-level proxy for METHODS §3; the verifier checks per rule)
        corro = [sources[s] for s in decisive if s in sources and sources[s].get("tier") in CORROBORATING_TIERS]
        bodies = {s.get("authority") or s.get("organization") or (s.get("authors") or ["?"])[0] for s in corro}
        non_fed = [s for s in corro if s.get("jurisdiction") != "us-federal"]
        if len(bodies) < 2 or not non_fed:
            (rep.error if strict else rep.warn)(
                where, "corroboration: needs tier 1/2/R decisive sources from ≥2 bodies, ≥1 not US federal")

        # Long quotations
        for q in QUOTE_RE.findall(body):
            if len(q.split()) >= 15:
                rep.error(where, f"quotation of {len(q.split())} words; limit is under 15 (METHODS §5)")

    # Sources pointing at topics
    for sid, s in sources.items():
        for t in s.get("topics") or []:
            if t not in topic_meta and t not in map_ids:
                rep.warn(f"references/sources/{sid}.yaml", f"lists unknown topic '{t}'")

    if mode == "upstream":
        check_upstream_privacy(rep)

    if args.write_index:
        write_index(topic_meta, sources, map_ids)

    for line in rep.warnings + rep.errors:
        print(line)
    note = "" if jsonschema else " (jsonschema not installed: schema checks skipped)"
    print(f"\n{mode} mode · {len(map_ids)} mapped topics · {len(topic_meta)} topic files · "
          f"{len(sources)} sources · {len(rep.errors)} errors · {len(rep.warnings)} warnings{note}")
    return 1 if rep.errors else 0


def write_index(topic_meta: dict, sources: dict, map_ids: dict) -> None:
    lines = [
        "# Research index",
        "",
        "Generated by `python tools/check.py --write-index`. Do not edit by hand.",
        "",
    ]
    if not topic_meta:
        lines += ["_No topics published yet._", ""]
    else:
        lines += [
            "| Topic | What it answers | Status | Confidence | Version | Reviewed | Next check | Human review |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for tid in sorted(topic_meta):
            fm = topic_meta[tid]
            lines.append(
                f"| [`{tid}`](topics/{tid}.md) | {fm.get('description', '')} | {fm.get('status', '')} | "
                f"{fm.get('confidence', '')} | {fm.get('version', '')} | {fm.get('reviewed', '')} | "
                f"{fm.get('next_check', '')} | {fm.get('human_review', '')} |"
            )
        lines.append("")
    pending = [t for t, m in map_ids.items() if t not in topic_meta and m.get("status") != "rejected"]
    if pending:
        lines += ["## Mapped but not yet published", ""]
        for t in sorted(pending, key=lambda x: (map_ids[x].get("priority", 9), x)):
            m = map_ids[t]
            lines.append(f"- `{t}` — {m.get('title', '')} (priority {m.get('priority')}, {m.get('status')})")
        lines.append("")
    counts: dict[str, int] = {}
    for s in sources.values():
        counts[s.get("status", "?")] = counts.get(s.get("status", "?"), 0) + 1
    lines += ["## Sources", "", ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "None yet.", ""]
    INDEX.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
