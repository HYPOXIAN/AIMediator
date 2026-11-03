"""Render saved local test results as a standalone, offline HTML viewer."""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    reports = []
    for folder in sorted((ROOT / "reports").glob("smoke-*")):
        result_file = folder / "results.json"
        if not result_file.exists():
            continue
        reports.append({"name": folder.name,
                        "records": json.loads(result_file.read_text()),
                        "cases": json.loads((folder / "cases.json").read_text()),
                        "metadata": json.loads((folder / "metadata.json").read_text()),
                        "interrupted": (folder / "interruption.md").exists(),
                        "complete": (folder / "review.md").exists()})
    data = json.dumps({"reports": reports, "snapshot": datetime.now(timezone.utc).isoformat()}, ensure_ascii=False)
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = TEMPLATE.replace("__DATA__", data)
    output = ROOT / "reports" / "results-viewer.html"
    output.write_text(html, encoding="utf-8")
    print(output)


TEMPLATE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Mediator · Test results</title>
<style>
:root{color-scheme:light;--bg:#f5f6f8;--ink:#202731;--muted:#626d7b;--line:#dce1e7;--accent:#2458b4;--warn:#8b4c10}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.6 system-ui,sans-serif}main{max-width:1450px;margin:auto;padding:30px}h1{font-size:24px;margin:0}h2{font-size:18px;margin:0 0 12px}p{margin:8px 0}.muted{color:var(--muted)}.toolbar{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0 18px;align-items:end}label{display:grid;gap:4px;color:var(--muted)}select,input,button{font:inherit;border:1px solid var(--line);border-radius:5px;padding:8px;background:white;color:var(--ink)}.summary{display:flex;gap:28px;flex-wrap:wrap;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:16px 0;margin-bottom:20px}.stat strong{font-size:21px;display:block}.layout{display:grid;grid-template-columns:minmax(380px,.85fr) minmax(440px,1.15fr);gap:25px;align-items:start}.list{overflow:auto;max-height:70vh;border:1px solid var(--line);background:white}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--muted);font-weight:500;background:#f0f2f5;position:sticky;top:0}tr[data-key]{cursor:pointer}tr[data-key]:hover{background:#f2f5fa}tr.selected{background:#e8effa}td:last-child{white-space:nowrap}.badge{font-size:12px;color:var(--accent)}.warn{color:var(--warn)}.detail{min-width:0}pre{font:12px/1.65 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:white;border:1px solid var(--line);padding:14px;margin:8px 0 18px;max-height:450px;overflow:auto}.quote{background:white;border-left:3px solid var(--accent);padding:12px 16px;white-space:pre-wrap;margin:8px 0 20px}.checks{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 20px}.check{border:1px solid var(--line);padding:4px 8px;font-size:12px;background:white}.claim{padding:12px 0;border-top:1px solid var(--line)}.claim-title{font-weight:600}.evidence{font-size:13px;white-space:pre-wrap;color:var(--muted)}details{margin:12px 0}summary{cursor:pointer;color:var(--accent)}@media(max-width:950px){main{padding:18px}.layout{grid-template-columns:1fr}.list{max-height:45vh}}
</style></head><body><main>
<h1>AI Mediator / Test results</h1>
<p class="muted">Street Fighter 6 · 08.03.2026 Update · Original ten synthetic comments · Human review pending</p>
<div class="toolbar"><label>Report<select id="report"></select></label><label>Model<select id="model"><option value="">All models</option></select></label><label>Search<input id="search" placeholder="Comment ID, text, output"></label><label>Load an updated results.json<input type="file" id="upload" accept=".json,application/json"></label></div>
<div id="summary" class="summary"></div><p id="status" class="muted"></p>
<div class="layout"><section><div class="list"><table><thead><tr><th>Comment / model</th><th>Request</th><th>JSON</th><th>Seconds</th></tr></thead><tbody id="rows"></tbody></table></div><p id="snapshot" class="muted"></p></section><section id="detail" class="detail"></section></div>
</main><script id="data" type="application/json">__DATA__</script><script>
const DATA=JSON.parse(document.getElementById('data').textContent);let selected=null;
const $=id=>document.getElementById(id),escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pretty=value=>escape(JSON.stringify(value,null,2));
DATA.reports.forEach((r,i)=>{const o=document.createElement('option');o.value=i;o.textContent=r.name+(r.metadata.options.num_gpu===0?' · CPU':' · GPU/default');$('report').append(o)});$('report').value=DATA.reports.length-1;
function current(){return DATA.reports[Number($('report').value)]}
function models(r){return Object.keys(r.metadata.model_details||{})}
function entries(r){return models(r).flatMap(model=>r.cases.map(c=>({key:model+'|'+c.comment_id,model,case:c,record:r.records.find(x=>x.model===model&&x.comment_id===c.comment_id)})))}
function resetModels(){const old=$('model').value;$('model').innerHTML='<option value="">All models</option>';models(current()).forEach(m=>{const o=document.createElement('option');o.value=m;o.textContent=m;$('model').append(o)});if(models(current()).includes(old))$('model').value=old;selected=null;render()}
function render(){const r=current(),all=entries(r),records=r.records,done=records.filter(x=>x.response?.done===true),valid=done.filter(x=>x.checks?.json_valid===true),exact=done.filter(x=>x.checks?.evidence_exact===true),na=done.filter(x=>x.checks?.evidence_exact===null),failed=records.filter(x=>x.error||x.response?.done!==true);
$('summary').innerHTML=[['Completed requests',done.length+' / '+all.length],['Valid JSON',valid.length+' / '+done.length],['Exact evidence',exact.length+' / '+(done.length-na.length)],['Failed / unfinished requests',failed.length],['Not yet recorded',all.length-records.length]].map(([label,n])=>'<div class="stat"><strong>'+escape(n)+'</strong>'+label+'</div>').join('');
$('status').textContent=(r.interrupted?'Interrupted GPU run. ':r.complete?'Run finished. ':'Partial snapshot; the run may still be active. ')+'Checks describe the unchanged raw output, not semantic accuracy. Exact-evidence counts exclude empty-claim responses. Loading a newer JSON file updates this view only.';
const q=$('search').value.toLowerCase(),rows=all.filter(x=>(!$('model').value||x.model===$('model').value)&&(!q||JSON.stringify(x).toLowerCase().includes(q)));
if(!rows.some(x=>x.key===selected))selected=(rows.find(x=>x.record)||rows[0])?.key;
$('rows').innerHTML=rows.map(x=>{const a=x.record,ok=a?.response?.done===true;return '<tr data-key="'+escape(x.key)+'" class="'+(x.key===selected?'selected':'')+'"><td><strong>'+escape(x.case.comment_id)+'</strong> · '+escape(x.case.language)+'<br><span class="muted">'+escape(x.model)+'</span></td><td><span class="'+(a&&!ok?'warn':'badge')+'">'+(!a?'Not recorded':ok?'Completed':'Failed / unfinished')+'</span></td><td>'+(!a?'—':a.checks?.json_valid?'Pass':'Fail')+'</td><td>'+escape(a?.wall_seconds??'—')+'</td></tr>'}).join('');
$('rows').querySelectorAll('tr').forEach(tr=>tr.onclick=()=>{selected=tr.dataset.key;render()});$('snapshot').textContent='Snapshot: '+DATA.snapshot+' · Source: reports/'+r.name+'/results.json';
const x=rows.find(x=>x.key===selected);if(!x){$('detail').innerHTML='';return}detail(x)}
function detail(x){const a=x.record,c=x.case;let html='<h2>'+escape(c.comment_id)+' / '+escape(x.model)+'</h2><span class="muted">Original comment · '+escape(c.language)+'</span><div class="quote">'+escape(c.text)+'</div>';
if(a){const checks=a.checks||{};html+='<div class="checks">'+Object.entries(checks).map(([k,v])=>'<span class="check">'+escape(k)+': '+(v===null?'N/A':v?'Pass':'Fail')+'</span>').join('')+'</div>';if(a.error)html+='<p class="warn">'+escape(a.error)+'</p>';
const obj=a.parsed_output;if(obj&&Array.isArray(obj.claims)){html+='<h2>Parsed claims</h2><p class="muted">Output language: '+escape(obj.language)+' · Emotional tone: '+escape(obj.emotional_tone)+'</p>';if(!obj.claims.length)html+='<p>The model returned an empty claims array.</p>';obj.claims.forEach(cl=>{html+='<div class="claim"><div class="claim-title">'+escape(cl.character)+' / '+escape(cl.mechanic)+' · '+escape(cl.direction)+'</div><p>'+escape(cl.reason)+'</p><p class="evidence">Evidence: '+escape(cl.evidence)+'</p><span class="muted">Uncertain: '+escape(cl.uncertain)+'</span></div>'})}
html+='<h2 style="margin-top:20px">Raw model output</h2><pre>'+escape(a.response?.response??a.error??'')+'</pre><details><summary>Complete result record (original JSON)</summary><pre>'+pretty(a)+'</pre></details>'}
else html+='<p class="muted">This request has no saved result in this snapshot.</p>';
html+='<details><summary>Provisional expected labels (not reviewed)</summary><pre>'+pretty(c.expected)+'</pre></details>';$('detail').innerHTML=html}
$('report').onchange=resetModels;$('model').onchange=render;$('search').oninput=render;
$('upload').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{const records=JSON.parse(await file.text());if(!Array.isArray(records)||records.some(x=>!x.model||!x.comment_id))throw Error('Expected an array of test result records.');current().records=records;DATA.snapshot=new Date().toISOString()+' (loaded file)';render()}catch(error){alert(error.message)}};
resetModels();
</script></body></html>'''

if __name__ == "__main__":
    main()
