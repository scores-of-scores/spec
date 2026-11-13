"""Validation of every layer and of the links between layers. Returns a list of error strings."""
from collections import defaultdict

from common import ROOT, RULE_REF, feature_index, mark_status, schema_errors

PERMISSION_DOMAINS = {"normalise", "correct"}


def find_cycle(edges):
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


def check_core(core, fidx):
    errs = schema_errors(core, "principles-registry.schema.json", label="core/principles.yaml")
    if errs:
        return errs
    rules = core["rules"]
    ids = [r["id"] for r in rules]
    byid = {r["id"]: r for r in rules}
    errs += [f"duplicate rule id: {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
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
            errs.append(f"{r['id']}: theme '{r['theme']}' belongs to another domain")
        is_perm = r["kind"] == "permission"
        if is_perm and dom not in PERMISSION_DOMAINS:
            errs.append(f"{r['id']}: a permission must be in {sorted(PERMISSION_DOMAINS)}")
        if dom == "normalise" and not is_perm and r["id"] != "normalise.closed-list":
            errs.append(f"{r['id']}: rules in 'normalise' are permissions")
        for rel, targets in r.get("relations", {}).items():
            for t in targets:
                if t not in byid:
                    errs.append(f"{r['id']}: {rel} -> unknown rule {t}")
                elif t == r["id"]:
                    errs.append(f"{r['id']}: {rel} points to itself")
                elif byid[t].get("status", "active") == "retired" and r.get("status", "active") == "active":
                    errs.append(f"{r['id']}: {rel} -> retired rule {t}")
        for f in r.get("format_features", []):
            if f not in fidx:
                errs.append(f"{r['id']}: format_features -> unknown feature {f}")
        for a in r.get("aliases", []):
            if a in seen_alias:
                errs.append(f"alias {a} used by both {seen_alias[a]} and {r['id']}")
            seen_alias[a] = r["id"]
        for t in r.get("replaced_by", []):
            if t not in byid:
                errs.append(f"{r['id']}: replaced_by unknown rule {t}")
    for k, c in core["mark_categories"].items():
        if "format_feature" in c and c["format_feature"] not in fidx:
            errs.append(f"mark category {k}: unknown feature {c['format_feature']}")
        if "default_treatment" in c and c["default_treatment"] not in core["treatments"]:
            errs.append(f"mark category {k}: unknown treatment '{c['default_treatment']}'")
    return errs


def check_profile(core, prof, fdata, fidx):
    pid = prof["profile"]
    errs = schema_errors(prof, "profile.schema.json", label=f"profiles/{pid}.yaml")
    if errs:
        return errs
    rules = core["rules"]
    byid = {r["id"]: r for r in rules}
    if core["principles_version"] != prof["principles_version"]:
        errs.append(f"{pid}: targets principles_version {prof['principles_version']}, registry is {core['principles_version']}")
    active = {r["id"] for r in rules if r.get("status", "active") == "active"}
    st = prof["strengths"]
    errs += [f"{pid}: no strength for active rule {i}" for i in sorted(active - set(st))]
    errs += [f"{pid}: strength given for unknown rule {i}" for i in sorted(set(st) - set(byid))]
    errs += [f"{pid}: basis names unknown rule {i}" for i in sorted(set(prof.get("basis", {})) - set(byid))]
    for r in rules:  # a rule that is adopted cannot require one that is not
        if st.get(r["id"], "OFF") == "OFF":
            continue
        for t in r.get("relations", {}).get("requires", []):
            if st.get(t, "OFF") == "OFF":
                errs.append(f"{pid}: {r['id']} is {st[r['id']]} but requires {t}, which is OFF")
    for a in prof.get("aim_order", []):
        if a["rule"] not in byid:
            errs.append(f"{pid}: aim_order names unknown rule {a['rule']}")
    enc = prof["scope"]["encoding"]
    if enc["format"] not in {f["id"] for f in fdata["formats"]}:
        errs.append(f"{pid}: unknown format {enc['format']}")
    for f in enc["accept_extensions"]:
        if f not in fidx:
            errs.append(f"{pid}: accept_extensions names unknown feature {f}")
        elif fidx[f]["cells"][enc["format"]]["status"] != "extension":
            errs.append(f"{pid}: accept_extensions {f}, but its status in {enc['format']} is not 'extension'")
    for k, o in prof["scope"].get("marks", {}).items():
        if k not in core["mark_categories"]:
            errs.append(f"{pid}: scope.marks names unknown mark category '{k}'")
        elif o["treatment"] not in core["treatments"]:
            errs.append(f"{pid}: scope.marks.{k}: unknown treatment '{o['treatment']}'")
        elif not o.get("reason"):
            errs.append(f"{pid}: scope.marks.{k}: a reclassification needs a reason")
    tensions = {frozenset((r["id"], t)) for r in rules for t in r.get("relations", {}).get("tension-with", [])}
    edges, resolved = defaultdict(set), set()
    for p in prof["precedence"]:
        for k in ("over", "under"):
            if p[k] not in byid:
                errs.append(f"{pid}: precedence names unknown rule {p[k]}")
        edges[p["over"]].add(p["under"])
        resolved.add(frozenset((p["over"], p["under"])))
    for r in rules:
        for t in r.get("relations", {}).get("exception-of", []):
            edges[r["id"]].add(t)
    errs += [f"{pid}: unresolved tension " + " <-> ".join(sorted(tp)) for tp in tensions - resolved]
    cyc = find_cycle(edges)
    if cyc:
        errs.append(f"{pid}: precedence cycle: " + " > ".join(cyc))
    return errs


def check_notes(notes, core, prof):
    errs = schema_errors(notes, "notes-registry.schema.json", label="notes/registry.yaml")
    if errs:
        return errs
    rules = {r["id"]: r for r in core["rules"]}
    domains = set(core["domains"])
    ids, seen_alias = [], {}
    if notes["profile"] != prof["profile"]:
        errs.append(f"notes target profile {notes['profile']}, profile is {prof['profile']}")
    errs += [f"area '{a}' reuses a core domain name" for a in notes["areas"] if a in domains]
    for n in notes["notes"]:
        ids.append(n["id"])
        if n["id"].split(".")[0] != n["area"]:
            errs.append(f"{n['id']}: ID prefix does not match area '{n['area']}'")
        if n["area"] not in notes["areas"]:
            errs.append(f"{n['id']}: unknown area '{n['area']}'")
        if n["id"] in rules:
            errs.append(f"{n['id']}: clashes with a core rule ID")
        for t in n.get("applies", []):
            if t not in rules:
                errs.append(f"{n['id']}: applies unknown core rule {t}")
            elif t.split(".")[0] in PERMISSION_DOMAINS and t != "normalise.closed-list" and prof["strengths"].get(t) == "OFF":
                errs.append(f"{n['id']}: applies {t}, which the profile does not permit (OFF)")
        if n["kind"] == "presentation" and not any(t.startswith("normalise.") for t in n.get("applies", [])):
            errs.append(f"{n['id']}: kind 'presentation' must apply a registered normalisation")
        for a in n.get("aliases", []):
            if a in seen_alias:
                errs.append(f"alias {a} used by both {seen_alias[a]} and {n['id']}")
            seen_alias[a] = n["id"]
    errs += [f"duplicate note id: {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    return errs


def check_formats(fdata, core, profiles):
    errs = []
    errs += schema_errors({k: fdata[k] for k in ("formats_version", "title", "methodology", "formats", "statuses", "categories")},
                          "formats.schema.json", "formats_file", "formats/formats.yaml")
    errs += schema_errors(fdata["sources"], "formats.schema.json", "sources_file", "formats/sources.yaml")
    errs += schema_errors(fdata["cases"], "formats.schema.json", "cases_file", "formats/cases.yaml")
    errs += schema_errors(fdata["fixtures"], "formats.schema.json", "fixtures_file", "formats/fixtures.yaml")
    for cat, items in fdata["_feature_files"].items():
        errs += schema_errors(items, "formats.schema.json", "features_file", f"formats/features/{cat}.yaml")
    if errs:
        return errs
    fids = [f["id"] for f in fdata["features"]]
    errs += [f"duplicate feature id: {i}" for i in sorted({i for i in fids if fids.count(i) > 1})]
    for p in (ROOT / "formats" / "features").glob("*.yaml"):
        if p.stem not in {c["id"] for c in fdata["categories"]}:
            errs.append(f"formats/features/{p.name}: no such category in formats.yaml")
    fmt_ids = {f["id"] for f in fdata["formats"]}
    src = fdata["sources"]
    for f in fdata["formats"]:
        errs += [f"format {f['id']}: unknown source {s}" for s in f["sources"] if s not in src]
    for f in fdata["features"]:
        if set(f["cells"]) != fmt_ids:
            errs.append(f"{f['id']}: cells do not match the formats")
        for k, c in f["cells"].items():
            if c["status"] not in fdata["statuses"]:
                errs.append(f"{f['id']}.{k}: unknown status {c['status']}")
            if c["evidence"] not in fdata["methodology"]["evidence"]:
                errs.append(f"{f['id']}.{k}: unknown evidence {c['evidence']}")
            errs += [f"{f['id']}.{k}: unknown source {s}" for s in c["sources"] if s not in src]
            if c["status"] == "extension" and not c["subset"]:
                errs.append(f"{f['id']}.{k}: an 'extension' cell must name the extension in `subset`")
    for c in fdata["cases"]:
        errs += [f"case {c['id']}: unknown feature {x}" for x in c["rows"] if x not in fids]
        errs += [f"case {c['id']}: unknown source {s}" for s in c["sources"] if s not in src]
    rule_ids = {r["id"] for r in core["rules"]}
    fx_ids = [x["id"] for x in fdata["fixtures"]]
    errs += [f"duplicate fixture id: {i}" for i in sorted({i for i in fx_ids if fx_ids.count(i) > 1})]
    fidx = feature_index(fdata)
    for x in fdata["fixtures"]:
        errs += [f"{x['id']}: unknown feature {f}" for f in x["features"] if f not in fids]
        errs += [f"{x['id']}: unknown rule {r}" for r in x.get("rules", []) if r not in rule_ids]
        if x.get("paper"):
            if set(x.get("positions", {})) != set(profiles):
                errs.append(f"{x['id']}: positions must cover exactly the profiles {sorted(profiles)}")
            for pid, text in x.get("positions", {}).items():
                for ref in RULE_REF.findall(text):
                    if ref not in rule_ids:
                        errs.append(f"{x['id']}.positions.{pid}: cites unknown rule {ref}")
        exp = x.get("expect_treatment")
        if exp:
            for pid, want in exp.items():
                if pid == "mark_category":
                    continue
                got = {m["id"]: m["treatment"] for m in mark_status(core, profiles[pid], fidx)}.get(exp["mark_category"])
                if got != want:
                    errs.append(f"{x['id']}: expected {exp['mark_category']} to be '{want}' under {pid}, derived '{got}'")
    # every rule-linked feature is a known feature; every feature linked to a rule is relevant to a format-dependent rule
    return errs


def check_global_ids(core, notes, fdata):
    seen, errs = {}, []
    groups = [("rule", [r["id"] for r in core["rules"]]), ("note", [n["id"] for n in notes["notes"]]),
              ("feature", [f["id"] for f in fdata["features"]]), ("fixture", [x["id"] for x in fdata["fixtures"]])]
    for kind, ids in groups:
        for i in ids:
            if i in seen and seen[i] != kind:
                errs.append(f"id {i} is used by both a {seen[i]} and a {kind}")
            seen[i] = kind
    return errs


def check_all(core, profiles, notes, fdata, notes_profile):
    fidx = feature_index(fdata)
    errs = check_formats(fdata, core, profiles)
    if errs:
        return errs
    errs += check_core(core, fidx)
    if errs:
        return errs
    for p in profiles.values():
        errs += check_profile(core, p, fdata, fidx)
    if errs:
        return errs
    errs += check_notes(notes, core, profiles[notes_profile])
    errs += check_global_ids(core, notes, fdata)
    return errs
