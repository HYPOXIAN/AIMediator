"""Engineering-brief readiness: player evidence kept apart from design prerequisites and hypotheses."""
import re


def validate_move_data(rows):
    seen=set()
    required={'character','target','patch_version','metric','current','unit','source_url','verified'}
    for row in rows:
        if set(row)!=required or row['verified'] is not True:
            raise ValueError('Move data needs exact required fields and verified=true')
        if any(not isinstance(row[k],str) or not row[k].strip() for k in required-{'verified'}):
            raise ValueError('Move data fields must be nonempty strings')
        if not row['source_url'].startswith(('https://','http://')):
            raise ValueError('Move data requires a reference URL')
        key=tuple(row[k] for k in ('character','target','patch_version','metric'))
        if key in seen:
            raise ValueError('Duplicate move data key')
        seen.add(key)


def quality_design_errors(claim):
    q = claim.get('evidence_quality') or {}
    errors = []
    if (q.get('mode') != 'enforce' or q.get('route') != 'mechanism_evidence'
            or q.get('schema_version') not in ('evidence-quality-v1', 'evidence-quality-v2')
            or q.get('comment_id') != claim.get('comment_id')):
        errors.append('mechanism_evidence_qualification_required')
    points, spans = q.get('selected_points', []), q.get('selected_segments', [])
    if (len(points) != 1 or not spans or q.get('point_ids') != claim.get('quality_point_ids')
            or q.get('point_ids') != [p.get('point_id') for p in points]
            or any(p.get('scope') != 'character_balance' or p.get('detail_level') != 'concrete'
                   or p.get('stance') == 'uncertain' for p in points)):
        errors.append('concrete_selected_point_required')
    if not (claim.get('semantic_audit') or {}).get('supported'):
        errors.append('selected_point_semantic_audit_required')
    for span in spans:
        matching = [e for e in claim.get('evidence', []) if e.get('evidence_id') == span.get('evidence_id')
                    and e.get('comment_id') == claim.get('comment_id')]
        if (type(span.get('start')) is not int or type(span.get('end')) is not int
                or not any(e['start'] <= span['start'] < span['end'] <= e['end']
                           and e['text'][span['start'] - e['start']:span['end'] - e['start']] == span.get('quote')
                           for e in matching)):
            errors.append('quality_source_binding_required')
    return errors


def prepare_briefs(claims, move_data=None, target_patch=None, pending_adjudication_ids=(), quality_mode=None):
    rows=move_data or []
    validate_move_data(rows)
    briefs=[]
    for claim in claims:
        blockers=[]
        identity=claim.get('character_identity',{})
        assessed = quality_mode == 'enforce' or 'evidence_quality' in claim or 'quality_point_ids' in claim
        quality_status = 'enforce' if assessed else 'legacy/quality_not_assessed'
        if assessed:
            blockers.extend(quality_design_errors(claim))
            if identity.get('normalization_status') != 'glossary_reference' or identity.get('canonical_name') != claim.get('character'):
                blockers.append('official_character_identity_unverified')
        if claim['comment_id'] in pending_adjudication_ids:
            blockers.append('source_annotation_adjudication_required')
        if not claim.get('source_review',{}).get('decision')=='accept':
            blockers.append('source_review_required')
        if identity.get('normalization_status')=='source_literal_unverified' or claim.get('character') is None:
            blockers.append('official_character_identity_unverified')
        if claim.get('uncertain') or claim['direction'] not in ('buff','nerf','keep'):
            blockers.append('source_intent_unresolved')
        if not claim.get('target'):
            blockers.append('exact_move_or_mechanic_required')
        if not re.search(r'\b(?:buff|nerf|strengthen|weaken|reduce|reduction|increase|improve|remove|change|adjust|keep|preserve|review|consider)\b|加强|削弱|降低|提高|改善|移除|调整|保持|保留|复核|评估',claim['recommendation'],re.I):
            blockers.append('engineering_action_text_required')
        if not target_patch:
            blockers.append('target_patch_required')
        matching=[r for r in rows if r['character']==claim['character'] and r['target']==claim.get('target') and r['patch_version']==target_patch]
        if not matching:
            blockers.append('matching_versioned_move_data_required')
        briefs.append({'claim_id':claim['claim_id'],'comment_id':claim['comment_id'],
            'quality_assessment':quality_status, 'source_request':claim,'target_patch':target_patch,'verified_move_data':matching,
            'readiness':'blocked' if blockers else 'ready_for_engineering_design',
            'blockers':blockers,'engineering_hypotheses':[],
            'validation_plan':['Check matchup-specific effects and resource conditions.',
                'Test combos, punish windows and defensive counterplay before/after.',
                'Compare relevant skill brackets and preserve opposing source opinions.'],
            'release_status':'not_approved_for_game_changes'})
    return {'stage':'engineering_design_preparation','source_requests_unchanged':True,
        'summary':{'briefs':len(briefs),'ready':sum(b['readiness']=='ready_for_engineering_design' for b in briefs),
            'blocked':sum(b['readiness']=='blocked' for b in briefs)},'briefs':briefs,
        'design_contract':{'hypothesis_fields':['assumption','parameter_changes','design_rationale','versioned_data_references','expected_effect','test_plan','validation_result'],
            'rule':'Each hypothesis must be explicitly labeled engineering design, never a player quote. Readiness is not tuning correctness or release approval.'}}
