# Low-alias move review

Searched on 2026-10-22. 293 moves across 31 characters; 594 proposed alias mappings. All decisions are blank. Runtime data and selected aliases are unchanged.

## Selection and evidence

Explicit aliases only, excluding canonical English name and Chinese label; count <= 1. Character Special/Unique/Throw Move and universal Normal Move categories; Super Arts checked separately.

The cutoff counts the aliases displayed in docs/glossary.md, not the canonical and reference-translation records stored in JSON. Wrapped lines are joined before counting. Character State, system mechanics, directions and tactics are outside the move scope. Super Arts have more than one displayed alias and do not qualify. Unique and Normal Move sections were checked and have no qualifying rows.

[SPMoves Chinese command list](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html) was inspected across all 31 character sections. Match each move by its existing Chinese label within the corresponding character. This is a community command reference, not official alias usage evidence. Capcom Luke movelist access returned HTTP 403. No numerical balance data were imported.

Most additions are **editorial_notation_candidate**: compact numerical inputs and Chinese button/direction renderings derived from the inspected command list. They are proposed searchable forms, not independently attested nicknames. Two no-button/automatic transitions use editorial_description_candidate labels instead of invented commands. Conditions and prerequisite branches must be reviewed; do not match bare P/K or generic throw inputs globally. An automatic transition is not a separately executable move.

The smaller set of source-observed names is labeled separately. Search excerpts attest wording only, not frequency or final mapping. Legacy names require an SF6 applicability check. The reference page was updated after the target patch; all patch-dependent inputs remain unverified for 08.03.2026.

Review each candidate using `accept`, `reject`, or `revise`, plus reviewer and notes. This document and [structured review records](low-alias-review.json) are a pending staging area; neither is loaded by the application. Apply approved selections to the glossary in a separate step. Existing pending reviews are preserved.

## Ryu

### Shoryuken / 升龙拳

- Entry: `ryu.shoryuken`
- Existing aliases (1): 升龙
- Context: Require Ryu and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: p
  - Reviewer:
  - Notes:

### Hashogeki / 波掌击

- Entry: `ryu.hashogeki`
- Existing aliases (1): 波掌
- Context: Require Ryu and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: p
  - Reviewer:
  - Notes:

### Shoulder Throw / 背负投

- Entry: `ryu.forward_throw`
- Existing aliases (1): 前投
- Context: Require Ryu and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: p
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: p
  - Reviewer:
  - Notes:

### Somersault Throw / 巴投

- Entry: `ryu.back_throw`
- Existing aliases (1): 后投
- Context: Require Ryu and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: p
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Luke

### Sand Blast / 砂爆

