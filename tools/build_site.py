#!/usr/bin/env python3
"""Build one stand-alone HTML page from the project's Markdown documents.

Usage:  python3 tools/build_site.py
Input:  docs/*.md (run tools/build.py first), build/*.json|csv
Output: site/index.html  (no external files, fonts, scripts or network calls: host it anywhere)

Cross-document links become in-page anchors, rule and note IDs link to their
definitions, local images are embedded, and the machine-readable files are
embedded as downloads. Output is deterministic (no timestamps).
"""
import base64
import html
import mimetypes
import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = [  # (file, section id, nav label, deepest heading level shown in the contents)
    ("start-here.md", "doc-start", "Start here", 2),
    ("principles-framework.md", "doc-framework", "Principles framework", 2),
    ("principles-rules.md", "doc-rules", "Rules table", 3),
    ("format-support.md", "doc-formats", "Format support", 2),
    ("notes-for-transcribers.md", "doc-notes", "Notes for Transcribers", 2),
    ("glossary.md", "doc-glossary", "Glossary", 1),
]
DOWNLOADS = [("principles.json", "application/json"), ("principles.csv", "text/csv"), ("notes.json", "application/json"),
             ("formats.json", "application/json"), ("formats.csv", "text/csv")]
FILE_TO_SECTION = {f: s for f, s, _, _ in DOCS}
STRENGTH = {"MUST": "must", "SHOULD": "should", "MAY": "may", "OFF": "off"}


def data_uri(path, mime=None):
    mime = mime or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def render(md_file, prefix):
    def slug(value, sep):
        s = re.sub(r"[^\w\s-]", "", value.lower()).strip()
        return prefix + "-" + re.sub(r"[\s_-]+", sep, s)
    md = markdown.Markdown(extensions=["tables", "toc", "sane_lists"],
                           extension_configs={"toc": {"slugify": slug, "toc_depth": "1-3"}})
    body = md.convert((ROOT / "docs" / md_file).read_text(encoding="utf-8"))
    return body, md.toc_tokens


def fix_links(body, ids, feats=frozenset()):
    def href(m):
        target, frag = m.group(1), m.group(3)
        if target in FILE_TO_SECTION:
            return f'href="#{frag or FILE_TO_SECTION[target]}"'
        return m.group(0)
    body = body.replace('href="../site/formats.html"', 'href="formats.html"')
    body = re.sub(r'href="([\w.-]+\.md)(#([^"]+))?"', href, body)
    body = re.sub(r'href="([\w.-]+\.md)#', 'href="#', body)

    def img(m):  # embed local images
        src = m.group(1)
        p = (ROOT / "docs" / src).resolve()
        return f'src="{data_uri(p)}"' if p.is_file() and not src.startswith(("http", "data:")) else m.group(0)
    body = re.sub(r'src="([^"]+)"', img, body)

    # link `rule.id` / `area.slug` code spans to their definitions (not inside links or headings)
    out, depth_a, depth_h, toks = [], 0, 0, re.split(r"(<[^>]+>)", body)
    i = 0
    while i < len(toks):
        t = toks[i]
        if re.match(r"<a[ >]", t) and not t.endswith("></a>"):
            depth_a += 1
        elif t == "</a>":
            depth_a = max(0, depth_a - 1)
        elif re.match(r"<h[1-6][ >]", t):
            depth_h += 1
        elif re.match(r"</h[1-6]>", t):
            depth_h = max(0, depth_h - 1)
        if (t == "<code>" and i + 2 < len(toks) and (toks[i + 1] in ids or toks[i + 1] in feats) and toks[i + 2] == "</code>"
                and not depth_a and not depth_h and not (out and out[-1] == "</a>")):
            target = f"formats.html#feature-{toks[i + 1]}" if toks[i + 1] in feats else f"#{toks[i + 1]}"
            out.append(f'<a class="ref" href="{target}"><code>{toks[i + 1]}</code></a>')
            i += 3
            continue
        out.append(t)
        i += 1
    body = "".join(out)
    # let IDs wrap only after a dot or hyphen
    body = re.sub(r"<code>([^<]+)</code>", lambda m: "<code>" + re.sub(r"([.-])", r"\1<wbr>", m.group(1)) + "</code>" if m.group(1) in ids or m.group(1) in feats else m.group(0), body)
    body = re.sub(r"<td>(MUST|SHOULD|MAY|OFF)</td>", lambda m: f'<td><span class="st st-{STRENGTH[m.group(1)]}">{m.group(1)}</span></td>', body)
    return body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")


