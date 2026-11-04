from pathlib import Path
import sys
import types
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from aimediator.collection import expansion


class ExpansionTests(unittest.TestCase):
    def test_target_counts_use_kept_records_not_raw_volume(self):
        store=types.SimpleNamespace(rows=[
            {'record_id':'test:1','language':'en','text_original':'Ryu needs a nerf.'},
            {'record_id':'test:2','language':'en','text_original':'Great video!'},
            {'record_id':'test:3','language':'en','text_original':'Drive impact'},
            {'record_id':'test:4','language':'zh','text_original':'这游戏平衡很好'},
        ])
        self.assertEqual(dict(expansion.kept_counts(store,{})),{'en':1,'zh':1})

    def test_stale_boundary_overrides_stop_before_counting_as_kept(self):
        store=types.SimpleNamespace(rows=[{'record_id':'test:1','language':'en','text_original':'changed'}])
        with self.assertRaises(ValueError):
            expansion.kept_counts(store,{'test:1':{'text_sha256':'stale','decision':'keep','reason':'previous decision'}})


if __name__=='__main__':
    unittest.main()