- Entry: `luke.special.sand_blast`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: 发波
  - Kind: community_attested_candidate
  - Source: [reference](https://www.taptap.cn/moment/292028933610671843); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `Sand Blaster`
  - Kind: legacy_name_candidate
  - Source: [reference](https://streetfighter.fandom.com/wiki/Sand_Blaster); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:

### Fatal Shot / 致命射击

- Entry: `luke.special.fatal_shot`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 砂爆; confirm the exact intermediate branch before acceptance.
- Candidate: OD波
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: np
  - Reviewer:
  - Notes:

### DDT / 深度死亡摔

- Entry: `luke.special.ddt`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 迅闪指节拳; confirm the exact intermediate branch before acceptance.
- Candidate: DDT
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: np
  - Reviewer:
  - Notes:

### Aerial Flash Knuckle / 空中迅闪指节拳

- Entry: `luke.special.aerial_flash_knuckle`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `直跳或前跳 214P > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `直跳或前跳 ↓↙←拳 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Avenger / 复仇者

- Entry: `luke.special.avenger`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### No Chaser / 勇往直前

- Entry: `luke.special.no_chaser`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 复仇者; confirm the exact intermediate branch before acceptance.
- Candidate: 肩撞
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: p
  - Reviewer:
  - Notes:
- Candidate: `拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision: np
  - Reviewer:
  - Notes:

### Impaler / 穿刺者

- Entry: `luke.special.impaler`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 复仇者; confirm the exact intermediate branch before acceptance.
- Candidate: 翻腿
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Rising Uppercut / 上升勾拳

- Entry: `luke.special.rising_uppercut`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Slam Dunk / 灌篮

- Entry: `luke.special.slam_dunk`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 上升勾拳; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆版中 PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sweeper / 扫摔

- Entry: `luke.throw.sweeper`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Scrapper / 拳击手

- Entry: `luke.throw.scrapper`
- Existing aliases (0): (none)
- Context: Require Luke and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Jamie

### Freeflow Strikes / 流醉拳

- Entry: `jamie.special.freeflow_strikes`
- Existing aliases (1): rekka
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P > 6P > 6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳 > →拳 > →拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Arrow Kick / 挽弓腿

- Entry: `jamie.special.arrow_kick`
- Existing aliases (1): DP
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Luminous Dive Kick / 无影踢

- Entry: `jamie.special.luminous_dive_kick`
- Existing aliases (0): (none)
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `醉意1 前跳 214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `醉意↙ 前跳 ↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `无影脚`
  - Kind: community_attested_candidate
  - Source: [reference](https://www.taptap.cn/moment/292028933610671843); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:

### Bakkai / 爆回

- Entry: `jamie.special.bakkai`
- Existing aliases (1): breakdance
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `醉意2236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `醉意↓↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tenshin / 点辰

- Entry: `jamie.special.tenshin`
- Existing aliases (0): (none)
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `醉意3 (近身) 63214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `醉意↘ (近身) →↘↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Swagger Hermit Punch / 疾步仙掌

- Entry: `jamie.special.swagger_hermit_punch`
- Existing aliases (0): (none)
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `醉意4214P > 4P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `醉意←↓↙←拳 > ←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Back Shaver / 背剪手

- Entry: `jamie.throw.back_shaver`
- Existing aliases (0): (none)
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Wheel Punch / 转轮冲

- Entry: `jamie.throw.wheel_punch`
- Existing aliases (0): (none)
- Context: Require Jamie and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Chun-Li

### Kikoken / 气功拳

- Entry: `chunli.special.kikoken`
- Existing aliases (1): Kikouken
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `[4]6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `[←]→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hundred Lightning Kicks / 百裂腿

- Entry: `chunli.special.hundred_lightning_kicks`
- Existing aliases (1): 百裂脚
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Lightning Kick Barrage / 百裂连腿

- Entry: `chunli.special.lightning_kick_barrage`
- Existing aliases (1): 百裂连脚
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 百裂腿; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆版中 KK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 双脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Aerial Hundred Lightning Kicks / 空中百裂腿

- Entry: `chunli.special.aerial_hundred_lightning_kicks`
- Existing aliases (0): (none)
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `直跳或前跳 236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `直跳或前跳 ↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hazanshu / 霸山踢

- Entry: `chunli.special.hazanshu`
- Existing aliases (1): 霸山蹴
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tensho Kicks / 天升腿

- Entry: `chunli.special.tensho_kicks`
- Existing aliases (1): 天升脚
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Koshuto / 虎袭倒

- Entry: `chunli.throw.koshuto`
- Existing aliases (0): (none)
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Taiji Fan / 太极扇

- Entry: `chunli.throw.taiji_fan`
- Existing aliases (0): (none)
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ryuseiraku / 龙星落

- Entry: `chunli.throw.ryuseiraku`
- Existing aliases (0): (none)
- Context: Require Chun-Li and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Guile

### Sonic Boom / 音速手刀

- Entry: `guile.special.sonic_boom`
- Existing aliases (1): boom
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `[4]6+(JF) P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `[←]→+(JF) 拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `音速轰`
  - Kind: legacy_community_candidate
  - Source: [reference](https://www.baike.com/wikiid/5741020207254329162); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `音速飞刀`
  - Kind: legacy_community_candidate
  - Source: [reference](https://www.baike.com/wikiid/5741020207254329162); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:

### Sonic Blade / 音速波刃

- Entry: `guile.special.sonic_blade`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sonic Cross / 音速交叠

- Entry: `guile.special.sonic_cross`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 音速波刃; confirm the exact intermediate branch before acceptance.
- Candidate: `普通版中 6+(JF) P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `普通版中 →+(JF) 拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### OD Sonic Cross / 斗爆音速交叠

- Entry: `guile.special.od_sonic_cross`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 音速波刃; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆版中 6PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 →双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sonic Break / 音速连破

- Entry: `guile.special.sonic_break`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `「实拳手」状态中 6/n/4PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `「实拳手」状态中 →/n/←双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Dragon Suplex / 龙式过背摔

- Entry: `guile.throw.dragon_suplex`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Judo Throw / 柔道摔

- Entry: `guile.throw.judo_throw`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Flying Mare / 单臂摔

- Entry: `guile.throw.flying_mare`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Flying Buster Drop / 空中爆落摔

- Entry: `guile.throw.flying_buster_drop`
- Existing aliases (0): (none)
- Context: Require Guile and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Kimberly

### Bushin Senpukyaku / 武神旋风腿

- Entry: `kimberly.special.bushin_senpukyaku`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Aerial Bushin Senpukyaku / 空中武神旋风腿

- Entry: `kimberly.special.aerial_bushin_senpukyaku`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `前跳 214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `前跳 ↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sprint / 疾行

- Entry: `kimberly.special.sprint`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K > 可长按 6`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚 > 可长按 →`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `疾驱`
  - Kind: community_attested_candidate
  - Source: [reference](https://www.taptap.cn/moment/321623512936615744); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:

### Emergency Stop / 急停止

- Entry: `kimberly.special.emergency_stop`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 疾行; confirm the exact intermediate branch before acceptance.
- Candidate: `P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Torso Cleaver / 体砍

- Entry: `kimberly.special.torso_cleaver`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 疾行; confirm the exact intermediate branch before acceptance.
- Candidate: `LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Shadow Slide / 影捞い

- Entry: `kimberly.special.shadow_slide`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 疾行; confirm the exact intermediate branch before acceptance.
- Candidate: `MK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `中脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Neck Hunter / 猎首

- Entry: `kimberly.special.neck_hunter`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 疾行; confirm the exact intermediate branch before acceptance.
- Candidate: `HK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `重脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Arc Step / 弧空

- Entry: `kimberly.special.arc_step`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 疾行; confirm the exact intermediate branch before acceptance. Automatic transition, not a separately executable command; aliases describe the transition.
- Candidate: `疾行自动跳`
  - Kind: editorial_description_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `Sprint auto hop`
  - Kind: editorial_description_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Bushin Izuna Otoshi / 武神饭纲落

- Entry: `kimberly.special.bushin_izuna_otoshi`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 疾行; confirm the exact intermediate branch before acceptance.
- Candidate: `P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Bushin Hojin Kick / 武神矛刃腿

- Entry: `kimberly.special.bushin_hojin_kick`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 疾行; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Vagabond Edge / 流转一文字

- Entry: `kimberly.special.vagabond_edge`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hidden Variable / 彩隐形

- Entry: `kimberly.special.hidden_variable`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Genius at Play / 招雷改造弹

- Entry: `kimberly.special.genius_at_play`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Shuriken Bomb / 手里剑炸弹

- Entry: `kimberly.special.shuriken_bomb`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `至少有1罐 22P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `至少有↙罐 ↓↓拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Shuriken Bomb Spread / 手里剑乱爆弹

- Entry: `kimberly.special.shuriken_bomb_spread`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `至少有2罐 22PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `至少有↓罐 ↓↓双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Nue Twister / 荒妖捻

- Entry: `kimberly.special.nue_twister`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) 236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) ↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ripcord Throw / 绳缚背负投

- Entry: `kimberly.throw.ripcord_throw`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Bell Ringer / 敲钟巴投

- Entry: `kimberly.throw.bell_ringer`
- Existing aliases (0): (none)
- Context: Require Kimberly and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Juri

### Fuhajin / 风破刃

- Entry: `juri.special.fuhajin`
- Existing aliases (0): (none)
- Context: Require Juri and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Saihasho / 岁破冲

