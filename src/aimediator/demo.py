"""Authored bilingual fixtures injected through the real pipeline boundaries."""
from pathlib import Path
from .common import canonical, new_path, read, write
from .config import defaults
from .resources import asset_path
from .fixture_transport import FixtureTransport


def demo(out, quiet=False):
    from .operations import analyze
    from .review import export_review
    from .reporting import export_report
    out = new_path(out)
    out.mkdir(parents=True)
    cases = read(asset_path('fixtures/cases.json'))
    dataset = out / 'synthetic-input.jsonl'
    dataset.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))
    write(out / 'demo-provenance.json', {'execution': FixtureTransport.provenance, 'semantic_accuracy':None,
        'retrieval': 'fixture_vectors_all_admitted', 'source': 'authored_synthetic',
        'not_independent_human_labels':True})
    for mode in ('off','shadow','enforce'):
        cfg = defaults()
        cfg.update(evidence_quality=mode,base_url='http://fixture.invalid')
        analyze(dataset, out / mode, cfg, transport=FixtureTransport(cfg), quiet=quiet)
        write(out / mode / 'execution-provenance.json', {'execution': FixtureTransport.provenance,'semantic_accuracy':None})
    export_report(out / 'enforce', out / 'example-report')
    export_review(out / 'enforce', out / 'review-template')
    return out
