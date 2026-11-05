"""Shared live extract, ground and audit loop of the research diagnostics; returns neutral records."""
from .evidence import character_reference, evidence_units, ground_claim
from .evidence_quality import bind_claim


def extract(runner, model, language, row, *, allowed_points=None):
    """Send the extraction request for one source row and return (parsed, meta); the model sees its extraction view."""
    text = row['text_original']
    comment = {'comment_id': row['record_id'], 'units': evidence_units(text)}
    if allowed_points is not None:
        comment['allowed_quality_points'] = allowed_points
    data = {'comments': [comment], 'character_normalization_reference': character_reference(text)}
    return runner.generate(model, language, 'extract', data, [row['record_id']])


def audit(runner, model, language, row, claims, characters, *, quality_record=None):
    """Ground each claim, bind it when a quality record is given, and audit it only when no error remains."""
    text = row['text_original']
    records = []
    for index, claim in enumerate(claims, 1):
        errors, enriched = ground_claim(claim, row, characters)
        if quality_record is not None:
            bound, qualification = bind_claim(claim, quality_record, character_reference(text))
            errors += bound
            if enriched:
                enriched['evidence_quality'] = qualification
        verdict, audit_meta = None, None
        if not errors:
            claim_id = row['record_id'] + ':' + str(index)
            envelope = {'claim_id': claim_id, 'comment_id': row['record_id'], 'claim': enriched}
            parsed, audit_meta = runner.generate(model, language, 'verify',
                                                 {'claims': [envelope], 'original_comment': text}, [claim_id])
            verdict = parsed['verdicts'][0] if parsed else None
        records.append({'index': index, 'claim': claim, 'enriched': enriched, 'errors': errors,
                        'audit': verdict, 'audit_meta': audit_meta})
    return records