- Entry: `juri.special.saihasho`
- Existing aliases (1): 脚波
- Context: Require Juri and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ankensatsu / 暗剑杀

- Entry: `juri.special.ankensatsu`
- Existing aliases (0): (none)
- Context: Require Juri and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236MK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→中脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Go Ohsatsu / 五黄杀

- Entry: `juri.special.go_ohsatsu`
- Existing aliases (0): (none)
- Context: Require Juri and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236HK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→重脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tensenrin / 天穿轮

- Entry: `juri.special.tensenrin`
- Existing aliases (1): pinwheel
- Context: Require Juri and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Spider Fang Throw / 蜘穿腿

- Entry: `juri.throw.spider_fang_throw`
- Existing aliases (0): (none)
- Context: Require Juri and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Shadow Kick Throw / 苛影腿

- Entry: `juri.throw.shadow_kick_throw`
- Existing aliases (0): (none)
- Context: Require Juri and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Ken

### Hadoken / 波动拳

- Entry: `ken.special.hadoken`
- Existing aliases (0): (none)
- Context: Require Ken and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Kazekama Shin Kick / 风镰踢

- Entry: `ken.special.kazekama_shin_kick`
- Existing aliases (0): (none)
- Context: Require Ken and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 迅雷腿; confirm the exact intermediate branch before acceptance.
- Candidate: `6LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Gorai Axe Kick / 轰雷落

- Entry: `ken.special.gorai_axe_kick`
- Existing aliases (0): (none)
- Context: Require Ken and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 迅雷腿; confirm the exact intermediate branch before acceptance.
- Candidate: `6MK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→中脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Senka Snap Kick / 闪火踢

- Entry: `ken.special.senka_snap_kick`
- Existing aliases (0): (none)
- Context: Require Ken and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 迅雷腿; confirm the exact intermediate branch before acceptance.
- Candidate: `6HK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→重脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Kasai Thrust Kick / 火碎踢

- Entry: `ken.special.kasai_thrust_kick`
- Existing aliases (0): (none)
- Context: Require Ken and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source uses a cross-reference; resolve its prerequisite before acceptance.
- Candidate: `斗爆版派生的 ① 中 6K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版派生的 ① 中 →脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Knee Strikes / 抓膝踢

- Entry: `ken.throw.knee_strikes`
- Existing aliases (0): (none)
- Context: Require Ken and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hell Wheel / 地狱车

- Entry: `ken.throw.hell_wheel`
- Existing aliases (0): (none)
- Context: Require Ken and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Blanka

### Electric Thunder / 雷霆放电

- Entry: `blanka.special.electric_thunder`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Rolling Attack / 回旋撞

- Entry: `blanka.special.rolling_attack`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `[4]6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `[←]→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Aerial Rolling Attack / 空中回旋撞

- Entry: `blanka.special.aerial_rolling_attack`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 [4]6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 [←]→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Wild Hunt / 野兽捕猎摔

- Entry: `blanka.special.wild_hunt`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Rolling Cannon / 回旋炮弹

- Entry: `blanka.special.rolling_cannon`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source uses a cross-reference; resolve its prerequisite before acceptance.
- Candidate: `「电光猛兽」状态中 ① 中 任意方向+P > 连续3回`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `「电光猛兽」状态中 ① 中 任意方向+拳 > 连续↘回`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Wild Fang / 野兽獠牙

- Entry: `blanka.throw.wild_fang`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Jungle Flip / 丛林翻转

- Entry: `blanka.throw.jungle_flip`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Wild Bites / 野兽啃咬

- Entry: `blanka.throw.wild_bites`
- Existing aliases (0): (none)
- Context: Require Blanka and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Dhalsim

### Yoga Fire / 瑜伽火球

- Entry: `dhalsim.special.yoga_fire`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Arch / 瑜伽弧

- Entry: `dhalsim.special.yoga_arch`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Flame / 瑜伽烈焰

- Entry: `dhalsim.special.yoga_flame`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `63214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↘↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Blast / 瑜伽爆炎

- Entry: `dhalsim.special.yoga_blast`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `63214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↘↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Comet / 瑜伽彗星

- Entry: `dhalsim.special.yoga_comet`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 63214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 →↘↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Float / 瑜伽漂浮

- Entry: `dhalsim.special.yoga_float`
- Existing aliases (1): float
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `2/3KK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓/↘双脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Aerial Yoga Float / 空中瑜伽漂浮

- Entry: `dhalsim.special.aerial_yoga_float`
- Existing aliases (1): float
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 2KK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 ↓双脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Teleport / 瑜伽瞬移

- Entry: `dhalsim.special.yoga_teleport`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `6/4PPP/KKK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→/←三拳/三脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Aerial Yoga Teleport / 空中瑜伽瞬移

- Entry: `dhalsim.special.aerial_yoga_teleport`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 6/4PPP/KKK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 →/←三拳/三脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Smash / 瑜伽猛击

- Entry: `dhalsim.throw.yoga_smash`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Throw / 瑜伽摔

- Entry: `dhalsim.throw.yoga_throw`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yoga Splash / 瑜伽泼

- Entry: `dhalsim.throw.yoga_splash`
- Existing aliases (0): (none)
- Context: Require Dhalsim and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 2LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ↓轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## E. Honda

### Hundred Hand Slap / 百裂张手

- Entry: `honda.special.hundred_hand_slap`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Oicho Throw / 大银杏投

- Entry: `honda.special.oicho_throw`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 63214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →↘↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sumo Dash / 相扑移步

- Entry: `honda.special.sumo_dash`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Teppo Triple Slap / 铁炮掌

- Entry: `honda.special.teppo_triple_slap`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 相扑移步; confirm the exact intermediate branch before acceptance.
- Candidate: `P > P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳 > 拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Taiho Cannon Lift / 大炮

- Entry: `honda.special.taiho_cannon_lift`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 相扑移步; confirm the exact intermediate branch before acceptance.
- Candidate: `2P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Neko Damashi / 相扑猫骗

- Entry: `honda.special.neko_damashi`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sumo Spirit / 相扑魂

- Entry: `honda.special.sumo_spirit`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Saba Ori / 相扑鲭折

