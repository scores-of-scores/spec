"""Fill the generated tables in paper/paper.md from the profiles, rules and formats data."""
from common import feature_index, mark_status
from gen_docs import inject


def _short(fdata, fid):
    return next(f["short"] for f in fdata["formats"] if f["id"] == fid)


def _enc(p, fdata):
    e = p["scope"]["encoding"]
    f = next(x for x in fdata["formats"] if x["id"] == e["format"])
    return f"{f['short']} ({f['version']})"


def positions_table(core, profiles, fdata, order):
    fidx = feature_index(fdata)
    rules = {r["id"]: r for r in core["rules"]}
    norms = [r["id"] for r in core["rules"] if r["id"].startswith("normalise.") and r["id"] != "normalise.closed-list"]
    P = [profiles[i] for i in order]

    def correction(p):
        s = p["strengths"]
        if s["correct.in-place"] != "OFF":
            return f"Corrected in the transcription ({s['correct.in-place']}), and recorded"
        if s["correct.layer"] != "OFF":
            return f"Kept as printed; the correction is recorded in a separate layer ({s['correct.layer']})"
        return "Kept as printed"

    def prec(p):
        for x in p["precedence"]:
            if x["over"] == "stance.meaning-over-appearance" and x["under"] == "stance.faithful-reading":
                return f"Meaning over appearance wins: {x['scope'].rstrip('.')}"
        return "Not stated"

    def status(p):
        if p["status"] == "adopted":
            return "Adopted"
        n = len(set(p["strengths"]) - set(p.get("basis", {})))
        return f"Draft: {len(p['strengths']) - n} of {len(p['strengths'])} strengths documented, {n} core defaults unconfirmed"

    rows = [
        ("Clear source error (`correct.error-test`)", correction),
        ("Source error that is not clear", lambda p: "Kept as printed; observation recorded" if p["strengths"]["read.preserve-errors"] != "OFF" else "Not stated"),
        ("Test for \"clear\"", lambda p: f"The same core test (`correct.error-test`, {p['strengths']['correct.error-test']})"),
        ("Presentation normalisations", lambda p: f"{sum(p['strengths'][n] != 'OFF' for n in norms)} of {len(norms)} registered normalisations permitted, {sum(p['strengths'][n] == 'MUST' for n in norms)} always applied"),
        ("Format of the version of record", lambda p: _enc(p, fdata)),
        ("Marks left out because the format cannot express them", lambda p: ", ".join(m["title"].lower() for m in mark_status(core, p, fidx) if m["treatment"] == "unsupported") or "None"),
        ("Highest-ranked aim", lambda p: rules[p["aim_order"][0]["rule"]]["title"] + (f" ({p['aim_order'][0]['note'].rstrip('.').lower()})" if p["aim_order"][0].get("note") and not p["aim_order"][0]["note"].startswith("Applies") else "")),
        ("Where meaning and faithful reading conflict", prec),
        ("Status of the profile", status),
    ]
    L = ["| Choice | " + " | ".join(p["title"] for p in P) + " |", "|---|" + "---|" * len(P)]
    for name, fn in rows:
        L.append(f"| {name} | " + " | ".join(fn(p) for p in P) + " |")
    return "\n".join(L)


def examples_table(fdata, order, profiles):
    L = ["| Example | Rules | " + " | ".join(profiles[i]["title"] for i in order) + " |", "|---|---|" + "---|" * len(order)]
    for x in fdata["fixtures"]:
        if x.get("paper"):
            L.append(f"| {x['title']} (`{x['id']}`) | " + ", ".join(f"`{r}`" for r in x["rules"]) + " | " + " | ".join(x["positions"][i] for i in order) + " |")
    return "\n".join(L)


def formats_table(core, fdata):
    fidx = feature_index(fdata)
    used = []
    for x in fdata["fixtures"]:
        if x.get("paper"):
            for f in x["features"]:
                if f not in used:
                    used.append(f)
    st = {k: v["label"] for k, v in fdata["statuses"].items()}
    tag = {"documented": "", "inference": " (inferred)", "unverified": " (unverified)"}
    L = ["| Feature | " + " | ".join(f["short"] for f in fdata["formats"]) + " |", "|---|" + "---|" * len(fdata["formats"])]
    for f in used:
        cells = " | ".join(st[fidx[f]["cells"][x["id"]]["status"]] + tag[fidx[f]["cells"][x["id"]]["evidence"]] for x in fdata["formats"])
        L.append(f"| `{f}`: {fidx[f]['feature']} | {cells} |")
    return "\n".join(L)


def state_box(core, profiles, fdata, notes):
    doms = {}
    for r in core["rules"]:
        doms[r["id"].split(".")[0]] = doms.get(r["id"].split(".")[0], 0) + 1
    linked = sum(1 for f in fdata["features"] if f["rules"])
    tested = sum(1 for f in fdata["features"] for c in f["cells"].values() if c["tested"])
    return "\n".join([
        f"- Principles version {core['principles_version']}: {len(core['rules'])} rules (" + ", ".join(f"{n} {d}" for d, n in doms.items()) + ").",
        f"- Profiles: " + ", ".join(f"`{p}` ({v['status']})" for p, v in profiles.items()) + ".",
        f"- Notes for the Scores of Scores profile: {len(notes['notes'])}.",
        f"- Formats data {fdata['formats_version']}: {len(fdata['features'])} features in four formats ({len(fdata['features']) * 4} assessments), {linked} linked to a rule, {len(fdata['sources'])} primary sources.",
        f"- Fixtures: {len(fdata['fixtures'])}, of which {sum(1 for x in fdata['fixtures'] if x.get('paper'))} are worked examples in this paper. Assessments with a recorded test: {tested}.",
    ])


def gen_paper(core, profiles, fdata, notes):
    order = ["openscore-2026-11", "sos-2026-11"]
    path = "paper/paper.md"
    inject(path, "two-positions", positions_table(core, profiles, fdata, order))
    inject(path, "worked-examples", examples_table(fdata, order, profiles))
    inject(path, "paper-formats", formats_table(core, fdata))
    inject(path, "state-box", state_box(core, profiles, fdata, notes))
