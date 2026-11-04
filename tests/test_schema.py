"""Serialized forms of the schema builders and constants, which reach the model in every request."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from aimediator.schema import NULLABLE_NONEMPTY_STRING, NULLABLE_STRING, STRING, obj, quality_obj


class SchemaSerialization(unittest.TestCase):
    def test_builders_and_constants_serialize_unchanged(self):
        # Ollama compiles property order into the decoding grammar, so key order is request behavior.
        self.assertEqual(json.dumps(obj({'a': STRING})),
                         '{"type": "object", "additionalProperties": false, '
                         '"properties": {"a": {"type": "string", "minLength": 1}}, "required": ["a"]}')
        self.assertEqual(json.dumps(quality_obj({'a': STRING})),
                         '{"type": "object", "properties": {"a": {"type": "string", "minLength": 1}}, '
                         '"required": ["a"], "additionalProperties": false}')
        self.assertEqual(json.dumps(NULLABLE_STRING), '{"type": ["string", "null"]}')
        self.assertEqual(json.dumps(NULLABLE_NONEMPTY_STRING), '{"type": ["string", "null"], "minLength": 1}')


if __name__ == '__main__':
    unittest.main()