- Entry: `honda.throw.saba_ori`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tawara Throw / 土台投

- Entry: `honda.throw.tawara_throw`
- Existing aliases (0): (none)
- Context: Require E. Honda and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Dee Jay

### Air Slasher / 破空飞刃

- Entry: `deejay.special.air_slasher`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `[4]6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `[←]→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Jackknife Maximum / 屈体极点踢

- Entry: `deejay.special.jackknife_maximum`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `[2]8K > LK 版 4 减少前进的距离`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `[↓]↑脚 > 轻脚 版 ← 减少前进的距离`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Roll Through Feint / 佯动旋转步

- Entry: `deejay.special.roll_through_feint`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Jus Cool / 保持酷爽

- Entry: `deejay.special.jus_cool`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Funky Slicer / 放克刀锋腿

- Entry: `deejay.special.funky_slicer`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 保持酷爽; confirm the exact intermediate branch before acceptance.
- Candidate: `LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Waning Moon / 残月

- Entry: `deejay.special.waning_moon`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 保持酷爽; confirm the exact intermediate branch before acceptance.
- Candidate: `MK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `中脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Maximum Strike / 极点上踢

- Entry: `deejay.special.maximum_strike`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 保持酷爽; confirm the exact intermediate branch before acceptance.
- Candidate: `HK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `重脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Juggling Dash / 杂耍前冲

- Entry: `deejay.special.juggling_dash`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 保持酷爽; confirm the exact intermediate branch before acceptance.
- Candidate: `6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Juggling Sway / 花招摇摆

- Entry: `deejay.special.juggling_sway`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 保持酷爽; confirm the exact intermediate branch before acceptance.
- Candidate: `4P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Diss Track / 蹬踩·节拍

- Entry: `deejay.throw.diss_track`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Flip Throw / 翻转摔

- Entry: `deejay.throw.flip_throw`
- Existing aliases (0): (none)
- Context: Require Dee Jay and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Manon

### Dégagé / 代噶热动作

- Entry: `manon.special.degage`
- Existing aliases (1): Degage
- Context: Require Manon and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Grand Fouetté / 32圈挥舞转

- Entry: `manon.special.grand_fouette`
- Existing aliases (1): Grand Fouette
- Context: Require Manon and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 芭蕾回旋; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ouchi Gari / 大内刈

- Entry: `manon.throw.ouchi_gari`
- Existing aliases (0): (none)
- Context: Require Manon and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Uchi Mata / 内股

- Entry: `manon.throw.uchi_mata`
- Existing aliases (0): (none)
- Context: Require Manon and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Marisa

### Dimachaerus / 双剑角斗士

- Entry: `marisa.special.dimachaerus`
- Existing aliases (0): (none)
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > 6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > →拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Quadriga / 四马战车

- Entry: `marisa.special.quadriga`
- Existing aliases (1): 飞踹
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Scutum / 罗马塔盾

- Entry: `marisa.special.scutum`
- Existing aliases (0): (none)
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tonitrus / 雷鸣

- Entry: `marisa.special.tonitrus`
- Existing aliases (0): (none)
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 罗马塔盾; confirm the exact intermediate branch before acceptance.
- Candidate: `P > P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳 > 拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Procella / 暴风雨

- Entry: `marisa.special.procella`
- Existing aliases (0): (none)
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 罗马塔盾; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Enfold / 环抱

- Entry: `marisa.special.enfold`
- Existing aliases (0): (none)
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 罗马塔盾; confirm the exact intermediate branch before acceptance.
- Candidate: `(近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Mounted Grace / 优雅骑乘

- Entry: `marisa.throw.mounted_grace`
- Existing aliases (0): (none)
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ponte Milvio / 米尔维奥桥

- Entry: `marisa.throw.ponte_milvio`
- Existing aliases (0): (none)
- Context: Require Marisa and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## JP

### Triglav / 三头神特里格拉夫

- Entry: `jp.special.triglav`
- Existing aliases (1): 地刺
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Stribog / 风神斯特利伯格

- Entry: `jp.special.stribog`
- Existing aliases (0): (none)
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Departure: Window / 出行·窗口

- Entry: `jp.special.departure_window`
- Existing aliases (1): Departure Window
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 出行; confirm the exact intermediate branch before acceptance.
- Candidate: `214LP/MP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←轻拳/中拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Departure: Shadow / 出行·暗影

