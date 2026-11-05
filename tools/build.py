#!/usr/bin/env python3
"""Validate the Principles registry, a profile and the Notes registry, then generate the outputs.

Usage:  python3 tools/build.py [profile.yaml]
Outputs: docs/principles-rules.md, docs/notes-for-transcribers.md,
         build/principles.json, build/principles.csv, build/notes.json
Exit status is non-zero if any check fails.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
REL_ORDER = ["refines", "exception-of", "requires", "tension-with", "see-also"]
REL_LABEL = {"refines": "refines", "exception-of": "exception of", "requires": "requires",
             "tension-with": "tension with", "see-also": "see also"}


def load(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def schema_errors(instance, schema_file):
    schema = json.loads((ROOT / "schemas" / schema_file).read_text())
    v = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{schema_file}: {'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}" for e in v.iter_errors(instance)]


def find_cycle(edges):
    """edges: dict node -> set(nodes it beats). Return a cycle as a list, or None."""
    state, stack = {}, []

    def visit(n):
        state[n] = 1
        stack.append(n)
        for m in edges.get(n, ()):
            if state.get(m) == 1:
                return stack[stack.index(m):] + [m]
            if m not in state:
                c = visit(m)
                if c:
                    return c
        stack.pop()
        state[n] = 2
        return None

    for n in list(edges):
        if n not in state:
            c = visit(n)
            if c:
                return c
    return None


def check(core, prof):
    errs = schema_errors(core, "principles-registry.schema.json") + schema_errors(prof, "profile.schema.json")
    if errs:
        return errs  # structural problems first
    rules = core["rules"]
    ids = [r["id"] for r in rules]
    byid = {r["id"]: r for r in rules}
    if len(ids) != len(set(ids)):
        errs += [f"duplicate rule id: {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    if core["principles_version"] != prof["principles_version"]:
        errs.append(f"profile targets principles_version {prof['principles_version']}, registry is {core['principles_version']}")
    for t, d in core["themes"].items():
        if d["domain"] not in core["domains"]:
            errs.append(f"theme {t}: unknown domain {d['domain']}")
    seen_alias = {}
    for r in rules:
        dom = r["id"].split(".")[0]
        if dom not in core["domains"]:
            errs.append(f"{r['id']}: unknown domain '{dom}'")
        if r["theme"] not in core["themes"]:
            errs.append(f"{r['id']}: unknown theme '{r['theme']}'")
        elif core["themes"][r["theme"]]["domain"] != dom:
            errs.append(f"{r['id']}: theme '{r['theme']}' belongs to domain '{core['themes'][r['theme']]['domain']}', not '{dom}'")
        if (dom == "normalise") != (r["kind"] == "permission") and r["id"] != "normalise.closed-list":
            errs.append(f"{r['id']}: kind '{r['kind']}' does not fit domain '{dom}' (permissions live in 'normalise')")
        for rel, targets in r.get("relations", {}).items():
            for t in targets:
                if t not in byid:
                    errs.append(f"{r['id']}: {rel} -> unknown rule {t}")
                elif t == r["id"]:
                    errs.append(f"{r['id']}: {rel} points to itself")
                elif byid[t].get("status", "active") == "retired" and r.get("status", "active") == "active":
                    errs.append(f"{r['id']}: {rel} -> retired rule {t}")
        for a in r.get("aliases", []):
            if a in seen_alias:
                errs.append(f"alias {a} used by both {seen_alias[a]} and {r['id']}")
            seen_alias[a] = r["id"]
        for t in r.get("replaced_by", []):
            if t not in byid:
                errs.append(f"{r['id']}: replaced_by unknown rule {t}")
    # profile
    active = {r["id"] for r in rules if r.get("status", "active") == "active"}
    for i in active - set(prof["strengths"]):
        errs.append(f"profile: no strength for active rule {i}")
    for i in set(prof["strengths"]) - set(ids):
        errs.append(f"profile: strength given for unknown rule {i}")
    for r in rules:
        if r["id"].startswith("normalise.") and r["id"] != "normalise.closed-list":
            if prof["strengths"].get(r["id"]) == "OFF" and r["id"] in {x for p in prof["precedence"] for x in (p["over"], p["under"])}:
                errs.append(f"profile: {r['id']} is OFF but used in precedence")
    for a in prof.get("aim_order", []):
        if a["rule"] not in byid:
            errs.append(f"profile: aim_order names unknown rule {a['rule']}")
    for k, c in core["mark_categories"].items():
        if c["default_treatment"] not in core["treatments"]:
            errs.append(f"mark category {k}: unknown treatment '{c['default_treatment']}'")
    for k, o in prof.get("scope", {}).get("marks", {}).items():
        if k not in core["mark_categories"]:
            errs.append(f"profile: scope.marks names unknown mark category '{k}'")
        if o["treatment"] not in core["treatments"]:
            errs.append(f"profile: scope.marks.{k}: unknown treatment '{o['treatment']}'")
    # tensions must be resolved; precedence must be consistent
    tensions = {frozenset((r["id"], t)) for r in rules for t in r.get("relations", {}).get("tension-with", [])}
    edges = defaultdict(set)
    resolved = set()
    for p in prof["precedence"]:
        for k in ("over", "under"):
            if p[k] not in byid:
                errs.append(f"profile: precedence names unknown rule {p[k]}")
        edges[p["over"]].add(p["under"])
        resolved.add(frozenset((p["over"], p["under"])))
    for r in rules:  # exceptions beat the rule they limit
        for t in r.get("relations", {}).get("exception-of", []):
            edges[r["id"]].add(t)
    for tpair in tensions - resolved:
        errs.append("profile: unresolved tension " + " <-> ".join(sorted(tpair)))
    cyc = find_cycle(edges)
    if cyc:
        errs.append("precedence cycle: " + " > ".join(cyc))
    return errs


def check_notes(notes, core, prof):
    errs = schema_errors(notes, "notes-registry.schema.json")
    if errs:
        return errs
    rules = {r["id"]: r for r in core["rules"]}
    domains = set(core["domains"])
    ids, seen_alias = [], {}
    if notes["profile"] != prof["profile"]:
        errs.append(f"notes target profile {notes['profile']}, profile is {prof['profile']}")
    for a in notes["areas"]:
        if a in domains:
            errs.append(f"area '{a}' reuses a core domain name")
    for n in notes["notes"]:
        ids.append(n["id"])
        area = n["id"].split(".")[0]
        if area != n["area"]:
            errs.append(f"{n['id']}: ID prefix does not match area '{n['area']}'")
        if n["area"] not in notes["areas"]:
            errs.append(f"{n['id']}: unknown area '{n['area']}'")
        if n["id"] in rules:
            errs.append(f"{n['id']}: clashes with a core rule ID")
        for t in n.get("applies", []):
            if t not in rules:
                errs.append(f"{n['id']}: applies unknown core rule {t}")
            elif t.startswith("normalise.") and t != "normalise.closed-list" and prof["strengths"].get(t) == "OFF":
                errs.append(f"{n['id']}: applies {t}, which the profile does not permit (OFF)")
        if n["kind"] == "presentation" and not any(t.startswith("normalise.") for t in n.get("applies", [])):
            errs.append(f"{n['id']}: kind 'presentation' must apply a registered normalisation")
        for a in n.get("aliases", []):
            if a in seen_alias:
                errs.append(f"alias {a} used by both {seen_alias[a]} and {n['id']}")
            seen_alias[a] = n["id"]
    for i in {i for i in ids if ids.count(i) > 1}:
        errs.append(f"duplicate note id: {i}")
    # every permitted normalisation should be covered by at least one note or be left to the defaults on purpose
    return errs


def build_notes(notes, core, prof):
    flat = [dict(n, area_title=notes["areas"][n["area"]]["title"]) for n in notes["notes"]]
    (ROOT / "build" / "notes.json").write_text(json.dumps(
        {"notes_version": notes["notes_version"], "profile": notes["profile"], "notes": flat},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pre = (ROOT / "notes" / "preamble.md").read_text(encoding="utf-8").strip()
    L = []
    a = L.append
    a(f"# {notes['title']}")
    a("")
    a(f"*Local notes for transcribers and reviewers. Version {notes['notes_version']} (draft). Generated from `notes/registry.yaml`. Applies the profile `{notes['profile']}` of the Transcription Principles, version {core['principles_version']}. Part of the Scores of Scores document set (see the README).*")
    a("")
    a(pre)
    a("")
    a("## Contents")
    a("")
    a("| Area | Section |")
    a("|---|---|")
    for k, d in notes["areas"].items():
        a(f"| `{k}` | {d['title']} |")
    for area, d in notes["areas"].items():
        items = [n for n in notes["notes"] if n["area"] == area]
        if not items:
            continue
        a("")
        a(f"## {d['title']} (`{area}`)")
        a("")
        a(d["description"])
        for n in items:
            a("")
            a(f"<a id=\"{n['id']}\"></a>")
            a("")
            a(f"### `{n['id']}`: {n['title']}")
            a("")
            meta = f"*{n['kind']}*"
            if n.get("applies"):
                meta += "; applies " + ", ".join(f"[`{x}`](principles-rules.md#{x})" for x in n["applies"])
            a(meta)
            a("")
            a(n["statement"])
            for x in n.get("details", []):
                a("")
                a(f"- {x}")
            for x in n.get("exceptions", []):
                a("")
                a(f"- *Exception:* {x}")
            for e in n.get("examples", []):
                a("")
                a(f"- *Example:* {e['situation']} {e['handling']}")
            if n.get("aliases"):
                a("")
                a("Earlier codes: " + ", ".join(n["aliases"]) + ".")
    if notes.get("not_yet_covered"):
        a("")
        a("## Not yet covered")
        a("")
        a("To be added as core rules if general, or as Notes if house style. Until then, ask your reviewer (`workflow.ask-reviewer`) and record the decision in the report.")
        a("")
        for x in notes["not_yet_covered"]:
            a(f"- {x}")
    a("")
    a("## Concordance with the previous guide")
    a("")
    a("Codes not listed here moved to the core rules; see the concordance in the [rules table](principles-rules.md).")
    a("")
    a("| Earlier code | Note |")
    a("|---|---|")
    pairs = []
    for n in notes["notes"]:
        for al in n.get("aliases", []):
            pairs.append((al, n["id"]))
    def key(p):
        al = p[0]
        return (al[0], [int(x) for x in al[1:].split(".")])
    for al, i in sorted(pairs, key=key):
        a(f"| {al} | `{i}` |")
    a("")
    (ROOT / "docs" / "notes-for-transcribers.md").write_text("\n".join(L), encoding="utf-8")
    return len(flat)


def rel_text(r):
    parts = []
    for k in REL_ORDER:
        t = r.get("relations", {}).get(k)
        if t:
            parts.append(f"{REL_LABEL[k]} " + ", ".join(f"`{x}`" for x in t))
    return "; ".join(parts) or "-"


def mark_status(core, prof):
    """Effective treatment of each mark category: the profile's choice, else the core default."""
    over = prof.get("scope", {}).get("marks", {})
    out = []
    for k, c in core["mark_categories"].items():
        o = over.get(k, {})
        t = o.get("treatment", c["default_treatment"])
        out.append({"id": k, "title": c["title"], "description": c["description"],
                    "default_treatment": c["default_treatment"], "treatment": t,
                    "reclassified": t != c["default_treatment"], "reason": o.get("reason") or c.get("rationale", "")})
    return out


