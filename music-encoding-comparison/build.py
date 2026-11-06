#!/usr/bin/env python3
"""Render comparison.json to a standalone, offline HTML report. Python 3 stdlib only."""
import argparse
import csv
import html
import io
import json
from pathlib import Path

def esc(s): return html.escape(str(s), quote=True)

def validate(d):
    assert d['schema_version']=='1.0.0', 'Unsupported schema version'
    formats=[f['id'] for f in d['formats']]
    assert len(formats)==len(set(formats)) and len(formats)==4
    ids=[r['id'] for r in d['features']]
    assert len(ids)==len(set(ids)), 'Duplicate feature IDs'
    for r in d['features']:
        assert r['category'] in d['categories']
        assert set(r['cells'])==set(formats)
        for c in r['cells'].values():
            assert c['status'] in d['statuses']
            assert c['evidence'] in d['methodology']['evidence']
            assert c['summary'] and c['mechanism'] and c['sources']
            assert type(c['tested']) is bool
            assert all(x in d['sources'] for x in c['sources'])
    for case in d['cases']:
        assert all(x in ids for x in case['rows'])
    for test in d['test_plan']:
        assert all(x in ids for x in test['features'])
    assert all(s['url'].startswith('https://') for s in d['sources'].values())

def render(d, template):
    validate(d)
    source_numbers={k:i+1 for i,k in enumerate(d['sources'])}
    def refs(ids):
        return '<ul class="citations">'+''.join(
          f'<li><a href="{esc(d["sources"][s]["url"])}" target="_blank" rel="noopener noreferrer">[{source_numbers[s]}] {esc(d["sources"][s]["title"])}</a></li>' for s in ids)+'</ul>'
    profiles=''.join(f'<article class="profile"><div class="eyebrow">{esc(f["role"])}</div><h3>{esc(f["short"])}</h3><p>{esc(f["description"])}</p><small>{esc(f["baseline"])}</small>{refs(f["sources"])}</article>' for f in d['formats'])
    legend=''.join(f'<div><span class="badge {k}">{esc(v["label"])}</span><p>{esc(v["description"])}</p></div>' for k,v in d['statuses'].items())
    row_html=[]
    for i,r in enumerate(d['features']):
        cells=[]
        for f in d['formats']:
            c=r['cells'][f['id']]
            detail=f'<p><b>Mechanism.</b> {esc(c["mechanism"])}</p>'
            if c['caveat']: detail+=f'<p class="caveat"><b>Condition.</b> {esc(c["caveat"])}</p>'
            if c['workaround']: detail+=f'<p><b>Workaround.</b> {esc(c["workaround"])}</p>'
            if c['profile']: detail+=f'<p><b>Profile.</b> {esc(c["profile"])}</p>'
            testing='Empirical test recorded' if c['tested'] else 'No empirical test'
            detail+=f'<p class="evidence"><b>{esc(c["evidence"].capitalize())}</b>; {testing}</p>'+refs(c['sources'])
            tip=' '.join(c[k] for k in ['mechanism','caveat','workaround'] if c[k])
            cells.append(f'<td data-format="{f["id"]}"><details class="cell-detail"><summary title="{esc(tip)}"><span class="badge {c["status"]}">{esc(d["statuses"][c["status"]]["label"])}</span><span class="cell-summary">{esc(c["summary"])}</span><span class="detail-hint">Details & sources</span></summary><div class="cell-body">{detail}</div></details></td>')
        row_html.append(f'<tr id="feature-{esc(r["id"])}" data-id="{esc(r["id"])}" data-order="{i}"><th scope="row"><small>{esc(r["category"])}</small><a class="row-anchor" href="#feature-{esc(r["id"])}">{esc(r["feature"])}</a><p>{esc(r["question"])}</p></th>{"".join(cells)}</tr>')
    case_html=[]
    for c in d['cases']:
        timeline=''
        if 'timeline' in c:
            marks=''
            for y,name,steps,color in [(44,'3/4',c['timeline']['three'],'#216959'),(100,'4/4',c['timeline']['four'],'#9b5338')]:
                marks+=f'<text x="12" y="{y+5}" class="line-label">{name}</text><path d="M76 {y}H736" stroke="{color}" stroke-width="2"/>'
                for n in steps:
                    x=76+n*55
                    marks+=f'<path d="M{x} {y-12}V{y+12}" stroke="{color}" stroke-width="3"/>'
            ticks=''.join(f'<text x="{76+n*55}" y="142" text-anchor="middle">{n}</text>' for n in range(13))
            timeline=f'<figure class="timeline"><svg viewBox="0 0 775 160" role="img" aria-label="3/4 boundaries at 0, 3, 6, 9, 12 quarter notes; 4/4 boundaries at 0, 4, 8, 12.">{marks}{ticks}</svg><figcaption>Elapsed quarter notes; shared pulse; common boundary at 12</figcaption></figure>'
        snippets=''.join(f'<details class="snippet"><summary>{esc(s["format"])}</summary><pre><code>{esc(s["code"])}</code></pre><p>{esc(s["note"])}</p></details>' for s in c['snippets'])
        related=''.join(f'<a class="chip" href="#feature-{esc(r)}">{esc(next(x["feature"] for x in d["features"] if x["id"]==r))}</a>' for r in c['rows'])
        case_html.append(f'<article class="case" id="{c["id"]}"><div class="eyebrow">Worked comparison</div><h3>{esc(c["title"])}</h3><p class="lede">{esc(c["subtitle"])}</p><p>{esc(c["introduction"])}</p>{timeline}<ol>{"".join(f"<li>{esc(n)}</li>" for n in c["notes"])}</ol>{snippets}{refs(c["sources"])}<div class="chips">{related}</div></article>')
    sources=''.join(f'<tr><td>[{source_numbers[k]}]</td><td><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])}</a><small>{esc(s["url"])}</small></td><td>{esc(s["accessed"])}</td></tr>' for k,s in d['sources'].items())
    tests=''.join(f'<tr><th scope="row">{esc(t["title"])}</th><td>{esc(t["acceptance"])}</td><td>Not run</td></tr>' for t in d['test_plan'])
    replacements={
      'TITLE':esc(d['title']), 'DATE':esc(d['methodology']['date']), 'FEATURE_COUNT':str(len(d['features'])),
      'ASSESSMENT_COUNT':str(len(d['features'])*len(d['formats'])), 'SOURCE_COUNT':str(len(d['sources'])),
      'PROFILES':profiles, 'LEGEND':legend, 'ROWS':'\n'.join(row_html), 'CASES':'\n'.join(case_html),
      'SOURCES':sources, 'TESTS':tests,
      'ASSUMPTIONS':''.join(f'<li>{esc(x)}</li>' for x in d['methodology']['assumptions']),
      'COVERAGE':esc(d['methodology']['coverage_limits']),
      'EVIDENCE':''.join(f'<dt>{esc(k.capitalize())}</dt><dd>{esc(v)}</dd>' for k,v in d['methodology']['evidence'].items()),
      'CATEGORIES':''.join(f'<option>{esc(x)}</option>' for x in d['categories']),
      'FORMATS':''.join(f'<label><input type="checkbox" value="{f["id"]}" checked> {esc(f["short"])}</label>' for f in d['formats']),
      'FORMAT_OPTIONS':''.join(f'<option value="{f["id"]}">{esc(f["short"])}</option>' for f in d['formats']),
      'HEADERS':''.join(f'<th scope="col" data-format="{f["id"]}">{esc(f["short"])}<small>{esc(f["role"])}</small></th>' for f in d['formats']),
      'STATUS_OPTIONS':''.join(f'<option value="{k}">{esc(v["label"])}</option>' for k,v in d['statuses'].items()),
      'DATA':json.dumps(d,ensure_ascii=False).replace('<','\\u003c').replace('&','\\u0026'),
    }
    for k,v in replacements.items(): template=template.replace('{{'+k+'}}',v)
    return template

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data',type=Path,default=Path(__file__).with_name('comparison.json'))
    ap.add_argument('--template',type=Path,default=Path(__file__).with_name('template.html'))
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('music-encoding-comparison.html'))
    args=ap.parse_args()
    d=json.loads(args.data.read_text(encoding='utf-8'))
    args.output.write_text(render(d,args.template.read_text(encoding='utf-8')),encoding='utf-8')
    print(f'Built {args.output.name}: {len(d["features"])} features, {len(d["sources"])} sources')
if __name__=='__main__': main()
