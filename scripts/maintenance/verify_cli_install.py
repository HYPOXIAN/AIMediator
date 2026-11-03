"""Run against an installed wheel from outside the checkout, with network denied.

Usage: /path/to/venv/bin/python -I /path/to/this/script.py --out /new/directory
No repository imports or PYTHONPATH are used.
"""
import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import urllib.request


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    import aimediator
    from aimediator.cli import main as cli
    from aimediator.resources import asset_path
    environment=dict(os.environ);environment.pop('PYTHONPATH',None)
    console=Path(sys.executable).parent/'aimediator'
    records=[]
    for argv in (['--help'],['--version']):
        p=subprocess.run([str(console),*argv],capture_output=True,text=True,env=environment,check=True,cwd=out)
        records.append({'argv':argv,'exit':p.returncode,'stdout':p.stdout})
    os.chdir(out)
    os.environ['EMBEDDING_API_KEY']='UNRELATED_ACCEPTANCE_SECRET'
    Path('.env').write_text('EMBEDDING_API_URL=https://unrelated.invalid\nEMBEDDING_API_KEY=UNRELATED_ENV_FILE_SECRET\n',encoding='utf-8')
    def deny(*args,**kwargs):raise AssertionError('Offline acceptance attempted network access')
    socket.socket.connect=deny;urllib.request.urlopen=deny
    def run(argv,expected=0):
        stdout,stderr=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):code=cli([*argv,'--json','--quiet'])
        result=json.loads(stdout.getvalue())
        if code!=expected:raise AssertionError((argv,code,result,stderr.getvalue()))
        for key in ('command','status','artifacts','counts','warnings','error_code','error_message'):assert key in result
        records.append({'argv':argv,'exit':code,'result':result,'stderr':stderr.getvalue()})
        return result
    run(['init','--out','config.json'])
    run(['doctor','--config','config.json','--offline'])
    run(['demo','--out','demo'])
    run(['doctor','--config','config.json','--input','demo/synthetic-input.jsonl','--out','prospective','--offline'])
    assert not Path('prospective').exists()
    run(['status','--run','demo/enforce'])
    # Completed fixture resume must stay offline and make no new transport calls.
    run(['analyze','--resume','demo/enforce'])
    run(['review','export','--run','demo/enforce','--out','template'])
    decisions=json.loads(Path('template/decisions.json').read_text(encoding='utf-8'))
    run(['review','import','--run','demo/enforce','--decisions','template/decisions.json','--out','invalid-overlay'],2)
    decisions.update(reviewer_type='agent',reviewer_id='installed-wheel-synthetic-acceptance')
    Path('template/decisions.json').write_text(json.dumps(decisions,ensure_ascii=False),encoding='utf-8')
    result=run(['review','import','--run','demo/enforce','--decisions','template/decisions.json','--out','overlay'])
    assert result['counts']['source_accepted_claims']==0
    run(['report','--run','demo/enforce','--review','overlay','--out','reviewed-report'])
    for path in ('automatic-report-a','automatic-report-b'):
        run(['report','--run','demo/enforce','--out',path])
    for name in ('report.md','report.json'):
        assert (Path('automatic-report-a')/name).read_bytes()==(Path('automatic-report-b')/name).read_bytes()
    cases=json.loads(asset_path('fixtures/cases.json').read_text(encoding='utf-8'))
    labels=[]
    for case in cases:
        row=case['source'];labels.append({'comment_id':row['record_id'],'language':row['language'],
            'text_original':row['text_original'],'content_sha256':hashlib.sha256(row['text_original'].encode()).hexdigest(),
            'cluster_id':row['record_id'],'split':'development','reviewer_type':'agent_authored_synthetic',
            'source_stage':'fixed_admission','points':None,'point_matches':None})
    Path('labels.json').write_text(json.dumps(labels,ensure_ascii=False),encoding='utf-8')
    run(['evaluate','quality','--labels','labels.json','--run','demo/enforce','--out','evaluation'])
    run(['evaluate','quality','--labels','labels.json','--run','demo/off','--out','off-evaluation'],2)
    run(['analyze'],2)
    run(['init','--out','config.json'],4)
    for mode in ('off','shadow','enforce'):
        manifest=json.loads(Path('demo',mode,'manifest.json').read_text())
        assert manifest['schema_version']=='aimediator-run-v1'
        assert manifest['execution_provenance']=='agent_authored_synthetic_fixture_transports'
        ledger=json.loads(Path('demo',mode,'full-pipeline-coverage.json').read_text())
        assert len(ledger)==len(cases)==len({r['comment_id'] for r in ledger})
    assert json.loads(Path('reviewed-report/report.json').read_text())['counts']['formal_claims']==0
    for path in Path('demo').rglob('*'):
        if path.is_file():assert b'UNRELATED_' not in path.read_bytes()
    result={'passed':True,'network_calls':0,'package_file':str(Path(aimediator.__file__).resolve()),
            'python':sys.version,'numpy':__import__('numpy').__version__,'commands':records}
    Path('acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':True,'commands':len(records),'artifacts':str(out),'python':sys.version.split()[0],'numpy':result['numpy']}))


if __name__=='__main__':main()