- Entry: `jp.special.departure_shadow`
- Existing aliases (1): Departure Shadow
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 出行; confirm the exact intermediate branch before acceptance.
- Candidate: `214HP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←重拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Amnesia / 失忆

- Entry: `jp.special.amnesia`
- Existing aliases (1): 摊手
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Torbalan / 怪物托尔巴兰

- Entry: `jp.special.torbalan`
- Existing aliases (0): (none)
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Embrace / 抱拥

- Entry: `jp.special.embrace`
- Existing aliases (0): (none)
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ravina / 雪崩

- Entry: `jp.throw.ravina`
- Existing aliases (0): (none)
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Uragan / 暴风

- Entry: `jp.throw.uragan`
- Existing aliases (0): (none)
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tornado / 龙卷风

- Entry: `jp.throw.tornado`
- Existing aliases (0): (none)
- Context: Require JP and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Zangief

### Double Lariat / 双截旋风掌

- Entry: `zangief.special.double_lariat`
- Existing aliases (1): lariat
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Screw Piledriver / 螺旋打桩机

- Entry: `zangief.special.screw_piledriver`
- Existing aliases (1): SPD
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 360+P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ↘→0+拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Borscht Dynamite / 罗宋汤爆炸

- Entry: `zangief.special.borscht_dynamite`
- Existing aliases (1): air SPD
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) 360+K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) ↘→0+脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Russian Suplex / 俄式过背摔

- Entry: `zangief.special.russian_suplex`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `近身 63214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `近身 →↘↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Siberian Express / 西伯利亚快车

- Entry: `zangief.special.siberian_express`
- Existing aliases (1): running bear grab
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `投距离外 63214LK/MK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `投距离外 →↘↓↙←轻脚/中脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tundra Storm / 冻原风暴

- Entry: `zangief.special.tundra_storm`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22HK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓重脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Bodyslam / 抱摔

- Entry: `zangief.throw.bodyslam`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) n+LP+LK > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) n+轻拳+轻脚 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Capture Suplex / 抓捕过背摔

- Entry: `zangief.throw.capture_suplex`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### German Suplex / 德式拱桥摔

- Entry: `zangief.throw.german_suplex`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Spinebuster / 脊背重摔

- Entry: `zangief.throw.spinebuster`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 3LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ↘轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Russian Drop / 俄式坠击

- Entry: `zangief.throw.russian_drop`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 1LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ↙轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Brain Buster / 脑部重摔

- Entry: `zangief.throw.brain_buster`
- Existing aliases (0): (none)
- Context: Require Zangief and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 2LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ↓轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Lily

### Condor Wind / 秃鹰风

- Entry: `lily.special.condor_wind`
- Existing aliases (1): wind
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Condor Spire / 秃鹰尖

- Entry: `lily.special.condor_spire`
- Existing aliases (1): spire
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tomahawk Buster / 战斧灭

- Entry: `lily.special.tomahawk_buster`
- Existing aliases (0): (none)
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Condor Dive / 秃鹰潜

- Entry: `lily.special.condor_dive`
- Existing aliases (0): (none)
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `直跳或前跳 PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `直跳或前跳 双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### OD Condor Dive / 斗爆秃鹰潜

- Entry: `lily.special.od_condor_dive`
- Existing aliases (0): (none)
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 战斧灭; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆版中 PPP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 三拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Mexican Typhoon / 墨西哥台风

- Entry: `lily.special.mexican_typhoon`
- Existing aliases (0): (none)
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 360+P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ↘→0+拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Canyon Throw / 峡谷摔

- Entry: `lily.throw.canyon_throw`
- Existing aliases (0): (none)
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) n/6LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) n/→轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Falling Cliff / 落崖坠

- Entry: `lily.throw.falling_cliff`
- Existing aliases (0): (none)
- Context: Require Lily and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Cammy

### Spiral Arrow / 螺旋飞箭

- Entry: `cammy.special.spiral_arrow`
- Existing aliases (1): 地箭
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K > HK 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚 > 重脚 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Cannon Spike / 神枪机兵

- Entry: `cammy.special.cannon_spike`
- Existing aliases (0): (none)
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623K > HK 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘脚 > 重脚 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Quick Spin Knuckle / 快旋反转拳

- Entry: `cammy.special.quick_spin_knuckle`
- Existing aliases (1): spin knuckle
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hooligan Combination / 流氓组合技

- Entry: `cammy.special.hooligan_combination`
- Existing aliases (1): hooligan
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P > HP 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳 > 重拳 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Reverse Edge / 倒翻刀锋腿

- Entry: `cammy.special.reverse_edge`
- Existing aliases (0): (none)
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 流氓组合技; confirm the exact intermediate branch before acceptance.
- Candidate: `2K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Fatal Leg Twister / 夺命旋风腿