def build(core, prof):
    strengths = prof["strengths"]
    rules = core["rules"]
    flat = []
    for r in rules:
        dom = r["id"].split(".")[0]
        flat.append({
            "id": r["id"], "domain": dom, "domain_title": core["domains"][dom]["title"],
            "theme": r["theme"], "theme_title": core["themes"][r["theme"]]["title"],
            "kind": r["kind"], "title": r["title"], "statement": r["statement"],
            "strength": strengths.get(r["id"]), "relations": r.get("relations", {}),
            "aliases": r.get("aliases", []), "status": r.get("status", "active"),
        })
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "principles.json").write_text(json.dumps(
        {"principles_version": core["principles_version"], "profile": prof["profile"],
         "mark_categories": mark_status(core, prof), "rules": flat},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with open(ROOT / "build" / "principles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "domain", "theme", "kind", "strength", "title", "statement", "relations", "aliases", "status"])
        for x in flat:
            rel = "; ".join(f"{k}: {' '.join(v)}" for k, v in x["relations"].items())
            w.writerow([x["id"], x["domain"], x["theme"], x["kind"], x["strength"], x["title"], x["statement"], rel, " ".join(x["aliases"]), x["status"]])

    L = []
    a = L.append
    a(f"# Transcription Principles: rules")
    a("")
    a(f"*Generated from `principles/registry.yaml` (version {core['principles_version']}) and `profiles/{prof['profile']}.yaml`. Do not edit by hand; edit the sources and run `python3 tools/build.py`.*")
    a("")
    a(f"Profile: **{prof['title']}** (`{prof['profile']}`). How the framework works is described in [Principles framework](principles-framework.md).")
    a("")
    a("## Tiers")
    a("")
    a("| Tier | Test |")
    a("|---|---|")
    for k, t in core["tiers"].items():
        a(f"| **{t['title']}** | {t['test']} |")
    a("")
    a("## Rules")
    a("")
    a("Strength is set by the profile: **MUST** always; **SHOULD** unless there is a recorded reason; **MAY** at discretion; **OFF** not adopted. For normalisations, MUST means always applied and OFF means not permitted.")
    for dom, d in core["domains"].items():
        a("")
        a(f"### {d['title']} (`{dom}`)")
        a("")
        a(d["description"])
        a("")
        a("| Theme | Rule | Statement | Strength | Relations |")
        a("|---|---|---|---|---|")
        for r in rules:
            if r["id"].split(".")[0] != dom:
                continue
            st = strengths.get(r["id"], "?")
            a(f"| {core['themes'][r['theme']]['title']} | <a id=\"{r['id']}\"></a>`{r['id']}` | **{r['title']}.** {r['statement']} | {st} | {rel_text(r)} |")
    a("")
    a("## Priorities in this profile")
    a("")
    if prof.get("aim_order"):
        a("**Ranked aims** (highest first):")
        a("")
        for i, x in enumerate(prof["aim_order"], 1):
            note = f" ({x['note']})" if x.get("note") else ""
            a(f"{i}. `{x['rule']}`{note}")
        a("")
    a("**Resolution of tensions:**")
    a("")
    a("| Wins | Over | Scope | Reason |")
    a("|---|---|---|---|")
    for p in prof["precedence"]:
        a(f"| `{p['over']}` | `{p['under']}` | {p.get('scope', '')} | {p['reason']} |")
    a("")
    a("**Structural precedence (all profiles):** a rule that is an `exception-of` another wins over it within its scope. `refines` and `see-also` never conflict.")
    sc = prof.get("scope", {})
    a("")
    a("## Scope in this profile")
    a("")
    if sc.get("encoding"):
        a(f"**Encoding format of the version of record:** {sc['encoding']}.")
        a("")
    a("**Categories of printed mark.** A category classed as editorial or unsupported is left out of the transcription systematically and stated once in each report. Every other printed mark is transcribed (`read.transcribe-all-marks`).")
    a("")
    a("| Treatment | Meaning |")
    a("|---|---|")
    for k, t in core["treatments"].items():
        a(f"| **{t['title']}** | {t['meaning']} |")
    a("")
    a("| Category | Description | Treatment here | Core default | Reason |")
    a("|---|---|---|---|---|")
    for m in mark_status(core, prof):
        a(f"| {m['title']} (`{m['id']}`) | {m['description']} | **{core['treatments'][m['treatment']]['title']}** | {core['treatments'][m['default_treatment']]['title']} | {m['reason'] or '-'} |")
    if sc.get("unsupported_sources"):
        a("")
        a("**Source types not yet covered:** " + ", ".join(sc["unsupported_sources"]) + ".")
    a("")
    a("## Concordance with earlier codes")
    a("")
    a("| Earlier code | Rule |")
    a("|---|---|")
    pairs = sorted(((al, r["id"]) for r in rules for al in r.get("aliases", [])),
                   key=lambda p: [int(x) for x in p[0][2:].split(".")])
    for al, i in pairs:
        a(f"| {al} | `{i}` |")
    a("")
    (ROOT / "docs" / "principles-rules.md").write_text("\n".join(L), encoding="utf-8")
    return len(flat)


def main():
    prof_path = sys.argv[1] if len(sys.argv) > 1 else ROOT / "profiles" / "sos-2026-11.yaml"
    core, prof = load(ROOT / "principles" / "registry.yaml"), load(prof_path)
    notes = load(ROOT / "notes" / "registry.yaml")
    errs = check(core, prof)
    if not errs:
        errs = check_notes(notes, core, prof)
    if errs:
        print("FAILED:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    n = build(core, prof)
    m = build_notes(notes, core, prof)
    print(f"OK: {n} rules and {m} notes, profile {prof['profile']}; wrote docs/principles-rules.md, docs/notes-for-transcribers.md, build/*.json, build/principles.csv")


if __name__ == "__main__":
    main()
