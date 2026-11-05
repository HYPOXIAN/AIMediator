"""Payload contract of the model-visible request views (pipeline upgrade plan 4.1, step U2.6; ADR 0003).

Every request of the offline demo (three modes) and of behavior-lock target L2 (the legacy runner in three modes)
holds only the keys of ``stages.MODEL_VISIBLE``, and the non-comment characters of each user message stay within
the budget of its stage.
"""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import behavior_lock as lock
from aimediator import stages
from aimediator.demo import demo

# Per stage, the largest non-comment character count of a user message over every request of the five U2-L1 live
# runs (session U2-L1, 2026-11-05, at the U2.4 code b7d1cc5; "budgets_u2_6" of its comparison, recorded in the
# U2-L1 findings of docs/records/20261104-pipeline-upgrade.md), plus 20 %, rounded up. Neither target sends a retrieval_review
# request (the fixture vectors queue no comment for review); its budget comes from the live runs all the same.
BUDGETS = {  # stage: ceil(1.2 * U2-L1 maximum)
    'relevance': 2512,  # 2,093
    'retrieval_review': 2422,  # 2,018
    'quality': 5688,  # 4,740
    'extract': 12072,  # 10,060
    'verify': 2376,  # 1,980
}


def comment_texts(user):
    """Return the comment texts a user message carries: comments[].text, comments[].units[].text, original_evidence.

    Their JSON-encoded length is not counted against the budget; quotes and every other key are.
    """
    texts = []
    for comment in user.get('comments') or []:
        if isinstance(comment.get('text'), str):
            texts.append(comment['text'])
        texts.extend(u['text'] for u in comment.get('units') or [] if isinstance(u.get('text'), str))
    if isinstance(user.get('original_evidence'), str):
        texts.append(user['original_evidence'])
    return texts


def non_comment_characters(content):
    """Characters of a user message outside its comment texts (each counted JSON-encoded, as sent)."""
    user = json.loads(content)
    return len(content) - sum(len(json.dumps(t, ensure_ascii=False)) for t in comment_texts(user))


def collect(root, label):
    """Return (label, stage, user message string) of every chat request under ``root``."""
    out = []
    for path in sorted(root.glob('*/requests/*/*/request.json')):
        request = json.loads(path.read_text(encoding='utf-8'))
        users = [m['content'] for m in request.get('messages') or [] if m.get('role') == 'user']
        if users:
            out.append(('%s/%s' % (label, path.parent.parent.parent.parent.name), path.parent.parent.name, users[0]))
    return out


class PayloadContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                demo(work / 'demo', quiet=True)
                legacy = lock.produce_legacy(work)
            cls.requests = collect(work / 'demo', 'demo') + collect(legacy, 'legacy')

    def test_both_targets_send_every_stage_but_retrieval_review(self):
        for label in ('demo', 'legacy'):
            for mode in ('off', 'shadow', 'enforce'):
                sent = {stage for run, stage, _ in self.requests if run == '%s/%s' % (label, mode)}
                expected = {'relevance', 'extract', 'verify'} | ({'quality'} if mode != 'off' else set())
                self.assertEqual(sent, expected, (label, mode))

    def test_every_request_holds_only_model_visible_keys(self):
        for run, stage, content in self.requests:
            user = json.loads(content)
            self.assertEqual(list(user)[-1], 'response_schema', (run, stage))
            self.assertLessEqual(set(user) - {'response_schema'}, stages.MODEL_VISIBLE[stage]['top'], (run, stage))
            for comment in user.get('comments', []):
                self.assertLessEqual(set(comment), stages.MODEL_VISIBLE[stage]['comments'], (run, stage))

    def test_quality_requests_carry_no_program_context(self):
        quality = [json.loads(c) for _, stage, c in self.requests if stage == 'quality']
        self.assertTrue(quality)
        for user in quality:
            self.assertFalse({'source', 'quality_contract', 'attempt'} & set(user))

    def test_non_comment_characters_stay_within_the_budgets(self):
        self.assertEqual(set(BUDGETS), set(stages.MODEL_VISIBLE))
        for run, stage, content in self.requests:
            self.assertLessEqual(non_comment_characters(content), BUDGETS[stage], (run, stage))

    def test_the_count_excludes_only_comment_texts(self):
        user = {'comments': [{'comment_id': 'c', 'text': '平衡"', 'units': [{'evidence_id': 'E1', 'text': 'ab'}]}],
                'original_evidence': 'xyz', 'response_schema': {}}
        content = json.dumps(user, ensure_ascii=False)
        self.assertEqual(non_comment_characters(content),
                         len(content) - len('"平衡\\""') - len('"ab"') - len('"xyz"'))


if __name__ == '__main__':
    unittest.main()
