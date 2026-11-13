"""Generate the Markdown documents and JSON/CSV data from the YAML sources."""
import csv
import json
import re

from common import ROOT, expressible, feature_index, load, mark_status

REL_ORDER = ["refines", "exception-of", "requires", "tension-with", "see-also"]
REL_LABEL = {"refines": "refines", "exception-of": "exception of", "requires": "requires",
             "tension-with": "tension with", "see-also": "see also"}


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def rel_text(r):
    parts = []
    for k in REL_ORDER:
        t = r.get("relations", {}).get(k)
        if t:
            parts.append(f"{REL_LABEL[k]} " + ", ".join(f"`{x}`" for x in t))
    if r.get("format_features"):
        parts.append("formats " + ", ".join(f"`{x}`" for x in r["format_features"]))
    return "; ".join(parts) or "-"


def gen_principles(core, profiles, fdata):
    fidx = feature_index(fdata)
    pids = list(profiles)
    rules = core["rules"]
    flat = []
    for r in rules:
        dom = r["id"].split(".")[0]
        flat.append({
            "id": r["id"], "domain": dom, "domain_title": core["domains"][dom]["title"],
            "theme": r["theme"], "theme_title": core["themes"][r["theme"]]["title"],
            "kind": r["kind"], "title": r["title"], "statement": r["statement"],
            "strengths": {p: profiles[p]["strengths"].get(r["id"]) for p in pids},
            "relations": r.get("relations", {}), "format_features": r.get("format_features", []),
            "aliases": r.get("aliases", []), "status": r.get("status", "active")})
    write("build/principles.json", json.dumps({
        "principles_version": core["principles_version"], "profiles": pids,
        "mark_categories": {p: mark_status(core, profiles[p], fidx) for p in pids}, "rules": flat},
        indent=2, ensure_ascii=False) + "\n")
    with open(ROOT / "build" / "principles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "domain", "theme", "kind"] + [f"strength:{p}" for p in pids] +
                   ["title", "statement", "relations", "format_features", "aliases", "status"])
        for x in flat:
            rel = "; ".join(f"{k}: {' '.join(v)}" for k, v in x["relations"].items())
            w.writerow([x["id"], x["domain"], x["theme"], x["kind"]] + [x["strengths"][p] for p in pids] +
                       [x["title"], x["statement"], rel, " ".join(x["format_features"]), " ".join(x["aliases"]), x["status"]])

    L, a = [], None
    L_append = L.append
    L_append("# Transcription Principles: rules")
    L_append("")
    L_append(f"*Generated from `core/principles.yaml` (version {core['principles_version']}), the profiles in `profiles/` and the formats data in `formats/`. Do not edit by hand; edit the sources and run `python3 tools/build.py`.*")
    L_append("")
    L_append("Profiles shown: " + ", ".join(f"**{profiles[p]['title']}** (`{p}`, {profiles[p]['status']})" for p in pids)
             + ". How the framework works is described in [Principles framework](principles-framework.md); what each format can express is in [Format support](format-support.md).")
    L_append("")
    L_append("## Tiers")
    L_append("")
    L_append("| Tier | Test |")
    L_append("|---|---|")
    for t in core["tiers"].values():
        L_append(f"| **{t['title']}** | {t['test']} |")
    L_append("")
    L_append("## Rules")
    L_append("")
    L_append("Strength is set by each profile: **MUST** always; **SHOULD** unless there is a recorded reason; **MAY** at discretion; **OFF** not adopted. For normalisations and corrections, MUST means always applied and OFF means not permitted.")
    for dom, d in core["domains"].items():
        L_append("")
        L_append(f"### {d['title']} (`{dom}`)")
        L_append("")
        L_append(d["description"])
        L_append("")
        L_append("| Theme | Rule | Statement | " + " | ".join(pids) + " | Relations |")
        L_append("|---|---|---|" + "---|" * len(pids) + "---|")
        for r in rules:
            if r["id"].split(".")[0] != dom:
                continue
            sts = " | ".join(profiles[p]["strengths"].get(r["id"], "?") for p in pids)
            L_append(f"| {core['themes'][r['theme']]['title']} | <a id=\"{r['id']}\"></a>`{r['id']}` | **{r['title']}.** {r['statement']} | {sts} | {rel_text(r)} |")
    for pid in pids:
        pr = profiles[pid]
        L_append("")
        L_append(f"## Profile `{pid}`")
        L_append("")
        L_append(f"{pr['title']}. Status: **{pr['status']}**.")
        if pr["status"] == "draft":
            undoc = sorted(set(pr["strengths"]) - set(pr.get("basis", {})))
            L_append("")
            L_append(f"Draft: {len(pr['strengths']) - len(undoc)} of {len(pr['strengths'])} strengths have a documented basis. The other {len(undoc)} take the Scores of Scores strength as a core default and are not yet confirmed choices of the project.")
        L_append("")
        L_append("**Ranked aims** (highest first):")
        L_append("")
        for i, x in enumerate(pr.get("aim_order", []), 1):
            L_append(f"{i}. `{x['rule']}`" + (f" ({x['note']})" if x.get("note") else ""))
        L_append("")
        L_append("**Resolution of tensions:**")
        L_append("")
        L_append("| Wins | Over | Scope | Reason |")
        L_append("|---|---|---|---|")
        for p in pr["precedence"]:
            L_append(f"| `{p['over']}` | `{p['under']}` | {p.get('scope', '')} | {p['reason']} |")
        enc = pr["scope"]["encoding"]
        L_append("")
        L_append(f"**Format of the version of record:** `{enc['format']}`. {enc['dialect']}")
        L_append("")
        L_append("Extensions accepted: " + (", ".join(f"`{x}`" for x in enc["accept_extensions"]) or "none") + ".")
        L_append("")
        L_append("**Categories of printed mark.** The treatment is derived from the formats data (direct or qualified: transcribed; extension: transcribed only if accepted; otherwise unsupported). A category classed as unsupported is left out systematically and stated once in each report. Every other printed mark is transcribed (`read.transcribe-all-marks`).")
        L_append("")
        L_append("| Category | Treatment | Derived from |")
        L_append("|---|---|---|")
        for m in mark_status(core, pr, fidx):
            L_append(f"| {m['title']} (`{m['id']}`) | **{core['treatments'][m['treatment']]['title']}** | {m['reason']} |")
        if pr["scope"].get("unsupported_sources"):
            L_append("")
            L_append("**Source types not covered:** " + ", ".join(pr["scope"]["unsupported_sources"]) + ".")
    L_append("")
    L_append("**Structural precedence (all profiles):** a rule that is an `exception-of` another wins over it within its scope. `refines` and `see-also` never conflict.")
    L_append("")
    L_append("## Concordance with earlier codes")
    L_append("")
    L_append("| Earlier code | Rule |")
    L_append("|---|---|")
    for al, i in sorted(((al, r["id"]) for r in rules for al in r.get("aliases", [])), key=lambda p: [int(x) for x in p[0][2:].split(".")]):
        L_append(f"| {al} | `{i}` |")
    L_append("")
    write("docs/principles-rules.md", "\n".join(L))
    return len(flat)


