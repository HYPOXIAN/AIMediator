"""Rerun the corpus on current code, reusing only identical model-visible requests.

Cache reuse is explicit transport provenance. Different schemas, prompts, input
strings, options or model digests require fresh inference. No model output is
rewritten and every response is revalidated by the current pipeline.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import shutil
import time

import run_balance_analysis as m


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--from-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--dataset',type=Path,required=True);p.add_argument('--base-url',default='http://127.0.0.1:11434')
    args=p.parse_args();parent=args.from_run.resolve();out=args.out.resolve()
    old=m.strict_json((parent/'manifest.json').read_text())
    if old['identity']['dataset_sha256']!=m.digest(args.dataset.read_bytes()):raise ValueError('Dataset changed')
    tags={r['name']:r['digest'] for r in m.api(args.base_url,'/api/tags')['models']}
    if any(tags.get(n)!=d for n,d in old['identity']['models'].items()):raise ValueError('Local weights changed')
    index={}
    for response_path in sorted((parent/'requests').glob('*/*/response.json')):
        request_path=response_path.parent/'request.json'
        if not request_path.exists():continue
        payload=m.strict_json(request_path.read_text());key=m.digest(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode())
        index[key]=(request_path,response_path)
    out.mkdir(parents=True,exist_ok=True)
    provenance={'kind':'exact_model_visible_request_reuse_only','parent_manifest_sha256':m.digest((parent/'manifest.json').read_bytes()),
        'transport_script_sha256':m.digest(Path(__file__).read_bytes()),'current_runner_sha256':m.digest((m.ROOT/'scripts/run_balance_analysis.py').read_bytes()),
        'dataset_sha256':m.digest(args.dataset.read_bytes()),'models':old['identity']['models'],
        'comparison':'Entire model-visible payload including message strings, schema, options and model tag, with identical weight digests. No constraint-equivalence shortcuts.'}
    path=out/'transport-reuse-manifest.json'
    if path.exists() and m.strict_json(path.read_text())!=provenance:raise ValueError('Transport identity changed')
    m.write_json(path,provenance)
    (out/'transport-snapshot.py').write_bytes(Path(__file__).read_bytes())
    if not (out/'embeddings').exists():shutil.copytree(parent/'embeddings',out/'embeddings')
    actual_stream=m.streamed_chat
    def stream(base,payload,partial_path):
        key=m.digest(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode())
        if key in index:
            request_path,response_path=index[key]
            assert m.strict_json(request_path.read_text())==payload
            envelope=m.strict_json(response_path.read_text());raw=copy.deepcopy(envelope['response'])
            partial_path.write_text(raw.get('message',{}).get('content',''))
            m.write_json(partial_path.parent/'transport-provenance.json',{'kind':'reused_identical_model_request',
                'source_request':str(request_path),'source_response':str(response_path),
                'source_response_sha256':m.digest(response_path.read_bytes()),'source_elapsed_seconds':envelope.get('elapsed_seconds'),
                'model_visible_request_sha256':key})
            return raw
        m.write_json(partial_path.parent/'transport-provenance.json',{'kind':'fresh_inference','model_visible_request_sha256':key})
        return actual_stream(base,payload,partial_path)
    m.streamed_chat=stream
    run_args=argparse.Namespace(dataset=args.dataset,out=out,model=None,embedding_model='qwen3-embedding:8b',
        embedding_provider='configured',env_file=m.ROOT/'.env',num_gpu=99,base_url=args.base_url,
        evidence_quality='off',relevance_only=False,quality_only=False)
    m.run(run_args)
    stats=Counter();by_stage={}
    for item in (out/'requests').glob('*/*/transport-provenance.json'):
        mode=m.strict_json(item.read_text())['kind'];stage=item.parent.parent.name
        stats[mode]+=1;by_stage.setdefault(stage,Counter())[mode]+=1
    m.write_json(out/'transport-reuse-summary.json',{'counts':dict(stats),'by_stage':{s:dict(c) for s,c in by_stage.items()},
        'note':'Reused results are not fresh inference; all changed model requests were executed, and every response was validated by current code.'})
    print('Exact request reuse:',dict(stats),flush=True)


if __name__=='__main__':main()
