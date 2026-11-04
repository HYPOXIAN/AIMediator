"""Explicit-source adapter to the existing quality scorer."""
from . import evidence, evidence_quality
from .common import Failure, new_path, read, sha, write
from .quality_scoring import evaluate
from .review import load_run


def evaluate_quality(run, labels_path, out):
    data = load_run(run)
    if data['raw']['evidence_quality_mode'] == 'off':
        raise Failure(2, 'Quality=off has no quality predictions')
    labels = read(labels_path)
    if not isinstance(labels, list):
        raise Failure(2, 'Labels must be an annotation-template JSON array')
    required = {'comment_id','language','text_original','content_sha256','cluster_id','split','reviewer_type','source_stage'}
    for label in labels:
        if not isinstance(label, dict) or not required <= set(label):
            raise Failure(2, 'Label is missing schema/provenance fields')
        source = data['sources'].get(label['comment_id'])
        if not source or any(label[k] != source[k] for k in ('text_original','language')) or label['content_sha256'] != sha(source['text_original'].encode('utf-8')):
            raise Failure(4, 'Label source identity does not match the run')
        if label['reviewer_type'] not in ('human','silver','agent_authored_synthetic','unlabeled') or label['split'] not in ('development','test') or label['source_stage'] not in ('raw_pre_screen','screened','fixed_admission'):
            raise Failure(2, 'Invalid label provenance, split or source stage')
        if not isinstance(label['cluster_id'],str) or not label['cluster_id']:
            raise Failure(2, 'Label cluster_id is required')
        points = label.get('points')
        if points is not None and (not isinstance(points,list) or len({p['point_id'] for p in points}) != len(points)):
            raise Failure(2, 'Invalid or duplicate gold point IDs')
        if label.get('point_matches') is not None and points is None:
            raise Failure(2, 'Point matches require explicitly labeled gold points')
        segments = label.get('segments')
        if segments is not None:
            schema = evidence_quality.annotation_schema([label['comment_id']])['properties']['segments']
            if evidence_quality.schema_errors(segments, schema) or len({s['segment_id'] for s in segments}) != len(segments):
                raise Failure(2, 'Invalid gold segment schema or duplicate segment IDs')
            units = {u['evidence_id']: u for u in evidence.evidence_units(source['text_original'])}
            for segment in segments:
                unit = units.get(segment['evidence_id'])
                if not unit or not unit['start'] <= segment['start'] < segment['end'] <= unit['end']:
                    raise Failure(2, 'Gold segment is outside its source evidence unit')
        if points:
            segment_ids = {s['segment_id'] for s in segments or []}
            for point in points:
                if (not {'point_id', 'route', 'segment_ids'} <= set(point)
                        or not isinstance(point['point_id'], str) or not point['point_id']
                        or point['route'] not in evidence_quality.ROUTES
                        or not isinstance(point['segment_ids'], list) or not point['segment_ids']
                        or len(set(point['segment_ids'])) != len(point['segment_ids'])
                        or not set(point['segment_ids']) <= segment_ids):
                    raise Failure(2, 'Gold point requires unique same-source segment references')
        matches = label.get('point_matches')
        if matches is not None and (not isinstance(matches, list) or any(
                not isinstance(match, dict) or set(match) != {'gold_point_id', 'predicted_point_id'} for match in matches)):
            raise Failure(2, 'Invalid point match schema')
    try:
        result = evaluate(labels, data['quality'], {cid: cid in data['admitted'] for cid in data['sources']})
    except (KeyError,ValueError,TypeError) as exc:
        raise Failure(2, 'Quality evaluation rejected labels (' + type(exc).__name__ + ')') from None
    result.update(run_fingerprints=data['fingerprints'], execution_provenance=data['provenance'])
    out = new_path(out, run)
    out.mkdir(parents=True)
    write(out / 'evaluation.json', result)
    return out, {'labeled_comments': result['labeled_comments'], 'unlabeled_comments': result['unlabeled_comments']}