def gen_notes(notes, core, prof):
    flat = [dict(n, area_title=notes["areas"][n["area"]]["title"]) for n in notes["notes"]]
    write("build/notes.json", json.dumps({"notes_version": notes["notes_version"], "profile": notes["profile"], "notes": flat},
                                         indent=2, ensure_ascii=False) + "\n")
    pre = (ROOT / "notes" / "preamble.md").read_text(encoding="utf-8").strip()
    L = []
    a = L.append
    a(f"# {notes['title']}")
    a("")
    a(f"*Local notes for transcribers and reviewers. Version {notes['notes_version']}. Generated from `notes/registry.yaml`. Applies the profile `{notes['profile']}` of the Transcription Principles, version {core['principles_version']}. Part of the Scores of Scores document set (see the README).*")
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
    if notes.get("outside_this_version"):
        a("")
        a("## Outside this version")
        a("")
        a("These topics have no Note in this version. The core rules apply to them unchanged: keep what the source prints (`stance.doubt-means-preserve`) and record an observation (`declare.observations`). A later pinned version adds Notes for them.")
        a("")
        for x in notes["outside_this_version"]:
            a(f"- {x}")
    a("")
    a("## Concordance with the previous guide")
    a("")
    a("Codes not listed here moved to the core rules; see the concordance in the [rules table](principles-rules.md).")
    a("")
    a("| Earlier code | Note |")
    a("|---|---|")
    pairs = [(al, n["id"]) for n in notes["notes"] for al in n.get("aliases", [])]
    for al, i in sorted(pairs, key=lambda p: (p[0][0], [int(x) for x in p[0][1:].split(".")])):
        a(f"| {al} | `{i}` |")
    a("")
    write("docs/notes-for-transcribers.md", "\n".join(L))
    return len(flat)


