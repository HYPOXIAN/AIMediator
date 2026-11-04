"""Coarse balance-relevance screening: deterministic rules, boundary overrides and the screening tool."""
import functools
import json
from pathlib import Path
import re

from ..resources import glossary, workspace_root
ROOT=workspace_root()


@functools.lru_cache(maxsize=1)
def _char_en():
    """Return the English character-name pattern, built from the packaged glossary on first use."""
    names=[e['canonical_name'] for e in glossary()['entries'] if e['category']=='character']+['Arjun','Viper','Bison','Akuma','Gouki','Gief','Honda','Deejay','Chun','Luke','Guile','Cammy']
    return re.compile(r'\b(?:'+ '|'.join(re.escape(x) for x in names)+r')\b',re.I)


CHAR_ZH=re.compile('隆|卢克|傑米|杰米|春丽|春麗|古烈|盖尔|蓋爾|朱莉|蛛俐|肯|布兰卡|布蘭卡|达尔西姆|達爾錫|本田|迪杰|迪傑|曼侬|曼儂|玛丽莎|瑪麗莎|桑吉|莉莉|嘉米|嘉蜜|阿鬼|豪鬼|维加|維加|特瑞|不知火舞|艾琳娜|沙加特|沙盖特|毒蛇|阿里克斯|英格丽德|雅思敏|阿俊|阿军|印度人|阿三|老桑|将军|將軍|警察|狮子|獅子|阿光|阿杜')
GAME=re.compile(r'\bsf\s*6\b|street\s*fighter|街霸|街头霸王|街頭霸王|快打旋風|ストリートファイター',re.I)
OTHER=re.compile(r'\b(?:tekken|mortal kombat|mk1|mk11|guilty gear|dragon ball|league of legends|elden ring|cyberpunk|gta|yakuza|batman|zelda|granblue)\b|铁拳|鐵拳|真人快打|英雄联盟|英雄聯盟|蠻王|蛮王|黑客.{0,20}义体|银手|魔强统一战',re.I)
EXPLICIT=re.compile(r'\b(?:balanc(?:e|ed|ing)|unbalanced|imbalanced|overpowered|underpowered|overtuned|undertuned|nerf(?:ed|s|ing)?|buff(?:ed|s|ing)?|pay[ -]?to[ -]?win|p2w|power[ -]?creep|top[ -]?tier|low[ -]?tier|bottom[ -]?tier|tier[ -]?list|win[ -]?rate|desbalancead\w*|balanceamento)\b|平衡|超模|超標|超标|强度|強度|削弱|加强|加強|下水道|毒瘤|粪角|糞角|三体人|三體人|轮椅|輪椅|数值怪|數值怪|付费.{0,3}(?:赢|赢)|付費.{0,3}贏|版本之子|人权卡|人權卡|(?:还|還|不|该|該|要|紧急|緊急|被|先|得|需要).{0,2}[削砍]|赢麻|贏麻',re.I)
MECH=re.compile(r'\b(?:drive[ -]?(?:rush|impact|reversal|gauge)|burn[ -]?out|perfect[ -]?parr\w*|parr(?:y|ies|ying)|chip[ -]?damage|hit[ -]?box|hurt[ -]?box|frame[ -]?(?:data|advantage|trap|[+−-])|plus[ -]?(?:on[ -]?)?block|minus[ -]?(?:on[ -]?)?block|block[ -]?string|mix[ -]?ups?|match[ -]?ups?|zoning|projectiles?|fire[ -]?balls?|invincib\w*|armou?r|command[ -]?grabs?|throw[ -]?(?:loops?|tech)|drive[ -]?system|strike[ -]?throw|corner[ -]?carry|neutral|damage[ -]?(?:scaling|penalty|output)|input[ -]?delay|input[ -]?reading|auto[ -]?combos?|one[ -]?(?:buttons?|inputs?)|reaction[ -]?(?:time|super)|anti[ -]?airs?)\b|斗气|鬥氣|斗氣|斗技|綠衝|绿冲|绿冲|绿防|綠防|红冲|紅衝|红防|紅防|迸放|猛冲|猛衝|气槽|氣槽|白血|削血|霸体|霸體|确反|確反|拆投|投循环|投循環|(?:二|两|兩|三|四|混|打|猜|起身)[择擇]|压起身|壓起身|压制|壓制|打投|投技|指令投|判定|帧数|幀數|加帧|加幀|负帧|負幀|无敌|無敵|中段|下段|差合|波升|飞道|飛道|一键|一鍵|自动连|自動連|輔助連|辅助连|现代.{0,10}(?:伤害|反应|反應|对空|對空)|現代.{0,10}(?:傷害|反應|對空)|伤害|傷害|搓招|昇龍|升龙|升龍|防空|防禦|防御',re.I)
QUAL=re.compile(r'\b(?:too|unfair|advantage|disadvantage|strong\w*|weak\w*|broken|busted|cheap|abuse|abusing|spam\w*|punish\w*|reward\w*|risk|safe|unsafe|react\w*|counter\w*|defen[cs]\w*|offen[cs]\w*|domin\w*|oppressive|frustrat\w*|annoy\w*|brain[ -]?dead|unblockable|unavoidable|unbeatable|over.?tuned|skill[ -]?gap|without[ -]?skill|no[ -]?skill|100[ -]?percent|infinite|damage|health|fair)\b|太|过强|過強|过弱|過弱|无脑|無腦|赖|賴|逆天|摸奖|摸獎|摸一下|暴打|吊打|碾压|碾壓|爆杀|爆殺|垃圾|恶心|噁心|恶臭|壓力|压力|不合理|合理|不公平|公平|高手|劣势|劣勢|优势|優勢|崩|没法|沒法|不能|无解|無解|反应|反應|猜拳|罚|罰|提款|半血|三分之一|伤害|傷害|回报|回報|风险|風險|乱杀|亂殺|简单|簡單',re.I)
STRENGTH=re.compile(r'\b(?:too[ -]?(?:strong|weak)|stronger|weaker|overpowered|underpowered|over[ -]?tuned|under[ -]?tuned|broken|busted|cheap|unfair|brain[ -]?dead|oppressive|dominat\w*|overrated|underrated|carry|carries|carried)\b|太强|太強|太弱|过强|過強|过弱|過弱|无脑|無腦|逆天|暴打|吊打|碾压|碾壓|爆杀|爆殺|数值|數值|(?:角色|招式|技能).{0,12}(?:强|強|弱)|不公平|不合理|性能',re.I)
SOLO=re.compile(r'world[ -]?tour|single[ -]?player|story[ -]?mode|arcade[ -]?mode|\bNPCs?\b|boss[ -]?fight|世界巡游|世界巡遊|环球|環球|单人|單人|剧情|劇情|剧情|RPG|開放世界|开放世界',re.I)
PVP=re.compile(r'\bpvp\b|ranked|competitive|multiplayer|online[ -]?(?:match|battle|play)|对战|對戰|排位|天梯|人机以外|玩家对|玩家對|真人|人與人|人和人',re.I)
TECH=re.compile(r'netcode|\bping\b|connection|disconnect|matchmaking|lag(?:gy)?|stutter|crash|server|queue|cheaters?|hacker|smurf|匹配|配对|配對|延迟|延遲|掉线|掉線|网络|網路|网络|服务器|伺服器|连不上|連不上|外挂|外掛|炸房|闪退|閃退|卡顿|卡頓',re.I)
COMBAT_MECH=re.compile(r'drive[ -]?(?:rush|impact|reversal)|burn[ -]?out|parr(?:y|ying)|hit[ -]?box|hurt[ -]?box|frame|damage|mix[ -]?up|match[ -]?up|zoning|command[ -]?grab|throw[ -]?loop|气槽|氣槽|白血|压制|壓制|确反|確反|判定|帧|幀|伤害|傷害|霸体|霸體|搓招|对空|對空|现代|現代|经典|經典',re.I)
CONTROL=re.compile(r'\bmodern\b|classic[ -]?controls?|control[ -]?scheme|现代|現代|经典|經典|一键|一鍵|辅助|輔助',re.I)
META=re.compile(r'\bIGN\b|reviewer|great review|good review|nice review|thanks for (?:the |this )?review|subscrib|your channel|review score|评分|評分|评测|評測|测评|測評|讲解|講解|up主|博主|订阅|訂閱|留言',re.I)
SHOP=re.compile(r'\b(?:price|buy|bought|purchase|sale|expensive|money|cost|dollars?|denuvo|monetiz\w*|microtransaction|battle[ -]?pass)\b|价格|價格|售价|售價|買|买|花钱|花錢|氪金|付费|付費|通行证|通行證|光碟|实体|實體|季票',re.I)
PRESENTATION=re.compile(r'graphics|soundtrack|music|art[ -]?style|costume|outfit|animation|story|visual|画面|畫面|建模|美术|美術|皮肤|皮膚|音乐|音樂|剧情|劇情|服装|服裝|丝袜|絲襪|屁股|大腿|性感',re.I)
GAMEPLAY=re.compile(r'gameplay|mechanics?|controls?|combos?|learn|beginner|tutorial|difficulty|fighting|格斗|格鬥|连招|連招|入门|入門|操作|学习|學習|手柄|摇杆|搖桿|键盘|鍵盤|难度|難度|上手',re.I)
SPECIFIC=re.compile(r'\b(?:hit[ -]?box|hurt[ -]?box|frame[ -]?(?:data|advantage|trap)|damage[ -]?(?:scaling|penalty)|plus on block|minus on block|throw[ -]?loop|command[ -]?grab|chip[ -]?damage)\b|确反|確反|加帧|加幀|负帧|負幀|投循环|投循環|白血|三体人|三體人',re.I)