def nav_html(tokens_by_doc):
    def items(toks, maxlvl):
        s = ""
        for t in toks:
            if t["level"] > maxlvl:
                continue
            kids = items(t["children"], maxlvl)
            s += f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a>{"<ul>" + kids + "</ul>" if kids else ""}</li>'
        return s
    parts = []
    for (f, sid, label, maxlvl), toks in zip(DOCS, tokens_by_doc):
        kids = items(toks[0]["children"], maxlvl) if toks else ""
        parts.append(f'<li class="doc"><a href="#{sid}">{html.escape(label)}</a>{"<ul>" + kids + "</ul>" if kids else ""}</li>')
    return "<ul>" + "".join(parts) + "</ul>"


CSS = """
:root{--ink:#161c27;--muted:#566073;--paper:#fff;--tint:#f1f3f7;--line:#d3d9e3;--accent:#2b3a9f;--code:#e9ecf4;--mark:#fff3b8;
--serif:Charter,"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;--sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root{--ink:#e6e9f0;--muted:#9aa4b8;--paper:#12151c;--tint:#1a1f29;--line:#2c3443;--accent:#9fb0ff;--code:#252c3a;--mark:#4a4320}}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:1rem}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);font:1.0625rem/1.65 var(--serif)}
a{color:var(--accent);text-underline-offset:.15em}a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
header.top{padding:2.5rem 1.25rem 0;max-width:76rem;margin:0 auto}
.brand{font:700 clamp(1.9rem,4.2vw,3rem)/1.1 var(--serif);margin:0;letter-spacing:-.01em}
.staff{height:34px;margin:1rem 0 .75rem;max-width:34rem;background:repeating-linear-gradient(to bottom,var(--ink) 0 1.5px,transparent 1.5px 8px);background-size:100% 34px;background-repeat:no-repeat;opacity:.75}
.meta{font:.9rem var(--sans);color:var(--muted);margin:0 0 .4rem}.meta a{color:inherit}
.layout{display:grid;grid-template-columns:minmax(0,1fr);gap:0 3rem;max-width:76rem;margin:0 auto;padding:1rem 1.25rem 4rem}
@media (min-width:62rem){.layout{grid-template-columns:17rem minmax(0,1fr)}}
nav.toc{font:.88rem/1.45 var(--sans);align-self:start;border:1px solid var(--line);border-radius:6px;background:var(--tint);padding:.6rem .9rem;margin-bottom:1.5rem}
@media (min-width:62rem){nav.toc{position:sticky;top:1rem;max-height:calc(100vh - 2rem);overflow:auto;margin-bottom:0}}
nav.toc summary{cursor:pointer;font-weight:600}nav.toc ul{list-style:none;margin:.3rem 0;padding-left:.8rem}nav.toc>details>ul{padding:0}
nav.toc li.doc{margin-top:.6rem}nav.toc li.doc>a{font-weight:600}nav.toc a{text-decoration:none;color:var(--ink)}nav.toc a:hover{text-decoration:underline}
main section{padding-top:.5rem;margin-bottom:3.5rem}
main section+section{border-top:1px solid var(--line);padding-top:2.5rem}
h1,h2,h3{font-family:var(--serif);line-height:1.25}h1{font-size:2rem;margin:.2rem 0 .8rem}h2{font-size:1.45rem;margin:2.2rem 0 .6rem}h3{font-size:1.15rem;margin:1.8rem 0 .4rem}
p,li{max-width:44rem}p{margin:.7rem 0}
code{font:.86em var(--mono);background:var(--code);padding:.08em .3em;border-radius:3px;overflow-wrap:anywhere}td code{overflow-wrap:normal}a.ref{text-decoration:none}a.ref:hover code{text-decoration:underline}
.tw{overflow-x:auto;margin:1rem 0;border:1px solid var(--line);border-radius:6px}
table{border-collapse:collapse;width:100%;font:.9rem/1.5 var(--sans)}th,td{padding:.5rem .7rem;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:0}th{background:var(--tint);font-weight:600;white-space:nowrap}td:first-child{min-width:7rem}
.st{font:600 .75rem var(--sans);padding:.1rem .45rem;border-radius:3px;border:1.5px solid var(--ink);white-space:nowrap}
.st-must{background:var(--ink);color:var(--paper)}.st-should{background:transparent}.st-may{border-style:dashed}.st-off{border-style:dotted;color:var(--muted);border-color:var(--muted)}
tr:has(a:target){background:var(--mark)}p:has(>a:target)+h3{background:var(--mark)}
img{max-width:100%;height:auto}
footer{font:.85rem var(--sans);color:var(--muted);border-top:1px solid var(--line);padding-top:1rem}
@media print{nav.toc{display:none}.layout{display:block}.tw{overflow:visible}a{color:inherit}}
"""