- Entry: `cammy.special.fatal_leg_twister`
- Existing aliases (0): (none)
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 流氓组合技; confirm the exact intermediate branch before acceptance.
- Candidate: `对手站姿 (近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `对手站姿 (近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Silent Step / 暗中佯动

- Entry: `cammy.special.silent_step`
- Existing aliases (0): (none)
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 流氓组合技; confirm the exact intermediate branch before acceptance.
- Candidate: `P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Rough Landing / 粗暴摔地

- Entry: `cammy.throw.rough_landing`
- Existing aliases (0): (none)
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Delta Throw / 三角洲绞颈摔

- Entry: `cammy.throw.delta_throw`
- Existing aliases (0): (none)
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Leg Scissors Choke / 双腿剪刀绞

- Entry: `cammy.throw.leg_scissors_choke`
- Existing aliases (0): (none)
- Context: Require Cammy and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Rashid

### Spinning Mixer / 回旋搅

- Entry: `rashid.special.spinning_mixer`
- Existing aliases (1): mixer
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Eagle Spike / 雄鹰踢

- Entry: `rashid.special.eagle_spike`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Whirlwind Shot / 旋风踢射

- Entry: `rashid.special.whirlwind_shot`
- Existing aliases (1): tornado
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Arabian Cyclone / 阿拉伯飓风

- Entry: `rashid.special.arabian_cyclone`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Wing Stroke / 鹰翼式

- Entry: `rashid.special.wing_stroke`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 阿拉伯飓风; confirm the exact intermediate branch before acceptance.
- Candidate: `4K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Rolling Assault / 翻滚奇袭

- Entry: `rashid.special.rolling_assault`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 阿拉伯飓风; confirm the exact intermediate branch before acceptance.
- Candidate: `6K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Nail Assault / 痛踢奇袭

- Entry: `rashid.special.nail_assault`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 阿拉伯飓风; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Arabian Skyhigh / 阿拉伯高空

- Entry: `rashid.special.arabian_skyhigh`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `前跳 214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `前跳 ↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Riding Glider / 驾乘滑冲

- Entry: `rashid.throw.riding_glider`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sunset Drop / 落日坠击

- Entry: `rashid.throw.sunset_drop`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Desert Slider / 沙漠滑行

- Entry: `rashid.throw.desert_slider`
- Existing aliases (0): (none)
- Context: Require Rashid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## A.K.I.

### Nightshade Pulse / 紫烟炮

- Entry: `aki.special.nightshade_pulse`
- Existing aliases (1): bubble
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214LP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←轻拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Nightshade Chaser / 紫烟追

- Entry: `aki.special.nightshade_chaser`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 紫烟炮; confirm the exact intermediate branch before acceptance.
- Candidate: `6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Orchid Spring / 紫泡泉

- Entry: `aki.special.orchid_spring`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214MP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←中拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Toxic Wreath / 紫泡撒

- Entry: `aki.special.toxic_wreath`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214HP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←重拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Serpent Lash / 蛇头鞭

- Entry: `aki.special.serpent_lash`
- Existing aliases (1): whip
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Cruel Fate / 凶袭突

- Entry: `aki.special.cruel_fate`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Snake Step / 蛇轻功

- Entry: `aki.special.snake_step`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sinister Slide / 恶鬼蛇行

- Entry: `aki.special.sinister_slide`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `2PP > 8 取消`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓双拳 > ↑ 取消`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Venomous Fang / 猛毒牙

- Entry: `aki.special.venomous_fang`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 恶鬼蛇行; confirm the exact intermediate branch before acceptance.
- Candidate: `P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Heel Strike / 蛇连咬

- Entry: `aki.special.heel_strike`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 恶鬼蛇行; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Entrapment / 雁字缠

- Entry: `aki.special.entrapment`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 恶鬼蛇行; confirm the exact intermediate branch before acceptance.
- Candidate: `(近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Whisper / 赑屃

- Entry: `aki.throw.whisper`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Gluttony / 饕餮

- Entry: `aki.throw.gluttony`
- Existing aliases (0): (none)
- Context: Require A.K.I. and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Ed

### Psycho Spark / 精神力闪光

- Entry: `ed.special.psycho_spark`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Psycho Shoot / 精神力反射

- Entry: `ed.special.psycho_shoot`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 精神力闪光; confirm the exact intermediate branch before acceptance.
- Candidate: `6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Psycho Uppercut / 精神力上勾拳

- Entry: `ed.special.psycho_uppercut`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Psycho Blitz / 精神力闪攻

- Entry: `ed.special.psycho_blitz`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Kill Switch Break / 诛杀开关·破碎

- Entry: `ed.special.kill_switch_break`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 诛杀步 (前方); confirm the exact intermediate branch before acceptance.
- Candidate: `动作前半 6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `动作前半 →拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Kill Switch Chaser / 诛杀开关·追逐

- Entry: `ed.special.kill_switch_chaser`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 诛杀步 (前方); confirm the exact intermediate branch before acceptance.
- Candidate: `动作后半 6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `动作后半 →拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Face Buster / 脸部炸弹摔

- Entry: `ed.throw.face_buster`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Rib Crusher / 肋骨粉碎摔

- Entry: `ed.throw.rib_crusher`
- Existing aliases (0): (none)
- Context: Require Ed and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Akuma

### Gou Hadoken / 豪波动拳

- Entry: `akuma.special.gou_hadoken`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Zanku Hadoken / 斩空波动拳

- Entry: `akuma.special.zanku_hadoken`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `前跳 236P (斗爆版直跳可亦可)`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `前跳 ↓↘→拳 (斗爆版直跳可亦可)`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Gou Shoryuken / 豪升龙拳

- Entry: `akuma.special.gou_shoryuken`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Adamant Flame / 金刚灼火

- Entry: `akuma.special.adamant_flame`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > 6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > →拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Demon Raid / 百鬼袭

- Entry: `akuma.special.demon_raid`
- Existing aliases (1): Demon Flip
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Demon Low Slash / 百鬼豪斩

- Entry: `akuma.special.demon_low_slash`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 百鬼袭; confirm the exact intermediate branch before acceptance.
- Candidate: `百鬼无按键派生`
  - Kind: editorial_description_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `Demon Raid no-button follow-up`
  - Kind: editorial_description_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Demon Guillotine / 百鬼豪冲

- Entry: `akuma.special.demon_guillotine`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 百鬼袭; confirm the exact intermediate branch before acceptance.
- Candidate: `P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Demon Blade Kick / 百鬼豪刃

- Entry: `akuma.special.demon_blade_kick`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 百鬼袭; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Demon Swoop / 百鬼潜影

- Entry: `akuma.special.demon_swoop`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 百鬼袭; confirm the exact intermediate branch before acceptance.
- Candidate: `2`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Demon Gou Zanku / 百鬼豪斩空

- Entry: `akuma.special.demon_gou_zanku`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 百鬼袭; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆版中 236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 ↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Demon Gou Rasen / 百鬼豪螺旋

- Entry: `akuma.special.demon_gou_rasen`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 百鬼袭; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆版中 214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版中 ↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ashura Senku / 阿修罗闪空

- Entry: `akuma.special.ashura_senku`
- Existing aliases (1): teleport
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `6/4KKK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→/←三脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Oboro Throw / 胧

- Entry: `akuma.special.oboro_throw`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `6KKK > LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→三脚 > 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Goshoha / 豪冲破

- Entry: `akuma.throw.goshoha`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Shuretto / 朱裂刀

- Entry: `akuma.throw.shuretto`
- Existing aliases (0): (none)
- Context: Require Akuma and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## M. Bison

### Psycho Crusher Attack / 精神力旋冲击

- Entry: `mbison.special.psycho_crusher_attack`
- Existing aliases (1): 电钻
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `[4]6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `[←]→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `Psycho Crusher`
  - Kind: community_attested_candidate
  - Source: [reference](https://www.reddit.com/r/StreetFighter/comments/142ug8e/order_of_move_unlocks_in_world_tour/); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:

### Backfist Combo / 反手拳连招

- Entry: `mbison.special.backfist_combo`
- Existing aliases (0): (none)
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Shadow Rise / 影升

- Entry: `mbison.special.shadow_rise`
- Existing aliases (0): (none)
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `[2]8K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `[↓]↑脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Head Press / 头部踏压

- Entry: `mbison.special.head_press`
- Existing aliases (0): (none)
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 影升; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Somersault Skull Diver / 空翻头骨落

- Entry: `mbison.special.somersault_skull_diver`
- Existing aliases (0): (none)
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 影升; confirm the exact intermediate branch before acceptance.
- Candidate: `普通版中 6/n/4P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `普通版中 →/n/←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Devil Reverse / 逆魔破

- Entry: `mbison.special.devil_reverse`
- Existing aliases (0): (none)
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 影升; confirm the exact intermediate branch before acceptance.
- Candidate: `6/n/4P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→/n/←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Deadly Throw / 夺命摔

- Entry: `mbison.throw.deadly_throw`
- Existing aliases (0): (none)
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Death Tower / 死亡之塔

- Entry: `mbison.throw.death_tower`
- Existing aliases (0): (none)
- Context: Require M. Bison and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Terry

### Power Wave / 能量波

- Entry: `terry.special.power_wave`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236LP/MP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→轻拳/中拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Round Wave / 圆波

- Entry: `terry.special.round_wave`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236HP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→重拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Quick Burn / 快速燃烧

- Entry: `terry.special.quick_burn`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214LP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←轻拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Burning Knuckle / 燃烧指节

- Entry: `terry.special.burning_knuckle`
- Existing aliases (1): Burn Knuckle
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214MP/HP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←中拳/重拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Power Charge / 能量冲锋

- Entry: `terry.special.power_charge`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Crack Shoot / 崩裂喷射

- Entry: `terry.special.crack_shoot`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Rising Tackle / 升龙摔

- Entry: `terry.special.rising_tackle`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Grasping Upper / 强袭投

- Entry: `terry.throw.grasping_upper`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Buster Throw / 破坏投

- Entry: `terry.throw.buster_throw`
- Existing aliases (0): (none)
- Context: Require Terry and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Mai

### Midare Kachousen / 乱花蝶扇

- Entry: `mai.special.midare_kachousen`
- Existing aliases (0): (none)
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 花蝶扇; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆版蓄力后 6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆版蓄力后 →拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ryuuenbu / 龙炎舞

- Entry: `mai.special.ryuuenbu`
- Existing aliases (0): (none)
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hissatsu Shinobi Bachi / 必杀忍蜂

- Entry: `mai.special.hissatsu_shinobi_bachi`
- Existing aliases (0): (none)
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hishou Ryuuenjin / 飞翔龙炎阵

- Entry: `mai.special.hishou_ryuuenjin`
- Existing aliases (1): DP
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Musasabi no Mai / 鼯鼠之舞

- Entry: `mai.special.musasabi_no_mai`
- Existing aliases (0): (none)
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `前跳 214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `前跳 ↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Shiranui Gourin / 不知火刚临

- Entry: `mai.throw.shiranui_gourin`
- Existing aliases (0): (none)
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Fuusha Kuzushi / 风车崩

- Entry: `mai.throw.fuusha_kuzushi`
- Existing aliases (0): (none)
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Yume Zakura / 梦樱

- Entry: `mai.throw.yume_zakura`
- Existing aliases (0): (none)
- Context: Require Mai and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `空中 (近身) LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `空中 (近身) 轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Elena

### Rhino Horn / 犀角踢

- Entry: `elena.special.rhino_horn`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Scratch Wheel / 轮刮踢

- Entry: `elena.special.scratch_wheel`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Lynx Song / 连结之歌

- Entry: `elena.special.lynx_song`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Leopard Snap / 花豹迅击

- Entry: `elena.special.leopard_snap`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 连结之歌; confirm the exact intermediate branch before acceptance.
- Candidate: `(斗爆版中) 6LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(斗爆版中) →轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Harvest Circle / 圆弧收割

- Entry: `elena.special.harvest_circle`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 连结之歌; confirm the exact intermediate branch before acceptance.
- Candidate: `(斗爆版中) 6MK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(斗爆版中) →中脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Mallet Smash / 猛锤踢

- Entry: `elena.special.mallet_smash`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 连结之歌; confirm the exact intermediate branch before acceptance.
- Candidate: `(斗爆版中) 6HK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(斗爆版中) →重脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Lynx Whirl / 连结回旋

- Entry: `elena.special.lynx_whirl`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 旋转镰刀; confirm the exact intermediate branch before acceptance.
- Candidate: `6P ~ 斗爆版连结之歌`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→拳 ~ 斗爆版连结之歌`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Spinning Scythe / 旋转镰刀

- Entry: `elena.special.spinning_scythe`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Moon Glider / 半月弧影踢

- Entry: `elena.special.moon_glider`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > 6P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > →拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Leg Tackle / 腿锁摔

- Entry: `elena.throw.leg_tackle`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Leg Lift Throw / 腿举抛

- Entry: `elena.throw.leg_lift_throw`
- Existing aliases (0): (none)
- Context: Require Elena and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Sagat

### High Tiger Shot / 猛虎波

- Entry: `sagat.special.high_tiger_shot`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236MP/HP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→中拳/重拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Low Tiger Shot / 下段猛虎波

- Entry: `sagat.special.low_tiger_shot`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236LP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→轻拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tiger Uppercut / 猛虎升龙破

- Entry: `sagat.special.tiger_uppercut`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P > HP 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳 > 重拳 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tiger Knee Crush / 猛虎跳膝撞

- Entry: `sagat.special.tiger_knee_crush`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tiger Nexus / 猛虎连结

- Entry: `sagat.special.tiger_nexus`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Mighty Tiger / 猛虎威击

- Entry: `sagat.special.mighty_tiger`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 猛虎连结; confirm the exact intermediate branch before acceptance.
- Candidate: `6LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Greedy Tiger / 猛虎贪婪

- Entry: `sagat.special.greedy_tiger`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 猛虎连结; confirm the exact intermediate branch before acceptance.
- Candidate: `6MK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→中脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Nova Tiger / 猛虎新星

- Entry: `sagat.special.nova_tiger`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 猛虎连结; confirm the exact intermediate branch before acceptance.
- Candidate: `6HK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→重脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tiger Hang / 猛虎悬

- Entry: `sagat.throw.tiger_hang`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Tiger Carry / 猛虎摔

- Entry: `sagat.throw.tiger_carry`
- Existing aliases (0): (none)
- Context: Require Sagat and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## C. Viper

### Tracer Combination / 追踪组合技

- Entry: `cviper.special.tracer_combination`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 雷电掴打; confirm the exact intermediate branch before acceptance.
- Candidate: `普通版中 6PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `普通版中 →双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Feint / 假动作

- Entry: `cviper.special.feint`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 雷电掴打; confirm the exact intermediate branch before acceptance.
- Candidate: `普通版攻击前 K /  攻击前 K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `普通版攻击前 脚 /  攻击前 脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Burning Kick / 烈焰踢

- Entry: `cviper.special.burning_kick`
- Existing aliases (1): Burn Kick
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Knuckled Pursuit / 追击冲拳

- Entry: `cviper.special.knuckled_pursuit`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 烈焰踢; confirm the exact intermediate branch before acceptance.
- Candidate: `普通版中 PP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `普通版中 双拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Double Burn / 双重灼烧

- Entry: `cviper.special.double_burn`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 烈焰踢; confirm the exact intermediate branch before acceptance.
- Candidate: `普通版中 KK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `普通版中 双脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Aerial Burning Kick / 空中烈焰踢

- Entry: `cviper.special.aerial_burning_kick`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `直跳或前跳 236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `直跳或前跳 ↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Seismic Hammer / 震地重锤

- Entry: `cviper.special.seismic_hammer`
- Existing aliases (1): seismo
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Focus Force / 蓄能之力

- Entry: `cviper.special.focus_force`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214K > 可蓄 > 蓄力中 66 取消`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←脚 > 可蓄 > 蓄力中 →→ 取消`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### High Impulse / 过载脉冲

- Entry: `cviper.throw.high_impulse`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Thunder Cradle / 闪电怀抱

- Entry: `cviper.throw.thunder_cradle`
- Existing aliases (0): (none)
- Context: Require C. Viper and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Alex

### Flash Axe / 闪光手斧

- Entry: `alex.special.flash_axe`
- Existing aliases (0): (none)
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236LP/MP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→轻拳/中拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Flash Chop / 闪光手刀

- Entry: `alex.special.flash_chop`
- Existing aliases (0): (none)
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236HP`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→重拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Aerial Knee Smash / 空中膝撞

- Entry: `alex.special.aerial_knee_smash`
- Existing aliases (0): (none)
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Power Bomb / 炸弹摔

- Entry: `alex.special.power_bomb`
- Existing aliases (1): Pwr Bomb
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 63214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →↘↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Hyper Bomb / 超级炸弹

- Entry: `alex.special.hyper_bomb`
- Existing aliases (0): (none)
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 炸弹摔; confirm the exact intermediate branch before acceptance.
- Candidate: `斗爆强力摔中 6`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `斗爆强力摔中 →`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Arm Lock / 臂锁

- Entry: `alex.throw.arm_lock`
- Existing aliases (0): (none)
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Guillotine Hammer / 断头重锤

- Entry: `alex.throw.guillotine_hammer`
- Existing aliases (0): (none)
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Illegal Knees / 犯规膝撞

- Entry: `alex.throw.illegal_knees`
- Existing aliases (0): (none)
- Context: Require Alex and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 2LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ↓轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Ingrid

### Sun Shot / 日射

- Entry: `ingrid.special.sun_shot`
- Existing aliases (1): Sunshot
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳 > 可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sun Flare / 日耀

- Entry: `ingrid.special.sun_flare`
- Existing aliases (1): Sunflare
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > LP 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > 轻拳 版可蓄`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Solar Burst / 日焰

- Entry: `ingrid.special.solar_burst`
- Existing aliases (0): (none)
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `直跳或前跳 214P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `直跳或前跳 ↓↙←拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sun Rise / 日射踢

- Entry: `ingrid.special.sun_rise`
- Existing aliases (0): (none)
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Sun Veil / 太阳面纱

- Entry: `ingrid.special.sun_veil`
- Existing aliases (0): (none)
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Vanishing Sun / 日隐技

- Entry: `ingrid.special.vanishing_sun`
- Existing aliases (0): (none)
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `4/2/6KKK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `←/↓/→三脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Strange Knuckle / 奇异拳

- Entry: `ingrid.throw.strange_knuckle`
- Existing aliases (0): (none)
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 6/n+LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) →/n+轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Gravity Drop / 重力摔

- Entry: `ingrid.throw.gravity_drop`
- Existing aliases (0): (none)
- Context: Require Ingrid and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `(近身) 4LP+LK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `(近身) ←轻拳+轻脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

## Yasmine

### Daloy ng Tubig / 激流连击

- Entry: `yasmine.special.daloy_ng_tubig`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `Knife Rekka`
  - Kind: community_attested_candidate
  - Source: [reference](https://www.reddit.com/r/StreetFighter/comments/1vq4kev/ranking_every_special_move_for_avatars_yasmine/); access: search_excerpt
  - Decision:
  - Reviewer:
  - Notes:

### Alon / 涌浪

- Entry: `yasmine.special.alon`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 激流连击; confirm the exact intermediate branch before acceptance.
- Candidate: `击中或被防时 6P > 击中时 ~ 英雄模式`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `击中或被防时 →拳 > 击中时 ~ 英雄模式`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Talim ng Hangin / 旋风刃

- Entry: `yasmine.special.talim_ng_hangin`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `214P > 击中时 ~ 英雄模式`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↙←拳 > 击中时 ~ 英雄模式`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Mukha ng Langit / 天相显容

- Entry: `yasmine.special.mukha_ng_langit`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `236K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↘→脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Ulan / 骤雨

- Entry: `yasmine.special.ulan`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 天相显容; confirm the exact intermediate branch before acceptance.
- Candidate: `P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Kulog / 落雷

- Entry: `yasmine.special.kulog`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers. Source follow-up root: 天相显容; confirm the exact intermediate branch before acceptance.
- Candidate: `K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Lipad ng Agila / 雕王飞踢

- Entry: `yasmine.special.lipad_ng_agila`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `623K`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `→↓↘脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Pangil sa Likuran / 蛇牙回噬

- Entry: `yasmine.special.pangil_sa_likuran`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `22P`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `↓↓拳`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:

### Linya ng Liwanag / 光芒轨迹

- Entry: `yasmine.special.linya_ng_liwanag`
- Existing aliases (0): (none)
- Context: Require Yasmine and Classic move/input context; preserve strength, OD, air/ground, charge, stance and follow-up qualifiers.
- Candidate: `潜藏之力中 4KK`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
- Candidate: `潜藏之力中 ←双脚`
  - Kind: editorial_notation_candidate
  - Source: [reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html); access: full_page
  - Decision:
  - Reviewer:
  - Notes:
