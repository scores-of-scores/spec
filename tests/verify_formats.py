#!/usr/bin/env python3
"""Data, HTML and actual JavaScript-model checks. Does not test music applications or browser layout."""
import copy
import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from common import load,load_formats,link_formats
import gen_formats
class Parse(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.hrefs=[];self.external_assets=[];self.scripts=[];self.current=None;self.script_attrs={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.hrefs.append(a.get('href',''))
        if tag in ('script','img','link') and any(k in a for k in ('src','href')):self.external_assets.append(a)
        if tag=='script':self.current='';self.script_attrs=a
    def handle_data(self,s):
        if self.current is not None:self.current+=s
    def handle_endtag(self,tag):
        if tag=='script' and self.current is not None:
            self.scripts.append((self.script_attrs,self.current));self.current=None

def main():
    core=load(ROOT/'core'/'principles.yaml')
    raw=link_formats(load_formats(),core)
    data=json.loads(json.dumps(gen_formats.assemble(raw)))
    template=(ROOT/'tools'/'templates'/'formats.html').read_text()
    output=gen_formats.render(raw,template)
    assert output==(ROOT/'site'/'formats.html').read_text(),'HTML is stale; run tools/build.py'
    assert not re.search(r'\{\{[A-Z_]+\}\}',output),'Unexpanded placeholder'
    p=Parse();p.feed(output)
    assert len(p.ids)==len(set(p.ids)),'Duplicate HTML IDs'
    assert not p.external_assets,'HTML must work without external assets'
    assert all(h[1:] in p.ids for h in p.hrefs if h.startswith('#')),'Broken internal anchor'
    assert 'index.html' in p.hrefs,'Missing link back to the rules and Notes page'
    embedded=next(s for a,s in p.scripts if a.get('type')=='application/json')
    assert json.loads(embedded)==data,'Embedded source differs from canonical JSON'
    assert sum(i.startswith('feature-') for i in p.ids)==len(data['features'])
    assert len(data['features'])>0 and sum(len(r['cells']) for r in data['features'])==4*len(data['features'])
    assert all(not c['tested'] for r in data['features'] for c in r['cells'].values()),'No fixture has a result, so no cell may be tested'
    linked=[f for f in data['features'] if f['rules']]
    assert linked and all('rule-linked' in f['tags'] for f in linked),'Rule-linked features must carry the tag'
    assert all(f['id'].startswith('fmt.') for f in data['features'])
    assert all('subset' in c and 'profile' not in c for r in data['features'] for c in r['cells'].values())
    assert data['cases'][2]['timeline']['three']==[0,3,6,9,12]
    assert data['cases'][2]['timeline']['four']==[0,4,8,12]
    for c in data['cases']:
        for snippet in c['snippets']:
            if snippet['code'].startswith('<'): ET.fromstring(snippet['code'])
    hostile=copy.deepcopy(raw)
    hostile['features'][0]['cells']['krn']['summary']='</script><img src=x onerror=alert(1)>'
    hostile_html=gen_formats.render(dict(raw,features=hostile['features']),template)
    hp=Parse();hp.feed(hostile_html)
    assert not hp.external_assets and len(hp.scripts)==2,'Data was not safely escaped'
    code=next(s for a,s in p.scripts if not a.get('type'))
    node=shutil.which('node')
    assert node,'Node.js is needed only for these JavaScript-model checks'
    pure=code[code.index('const ALL_FORMATS='):code.index('function apply(){')]
    pure=pure.replace("const records=new Map(DATA.features.map((f,i)=>[f.id,{feature:f,index:i,node:$('feature-'+f.id)}]));", "const records=new Map(DATA.features.map((f,i)=>[f.id,{feature:f,index:i}]));")
    csv=code[code.index('function csvText(){'):code.index("$('download-csv').addEventListener")]
    test=r'''
const assert=require('assert');
const base={q:'',category:'',status:'',evidence:'',matchFormat:'',sort:'theme',visible:[...ALL_FORMATS]};
const find=id=>DATA.features.find(r=>r.id===id);
assert.strictEqual(DATA.features.filter(f=>matches(f,base)).length,DATA.features.length);
assert(matches(find('fmt.independent-bars'),{...base,q:'12 quarters'}),'Search must include detailed notes');
assert(matches(find('fmt.editorial-accidentals'),{...base,q:'RDF signifier'}));
assert(!matches(find('fmt.independent-bars'),{...base,q:'no-such-word'}));
assert(matches(find('fmt.independent-bars'),{...base,status:'workaround',matchFormat:'musescore'}));
assert(!matches(find('fmt.independent-bars'),{...base,status:'direct',matchFormat:'musescore'}));
assert(!matches(find('fmt.independent-bars'),{...base,status:'workaround',visible:['mei']}));
const synthetic=JSON.parse(JSON.stringify(find('fmt.independent-bars')));
synthetic.cells.krn.status='direct';synthetic.cells.krn.evidence='documented';
synthetic.cells.mei.status='unknown';synthetic.cells.mei.evidence='unverified';
assert(!matches(synthetic,{...base,status:'direct',evidence:'unverified',visible:['krn','mei']}),'Status and evidence must match the same cell');
const voiceRows=DATA.features.filter(f=>matches(f,{...base,category:'Voices & staves'}));
assert(voiceRows.some(f=>f.id==='fmt.two-voices')&&voiceRows.every(f=>f.category==='Voices & staves'));
assert(DATA.features.filter(f=>matches(f,{...base,status:'unknown'})).length>0);
const sorted=[...DATA.features].sort((a,b)=>compareFeatures(a,b,{...base,sort:'musescore'}));
for(let i=1;i<sorted.length;i++)assert(STATUS_ORDER.indexOf(sorted[i-1].cells.musescore.status)<=STATUS_ORDER.indexOf(sorted[i].cells.musescore.status));
state.q='';state.category='Voices & staves';state.visible=['krn','mei'];
const exported=csvText();assert(exported.charCodeAt(0)===0xfeff);
assert(exported.includes('Two independent voices on one stave'));
console.log(JSON.stringify({search:'pass',combined_filters:'pass',visibility:'pass',sort:'pass',csv:'pass'}));
'''
    with tempfile.TemporaryDirectory(dir=ROOT) as temp:
        js=Path(temp)/'model-check.cjs'
        js.write_text('const DATA='+json.dumps(data)+';\n'+pure+'\n'+csv+'\n'+test)
        res=subprocess.run([node,str(js)],capture_output=True,text=True)
        assert res.returncode==0,res.stderr
        print(res.stdout.strip())
    print(f'PASS: data references, {len(data["features"])} topics / {4*len(data["features"])} cells, HTML anchors, embedded JSON, no remote assets, escaping, fragment well-formedness, search/filter/sort/CSV logic.')
    print('NOT TESTED: browser rendering/accessibility behaviour; music-format schema validation, conversion, engraving or playback.')
if __name__=='__main__':main()