def gen_format_support(core, profiles, fdata):
    fidx = feature_index(fdata)
    st = {k: v["label"] for k, v in fdata["statuses"].items()}
    tag = {"documented": "", "inference": " (inferred)", "unverified": " (unverified)"}
    pids = list(profiles)
    fm = [f for f in fdata["formats"]]
    L = []
    a = L.append
    a("# Format support for the rules")
    a("")
    a(f"*Generated from `core/principles.yaml`, `formats/` and the profiles. Formats data version {fdata['formats_version']}, research date {fdata['methodology']['date']}. Do not edit by hand.*")
    a("")
    a("Each rule that depends on what a format can express is linked to the features in the formats data that bear on it. The table shows the status of each feature in four formats, then whether the feature is expressible in each profile's format. Status is a capability label, not a quality score, and every cell is documentation-based, inferred or unverified; none has been tested by conversion (see [the formats reader](../site/formats.html) for mechanisms, conditions and sources).")
    a("")
    a("Expressible natively means the status is direct or qualified, or an extension that the profile accepts. \"No\" does not mean the rule fails: the point is then met in the report or through a workaround rather than in the encoding, and for a category of printed mark the derived treatment follows `read.transcribe-all-marks`.")
    a("")
    head = "| Rule | Feature | " + " | ".join(f["short"] for f in fm) + " | " + " | ".join(f"`{p}`" for p in pids) + " |"
    a(head)
    a("|---|---|" + "---|" * (len(fm) + len(pids)))
    n_rows = 0
    for r in core["rules"]:
        for fid in r.get("format_features", []):
            f = fidx[fid]
            cells = " | ".join(st[f["cells"][x["id"]]["status"]] + tag[f["cells"][x["id"]]["evidence"]] for x in fm)
            ex = []
            for p in pids:
                ok, s, note = expressible(profiles[p], fid, fidx)
                ex.append(("yes" if ok else "no") + (f" ({note})" if note else ""))
            a(f"| `{r['id']}` | `{fid}`: {f['feature']} | {cells} | " + " | ".join(ex) + " |")
            n_rows += 1
    a("")
    unlinked = [f for f in fdata["features"] if not f["rules"]]
    a(f"{len(fdata['features']) - len(unlinked)} of {len(fdata['features'])} features are linked to at least one rule. The other {len(unlinked)} are context for choosing or comparing formats and carry no rule.")
    a("")
    a("## Mark categories")
    a("")
    a("| Category | Feature | " + " | ".join(f"`{p}`" for p in pids) + " |")
    a("|---|---|" + "---|" * len(pids))
    for k, c in core["mark_categories"].items():
        cols = " | ".join(next(m for m in mark_status(core, profiles[p], fidx) if m["id"] == k)["treatment"] for p in pids)
        a(f"| `{k}` | `{c.get('format_feature', '-')}` | {cols} |")
    a("")
    write("docs/format-support.md", "\n".join(L))
    return n_rows


def gen_glossary():
    g = load(ROOT / "core" / "glossary.yaml")
    L = ["# Glossary", "",
         "*Generated from `core/glossary.yaml`. The same terms are used in the rules, the Notes and the paper.*", "",
         "| Term | Meaning |", "|---|---|"]
    for t in g["terms"]:
        L.append(f"| **{t['term']}** | {t['meaning']} |")
    L.append("")
    write("docs/glossary.md", "\n".join(L))
    return len(g["terms"])


def docmap_table():
    m = load(ROOT / "docs" / "manifest.yaml")["documents"]
    L = ["| Document | Answers | Audience |", "|---|---|---|"]
    for d in m:
        L.append(f"| [{d['title']}]({{prefix}}{d['file']}) | {d['answers']} | {d['audience']} |")
    return "\n".join(L)


def inject(path, name, text):
    """Replace the text between <!-- BEGIN name --> and <!-- END name --> markers."""
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    pat = re.compile(r"(<!-- BEGIN " + re.escape(name) + r" -->).*?(<!-- END " + re.escape(name) + r" -->)", re.S)
    if not pat.search(s):
        raise SystemExit(f"{path}: missing markers for {name}")
    p.write_text(pat.sub(lambda m: m.group(1) + "\n" + text + "\n" + m.group(2), s), encoding="utf-8")


def gen_docmap():
    table = docmap_table()
    inject("README.md", "docmap", table.replace("{prefix}", ""))
    inject("docs/overview.md", "docmap", table.replace("{prefix}", "../"))
