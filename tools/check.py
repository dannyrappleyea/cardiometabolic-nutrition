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
from datetime import date
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
SCOPE_FILE = ROOT / "SCOPE.md"
DISCOVERY_LOG = ROOT / "research" / "_plan" / "discovery-log.md"
SCOPE_CHECK = ROOT / "research" / "_plan" / "scope-check.yaml"
COVERAGE = ROOT / "research" / "_plan" / "coverage.yaml"

TODAY = date.today()
STALE_DAYS = 365
CORE_DOMAINS = ["blood-pressure", "glycemia", "lipids"]                   # SCOPE §3
DOMAIN_WORDS = {"blood-pressure": ("blood pressure", "hypertension", "blood-pressure"),
                "glycemia": ("glyc", "diabetes"), "lipids": ("lipid", "cholesterol")}
READ_SCOPES = {"full", "partial", "section"}                              # actually read
OPENED_ACCESS = {"full", "partial", "section", "abstract", "summary", "landing-page"}
WEAK_SCOPES = {"summary", "landing-page"}
LIMIT_TYPES = {"guideline", "scientific-statement", "systematic-review", "meta-analysis", "umbrella-review"}
NON_US = {"canada", "uk", "eu", "australia-nz", "who", "international", "other"}
DUP_OVERLAP, DUP_JACCARD = 0.55, 0.27   # share of the shorter question's words; similarity
METHOD_SCOPE = {"fetched-full-text": "full", "fetched-abstract": "abstract",
                "fetched-landing-page": "landing-page", "resolved-doi": "landing-page"}
STOP = set("""a an and are as at be by can do does for from has have how in is it its of on or
should that the their them they this to what when which who whom why will with within without
than then there these those into over under about more less most much many does did""".split())

WORDS_MIN, WORDS_MAX = 1200, 3500          # METHODS §6
MAX_DECISIVE = 15
CORROBORATING_TIERS = {"1", "2", "R"}
REQUIRED_HEADINGS = [
    "Bottom line", "In plain terms", "What the evidence shows", "How sure are we",
    "Where authorities agree and differ", "Putting it into practice",
    "Medication interactions", "Personalization hooks", "Adjacent cohort cautions",
    "Open questions and watch list", "Re-check when", "References", "Reviewer notes",
]
LABEL_EVIDENCE_RE = re.compile(r"accessdata\.fda\.gov|dailymed\.nlm\.nih\.gov|nctr-crs\.fda\.gov/fdalabel", re.I)
LABEL_OLD_YEARS = 2                        # a label older than this needs listed_latest to stay "current"
FAST_LABEL_DAYS = 30                       # recently revised labels: edition check this fresh
# Phrases that express doubt about currency. Kept narrow on purpose: neutral wording such as
# "no newer version listed" or "not checked" (about something else) must not trigger a warning.
DOUBT_PHRASES = ("may have newer", "may not be the latest", "may be outdated", "possibly outdated",
                 "could not confirm", "couldn't confirm")
