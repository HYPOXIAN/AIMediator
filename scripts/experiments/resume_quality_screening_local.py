"""Resume the frozen experiment with explicit CPU placement and an auditable transport log.

Hardware placement is recorded separately; model, prompts, context, seed and policy
remain those of the frozen experiment. Original request/cache identities stay intact.
"""
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))  # scripts/ holds the registered forwarding shells
import run_balance_analysis as m
import run_quality_screening_experiment as experiment

original_stream = m.streamed_chat
original_generate = m.Runner.generate


def stream(base, payload, partial_path):
    effective = {**payload, 'options': {**payload['options'], 'num_gpu': 0}}
    user = json.loads(payload['messages'][1]['content'])
    first = ('quality_contract', 'language', 'character_normalization_reference')
    ordered = {key: user[key] for key in first if key in user}
    ordered.update({key: value for key, value in user.items() if key not in ordered})
    content = json.dumps(ordered, ensure_ascii=False)
    assert json.loads(content) == user
    effective['messages'] = [payload['messages'][0], {**payload['messages'][1], 'content': content}]
    m.write_json(partial_path.parent / 'effective-runtime-request.json', effective)
    return original_stream(base, effective, partial_path)


def generate(self, model, language, stage, data, ids):
    # JSON object key order is not model input semantics. Reuse a validated
    # response whose parsed request is otherwise exactly equal, keeping its ID.
    if stage == 'quality':
        schema = m.schema_for(stage, ids, data)
        expected_user = {**data, 'response_schema': schema}
        expected_options = {'temperature': 0, 'seed': 42, 'num_ctx': self.quality_policy['num_ctx'],
                            'num_predict': self.quality_policy['num_predict']}
        for response in sorted((self.folder / 'requests' / stage).glob('*/response.json')):
            try:
                payload = json.loads((response.parent / 'request.json').read_text())
                envelope = json.loads(response.read_text())['response']
                validation = json.loads((response.parent / 'validation.json').read_text())
                if (payload['model'] != model or payload['options'] != expected_options or
                    payload['messages'][0]['content'] != self.prompts[stage][language] or
                    payload['format'] != schema or
                    json.loads(payload['messages'][1]['content']) != expected_user or
                    envelope.get('done') is not True or envelope.get('done_reason') != 'stop' or
                    validation['errors']):
                    continue
                cached_data = json.loads(payload['messages'][1]['content'])
                cached_data.pop('response_schema')
                parsed, meta = original_generate(self, model, language, stage, cached_data, ids)
                assert meta['request_id'] == response.parent.name
                return parsed, {**meta, 'recovered_by': 'exact_parsed_request_equivalence'}
            except (ValueError, KeyError, OSError, TypeError):
                continue
    return original_generate(self, model, language, stage, data, ids)


if __name__ == '__main__':
    folder = Path(sys.argv[sys.argv.index('--out') + 1]).resolve()
    m.write_json(folder / 'runtime-recovery.json', {
        'hardware_override': {'num_gpu': 0}, 'workers': 1,
        'reason': 'Measured local CPU generation at 8.46 tokens/second versus 2.85 on GPU; use CPU for this recovery. See local-speed-diagnostic.json.',
        'semantic_settings_unchanged': ['model_digest', 'prompt', 'schema', 'temperature', 'seed', 'num_ctx', 'num_predict', 'quality_policy', 'frozen_relevance', 'input_group'],
        'effective_requests': 'requests/quality/*/effective-runtime-request.json for new calls made by this adapter',
        'user_json_order': 'Invariant fields first for prefix cache reuse; parsed object values unchanged',
        'adapter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'note': 'Hardware placement can change floating-point execution; this is a continued local inference run, not a bitwise reproducibility claim.'})
    m.streamed_chat = stream
    m.Runner.generate = generate
    experiment.main()
