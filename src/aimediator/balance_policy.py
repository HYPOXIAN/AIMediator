"""Conservative identity, retrieval triage and numeric-request safety boundaries.

These checks can require additional review. They do not prove semantic entailment.
"""
import json
from functools import lru_cache
from pathlib import Path
import re

from .resources import asset_path
ROOT = asset_path()
POLICY_PATH = asset_path('configs/balance-review-policy.json')


@lru_cache(maxsize=1)
def load_policy():
    return json.loads(POLICY_PATH.read_text(encoding='utf-8'))


def term_matches(term, text):
    if not term:
        return False
    if re.search('[A-Za-z]', term):
        return re.search(r'(?<![A-Za-z])' + re.escape(term) + r'(?![A-Za-z])', text, re.I) is not None
    return term in text


def identity_alias_allowed(alias):
    return alias.casefold() not in {a.casefold() for a in load_policy()['blocked_identity_only_aliases']}


def numeric_request_supported(text, parameter):
    """Require a local requested-change cue, beyond merely matching quantities.

    Returns a conservative admissibility result; ambiguous wording goes to review.
    No current/target value is inferred or repaired here.
    """
    values = [parameter.get(k) for k in ('proposed', 'delta') if parameter.get(k)]
    if not values:
        return False
    clauses = re.split(r'[;；。!?！？\n,，]', text)
    for clause in clauses:
        if not all(value in clause for value in values):
            continue
        if re.search(r'\b(?:used to|previously|last patch|already|we reduced|we increased)\b|上次|上个版本|此前|已经|曾经|已被', clause, re.I):
            continue
        if re.search(r'\b(?:do not|don.t|never|should not|shouldn.t)\b.*\b(?:reduce|increase|change|nerf|buff)\b|不要.*(?:降低|增加|改|削|加强)', clause, re.I):
            continue
        en_change = re.search(r'\b(?:reduce|increase|lower|raise|change|set|add|remove|make|cost|take|buff|nerf)\b', clause, re.I)
        en_target = re.search(r'\b(?:from|to|by|at|additional|less|more)\b', clause, re.I)
        en_request = re.search(r'\b(?:please|should|must|need|want|wish|would|suggest|prefer|let.s)\b', clause, re.I)
        imperative = re.match(r'\s*(?:please\s+)?(?:reduce|increase|lower|raise|change|set|add|remove|make|buff|nerf)\b', clause, re.I)
        if en_change and en_target and (en_request or imperative):
            return True
        # "it should take 2 hits" is a target request even without "to/by".
        if en_request and re.search(r'\b(?:take|cost|be)\s+[+-]?\d', clause, re.I):
            return True
        zh_change = re.search(r'降低|减少|提高|增加|加|减|改成|改为|改到|降到|升到|移除|取消', clause)
        zh_request = re.search(r'请|希望|建议|应该|应当|能不能|最好|不如|给|把|将', clause)
        if zh_change and zh_request:
            return True
    return False


def direction_action_conflicts(claim):
    """Catch explicit action/tag reversals without inferring frame effects."""
    text = claim['recommendation'].strip()
    buff_action = re.match(r'(?:please\s+|consider\s+)?(?:buff|strengthen)\b|(?:请|建议|考虑)?加强', text, re.I)
    nerf_action = re.match(r'(?:please\s+|consider\s+)?(?:nerf|weaken)\b|(?:请|建议|考虑)?削弱', text, re.I)
    return bool((buff_action and claim['direction']=='nerf') or (nerf_action and claim['direction']=='buff'))


def attributed_candidates(text, reference, candidates):
    """Exclude explicit cosmetic-only mentions and unambiguous damage recipients.

    Conservative source grammar only. This does not resolve general comparisons
    or sarcasm; omitted mentions remain available in the full original source.
    """
    # The term list of evidence.character_terms, built here because evidence imports this module.
    terms = {e['canonical_name']: list(dict.fromkeys(t for t in
             [e['canonical_name'], e.get('chinese_label')] + [a['text'] for a in e['aliases']]
             if t and term_matches(t, text))) for e in reference if e['canonical_name'] in candidates}
    units = re.split(r'\r?\n+|[。!?！？]+|\.(?=\s|$)', text)
    cosmetic = r'\b(?:cute|costumes?|outfits?|looks?|skins?|roster|lineup|where.?s|poster|teeth|white.washed)\b|外观|衣服|服装|皮肤|好看|可爱|阵容|客串|联动'
    strength = r'\b(?:buff|nerf|weak|strong|overpowered|underpowered|broken|unbalanced|damage|frames?|startup|recovery)\b|加强|削弱|太强|太弱|强度|伤害|帧|平衡|无敌|赖'
    excluded = {}
    for name, aliases in terms.items():
        mentions = [unit for unit in units if any(term_matches(t, unit) for t in aliases)]
        if mentions and all(re.search(cosmetic, unit, re.I) and not re.search(strength, unit, re.I) for unit in mentions):
            excluded[name] = 'explicit_cosmetic_or_roster_only_mentions'
    for actor, actor_terms in terms.items():
        for victim, victim_terms in terms.items():
            if actor == victim:
                continue
            for a in actor_terms:
                for v in victim_terms:
                    relation = re.search(re.escape(a) + r'(?:的)?(?:一招|一拳|一脚|一套)给(?:我)?' + re.escape(v) + r'(?:打|造成)', text)
                    relation = relation or re.search(re.escape(a) + r'\s+(?:hits?|grabs?|damages?)\s+(?:my\s+)?' + re.escape(v) + r'\b', text, re.I)
                    independent = re.search(r'(?:加强|削弱|buff\s+|nerf\s+)' + re.escape(v), text, re.I) or re.search(re.escape(v) + r'.{0,12}(?:太强|太弱|需要加强|需要削弱|too weak|too strong)', text, re.I)
                    if relation and not independent and len(re.findall(re.escape(v), text, re.I)) == 1:
                        excluded[victim] = 'explicit_recipient_not_attack_subject'
    return [name for name in candidates if name not in excluded], excluded


def explicit_numeric_request(text):
    # Used only to nominate a source for relevance review, never to admit it.
    values = re.findall(r'[+-]?\d+(?:\.\d+)?%?|[一二三四五六七八九十百]+', text)
    return any(numeric_request_supported(text, {'proposed': value}) for value in values)


def triage_retrieval(row, text, margin=0.04):
    if row['positive_score'] > row['negative_score']:
        return 'candidate', ['positive_topic_margin']
    reasons = []
    if abs(row['positive_score'] - row['negative_score']) <= margin:
        reasons.append('borderline_topic_margin')
    if explicit_numeric_request(text):
        reasons.append('explicit_numeric_request')
    return ('review_queue', reasons) if reasons else ('unrelated', ['negative_topic_margin'])


def retrieval_review_agrees(retrieved, review):
    # A queued source needs an affirmative *retrieval relevance review* and a
    # separate model relevance verdict. Nomination itself never grants admission.
    retrieval_pass = retrieved.get('retrieval_related') is True or (
        retrieved.get('retrieval_triage') == 'review_queue'
        and retrieved.get('retrieval_review_related') is True
        and retrieved.get('retrieval_review_uncertain') is False)
    return retrieval_pass and review.get('related') is True and review.get('uncertain') is False