def main():
    core = yaml.safe_load((ROOT / "core" / "principles.yaml").read_text(encoding="utf-8"))
    notes = yaml.safe_load((ROOT / "notes" / "registry.yaml").read_text(encoding="utf-8"))
    profiles = sorted(p.stem for p in (ROOT / "profiles").glob("*.yaml"))
    feats = []
    for f in (ROOT / "formats" / "features").glob("*.yaml"):
        feats += [x["id"] for x in yaml.safe_load(f.read_text(encoding="utf-8"))]
    ids = {r["id"] for r in core["rules"]} | {n["id"] for n in notes["notes"]}
    feats = set(feats)
    sections, tokens = [], []
    for f, sid, label, _ in DOCS:
        body, toks = render(f, sid.replace("doc-", ""))
        tokens.append(toks)
        sections.append(f'<section id="{sid}">{fix_links(body, ids, feats)}</section>')
    dl = " &middot; ".join(f'<a download="{n}" href="{data_uri(ROOT / "build" / n, m)}">{n}</a>' for n, m in DOWNLOADS)
    ver = core["principles_version"]
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Transcription Principles and Notes for Transcribers, version {ver}</title>
<meta name="description" content="Rules for an exact, citable digital transcription of a printed score, for editorial projects and others to build on.">
<style>{CSS}</style></head><body>
<header class="top"><p class="brand">Transcription Principles and Notes</p><div class="staff" aria-hidden="true"></div>
<p class="meta">Scores of Scores &middot; version {ver} &middot; profiles {', '.join('<code>' + x + '</code>' for x in profiles)} &middot; <a href="formats.html">Format reader</a></p>
<p class="meta">Data: {dl}</p></header>
<div class="layout"><nav class="toc" aria-label="Contents"><details open><summary>Contents</summary>{nav_html(tokens)}</details></nav>
<main>{''.join(sections)}
<footer>Generated by <code>tools/build_site.py</code> from the Markdown in <code>docs/</code>. This page is a single file with no external dependencies and can be hosted anywhere.</footer></main></div>
<script>if(matchMedia("(max-width:61.99rem)").matches){{document.querySelector("nav.toc details").open=false}}</script>
</body></html>
"""
    (ROOT / "site").mkdir(exist_ok=True)
    (ROOT / "site" / "index.html").write_text(page, encoding="utf-8")
    print(f"OK: wrote site/index.html ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