def classify_rules(row):
 text=row['text_original'];char=bool(_char_en().search(text) or CHAR_ZH.search(text));game=bool(GAME.search(text));explicit=EXPLICIT.search(text);mech=MECH.search(text);qual=QUAL.search(text)
 if re.search(r'top[ -]?tier.{0,16}(?:editing|thumbnail|reviewing|video production)',text,re.I) and not COMBAT_MECH.search(text) and not char:return 'exclude','creator_video_or_review_meta_discussion',[]
 if re.search(r'(?:balance.{0,60}nostalgia|nostalgia.{0,90}balance)',text,re.I) and not COMBAT_MECH.search(text):return 'exclude','presentation_cosmetics_or_story',[]
 if explicit and re.search(r'(?:buff|nerf).{0,20}(?:graphics|soundtrack|outfits?|visuals?)',text,re.I) and not COMBAT_MECH.search(text) and not char:return 'exclude','presentation_cosmetics_or_story',[]
 if OTHER.search(text) and not game and not char and not COMBAT_MECH.search(text):return 'exclude','other_game_or_unrelated_reference',[]
 if SOLO.search(text) and not PVP.search(text) and not explicit:return 'exclude','single_player_story_or_pve_difficulty',[]
 if explicit:
  return 'keep','explicit_balance_or_strength_claim',[explicit.group()]
 if char and STRENGTH.search(text):
  return 'keep','character_strength_or_matchup_claim',[STRENGTH.search(text).group()]
 if SPECIFIC.search(text):return 'keep','specific_competitive_mechanic',[SPECIFIC.search(text).group()]
 if mech and qual and (COMBAT_MECH.search(text) or CONTROL.search(text)):
  return 'keep','competitive_mechanic_with_claim',[mech.group(),qual.group()]
 if mech and not META.search(text) and not (SHOP.search(text) or PRESENTATION.search(text) or SOLO.search(text)):
  return 'review','combat_mechanic_without_clear_balance_claim',[mech.group()]
 if char and re.search(r'\bhate\b|\bspam\w*\b|恶心|噁心|垃圾|大变|大變|体验|體驗',text,re.I) and not PRESENTATION.search(text):return 'review','character_complaint_without_clear_reason',[]
 if TECH.search(text):return 'exclude','technical_network_matchmaking_or_cheating',[]
 if META.search(text):return 'exclude','creator_video_or_review_meta_discussion',[]
 if SHOP.search(text):return 'exclude','purchase_price_or_monetization_without_balance',[]
 if SOLO.search(text):return 'exclude','single_player_story_or_pve_content',[]
 if PRESENTATION.search(text):return 'exclude','presentation_cosmetics_or_story',[]
 if GAMEPLAY.search(text):return 'exclude','general_gameplay_learning_without_balance_claim',[]
 return 'exclude','generic_reaction_or_insufficient_game_balance_evidence',[]


