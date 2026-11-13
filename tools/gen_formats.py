"""Render the formats data to a stand-alone HTML reader, a JSON file and a CSV file."""
import csv
import html
import io
import json

from common import ROOT


def esc(s):
    return html.escape(str(s), quote=True)


def assemble(d):
    """The assembled dataset embedded in the reader and written to build/formats.json."""
    out = {k: d[k] for k in ("formats_version", "title", "methodology", "formats", "statuses", "sources", "cases")}
    out["categories"] = [c["title"] for c in d["categories"]]
    out["features"] = [{k: v for k, v in f.items()} for f in d["features"]]
    out["test_plan"] = [dict(x, status=("not_run" if not any(r != "not_run" for r in x.get("results", {}).values()) else "run"))
                        for x in d["fixtures"]]
    return out


def render(d, template):
    D = assemble(d)
    numbers = {k: i + 1 for i, k in enumerate(D["sources"])}

    def refs(ids):
        return '<ul class="citations">' + "".join(
            f'<li><a href="{esc(D["sources"][s]["url"])}" target="_blank" rel="noopener noreferrer">[{numbers[s]}] {esc(D["sources"][s]["title"])}</a></li>'
            for s in ids) + "</ul>"

    profiles = "".join(
        f'<article class="profile"><div class="eyebrow">{esc(f["role"])}</div><h3>{esc(f["short"])}</h3><p>{esc(f["description"])}</p>'
        f'<small>{esc(f["baseline"])}; version {esc(f["version"])}</small>{refs(f["sources"])}</article>' for f in D["formats"])
    legend = "".join(f'<div><span class="badge {k}">{esc(v["label"])}</span><p>{esc(v["description"])}</p></div>' for k, v in D["statuses"].items())
    rows = []
    for i, r in enumerate(D["features"]):
        cells = []
        for f in D["formats"]:
            c = r["cells"][f["id"]]
            detail = f'<p><b>Mechanism.</b> {esc(c["mechanism"])}</p>'
            if c["caveat"]:
                detail += f'<p class="caveat"><b>Condition.</b> {esc(c["caveat"])}</p>'
            if c["workaround"]:
                detail += f'<p><b>Workaround.</b> {esc(c["workaround"])}</p>'
            if c["subset"]:
                detail += f'<p><b>Subset.</b> {esc(c["subset"])}</p>'
            testing = "Empirical test recorded" if c["tested"] else "No empirical test"
            detail += f'<p class="evidence"><b>{esc(c["evidence"].capitalize())}</b>; {testing}</p>' + refs(c["sources"])
            tip = " ".join(c[k] for k in ("mechanism", "caveat", "workaround") if c[k])
            cells.append(
                f'<td data-format="{f["id"]}"><details class="cell-detail"><summary title="{esc(tip)}"><span class="badge {c["status"]}">{esc(D["statuses"][c["status"]]["label"])}</span>'
                f'<span class="cell-summary">{esc(c["summary"])}</span><span class="detail-hint">Details &amp; sources</span></summary><div class="cell-body">{detail}</div></details></td>')
        rule_line = ('<p class="rules">Rules: ' + ", ".join(esc(x) for x in r["rules"]) + "</p>") if r["rules"] else ""
        rows.append(f'<tr id="feature-{esc(r["id"])}" data-id="{esc(r["id"])}" data-order="{i}"><th scope="row"><small>{esc(r["category"])}</small>'
                    f'<a class="row-anchor" href="#feature-{esc(r["id"])}">{esc(r["feature"])}</a><p>{esc(r["question"])}</p>{rule_line}</th>{"".join(cells)}</tr>')
    cases = []
    for c in D["cases"]:
        timeline = ""
        if "timeline" in c:
            marks = ""
            for y, name, steps, color in [(44, "3/4", c["timeline"]["three"], "#216959"), (100, "4/4", c["timeline"]["four"], "#9b5338")]:
                marks += f'<text x="12" y="{y + 5}" class="line-label">{name}</text><path d="M76 {y}H736" stroke="{color}" stroke-width="2"/>'
                for n in steps:
                    x = 76 + n * 55
                    marks += f'<path d="M{x} {y - 12}V{y + 12}" stroke="{color}" stroke-width="3"/>'
            ticks = "".join(f'<text x="{76 + n * 55}" y="142" text-anchor="middle">{n}</text>' for n in range(13))
            timeline = (f'<figure class="timeline"><svg viewBox="0 0 775 160" role="img" aria-label="3/4 boundaries at 0, 3, 6, 9, 12 quarter notes; 4/4 boundaries at 0, 4, 8, 12.">'
                        f'{marks}{ticks}</svg><figcaption>Elapsed quarter notes; shared pulse; common boundary at 12</figcaption></figure>')
        snippets = "".join(f'<details class="snippet"><summary>{esc(s["format"])}</summary><pre><code>{esc(s["code"])}</code></pre><p>{esc(s["note"])}</p></details>' for s in c["snippets"])
        names = {x["id"]: x["feature"] for x in D["features"]}
        related = "".join(f'<a class="chip" href="#feature-{esc(r)}">{esc(names[r])}</a>' for r in c["rows"])
        cases.append(f'<article class="case" id="{c["id"]}"><div class="eyebrow">Worked comparison</div><h3>{esc(c["title"])}</h3><p class="lede">{esc(c["subtitle"])}</p>'
                     f'<p>{esc(c["introduction"])}</p>{timeline}<ol>{"".join(f"<li>{esc(n)}</li>" for n in c["notes"])}</ol>{snippets}{refs(c["sources"])}<div class="chips">{related}</div></article>')
    sources = "".join(f'<tr><td>[{numbers[k]}]</td><td><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])}</a><small>{esc(s["url"])}</small></td><td>{esc(s["accessed"])}</td></tr>'
                      for k, s in D["sources"].items())
    tests = "".join(f'<tr><th scope="row">{esc(t["title"])}</th><td>{esc(t["acceptance"])}</td><td>{"Not run" if t["status"] == "not_run" else "Run"}</td></tr>' for t in D["test_plan"])
    rep = {
        "TITLE": esc(D["title"]), "DATE": esc(D["methodology"]["date"]), "FEATURE_COUNT": str(len(D["features"])),
        "ASSESSMENT_COUNT": str(len(D["features"]) * len(D["formats"])), "SOURCE_COUNT": str(len(D["sources"])),
        "PROFILES": profiles, "LEGEND": legend, "ROWS": "\n".join(rows), "CASES": "\n".join(cases), "SOURCES": sources, "TESTS": tests,
        "ASSUMPTIONS": "".join(f"<li>{esc(x)}</li>" for x in D["methodology"]["assumptions"]),
        "COVERAGE": esc(D["methodology"]["coverage_limits"]),
        "EVIDENCE": "".join(f"<dt>{esc(k.capitalize())}</dt><dd>{esc(v)}</dd>" for k, v in D["methodology"]["evidence"].items()),
        "CATEGORIES": "".join(f"<option>{esc(x)}</option>" for x in D["categories"]),
        "FORMATS": "".join(f'<label><input type="checkbox" value="{f["id"]}" checked> {esc(f["short"])}</label>' for f in D["formats"]),
        "FORMAT_OPTIONS": "".join(f'<option value="{f["id"]}">{esc(f["short"])}</option>' for f in D["formats"]),
        "HEADERS": "".join(f'<th scope="col" data-format="{f["id"]}">{esc(f["short"])}<small>{esc(f["role"])}</small></th>' for f in D["formats"]),
        "STATUS_OPTIONS": "".join(f'<option value="{k}">{esc(v["label"])}</option>' for k, v in D["statuses"].items()),
        "DATA": json.dumps(D, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026"),
    }
    for k, v in rep.items():
        template = template.replace("{{" + k + "}}", v)
    return template


def csv_text(d):
    D = assemble(d)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["Feature ID", "Category", "Feature", "Format", "Capability", "Summary", "Mechanism", "Condition", "Workaround",
                "Evidence", "Subset", "Empirically tested", "Linked rules", "Sources"])
    for f in D["features"]:
        for fm in D["formats"]:
            c = f["cells"][fm["id"]]
            w.writerow([f["id"], f["category"], f["feature"], fm["short"], D["statuses"][c["status"]]["label"], c["summary"], c["mechanism"],
                        c["caveat"], c["workaround"], c["evidence"], c["subset"], str(c["tested"]).lower(), " ".join(f["rules"]),
                        " | ".join(D["sources"][s]["url"] for s in c["sources"])])
    return "\ufeff" + buf.getvalue()


def gen_formats(d):
    template = (ROOT / "tools" / "templates" / "formats.html").read_text(encoding="utf-8")
    page = render(d, template)
    (ROOT / "site").mkdir(exist_ok=True)
    (ROOT / "site" / "formats.html").write_text(page, encoding="utf-8")
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "formats.json").write_text(json.dumps(assemble(d), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "build" / "formats.csv").write_text(csv_text(d), encoding="utf-8", newline="")
    return len(d["features"])
