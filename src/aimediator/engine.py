"""Full-corpus retrieval, relevance agreement, bilingual extraction and source audit.

Dependencies: Python 3.9+, numpy, local Ollama. All requests and raw responses are
content-addressed and resumable; model-written quotes are never trusted.
"""
import argparse
from datetime import datetime, timezone
from functools import partial
import json
from pathlib import Path

from . import evidence_quality as quality
from . import glossary_vectors, resources
from .common import sha as digest, write as write_json
from .balance_policy import POLICY_PATH, load_policy
from .resources import asset_path, module_path
from .inference import api
from .runner import Runner
from .retrieval import retrieve
from .pipeline import VERSION, process, validate_modes
ROOT = Path.cwd()


def run(args, *, api_transport=None, chat_transport=None, embed_transport=None, retrieval_service=None, log=None):
    quality_mode = validate_modes(args)
    quality_policy = quality.load_policy() if quality_mode != 'off' else None
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    source = args.dataset.read_bytes()
    rows = [json.loads(line) for line in source.decode().splitlines() if line.strip()]
    if len({r['record_id'] for r in rows}) != len(rows):
        raise ValueError('Dataset has duplicate record IDs')
    routing = json.loads((asset_path('configs/local-language-routing.json')).read_text(encoding='utf-8'))
    routes = routing['models']
    models = [args.model] if args.model else list(routes)
    tags = (api_transport or api)(args.base_url, '/api/tags')['models']
    installed = {m['name']: m['digest'] for m in tags}
    embedding_config = None
    if getattr(args, 'embedding_provider', 'ollama') == 'configured':
        embedding_config = glossary_vectors.config(args.env_file)
        args.embedding_model = embedding_config['model']
    missing_models = sorted(set(models + ([] if embedding_config else [args.embedding_model])) - set(installed))
    if missing_models:
        raise ValueError('Required local models unavailable: ' + ', '.join(missing_models))
    prompts = resources.prompts(quality_mode)
    quality_identity = {'mode': quality_mode, 'policy': quality_policy,
        'runner_sha256': digest(module_path('engine.py').read_bytes()),
        'model_digests': {m: installed[m] for m in models},
        'glossary_sha256': digest((asset_path('data/glossary.json')).read_bytes()),
        'policy_module_sha256': digest((module_path('balance_policy.py')).read_bytes()),
        'review_policy_sha256': digest(POLICY_PATH.read_bytes()),
        'prompts_sha256': digest(json.dumps(prompts, sort_keys=True, ensure_ascii=False).encode()),
        'module_sha256': digest((module_path('evidence_quality.py')).read_bytes()),
        'schema_sha256': digest(json.dumps(quality.annotation_schema(['COMMENT_ID']), sort_keys=True).encode())}
    positive_anchors, negative_anchors = resources.anchors()
    identity = {'version': VERSION, 'dataset_sha256': digest(source),
        'shared_code_sha256': {p.name: digest(p.read_bytes()) for p in sorted(module_path('engine.py').parent.glob('*.py'))},
        'models': {m: installed[m] for m in models}, 'embedding_model': args.embedding_model,
        'embedding_digest': None if embedding_config else installed[args.embedding_model], 'routing': routing,
        'glossary_sha256': digest((asset_path('data/glossary.json')).read_bytes()),
        'script_sha256': digest(module_path('engine.py').read_bytes()),
        'policy_module_sha256': digest((module_path('balance_policy.py')).read_bytes()),
        'review_policy_sha256': digest(POLICY_PATH.read_bytes()),
        'mode': 'relevance_only' if getattr(args, 'relevance_only', False) else 'quality_only' if getattr(args, 'quality_only', False) else 'full_pipeline',
        'evidence_quality': quality_identity,
        'anchor_sha256': digest(json.dumps([positive_anchors, negative_anchors], ensure_ascii=False).encode()),
        'prompts': {stage: {lang: digest(t.encode()) for lang, t in pair.items()}
                    for stage, pair in prompts.items()}}
    if embedding_config:
        identity['embedding_service'] = {'provider': 'configured', 'endpoint': embedding_config['url'],
            'model': embedding_config['model'], 'model_digest': None,
            'limitation': 'Configured remote embedding model has no locally verifiable weight digest.'}
    if getattr(args, 'num_gpu', None) is not None:
        identity['runtime_options'] = {'num_gpu': args.num_gpu}
    manifest_path = folder / 'manifest.json'
    if manifest_path.exists():
        if json.loads(manifest_path.read_text(encoding='utf-8'))['identity'] != identity:
            raise ValueError('Run inputs/code/models changed; use a new output directory')
    else:
        write_json(manifest_path, {'identity': identity, 'dataset': str(args.dataset.resolve()),
            'created_at_utc': datetime.now(timezone.utc).isoformat(),
            'retrieval': {'positive_anchors': positive_anchors, 'negative_anchors': negative_anchors,
                'score': 'mean top-3 cosine per class', 'pass': 'positive > negative',
                'agreement': 'retrieval pass AND same-language model related AND not uncertain'}})
        write_json(folder / 'source-snapshot.json', rows)
        write_json(folder / 'prompt-snapshot.json', prompts)
        write_json(folder / 'review-policy-snapshot.json', load_policy())
        write_json(folder / 'quality-policy-snapshot.json', quality_policy)
        (folder / 'quality-module-snapshot.py').write_bytes((module_path('evidence_quality.py')).read_bytes())
        (folder / 'runner-snapshot.py').write_bytes(module_path('engine.py').read_bytes())
        (folder / 'policy-module-snapshot.py').write_bytes((module_path('balance_policy.py')).read_bytes())
        (folder / 'code-snapshot').mkdir(exist_ok=True)
        for path in sorted(module_path('engine.py').parent.glob('*.py')):
            (folder / 'code-snapshot' / path.name).write_bytes(path.read_bytes())
    runner_factory = partial(Runner, chat_transport=chat_transport, log=log)
    if retrieval_service is None:
        retrieval_service = partial(retrieve, api_transport=api_transport, embed_transport=embed_transport, log=log)
    return process(args, rows, routing, models, prompts, quality_identity,
                   quality_policy, identity, embedding_config, runner_factory, retrieval_service, log=log)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, default=ROOT / 'data/raw/feedback/20261015-expanded/screened/records.jsonl')
    parser.add_argument('--out', type=Path, default=ROOT / 'runs/balance-quality-v1')
    parser.add_argument('--model', choices=['qwen2.5:7b', 'llama3.1:latest'])
    parser.add_argument('--embedding-model', default='qwen3-embedding:8b')
    parser.add_argument('--embedding-provider', choices=['ollama', 'configured'], default='ollama')
    parser.add_argument('--env-file', type=Path, default=ROOT / '.env')
    parser.add_argument('--num-gpu', type=int, help='Explicit Ollama GPU layer count; 0 requests CPU inference')
    parser.add_argument('--base-url', default='http://127.0.0.1:11434')
    parser.add_argument('--evidence-quality', choices=['off', 'shadow', 'enforce'], default='off')
    parser.add_argument('--quality-only', action='store_true', help='Stop after quality annotation; requires shadow/enforce')
    parser.add_argument('--relevance-only', action='store_true', help='Complete retrieval and relevance gates without extraction')
    args = parser.parse_args()
    try:
        validate_modes(args)
    except ValueError as exc:
        parser.error(str(exc))
    run(args, log=lambda text: print(text, flush=True))


if __name__ == '__main__':
    main()