def classify(row, overrides=None):
    import hashlib
    override=(overrides or {}).get(row['record_id'])
    if override:
        digest=hashlib.sha256(row['text_original'].encode()).hexdigest()
        if digest!=override['text_sha256']:
            raise ValueError('Source text changed for a reviewed boundary record; reassess its override: '+row['record_id'])
        return override['decision'],override['reason'],[],'agent_boundary_review'
    decision,reason,signals=classify_rules(row)
    return decision,reason,signals,'rules'


def load_sources(folder):
    import hashlib
    files=sorted(folder.glob('*.jsonl'))
    if not files:
        raise ValueError('No input JSONL files found')
    union={};members={};hashes={}
    for path in files:
        hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
        ids=[]
        for line in path.read_text(encoding='utf-8').splitlines():
            row=json.loads(line)
            identity=row['record_id']
            if not isinstance(row['text_original'],str):
                raise ValueError('Non-text evidence: '+identity)
            if identity in union and union[identity]!=row:
                raise ValueError('Conflicting copies of a record across input views: '+identity)
            if identity in ids:
                raise ValueError('Duplicate ID within input view: '+path.name)
            union[identity]=row;ids.append(identity)
        members[path.name]=ids
    return union,members,hashes


def write_rows(path, rows):
    temporary=path.with_suffix(path.suffix+'.tmp')
    with temporary.open('w',encoding='utf-8') as stream:
        for row in rows:
            stream.write(json.dumps(row,ensure_ascii=False)+'\n')
    temporary.replace(path)


