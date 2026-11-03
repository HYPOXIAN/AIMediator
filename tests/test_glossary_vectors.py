import sys
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import glossary_vectors as v


class VectorTests(unittest.TestCase):
    def test_endpoint_config_without_mutating_env(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / '.env'
            content = 'EMBEDDING_MODEL=m\nEMBEDDING_API_KEY=secret\nEMBEDDING_API_URL=https://example.com/api/v1/chat/completions\n'
            path.write_text(content)
            with patch.dict(v.os.environ, {}, clear=True):
                cfg = v.config(path)
            self.assertEqual(cfg['url'], 'https://example.com/api/v1/embeddings')
            self.assertEqual(path.read_text(), content)

    def test_pending_alias_and_conditions_preserved(self):
        entry = {'id': 'x', 'scope': 'Ryu', 'canonical_name': 'Shoryuken',
                 'aliases': [{'text': 'DP', 'candidate_only': True, 'requires_context': True}]}
        self.assertEqual(json.loads(v.document(entry))['aliases'], entry['aliases'])

    def test_embedding_response_order_and_unit_length(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self):
                return json.dumps({'data': [{'index': 1, 'embedding': [0, 2]},
                                             {'index': 0, 'embedding': [3, 0]}]}).encode()
        with patch.object(v, 'urlopen', return_value=Response()):
            matrix, _ = v.embed({'model': 'm', 'key': 'secret', 'url': 'https://example.com/embeddings'}, ['a', 'b'])
        np.testing.assert_array_equal(matrix, np.eye(2))

    def test_invalid_vectors_rejected(self):
        for data in ([[0, 0]], [[float('nan'), 1]], [1, 2]):
            with self.assertRaises(ValueError):
                v.normalize(data)


if __name__ == '__main__':
    unittest.main()
