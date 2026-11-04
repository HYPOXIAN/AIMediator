"""Authored bilingual fixture transport injected through the real pipeline boundaries."""
import json

import numpy as np
from .common import read
from .evidence import character_candidates, character_reference
from .inference import Transport
from .resources import anchors, asset_path


class FixtureTransport(Transport):
    provenance = 'agent_authored_synthetic_fixture_transports'

    def __init__(self, cfg, key=None, folder=None):
        super().__init__(cfg, key, folder)
        self.cases = read(asset_path('fixtures/cases.json'))
        self.annotations = {c['source']['record_id']: c['annotation'] for c in self.cases}
        self.originals = {c['source']['record_id']: c['source'] for c in self.cases}
        self.calls = []

    def tags(self):
        return {'models': [{'name': name, 'digest': 'FIXTURE-NOT-REAL-WEIGHTS:' + name}
                           for name in list(self.cfg['routing']['models']) + [self.cfg['embedding']['model']]]}

    def api(self, base, endpoint, payload=None):
        self.calls.append(('embedding', len(payload['input'])))
        # Exercise actual cosine retrieval with deterministic synthetic vectors.
        return {'embeddings': [[0., 1.] if text in anchors()[1] else [1., 0.] for text in payload['input']],
                'fixture_transport': True}

    def embed(self, cfg, texts):
        return np.asarray([[1.,0.] for text in texts],dtype=np.float32), {}

    def chat(self, base, payload, partial_path):
        self.calls.append(('chat', payload['model']))
        data = json.loads(payload['messages'][1]['content'])
        props = payload['format']['properties']
        if 'segments' in props:
            result = self.annotations[data['comments'][0]['comment_id']]
        elif 'decisions' in props:
            result = {'decisions': ['related'] * len(data['comments'])}
        elif 'support' in props:
            result = {'support': 'supported'}
        else:
            assessments = {}
            for row in data['comments']:
                cid, claims = row['comment_id'], []
                annotation = self.annotations[cid]
                for point in annotation['information_points']:
                    if point['scope'] != 'character_balance' or not point['character_literal'] or point['stance'] == 'uncertain':
                        continue
                    if 'allowed_quality_points' in row and point['point_id'] not in {p['point_id'] for p in row['allowed_quality_points']}:
                        continue
                    selected = [s for s in annotation['segments'] if s['segment_id'] in point['segment_ids']]
                    names = character_candidates(point['character_literal'], character_reference(self.originals[cid]['text_original']))
                    if len(names) != 1:
                        continue
                    claim = {'character': names[0], 'target': point['mechanic_literal'], 'direction': point['direction'],
                        'recommendation': ' '.join(s['quote'] for s in selected), 'specificity': 'qualitative_only',
                        'parameters': [], 'evidence_ids': list(dict.fromkeys(s['evidence_id'] for s in selected)), 'uncertain': False}
                    if 'numeric_request' in cid:
                        claim['specificity'] = 'source_numeric'
                        claim['parameters'] = [{'metric':'damage','current':'600','proposed':'500','delta':None,
                                                'unit':None,'evidence_id':selected[0]['evidence_id']}]
                    if 'allowed_quality_points' in row:
                        claim['quality_point_ids'] = [point['point_id']]
                    claims.append(claim)
                assessments[cid] = {'claims': claims}
            result = {'assessments': assessments}
        raw = json.dumps(result,ensure_ascii=False)
        partial_path.parent.mkdir(parents=True,exist_ok=True)
        partial_path.write_text(raw,encoding='utf-8')
        return {'done':True,'done_reason':'stop','fixture_transport':True,'message':{'content':raw}}