def main():
    import argparse,collections,datetime as dt,hashlib
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--language-corrections',type=Path)
    parser.add_argument('--overrides',type=Path,default=ROOT/'configs/feedback-screening-overrides.json')
    args=parser.parse_args();output=args.output or args.input/'screened'
    if output.resolve()==args.input.resolve():
        parser.error('Output must differ from the original source directory')
    union,members,hashes=load_sources(args.input)
    raw_overrides=json.loads(args.overrides.read_text(encoding='utf-8'))['entries'] if args.overrides.exists() else []
    overrides={r['record_id']:r for r in raw_overrides}
    if len(overrides)!=len(raw_overrides):
        raise ValueError('Duplicate boundary override IDs')
    language_corrections={r['record_id']:r for r in json.loads(args.language_corrections.read_text(encoding='utf-8'))['entries']} if args.language_corrections else {}
    tagged={};decisions=[]
    for identity,row in union.items():
        decision,reason,signals,method=classify(row,overrides)
        result={'version':'coarse-v1','decision':decision,'reason':reason,'signals':signals,'method':method,'text_sha256':hashlib.sha256(row['text_original'].encode()).hexdigest(),'human_review':'pending'}
        correction=language_corrections.get(identity)
        language=row['language']
        if correction:
            if correction['text_sha256']!=result['text_sha256']:
                raise ValueError('Stale language correction: '+identity)
            language=correction['language']
            result['language_correction']={'original_label':row['language'],'corrected_label':language,'reason':correction['reason'],'method':'agent_text_inspection'}
        tagged[identity]={**row,'language':language,'coarse_screening':result}
        decisions.append({'record_id':identity,'platform':row['platform'],'language':language,**result,'reviewer':'','human_decision':'','notes':''})
    output.mkdir(parents=True,exist_ok=True)
    file_stats={}
    for name,ids in members.items():
        view_ids=ids
        if args.language_corrections and name in ('english.jsonl','chinese.jsonl'):
            view_language='en' if name=='english.jsonl' else 'zh'
            view_ids=[i for i in tagged if tagged[i]['language']==view_language]
        subset=[tagged[i] for i in view_ids if tagged[i]['coarse_screening']['decision']=='keep']
        write_rows(output/name,subset)
        file_stats[name]={'input':len(ids),'keep':len(subset),'review':sum(tagged[i]['coarse_screening']['decision']=='review' for i in view_ids),'exclude':sum(tagged[i]['coarse_screening']['decision']=='exclude' for i in view_ids),'normalized_view_records':len(view_ids)}
    kept=[r for r in tagged.values() if r['coarse_screening']['decision']=='keep']
    excluded=[r for r in tagged.values() if r['coarse_screening']['decision']=='exclude']
    review=[r for r in tagged.values() if r['coarse_screening']['decision']=='review']
    if 'records.jsonl' not in members:
        write_rows(output/'records.jsonl',kept)
    write_rows(output/'excluded.jsonl',excluded)
    write_rows(output/'needs-review.jsonl',review)
    write_rows(output/'decisions.jsonl',decisions)
    assert len(kept)+len(excluded)+len(review)==len(union)
    assert len({r['record_id'] for r in kept+excluded+review})==len(union)
    assert all(hashlib.sha256((args.input/name).read_bytes()).hexdigest()==digest for name,digest in hashes.items())
    for r in tagged.values():
        assert r['text_original']==union[r['record_id']]['text_original']
    summary={'screened_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'version':'coarse-v1','method':'Deterministic rules with record-specific agent boundary corrections; no LLM or network requests. Not a human-validated benchmark.','unique_records':len(union),'counts':{'keep':len(kept),'review':len(review),'exclude':len(excluded)},'kept_by_language':dict(collections.Counter(r['language'] for r in kept)),'kept_by_platform':dict(collections.Counter(r['platform'] for r in kept)),'counts_by_platform':{p:dict(collections.Counter(r['coarse_screening']['decision'] for r in tagged.values() if r['platform']==p)) for p in sorted({r['platform'] for r in tagged.values()})},'reason_counts':dict(collections.Counter(r['reason'] for r in decisions)),'input_files':file_stats,'source_sha256':hashes,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'override_sha256':hashlib.sha256(args.overrides.read_bytes()).hexdigest() if args.overrides.exists() else None,'agent_boundary_overrides_applied':sum(r['method']=='agent_boundary_review' for r in decisions),'source_files_unchanged':True,'original_text_unchanged':True,'patch_filtering':False,'language_filtering':False,'human_review_fields_blank':True}
    summary['language_corrections_applied']=len(set(language_corrections)&set(union))
    summary['language_corrections_sha256']=hashlib.sha256(args.language_corrections.read_bytes()).hexdigest() if args.language_corrections else None
    summary['original_fields_unchanged_except_explicit_language_corrections']=True
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Coarse Balance Relevance Screening','','Scope: Street Fighter 6 competitive character/system balance. Original source files and text are unchanged. All five overlapping input views were classified once per stable source ID.','','Keep: explicit balance/strength opinions, requested buffs/nerfs, concrete offensive/defensive mechanics, matchup/resource/risk-reward claims, and Modern/Classic competitive fairness. Favorable, negative, sarcastic, and emotional balance opinions can all be retained.','','Exclude: unrelated games without an SF6 claim; shopping/price-only discussions; cosmetics, visuals, music, story and PvE-only content; network/crash/matchmaking-only issues; video/creator discussion; general learning/accessibility praise; generic reactions without a balance claim. Mixed reviews remain intact when a relevant balance claim exists.','','Review: potentially relevant but under-specified character/control complaints and ambiguous mechanic-only mentions. These are not included in the kept files.','','No date, patch, character-roster, sentiment, language/script, toxicity, truthfulness, or authenticity filter was applied. Inclusion does not confirm the claimed mechanic is true. Some records concern later patches. Original language labels are inherited and unverified.','','Rules and boundary corrections are coarse judgments, not a measured semantic-accuracy guarantee or human-approved labels. A human should still review the kept material and the separate uncertain set.','',f"Unique records: {len(union)}; kept: {len(kept)}; excluded: {len(excluded)}; needs review: {len(review)}.",'','## Output views','']
    if args.language_corrections:lines+=['', 'Explicit inspected language-label corrections were applied only to output copies. Original raw labels/text are unchanged; language_correction preserves old labels and reasons. English/Chinese views are rebuilt from corrected labels, so source-view input counts can differ from normalized output-view counts. Other unverified language labels are inherited.', '']
    for name,counts in file_stats.items():lines.append(f"- {name}: {counts['input']} input -> {counts['keep']} kept; {counts['exclude']} excluded; {counts['review']} needs review.")
    lines+=['','Do not sum overlapping language/platform views. Use records.jsonl as the canonical kept dataset. excluded.jsonl retains reversible exclusions with reasons; decisions.jsonl records every decision; needs-review.jsonl is the uncertain set. YouTube-derived files inherit their original refresh/delete obligations.','','## Human review','','Reviewer:','Decision:','Notes:','','## Uncertain records','']
    for row in review:
        lines += [f"### {row['record_id']}",'',f"Source: {row['source_url']}",'',f"Reason: {row['coarse_screening']['reason']}",'','Original text:','']+['> '+line for line in row['text_original'].splitlines()]+['','Reviewer:','Decision:','Notes:','']
    (output/'review.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['unique_records','counts','kept_by_language','kept_by_platform','input_files','agent_boundary_overrides_applied']},ensure_ascii=False,indent=2))