GAP_DOUBT_PHRASES = DOUBT_PHRASES + ("discontinued",)   # in a gap, a product named before this is doubted
SCOPE_LINE_RES = [  # SCOPE §6: medicine choice or dosing is out of scope
    re.compile(r"\bwhich (?:[\w-]+ ){0,3}(?:medicines?|medications?|drugs?)\b[^?]*\b(?:safe|safest|best|preferred|recommended|to use|to choose)\b", re.I),
    re.compile(r"\b(?:limit|lower|reduce|raise|increase|adjust|change|stop|start)\w*\b[^?]{0,40}"
               r"\b(?:statins?|medicines?|medications?|drugs?|tablets?)\b[^?]{0,20}\bdos(?:e|es|ing|age)\b", re.I),
    re.compile(r"\bdos(?:e|es|ing|age)\b[^?]{0,20}\bof (?:the |their |a |this |these )?(?:statins?|medicines?|medications?|drugs?)\b", re.I),
    re.compile(r"\bdrug[- ](?:drug|interactions? with other (?:drugs|medicines))\b", re.I),
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


def days_old(d: str | None) -> int | None:
    try:
        return (TODAY - date.fromisoformat(str(d))).days
    except (TypeError, ValueError):
        return None


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    """Return dependency cycles (each as a list of IDs) in a depends_on graph."""
    cycles, state, stack = [], {}, []

    def visit(n: str) -> None:
        state[n] = 1
        stack.append(n)
        for m in graph.get(n, []):
            if m not in graph:
                continue
            if state.get(m) == 1:
                cyc = stack[stack.index(m):] + [m]
                if sorted(cyc[:-1]) not in [sorted(c[:-1]) for c in cycles]:
                    cycles.append(cyc)
            elif state.get(m) is None:
                visit(m)
        stack.pop()
        state[n] = 2

    for node in graph:
        if state.get(node) is None:
            visit(node)
    return cycles


def question_tokens(q: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", q.lower()) if len(w) > 2 and w not in STOP}


def parse_discovery_log(rep: Report, sources: dict) -> dict[str, dict]:
    """Rows keyed by log ID, each with 'opened' (bool) and 'access'."""
    rows: dict[str, dict] = {}
    if not DISCOVERY_LOG.exists():
        return rows
    header: list[str] | None = None
    for line in DISCOVERY_LOG.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0].lower() == "log id":
            header = [c.lower() for c in cells]
            continue
        if not header or not re.fullmatch(r"D\d+[a-z]?", cells[0] or ""):
            continue
        row = dict(zip(header, cells))
        lid = cells[0]
        if lid in rows:
            rep.error(rel(DISCOVERY_LOG), f"duplicate log ID {lid}")
        src_cell = next((v for k, v in row.items() if k.startswith("source id")), "")
        src_ids = [x for x in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+", src_cell) if x in sources]
        access = row.get("access", "").strip("` ").lower() or None
        if access:
            opened = access in OPENED_ACCESS
            if opened and not src_ids:
                rep.warn(rel(DISCOVERY_LOG), f"{lid} has access '{access}' but no recorded source ID")
        else:  # older logs without an Access column: opened = has a recorded source
            opened = bool(src_ids)
        rows[lid] = {"opened": opened, "access": access, "sources": src_ids}
    if rows and header and "access" not in header:
        rep.warn(rel(DISCOVERY_LOG), "no Access column; treating rows with a recorded source as opened, others as snippets")
    return rows


def check_sources_quality(sources: dict, rep: Report) -> None:
    """Currency, read scope and population limits (METHODS §5)."""
    for sid, s in sources.items():
        where = f"references/sources/{sid}.yaml"
        if s.get("status") == "superseded":
            continue
        ver = s.get("verified") or {}
        scope = ver.get("scope")
        if not scope:
            rep.warn(where, "verified.scope missing: record how much was actually read")
        if ver.get("read_via") and ver["read_via"] not in sources:
            rep.error(where, f"verified.read_via '{ver['read_via']}' is not a recorded source")
        stype, tier = s.get("type"), s.get("tier")
        if tier == "1" and (scope in WEAK_SCOPES or ver.get("method") == "fetched-landing-page"):
            rep.warn(where, "tier-1 guideline known only from a summary or landing page; read its text before relying on it")
        if stype in ("drug-label", "guideline"):
            ec = s.get("edition_check")
            if stype == "drug-label" and not s.get("edition"):
                rep.warn(where, "drug label without 'edition' (supplement number and date)")
            if not ec:
                rep.warn(where, f"{stype} without edition_check: search for a newer edition and record it")
            else:
                age = days_old(ec.get("date"))
                if age is not None and age > STALE_DAYS:
                    rep.warn(where, f"edition_check is {age} days old; re-check for a newer edition")
                if ec.get("result") == "newer-not-recorded":
                    rep.warn(where, f"a newer edition exists but is not recorded: {ec.get('newer') or '(unnamed)'}")
                if ec.get("result") == "newer-recorded" and ec.get("newer") and ec["newer"] not in sources:
                    rep.error(where, f"edition_check.newer '{ec['newer']}' is not a recorded source")
                if ec.get("result") == "not-determined":
                    rep.warn(where, "edition_check could not determine the latest edition; explain in the PR and re-check before relying on it")
                if ec.get("result") == "current":
                    hits = [p for p in DOUBT_PHRASES if p in source_text(s)]
                    if hits:
                        rep.warn(where, f"edition_check.result is 'current' but the source's own notes say \"{hits[0]}\"; "
                                        "re-check, or use not-determined / newer-not-recorded")
            if stype == "drug-label":
                check_label_currency(s, ec or {}, where, rep)
        method, scope_ = ver.get("method"), ver.get("scope")
        if method == "fetched-full-text" and scope_ in WEAK_SCOPES | {"abstract"}:
            rep.warn(where, f"verified.method is fetched-full-text but scope is '{scope_}'; record the method that matches what was opened")
        if stype in LIMIT_TYPES and s.get("population_limits") is None:
            rep.warn(where, "population_limits not checked (who it excludes; conditional strength). Use [] if none")


def source_text(s: dict) -> str:
    """Free-text fields of a source, lowercased, for consistency checks (only narrow doubt phrases are matched)."""
    ec = s.get("edition_check") or {}
    parts = [s.get("limitations"), s.get("notes"), ec.get("searched")]
    return " ".join(str(p) for p in parts if p).lower()


def check_label_currency(s: dict, ec: dict, where: str, rep: Report) -> None:
    """Drug-label edition evidence (METHODS §5; playbooks/01-discover.md step 4)."""
    evidence = " ".join(str(x) for x in (ec.get("evidence_url"), ec.get("searched")) if x)
    if ec and not LABEL_EVIDENCE_RE.search(evidence):
        rep.warn(where, "drug-label edition_check has no Drugs@FDA or DailyMed URL; open the application overview or "
                        "the label's SPL and record it in edition_check.evidence_url (a web search alone can't show currency)")
    role = s.get("label_role")
    if not role:
        rep.warn(where, "drug label without label_role (rld | reference-standard | manufacturer-site | repackager | other)")
    elif role == "repackager":
        rep.warn(where, "label_role is repackager; METHODS §5 prefers the reference listed drug's label")
    year = s.get("year")
    if ec.get("result") == "current" and isinstance(year, int) and TODAY.year - year > LABEL_OLD_YEARS \
            and not ec.get("listed_latest"):
        rep.warn(where, f"label from {year} is marked current; record edition_check.listed_latest from the "
                        "Drugs@FDA or DailyMed page that shows it is still the latest")
    age = days_old(ec.get("date"))
    if isinstance(year, int) and TODAY.year - year <= LABEL_OLD_YEARS and age is not None and age > FAST_LABEL_DAYS:
        rep.warn(where, f"recently revised label (year {year}) checked {age} days ago; re-check its edition "
                        f"within {FAST_LABEL_DAYS} days of opening the PR")


def eff_scope(s: dict) -> str | None:
    """verified.scope, or a best guess from verified.method for sources recorded before scope existed."""
    ver = s.get("verified") or {}
    return ver.get("scope") or METHOD_SCOPE.get(ver.get("method"))


def source_domains(s: dict, authorities: dict) -> set[str]:
    if s.get("domains"):
        return set(s["domains"])
    a = authorities.get(s.get("authority") or "")
    return set((a or {}).get("domains") or [])


def check_discovery(map_ids: dict, sources: dict, authorities: dict, rep: Report) -> None:
    """Traceability, shape and coverage checks for a discovery run (playbooks/01-discover.md)."""
    tm = rel(TOPIC_MAP)
    log = parse_discovery_log(rep, sources)

    # depends_on cycles
    for cyc in find_cycles({t: list(m.get("depends_on") or []) for t, m in map_ids.items()}):
        rep.error(tm, "depends_on cycle: " + " → ".join(cyc))

    dependents = {t: 0 for t in map_ids}
    for m in map_ids.values():
        for d in m.get("depends_on") or []:
            if d in dependents:
                dependents[d] += 1

    for tid, m in map_ids.items():
        if m.get("status") == "rejected":
            continue
        via = list(m.get("discovered_via") or [])
        cited = set(re.findall(r"\bD\d+[a-z]?\b", m.get("rationale") or ""))
        for d in sorted(set(via) | cited):
            if log and d not in log:
                rep.error(tm, f"'{tid}' refers to {d}, which is not in the discovery log")
        for d in sorted(cited - set(via)):
            rep.warn(tm, f"'{tid}' rationale cites {d} but discovered_via doesn't list it")
        if log:
            opened = [d for d in via if log.get(d, {}).get("opened")]
            if not opened:
                (rep.warn if m.get("watch") else rep.error)(
                    tm, f"'{tid}' traces only to snippet rows; a topic needs at least one opened source (METHODS §1)")
            elif len(opened) < 2:
                rep.warn(tm, f"'{tid}' traces to only {len(opened)} opened row ({opened[0]}); aim for ≥2")
        if m.get("priority") == 1 and not m.get("safety") and dependents.get(tid, 0) == 0:
            rep.warn(tm, f"'{tid}' is priority 1 but no topic depends on it and safety is not set")
        if m.get("priority") in (2, 3) and dependents.get(tid, 0) >= 2:
            rep.warn(tm, f"'{tid}' is priority {m.get('priority')} but {dependents[tid]} topics depend on it; "
                         "foundational topics are priority 1 (step 8), or say why not in the rationale")
        for q in m.get("questions") or []:
            if any(rx.search(q) for rx in SCOPE_LINE_RES):
                rep.warn(tm, f"'{tid}' question may cross SCOPE §6 (choosing or dosing medicines): \"{q[:90]}\"; "
                             "ask only about food, drink and supplements")

    # near-duplicate questions across topics
    qs = [(tid, q, question_tokens(q)) for tid, m in map_ids.items() if m.get("status") != "rejected"
          for q in m.get("questions") or []]
    dups = []
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            (t1, q1, a), (t2, q2, b) = qs[i], qs[j]
            if t1 == t2 or not a or not b:
                continue
            overlap, jac = len(a & b) / min(len(a), len(b)), len(a & b) / len(a | b)
            if min(len(a), len(b)) >= 4 and overlap >= DUP_OVERLAP and jac >= DUP_JACCARD:
                dups.append((overlap, t1, q1, t2, q2))
    for sim, t1, q1, t2, q2 in sorted(dups, reverse=True)[:25]:
        rep.warn(tm, f"possible overlapping questions ({sim:.0%} shared words): '{t1}': \"{q1[:70]}…\" ≈ '{t2}': \"{q2[:70]}…\"; "
                     "give each question one canonical topic")

    check_scope_thresholds(sources, rep)
    gaps = check_coverage(map_ids, sources, rep)
    gaps_text = " ".join(gaps).lower()

    # guideline floors per core domain
    for dom in CORE_DOMAINS:
        g = [s for s in sources.values() if s.get("tier") == "1" and s.get("status") != "superseded"
             and dom in source_domains(s, authorities)]
        if not any(eff_scope(s) in READ_SCOPES for s in g):
            rep.warn(tm, f"no tier-1 guideline for '{dom}' has been read beyond a summary (verified.scope full/partial/section)")
        non_us = {s.get("jurisdiction") for s in g if s.get("jurisdiction") in NON_US and eff_scope(s) in OPENED_ACCESS}
        if not non_us:
            rep.warn(tm, f"no non-US tier-1 guideline opened for '{dom}' (METHODS §3 jurisdiction floor)")
        elif len(non_us) < 2 and not any(w in gaps_text for w in DOMAIN_WORDS[dom]):
            rep.warn(tm, f"only one non-US jurisdiction opened for '{dom}' ({', '.join(sorted(non_us))}); search a second "
                         "jurisdiction's current guideline and open it, or list what you tried under coverage gaps")

    # calendar completeness: every authority with a current tier-1 source has a next-edition entry
    tmap = load_yaml(TOPIC_MAP, rep) or {}
    cal = {str(c.get("source_or_authority")) for c in tmap.get("calendar") or [] if isinstance(c, dict)}
    cal_auth = cal | {sources[c].get("authority") for c in cal if c in sources}
    tier1_auth = sorted({s.get("authority") for s in sources.values()
                         if s.get("tier") == "1" and s.get("status") != "superseded" and s.get("authority")})
    missing_cal = [a for a in tier1_auth if a not in cal_auth]
    if missing_cal:
        rep.warn(tm, "calendar has no next-edition entry for authorities with tier-1 sources: " + ", ".join(missing_cal))


def scope_numbers() -> set[str]:
    """Numeric tokens in SCOPE.md §3–5, used to see that every threshold is enumerated."""
    if not SCOPE_FILE.exists():
        return set()
    text = SCOPE_FILE.read_text(encoding="utf-8")
    m = re.search(r"^## 3\..*?(?=^## 6\.)", text, flags=re.S | re.M)
    body = re.sub(r"§\s*\d+(?:[–-]\d+)?", "", m.group(0) if m else "")
    body = re.sub(r"^## \d+\..*$", "", body, flags=re.M)
    return set(re.findall(r"\d+(?:\.\d+)?", body))


def check_scope_thresholds(sources: dict, rep: Report) -> None:
    where = rel(SCOPE_CHECK)
    if not SCOPE_CHECK.exists():
        rep.warn(where, "missing: playbooks/01-discover.md step 1 records every SCOPE threshold here")
        return
    data = load_yaml(SCOPE_CHECK, rep) or {}
    schema_check(data, "scope-check.schema.json", where, rep)
    rows = data.get("thresholds") or []
    if not rows:
        rep.warn(where, "no thresholds recorded (step 1)")
        return
    covered = " ".join(str(r.get("threshold", "")) for r in rows)
    covered_nums = set(re.findall(r"\d+(?:\.\d+)?", covered))
    missing = sorted(scope_numbers() - covered_nums, key=lambda x: float(x))
    if missing:
        rep.warn(where, "SCOPE.md numbers with no threshold row: " + ", ".join(missing))
    unverified = [r.get("threshold") for r in rows if r.get("status") == "unverified"]
    if unverified:
        rep.warn(where, f"{len(unverified)} threshold(s) unverified: " + "; ".join(map(str, unverified))[:300])
    for r in rows:
        for sid in r.get("sources") or []:
            if sid not in sources:
                rep.error(where, f"'{r.get('threshold')}' cites unknown source '{sid}'")
        if r.get("status") in ("verified", "disagrees") and not r.get("sources"):
            rep.error(where, f"'{r.get('threshold')}' is {r.get('status')} but lists no source")
        if r.get("status") == "disagrees" and not r.get("proposed"):
            rep.warn(where, f"'{r.get('threshold')}' disagrees but has no proposed correction")


def check_coverage(map_ids: dict, sources: dict, rep: Report) -> list[str]:
    """Coverage checks (step 9). Returns the recorded gaps."""
    where = rel(COVERAGE)
    if not COVERAGE.exists():
        rep.warn(where, "missing: playbooks/01-discover.md step 9 records coverage here")
        return []
    data = load_yaml(COVERAGE, rep) or {}
    schema_check(data, "coverage.schema.json", where, rep)
    deps = transitive_deps(map_ids)
    for section in ("domains", "adjacent_flags", "medication_classes", "food_groups"):
        items = data.get(section) or []
        if not items:
            rep.warn(where, f"'{section}' is empty")
        for it in items:
            for t in it.get("topics") or []:
                if t not in map_ids:
                    rep.error(where, f"{section}: '{it.get('item')}' maps to unknown topic '{t}'")
            if not it.get("topics") and not it.get("note"):
                rep.warn(where, f"{section}: '{it.get('item')}' has no topic and no note explaining why")
            for sid in it.get("named_in") or []:
                if sid not in sources:
                    rep.error(where, f"{section}: '{it.get('item')}' named_in unknown source '{sid}'")
            check_canonical(section, it, map_ids, deps, where, rep)

    # gaps that doubt a source's currency while the source says "current"
    # (a source named before a doubt phrase in the same clause)
    gaps = [str(g) for g in data.get("gaps") or []]
    for g in gaps:
        for clause in re.split(r";\s*|\.\s+", g.lower()):
            hits = [clause.find(p) for p in GAP_DOUBT_PHRASES if p in clause]
            if not hits:
                continue
            cut = min(hits)
            for sid, s in sources.items():
                if s.get("status") == "superseded" or (s.get("edition_check") or {}).get("result") != "current":
                    continue
                name = label_name(s) if s.get("type") == "drug-label" else None
                for n in filter(None, (sid, name)):
                    m = re.search(rf"\b{re.escape(n)}\b", clause)
                    if m and m.start() < cut:
                        rep.warn(where, f"gap says \"{clause.strip()[:80]}…\" but '{sid}' records edition_check.result: current; make them agree")
                        break
    return gaps


def label_name(s: dict) -> str | None:
    """Product name at the start of a drug label's title, e.g. 'xenical' from 'XENICAL (orlistat) capsules'."""
    m = re.match(r"\s*([A-Za-z][A-Za-z0-9-]{3,})", str(s.get("title") or ""))
    name = m.group(1).lower() if m else None
    return None if name in {"label", "highlights", "prescribing", "full", "drug"} else name


def transitive_deps(map_ids: dict) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}

    def walk(t: str, seen: set[str]) -> set[str]:
        for d in map_ids.get(t, {}).get("depends_on") or []:
            if d not in seen:
                seen.add(d)
                walk(d, seen)
        return seen

    for t in map_ids:
        out[t] = walk(t, set())
    return out


def item_terms(it: dict) -> list[str]:
    """Names of a coverage item to look for in questions: the item, its parentheticals and its aliases."""
    raw = [str(it.get("item") or "")] + re.findall(r"\(([^)]+)\)", str(it.get("item") or "")) + list(it.get("aliases") or [])
    terms = set()
    for r in raw:
        r = re.sub(r"\([^)]*\)", "", r)
        for part in re.split(r"\s*/\s*|\s*;\s*|,\s+", r):
            part = part.strip().lower()
            if len(part) >= 4:
                terms.add(part)
    return sorted(terms)


def check_canonical(section: str, it: dict, map_ids: dict, deps: dict, where: str, rep: Report) -> None:
    """One canonical topic per item (step 8): other topics that ask about it must depend on the canonical one."""
    canon = it.get("canonical_topic")
    if not canon:
        return
    if canon not in map_ids:
        rep.warn(where, f"{section}: '{it.get('item')}' canonical_topic '{canon}' is not in the topic map")
        return
    pats = [re.compile(rf"\b{re.escape(t)}\b", re.I) for t in item_terms(it)]
    for tid, m in map_ids.items():
        if tid == canon or m.get("status") == "rejected" or canon in deps.get(tid, set()):
            continue
        for q in m.get("questions") or []:
            if any(p.search(q) for p in pats):
                rep.warn(where, f"{section}: '{it.get('item')}' is canonical in '{canon}', but '{tid}' asks about it "
                                f"without depending on it: \"{q[:80]}…\"; move the question or add depends_on")
                break


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
    check_sources_quality(sources, rep)
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

        # Quality of decisive sources (METHODS §5)
        for sid in sorted(decisive & sources.keys()):
            s = sources[sid]
            ver = s.get("verified") or {}
            if s.get("tier") == "1" and (ver.get("scope") in WEAK_SCOPES or ver.get("method") == "fetched-landing-page"):
                (rep.error if strict else rep.warn)(where, f"decisive tier-1 source '{sid}' was read only as a summary or landing page")
            ec = s.get("edition_check") or {}
            if ec.get("result") == "newer-not-recorded":
                rep.error(where, f"decisive source '{sid}' has a newer edition that isn't recorded")
            if ec.get("result") == "not-determined":
                (rep.error if strict else rep.warn)(where, f"decisive source '{sid}' has undetermined currency (edition_check.result: not-determined)")
            if s.get("type") in ("drug-label", "guideline") and not ec:
                (rep.error if strict else rep.warn)(where, f"decisive {s.get('type')} '{sid}' has no edition_check")

        # Long quotations
        for q in QUOTE_RE.findall(body):
            if len(q.split()) >= 15:
                rep.error(where, f"quotation of {len(q.split())} words; limit is under 15 (METHODS §5)")

    # Sources pointing at topics
    for sid, s in sources.items():
        for t in s.get("topics") or []:
            if t not in topic_meta and t not in map_ids:
                rep.warn(f"references/sources/{sid}.yaml", f"lists unknown topic '{t}'")

    # Topic-file depends_on cycles
    for cyc in find_cycles({t: list(fm.get("depends_on") or []) for t, fm in topic_meta.items()}):
        rep.error("research/topics", "depends_on cycle: " + " → ".join(cyc))

    if any(m.get("status") != "rejected" for m in map_ids.values()):
        check_discovery(map_ids, sources, authorities, rep)

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
