# Street Fighter 6 bilingual glossary

Collection: 849 entries, 4332 aliases, and 157 ambiguous alias records; 31
target-patch characters.

Scope: System, Mechanic, Tactic, Input, and Normal Move terms apply to all
characters. Character-specific names cover all 31 playable characters available
at the target patch, including Yasmine. Target patch: 08.03.2026 Update.

English canonical names, instructions, and notes are used throughout. Chinese
labels are simplified Chinese language data; traditional Chinese community
sources and aliases are excluded.

## Provenance and use

Capcom pages verify English move identities, the Chinese character name, control
types, and selected HUD labels. Chinese move labels come from community
references because the inspected official Chinese move and patch pages rendered
their move text in English.

Each record includes aliases, scope, sources, and blank review fields. Some
notation variants and translations are editorial combinations and remain
candidates for review. This collection is not a corpus frequency study or a
complete localization dictionary.

Live move pages were inspected on October 8, 2026. No frame counts, damage
values, costs, or current balance recommendations were imported. Validate
patch-sensitive behavior separately against the selected historical patch.

Unique Move aliases now follow the requested overhead/input rules. See [Unique
Move Alias Review](unique-move-alias-review.md) for all 244 entries, input
conditions, live properties, and blank historical-patch review fields.


Low-alias moves: see [Low-alias Move Review](low-alias-review.md) for the
2026-10-22 search and pending candidates. These proposals are staged only in
docs and have not been applied to this glossary or runtime data.

## Integration rules

- Load data/glossary.json; select relevant concepts rather than placing the full
  dictionary in every prompt.
- Normalize names in extracted fields; preserve original comment evidence
  unchanged.
- System, Mechanic, Tactic, Input, and Normal Move terms require no Ryu subject.
  Resolve character identity separately; use character-specific named moves only
  after establishing the corresponding subject. Shared names must not default to
  Ryu.
- Keep OD, move strength, Denjin, and control-type modifiers. For Chinese
  community feedback, normalize bare CA to the SA3 family; retain explicit
  enhanced-variant context separately.
- Consult ambiguous_aliases before applying short or overloaded aliases.
- Never use numerical direction to decide whether a request is a buff or nerf.

## Baseline correction

The original ZH02 debugging case incorrectly described a collarbone term as
Solar Plexus Strike. Collarbone Breaker is the 6MP move; Solar Plexus Strike is
the distinct 6HP move. The contradictory input remains unchanged in the
debugging dataset and later run snapshots. The initial report was deleted at the
user's request; the unchanged comment remains in subsequent debugging runs. Its
semantic expectations should be reviewed before reuse.

For a revised test, use the explicit English name Solar Plexus Strike with its
Chinese reference label, or test Collarbone Breaker separately. Do not count the
contradictory original case as independent evidence of model quality.

## Sources

- [Capcom Ryu command
  list](https://www.streetfighter.com/6/zh-hans/character/ryu/movelist) —
  official. Move labels rendered in English even on the Chinese locale. No
  official Chinese move translations inferred.
- [Capcom Ryu frame
  data](https://www.streetfighter.com/6/zh-hans/character/ryu/frame) — official.
  Used for terminology and move identity only. Live numerical values are not
  pinned to August 3, 2026.
- [Capcom Ryu August 3, 2026
  changes](https://www.streetfighter.com/6/buckler/zh-hans/battle_change/20260803/ryu)
  — official. Chinese character name verified; adjustment text rendered in
  English.
- [Capcom Chinese Fighting Ground HUD
  manual](https://game.capcom.com/manual/SF6/zh-hans/ps5/page/3/3) — official.
  Verified Chinese gauge, Burnout, and throw escape labels.
- [Capcom Chinese control types
  manual](https://game.capcom.com/manual/SF6/zh-hans/ps5/page/2/3) — official.
  Verified Chinese Modern, Classic, and Dynamic control labels.
- [SPMoves SF6 Chinese move
  list](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html) —
  community_reference. Used only for Chinese labels and input notation, not
  current balance values. Some names and Modern mappings differ from official
  current names.
- [Shaojing SF6 study notes](https://www.cnblogs.com/shaojing0713/p/18265627) —
  player_authored. Used to attest player vocabulary, not mechanics accuracy. The
  page contains contradictory aliases and old numerical descriptions; those
  rules were not imported.

## Character names and universal terms

### Character

- **Luke** / 卢克 (Luke); aliases: 卢子, 炉子, 撸子, 撸磕.
- **Ryu** / 隆 (Ryu).
- **Jamie** / 杰米 (Jamie); aliases: 醉拳辫子佬, 酒鬼, 杰米哥.
- **Chun-Li** / 春丽 (Chun-Li); aliases: Chun Li, ChunLi, Chun, Li。
- **Guile** / 古烈 (Guile); aliases: 美国兵, 盖尔, 大兵, 美国大兵, 扫把头, 特种, 古列, 古利, 骨裂.
- **Kimberly** / 金柏莉 (Kimberly); aliases: 金佰莉, 金伯利, 黑妹, 金伯莉.
- **Juri** / 朱莉 (Juri); aliases: 韩蛛俐, 蛛俐, 朱莉.
- **Ken** / 肯 (Ken); aliases: 啃啃侠, 肯肯侠.
- **Blanka** / 布兰卡 (Blanka); aliases: 狮子, 狮王, 大狮子, 野人, 野兽, 怪兽, 猴子, 电狼, 电猫儿.
- **Dhalsim** / 达尔西姆 (Dhalsim); aliases: Dhal, Sim, 长手瑜伽, 长手, 长臂, 长手怪, 长手长脚,
  印度佬, 印度人, 老印度, 瑜珈, 达尔锡, 阿三.
- **E. Honda** / 本田 (E. Honda); aliases: E.Honda, Honda, Ehonda, 相扑, 相扑儿, 相扑手,
  日本相扑, E Honda.
- **Dee Jay** / 迪杰 (Dee Jay); aliases: DeeJay, DJ, Dee_Jay.
- **Manon** / 曼侬 (Manon); aliases: 法国芭蕾柔道手.
- **Marisa** / 玛丽莎 (Marisa); aliases: 肌肉女角斗士, 爽朗大姐.
- **JP** / JP (JP); aliases: 勾批.
- **Zangief** / 桑吉尔夫 (Zangief); aliases: Gief, Zan, 老桑, 红色旋风, 大苏, 大苏联, 苏联佬,
  苏联大汉, 苏联大壮, 苏联大老肥, 苏联老块, 苏联大座, 大坐儿, 俄胖, 俄罗斯, 俄蛮, 毛子, 大膀, 桑叔, 苏联老马子.
- **Lily** / 莉莉 (Lily).
- **Cammy** / 嘉米 (Cammy), aliases: 倩咪.
- **Rashid** / 拉希德 (Rashid).
- **A.K.I.** / 阿鬼 (A.K.I.); aliases: AKI, A. K. I..
- **Ed** / 爱德 (Ed); aliases: 艾德.
- **Akuma** / 豪鬼 (Akuma); aliases: Gouki, 豪师傅.
- **M. Bison** / 维加 (M. Bison); aliases: M.Bison, Bison, Vega, 维嘉, 警察, 大警, 大警察,
  将军, 司令, M Bison, 城管.
- **Terry** / 特瑞 (Terry).
- **Mai** / 舞 (Mai); aliases: 不知火舞, 火舞.
- **Elena** / 艾琳娜 (Elena); aliases: 竹节虫.
- **Sagat** / 沙加特 (Sagat); aliases: 沙盖特, 泰格, 泰格儿, 泰格佬, TAIGE, 泰哥, 泰哥儿, 泰拳, 泰拳佬,
  tiger, 高人.
- **C. Viper** / 深红毒蛇 (C. Viper); aliases: C.Viper, Viper, 毒蛇, C Viper.
- **Alex** / 阿里克斯 (Alex); aliases: 艾力克斯, 阿历克斯, 阿列克谢.
- **Ingrid** / 英格丽德 (Ingrid); aliases: ygld.
- **Yasmine** / 亚思敏 (Yasmine); aliases: ysm.

### System

Bare CA in Chinese community comments normalizes to the SA3 family. The strict
Critical Art entry remains available only for explicit variant interpretation.

- **Drive System** / 斗气系统 (universal).
- **Drive Gauge** / 斗气槽 (universal); aliases: 斗气.
- **Drive Impact** / 斗气迸放 (universal); aliases: DI, 迸放, 迸发, 迸, 斗气冲击.
- **Drive Parry** / 斗气招架 (universal); aliases: 蓝防.
- **Perfect Parry** / 完美招架 (universal); aliases: PP, 精防.
- **Drive Rush** / 斗气冲锋 (universal); aliases: DR, 绿冲, 斗气冲刺.
- **Parry Drive Rush** / 招架绿冲 (universal); aliases: raw Drive Rush, 裸绿冲, PDR,
  直接绿冲.
- **Cancel Drive Rush** / 绿冲取消 (universal); aliases: Drive Rush Cancel, DRC,
  取消绿冲.
- **Drive Reversal** / 斗气反攻 (universal); aliases: 斗反, 斗气反击.
- **Overdrive** / OD必杀技 (universal); aliases: OD, EX special, EX必杀, 强化必杀, 斗气加强技,
  斗气必杀.
- **Burnout** / 虚损 (universal); aliases: 白.
- **Super Art** / 超级必杀技 (universal); aliases: SA, 超必杀, 超杀.
- **Super Art Gauge** / 超级必杀槽 (universal); aliases: Super Gauge, 超杀槽.
- **Critical Art** / 临界必杀技 (universal); aliases: CA, CA必杀, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3, 3格大招, 3级超必杀, 3气大招.
- **Classic Controls** / 经典操作 (universal); aliases: Classic, 经典模式, 经典.
- **Modern Controls** / 现代操作 (universal); aliases: Modern, 现代模式, 现代.

### Mechanic

- **Start-up** / 发生 (universal); aliases: startup, 前摇, 启动, 启动帧, 出招前摇, 发生帧, Start
  up.
- **Active Frames** / 持续帧 (universal); aliases: 判定帧, 命中判定.
- **Recovery** / 收招 (universal); aliases: 后摇, 收招硬直, 收招后摇.
- **Frame Advantage** / 帧优势 (universal); aliases: 有利帧, 硬直差, 帧数差.
- **Plus on Block** / 防御有利 (universa￼l); aliases: 加帧.
- **Minus on Block** / 防御不利 (universal); aliases: 负帧.
- **Hitstun** / 受击硬直 (universal).
- **Blockstun** / 防御硬直 (universal).
- **Pushback on Block** / 防御击退 (universal); aliases: block pushback, 被防击退,
  防御推开距离, 打防推开距离.
- **Combo Scaling** / 连招伤害修正 (universal); aliases: damage scaling, 伤害修正, 修正.
- **Counter Hit** / 打康 (universal); aliases: CH, 普通康, 黄康, 康.
- **Punish Counter** / 确反康 (universal); aliases: PC, 确反.
- **Hitbox** / 攻击判定 (universal); aliases: 攻击判定框, 攻击框.
- **Hurtbox** / 受击判定 (universal); aliases: 受击判定框, 受击框.

### Tactic

- **Neutral** / 立回 (universal).
- **Pressure** / 压制 (universal).
- **Hit Confirm** / 命中确认 (universal); aliases: 确认.
- **Combo** / 连招 (universal); aliases: 连段.
- **Cancel** / 取消 (universal).
- **Link** / 目押 (universal).
- **Whiff Punish** / 差合 (universal); aliases: 挥空惩罚.
- **Punish** / 确反 (universal).
- **Throw** / 投技 (universal); aliases: 摔投.
- **Throw Escape** / 拆投 (universal); aliases: throw tech.
- **Cross-up** / 逆向 (universal); aliases: Cross up, Crossup.
- **Mix-up** / 择 (universal); aliases: 二择, Mix up, Mixup.
- **Armor** / 霸体 (universal).
- **Overhead** / 中段攻击 (universal); aliases: 中段, 越头, 砸猪头.
- **Low Attack** / 下段攻击 (universal); aliases: 下段.
- **Knockdown** / 击倒 (universal); aliases: 倒地, KD.
- **Juggle** / 浮空追击 (universal); aliases: 浮空.
- **Projectile** / 飞行道具 (universal); aliases: 波动, 波.
- **Invincibility** / 无敌 (universal).

### Input

- **Light Punch** / 轻拳 (universal); aliases: LP, jab.
- **Medium Punch** / 中拳 (universal); aliases: MP, strong.
- **Heavy Punch** / 重拳 (universal); aliases: HP, fierce.
- **Light Kick** / 轻脚 (universal); aliases: LK, short.
- **Medium Kick** / 中脚 (universal); aliases: MK, forward.
- **Heavy Kick** / 重脚 (universal); aliases: HK, roundhouse.
- **Punch Button** / 拳键 (universal); aliases: P.
- **Kick Button** / 脚键 (universal); aliases: K.
- **Special Move Button** / 必杀技键 (universal); aliases: SP.
- **Assist Button** / 辅助键 (universal); aliases: Assist, AUTO.
- **Quarter-circle Forward** / 下前四分之一圈 (universal); aliases: qcf, 236, Quarter
  circle Forward, Quartercircle Forward, 正摇.
- **Quarter-circle Back** / 下后四分之一圈 (universal); aliases: qcb, 214, Quarter
  circle Back, Quartercircle Back, 反摇.
- **Dragon Punch Motion** / 升龙指令 (universal); aliases: 623, DP motion, 626, 266,
  628.
- **Standing** / 站立 (universal); aliases: st., s., 5.
- **Crouching** / 蹲下 (universal); aliases: cr., c., 2.
- **Jumping** / 跳跃 (universal); aliases: j., j, 8.
- **Forward Dash** / 前冲 (universal); aliases: forwarddash, dash forward, f.dash,
  66, 前前.
- **Backward Dash** / 后撤步 (universal); aliases: Back Dash, Backdash, Backwards
  Dash, dash backward, b.dash, 44, 后后.

Ordinary forward and backward dashes use double-direction inputs relative to
facing. They are distinct from Drive Rush and character-specific dash/run moves;
the notation does not establish frame data or invincibility.

### Normal Move

Normal-move names and Classic notation are universal vocabulary. Resolve the
character separately from the comment context. Shared labels do not imply
identical properties or availability across characters or control types.

- **Standing Light Punch** / 站立轻拳 (universal); aliases: st.LP, 5LP, 站轻拳, st. LP,
  stLP, st LP, standing LP, st.jab, st. jab, standing jab, s.LP, sLP, 站轻P, 站LP,
  站立轻P, 站立LP.
- **Standing Medium Punch** / 站立中拳 (universal); aliases: st.MP, 5MP, 站中拳, st.
  MP, stMP, st MP, standing MP, st.strong, st. strong, standing strong, s.MP,
  sMP, 站中P, 站MP, 站立中P, 站立MP.
- **Standing Heavy Punch** / 站立重拳 (universal); aliases: st.HP, 5HP, 站重拳, st. HP,
  stHP, st HP, standing HP, st.fierce, st. fierce, standing fierce, s.HP, sHP,
  站重P, 站HP, 站立重P, 站立HP, 站大拳.
- **Standing Light Kick** / 站立轻脚 (universal); aliases: st.LK, 5LK, 站轻脚, st. LK,
  stLK, st LK, standing LK, st.short, st. short, standing short, s.LK, sLK, 站轻K,
  站LK, 站轻腿, 站立轻K, 站立LK, 站立轻腿.
- **Standing Medium Kick** / 站立中脚 (universal); aliases: st.MK, 5MK, 站中脚, st. MK,
  stMK, st MK, standing MK, st.forward, st. forward, standing forward, s.MK,
  sMK, 站中K, 站MK, 站中腿, 站立中K, 站立MK, 站立中腿.
- **Standing Heavy Kick** / 站立重脚 (universal); aliases: st.HK, 5HK, 站重脚, st. HK,
  stHK, st HK, standing HK, st.roundhouse, st. roundhouse, standing roundhouse,
  s.HK, sHK, 站重K, 站HK, 站重腿, 站立重K, 站立HK, 站立重腿, 站大脚.
- **Crouching Light Punch** / 蹲轻拳 (universal); aliases: cr.LP, 2LP, 下轻拳, cr. LP,
  crLP, cr LP, crouching LP, cr.jab, cr. jab, crouching jab, c.LP, cLP, crouch
  LP, 下轻P, 下LP, 蹲轻P, 蹲LP, 蹲下轻拳, 蹲下轻P, 蹲下LP.
- **Crouching Medium Punch** / 蹲中拳 (universal); aliases: cr.MP, 2MP, 下中拳, cr.
  MP, crMP, cr MP, crouching MP, cr.strong, cr. strong, crouching strong, c.MP,
  cMP, crouch MP, 下中P, 下MP, 蹲中P, 蹲MP, 蹲下中拳, 蹲下中P, 蹲下MP.
- **Crouching Heavy Punch** / 蹲重拳 (universal); aliases: cr.HP, 2HP, 下重拳, cr. HP,
  crHP, cr HP, crouching HP, cr.fierce, cr. fierce, crouching fierce, c.HP, cHP,
  crouch HP, 下重P, 下HP, 蹲重P, 蹲HP, 蹲下重拳, 蹲下重P, 蹲下HP.
- **Crouching Light Kick** / 蹲轻脚 (universal); aliases: cr.LK, 2LK, 下轻脚, cr. LK,
  crLK, cr LK, crouching LK, cr.short, cr. short, crouching short, c.LK, cLK,
  crouch LK, 下轻K, 下LK, 下轻腿, 蹲轻K, 蹲LK, 蹲轻腿, 蹲下轻脚, 蹲下轻K, 蹲下LK, 蹲下轻腿.
- **Crouching Medium Kick** / 蹲中脚 (universal); aliases: cr.MK, 2MK, 下中脚, cr. MK,
  crMK, cr MK, crouching MK, cr.forward, cr. forward, crouching forward, c.MK,
  cMK, crouch MK, 下中K, 下MK, 下中腿, 蹲中K, 蹲MK, 蹲中腿, 蹲下中脚, 蹲下中K, 蹲下MK, 蹲下中腿.
- **Crouching Heavy Kick** / 蹲重脚 (universal); aliases: cr.HK, 2HK, 下重脚, cr. HK,
  crHK, cr HK, crouching HK, cr.roundhouse, cr. roundhouse, crouching
  roundhouse, c.HK, cHK, crouch HK, 下重K, 下HK, 下重腿, 蹲重K, 蹲HK, 蹲重腿, 蹲下重脚, 蹲下重K,
  蹲下HK, 蹲下重腿.
- **Jumping Light Punch** / 跳跃轻拳 (universal); aliases: j.LP, jLP, 跳轻拳, j. LP, j
  LP, jumping LP, j.jab, j. jab, jumping jab, jump LP, air LP, 跳轻P, 跳LP, 跳跃轻P,
  跳跃LP.
- **Jumping Medium Punch** / 跳跃中拳 (universal); aliases: j.MP, jMP, 跳中拳, j. MP, j
  MP, jumping MP, j.strong, j. strong, jumping strong, jump MP, air MP, 跳中P,
  跳MP, 跳跃中P, 跳跃MP.
- **Jumping Heavy Punch** / 跳跃重拳 (universal); aliases: j.HP, jHP, 跳重拳, j. HP, j
  HP, jumping HP, j.fierce, j. fierce, jumping fierce, jump HP, air HP, 跳重P,
  跳HP, 跳跃重P, 跳跃HP, 跳大拳.
- **Jumping Light Kick** / 跳跃轻脚 (universal); aliases: j.LK, jLK, 跳轻脚, j. LK, j
  LK, jumping LK, j.short, j. short, jumping short, jump LK, air LK, 跳轻K, 跳LK,
  跳轻腿, 跳跃轻K, 跳跃LK, 跳跃轻腿.
- **Jumping Medium Kick** / 跳跃中脚 (universal); aliases: j.MK, jMK, 跳中脚, j. MK, j
  MK, jumping MK, j.forward, j. forward, jumping forward, jump MK, air MK, 跳中K,
  跳MK, 跳中腿, 跳跃中K, 跳跃MK, 跳跃中腿.
- **Jumping Heavy Kick** / 跳跃重脚 (universal); aliases: j.HK, jHK, 跳重脚, j. HK, j
  HK, jumping HK, j.roundhouse, j. roundhouse, jumping roundhouse, jump HK, air
  HK, 跳重K, 跳HK, 跳重腿, 跳跃重K, 跳跃HK, 跳跃重腿, 跳大脚.

## Roster coverage and review status

Roster date: August 3, 2026. Yasmine joined with this update. Arjun (October 13,
2026), Tifa, and Bosch are outside this experiment version. Avatars and World
Tour NPCs are not playable-roster entries.
The roster is covered by official named Special Moves, Super Arts, Unique
Attacks, and Throws. Exact repeated labels in an official list are one
vocabulary concept; situational variants still require context. Common system
actions and generic normals remain universal. This is roster/name coverage, not
exhaustive coverage of every community nickname, hidden variant, or numerical
property.
Every new Chinese label is a community reference pairing unless explicitly
identified otherwise. Regional names such as Gouki/Akuma and Vega/M. Bison
require Street Fighter 6 context. Chinese community nickname frequency has not
been measured. All human review fields remain blank.
Official English and Japanese command-name lists were aligned only to verify
identity against the linked community references. Japanese text is intermediate
evidence; it is not registered as a Chinese alias. Raw name-only snapshots and
pairing evidence are in data/raw/glossary/.

### Additional universal inputs and tactics

- **Back-to-Forward Charge** / 后蓄前 (universal); aliases: charge back, forward,
  [4]6, 46, Back to Forward Charge, BacktoForward Charge.
- **Down-to-Up Charge** / 下蓄上 (universal); aliases: charge down, up, [2]8, 28,
  Down to Up Charge, DowntoUp Charge.
- **Half-circle Forward** / 后下前半圈 (universal); aliases: hcf, 41236, Half circle
  Forward, Halfcircle Forward.
- **Half-circle Back** / 前下后半圈 (universal); aliases: hcb, 63214, Half circle
  Back, Halfcircle Back.
- **360-degree Motion** / 一圈指令 (universal); aliases: 360, 360 degree Motion,
  360degree Motion.
- **720-degree Motion** / 两圈指令 (universal); aliases: 720, 720 degree Motion,
  720degree Motion.
- **Double Down** / 下下指令 (universal); aliases: 22.
- **Command Grab** / 指令投 (universal).
- **Forward Throw** / 前投 (universal).
- **Back Throw** / 后投 (universal).
-

## Character-specific terms

### Ryu / 隆

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/ryu/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#ryu).

#### Ryu Special Move

- **Hadoken** / 波动拳 (Ryu); aliases: Hadouken, 波, 波动.
- **Shoryuken** / 升龙拳 (Ryu); aliases: 升龙.
- **Tatsumaki Senpu-kyaku** / 龙卷旋风腿 (Ryu); aliases: Tatsumaki, Tatsu, 旋风脚, 旋风腿,
  直升机, 回旋踢, Tatsumaki Senpu kyaku, Tatsumaki Senpukyaku.
- **Aerial Tatsumaki Senpu-kyaku** / 空中龙卷旋风腿 (Ryu); aliases: air Tatsu, 空中旋风脚,
  空中直升机, Aerial Tatsumaki Senpu kyaku, Aerial Tatsumaki Senpukyaku.
- **High Blade Kick** / 上段足刀踢 (Ryu); aliases: 驴踢, donkey kick, Donkeykick,
  Joudan Sokutogeri, Joudan.
- **Hashogeki** / 波掌击 (Ryu); aliases: 波掌.
- **Denjin Charge** / 电刃炼气 (Ryu); aliases: 集中, 蓄电, 电刃.

#### Ryu Super Move

- **Shinku Hadoken** / 真空波动拳 (Ryu); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Shin Hashogeki** / 真波掌击 (Ryu); aliases: 真·波掌击, 真・波掌击, SA2, 二气, 2气, SA 2,
  SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Shin Shoryuken** / 真升龙拳 (Ryu); aliases: 真·升龙拳, 真・升龙拳, SA3, 三气, CA, 3气, SA 3,
  SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

- **Shin Shoryuken (Critical Art)** / 真升龙拳 CA版 (Ryu); aliases: CA Shin
  Shoryuken, CA, 真升龙拳CA.

#### Ryu Unique Move

- **Collarbone Breaker** / 锁骨破 (Ryu); aliases: 锁骨碎, 中段, 砸猪头.
- **Solar Plexus Strike** / 鸠尾碎 (Ryu); aliases: 鸽尾碎, 前重拳, 6hp.
- **Short Uppercut** / 上突 (Ryu); aliases: 后重拳, 4hp.
- **Axe Kick** / 踵落 (Ryu); aliases: 斧踢, 后重脚, 4hk.
- **Whirlwind Kick** / 旋风腿 (Ryu); aliases: 旋风脚, 前重脚, 6hk.
- **High Double Strike** / 上段二连击 (Ryu); aliases: 上段双连击, 重脚tc, hp>hk, 重拳>重脚.
- **Fuwa Triple Strike** / 不破三连击 (Ryu); aliases: 中拳tc, mp>lk>hk, 中拳>轻脚>重脚.

#### Ryu Throw Move

- **Shoulder Throw** / 背负投 (Ryu); aliases: 前投.
- **Somersault Throw** / 巴投 (Ryu); aliases: 后投.

### Luke / 卢克

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/luke/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#luke).

#### Luke Special Move

- **Sand Blast** / 砂爆 (Luke).
- **Fatal Shot** / 致命射击 (Luke).
- **Flash Knuckle** / 迅闪指节拳 (Luke); aliases: 指节拳, 蓄力指节拳, 完美指节拳, 蓄力讯闪指节拳, 蓄力拳.
- **DDT** / 深度死亡摔 (Luke).
- **Aerial Flash Knuckle** / 空中迅闪指节拳 (Luke).
- **Avenger** / 复仇者 (Luke).
- **No Chaser** / 勇往直前 (Luke).
- **Impaler** / 穿刺者 (Luke).
- **Rising Uppercut** / 上升勾拳 (Luke).
- **Slam Dunk** / 灌篮 (Luke).

#### Luke Super Move

- **Vulcan Blast** / 伏尔甘爆裂 (Luke); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Eraser** / 蒸发暗令 (Luke); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **Pale Rider** / 灰马骑士 (Luke); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3, LV.3,
  LVL3, Level 3, LV 3.

#### Luke Unique Move

- **Rawhide** / 生皮鞭 (Luke); aliases: 中段, 砸猪头.
- **Suppressor** / 枪械消音器 (Luke); aliases: 4hp, 后重拳.
- **Outlaw Kick** / 亡命踢 (Luke); aliases: 4hk, 后重脚.
- **Double Impact** / 双连冲击 (Luke); aliases: 6hp>hp, 前重拳>重拳.
- **Triple Impact** / 三连冲击 (Luke); aliases: lp>mp>hp, 轻拳>中拳>重拳.
- **Nose Breaker** / 鼻破 (Luke); aliases: 2mk>2hp, 下中脚>下重拳.
- **Snapback Combo** / 回返连击 (Luke); aliases: mp>mp>mp>mp, 中拳>中拳>中拳>中拳.

#### Luke Throw Move

- **Sweeper** / 扫摔 (Luke).
- **Scrapper** / 拳击手 (Luke).

### Jamie / 杰米

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/jamie/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#jamie).

#### Jamie Special Move

- **The Devil Inside** / 魔身 (Jamie); aliases: drink, raw drink.
- **Freeflow Strikes** / 流醉拳 (Jamie); aliases: rekka.
- **Freeflow Kicks** / 流醉脚 (Jamie); aliases: rekka, kick rekka, Rekka Kick.
- **Swagger Step** / 醉疾步 (Jamie); aliases: palm, 推掌, 重推掌.
- **Arrow Kick** / 挽弓腿 (Jamie); aliases: DP.
- **Luminous Dive Kick** / 无影踢 (Jamie).
- **Bakkai** / 爆回 (Jamie); aliases: breakdance.
- **Tenshin** / 点辰 (Jamie).
- **Swagger Hermit Punch** / 疾步仙掌 (Jamie).

#### Jamie Super Move

- **Breakin'** / 武丽禽 (Jamie); aliases: SA1, 一气, 1气, Breakin, Breakin’, SA 1,
  SA-1, LV1, LV.1, LVL1, Level 1, LV 1.
- **The Devil's Song** / 绝唱魔身 (Jamie); aliases: SA2, 二气, 2气, The Devils Song,
  The Devil’s Song, SA 2, SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Getsuga Saiho** / 月牙叉炮 (Jamie); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Jamie Unique Move

- **Tensei Kick** / 天晴腿 (Jamie); aliases: 2kk, 下双脚.
- **Phantom Sway** / 幻醉舞 (Jamie); aliases: 2hk>hk>p, 下重脚>重脚>拳.
- **Falling Star Kick** / 落星腿 (Jamie); aliases: 中段, 砸猪头.
- **Hermit's Elbow** / 仙姑肘 (Jamie); aliases: Hermits Elbow, Hermit’s Elbow, 4hp,
  后重拳.
- **Senei Kick** / 旋影腿 (Jamie); aliases: 6hk, 前重脚.
- **Bitter Strikes** / 锐钟打 (Jamie); aliases: lp>lk>mp, 轻拳>轻脚>中拳.
- **Full Moon Kick** / 圆月腿 (Jamie); aliases: 中段, 砸猪头.
- **Intoxicated Assault** / 酩酊袭 (Jamie); aliases: 4hp>hp>hk, 后重拳>重拳>重脚.
- **Ransui Haze** / 乱醉旋 (Jamie); aliases: 6hk>4hk>p, 前重脚>后重脚>拳.

#### Jamie Throw Move

- **Back Shaver** / 背剪手 (Jamie).
- **Wheel Punch** / 转轮冲 (Jamie).

#### Jamie Character State

- **Drink Level** / 醉意 (Jamie); aliases: drinks, 醉酒等级, 四酒, 满酒.

### Chun-Li / 春丽

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/chunli/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#chunli).

#### Chun-Li Special Move

- **Kikoken** / 气功拳 (Chun-Li); aliases: Kikouken.
- **Hundred Lightning Kicks** / 百裂腿 (Chun-Li); aliases: 百裂脚.
- **Lightning Kick Barrage** / 百裂连腿 (Chun-Li); aliases: 百裂连脚.
- **Aerial Hundred Lightning Kicks** / 空中百裂腿 (Chun-Li).
- **Spinning Bird Kick** / 回旋鹤脚踢 (Chun-Li); aliases: 倒立旋风腿, 回旋鹤腿踢, SBK.
- **Hazanshu** / 霸山踢 (Chun-Li); aliases: 霸山蹴.
- **Tensho Kicks** / 天升腿 (Chun-Li); aliases: 天升脚.

#### Chun-Li Super Move

- **Kikosho** / 气功掌 (Chun-Li); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Aerial Kikosho** / 空中气功掌 (Chun-Li); aliases: SA 1, SA-1, LV1, LV.1, LVL1,
  Level 1, LV 1.
- **Hoyoku-sen** / 凤翼扇 (Chun-Li); aliases: SA2, 二气, 2气, Hoyoku sen, Hoyokusen,
  SA 2, SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Soten Ranka** / 苍天乱华 (Chun-Li); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Chun-Li Unique Move

- **Swift Thrust** / 追刺拳 (Chun-Li); aliases: 4mp, 后中拳, 6mp, 前中拳.
- **Hakkei** / 发劲 (Chun-Li); aliases: 4hp, 后重拳.
- **Water Lotus Fist** / 水莲掌 (Chun-Li); aliases: 中段, 砸猪头.
- **Yokusen Kick** / 翼旋腿 (Chun-Li); aliases: 6hk, 前重脚.
- **Falling Crane** / 鹤脚落 (Chun-Li); aliases: 中段, 砸猪头.
- **Yoso Kick** / 鹰爪腿 (Chun-Li); aliases: 2mk, 下中脚, 2mk>2mk>2mk, 下中脚>下中脚>下中脚.
- **Wall Jump** / 三角跳 (Chun-Li); aliases: 9, 前上.
- **Soaring Eagle Punches** / 鹰嘴连拳 (Chun-Li); aliases: 中段, 砸猪头.
- **Serenity Stream** / 行云流水 (Chun-Li); aliases: 214p, 下后下后拳.
- **Orchid Palm** / 兰华 (Chun-Li); aliases: 5lp, 轻拳.
- **Snake Strike** / 长蛇打 (Chun-Li); aliases: 5mp, 中拳.
- **Lotus Fist** / 莲掌 (Chun-Li); aliases: 中段, 砸猪头.
- **Forward Strike** / 前击 (Chun-Li); aliases: 5lk, 轻脚.
- **Senpu Kick** / 仙风 (Chun-Li); aliases: 5mk, 中脚.
- **Tenku Kick** / 天空腿 (Chun-Li); aliases: 5hk, 重脚.

#### Chun-Li Throw Move

- **Koshuto** / 虎袭倒 (Chun-Li).
- **Taiji Fan** / 太极扇 (Chun-Li).
- **Ryuseiraku** / 龙星落 (Chun-Li).

### Guile / 古烈

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/guile/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#guile).

#### Guile Special Move

- **Sonic Boom** / 音速手刀 (Guile); aliases: boom.
- **Somersault Kick** / 空翻脚刀 (Guile); aliases: Flash Kick, Flashkick, FK.
- **Sonic Blade** / 音速波刃 (Guile).
- **Sonic Cross** / 音速交叠 (Guile).
- **OD Sonic Cross** / 斗爆音速交叠 (Guile).
- **Sonic Break** / 音速连破 (Guile).

#### Guile Super Move

- **Sonic Hurricane** / 音速飓风 (Guile); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Solid Puncher** / 实拳手 (Guile); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Crossfire Somersault** / 交火脚刀 (Guile); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### Guile Unique Move

- **Full Bullet Magnum** / 马格南满弹 (Guile); aliases: 中段, 砸猪头.
- **Burning Straight** / 燃烧直拳 (Guile); aliases: 4hp, 后重拳.
- **Spinning Back Knuckle** / 回旋反手拳 (Guile); aliases: 6hp, 前重拳.
- **Knee Bazooka** / 飞膝火箭炮 (Guile); aliases: 4lk, 后轻脚.
- **Rolling Sobat** / 翻身后旋踢 (Guile); aliases: 4mk, 后中脚, 6mk, 前中脚.
- **Reverse Spin Kick** / 倒旋踢 (Guile); aliases: 6hk, 前重脚.
- **Guile High Kick** / 古烈上段踢 (Guile); aliases: 3hk, 前下重脚.
- **Recoil Cannon** / 反冲加农 (Guile); aliases: mp>4hp, 中拳>后重拳.
- **Double Shot** / 双射 (Guile); aliases: 2mp>2mp, 下中拳>下中拳.
- **Drake Fang** / 龙牙连打 (Guile); aliases: 中段, 砸猪头.
- **Phantom Cutter** / 魅影切割 (Guile); aliases: 2hk>3hk, 下重脚>前下重脚.

#### Guile Throw Move

- **Dragon Suplex** / 龙式过背摔 (Guile).
- **Judo Throw** / 柔道摔 (Guile).
- **Flying Mare** / 单臂摔 (Guile).
- **Flying Buster Drop** / 空中爆落摔 (Guile).

### Kimberly / 金柏莉

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/kimberly/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#kimberly).

#### Kimberly Special Move

- **Bushin Senpukyaku** / 武神旋风腿 (Kimberly).
- **Aerial Bushin Senpukyaku** / 空中武神旋风腿 (Kimberly).
- **Sprint** / 疾行 (Kimberly).
- **Emergency Stop** / 急停止 (Kimberly).
- **Torso Cleaver** / 体砍 (Kimberly).
- **Shadow Slide** / 影捞い (Kimberly).
- **Neck Hunter** / 猎首 (Kimberly).
- **Arc Step** / 弧空 (Kimberly).
- **Bushin Izuna Otoshi** / 武神饭纲落 (Kimberly).
- **Bushin Hojin Kick** / 武神矛刃腿 (Kimberly).
- **Vagabond Edge** / 流转一文字 (Kimberly).
- **Hidden Variable** / 彩隐形 (Kimberly).
- **Genius at Play** / 招雷改造弹 (Kimberly).
- **Shuriken Bomb** / 手里剑炸弹 (Kimberly).
- **Shuriken Bomb Spread** / 手里剑乱爆弹 (Kimberly).
- **Nue Twister** / 荒妖捻 (Kimberly).

#### Kimberly Super Move

- **Bushin Beats** / 武神乱拍舞 (Kimberly); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Bushin Thunderous Beats** / 武神乱拍舞·雷谱 (Kimberly); aliases: SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Bushin Scramble** / 武神天翔亢龙 (Kimberly); aliases: SA2, 二气, 2气, SA 2, SA-2,
  LV2, LV.2, LVL2, Level 2, LV 2.
- **Soaring Bushin Scramble** / 空中武神天翔亢龙 (Kimberly); aliases: SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Bushin Ninjastar Cypher** / 武神降神舞 (Kimberly); aliases: SA3, 三气, 3气, CA, SA
  3, SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### Kimberly Unique Move

- **Water Slicer Slide** / 水漂腿 (Kimberly); aliases: 3mk, 前下中脚.
- **Windmill Kick** / 风车踢 (Kimberly); aliases: 中段, 砸猪头.
- **Hisen Kick** / 飞箭踢 (Kimberly); aliases: 6hk, 前重脚.
- **Step Up** / 藩篱越 (Kimberly); aliases: 7, 后上, 8, 上, 9, 前上.
- **Elbow Drop** / 肘落 (Kimberly); aliases: 2mp, 下中拳.
- **Bushin Tiger Fangs** / 武神虎连牙 (Kimberly); aliases: mp>hp, 中拳>重拳.
- **Bushin Prism Strikes** / 武神天架拳 (Kimberly); aliases: lp>mp>hp>hk,
  轻拳>中拳>重拳>重脚.
- **Bushin Hellchain** / 武神狱锁拳 (Kimberly); aliases: lp>mp>2hp>hk, 轻拳>中拳>下重拳>重脚.
- **Bushin Hellchain Throw** / 武神狱锁投 (Kimberly); aliases: lp>mp>2hp>2hk,
  轻拳>中拳>下重拳>下重脚.

#### Kimberly Throw Move

- **Ripcord Throw** / 绳缚背负投 (Kimberly).
- **Bell Ringer** / 敲钟巴投 (Kimberly).

### Juri / 朱莉

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/juri/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#juri).

#### Juri Special Move

- **Fuhajin** / 风破刃 (Juri).
- **Saihasho** / 岁破冲 (Juri); aliases: 脚波.
- **Ankensatsu** / 暗剑杀 (Juri).
- **Go Ohsatsu** / 五黄杀 (Juri).
- **Tensenrin** / 天穿轮 (Juri); aliases: pinwheel.
- **Shiku-sen** / 疾空闪 (Juri); aliases: Shiku sen, Shikusen.
- **Shiren-sen** / 死连闪 (Juri); aliases: Shiren sen, Shirensen.

#### Juri Super Move

- **Sakkai Fuhazan** / 杀界风破斩 (Juri); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Feng Shui Engine** / 风水引擎 (Juri); aliases: SA2, 二气, 2气, FSE, 风水, SA 2, SA-2,
  LV2, LV.2, LVL2, Level 2, LV 2.
- **Kaisen Dankai Raku** / 回旋断界落 (Juri); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### Juri Unique Move

- **Kyosesho** / 狂背掌 (Juri); aliases: 6mp, 前中拳.
- **Senkai Kick** / 歼回腿 (Juri); aliases: 中段, 砸猪头.
- **Renko Kicks** / 连克腿 (Juri); aliases: 6hp, 前重拳.
- **Korenzan** / 钩镰斩 (Juri); aliases: 4hk, 后重脚.
- **Death Crest** / 死纹踢 (Juri); aliases: mp>4hp>hp, 中拳>后重拳>重拳.

#### Juri Throw Move

- **Spider Fang Throw** / 蜘穿腿 (Juri).
- **Shadow Kick Throw** / 苛影腿 (Juri).
- **Zanka-sen** / 斩架闪 (Juri); aliases: Zanka sen, Zankasen.

#### Juri Character State

- **Fuha Stock** / 风破球 (Juri).

### Ken / 肯

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/ken/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#ken).

#### Ken Special Move

- **Hadoken** / 波动拳 (Ken).
- **Shoryuken** / 升龙拳 (Ken); aliases: DP, Shoryu.
- **Tatsumaki Senpu-kyaku** / 龙卷旋风腿 (Ken); aliases: Tatsu, Hurricane Kick,
  Tatsumaki Senpu kyaku, Tatsumaki Senpukyaku.
- **Aerial Tatsumaki Senpu-kyaku** / 空中龙卷旋风腿 (Ken); aliases: Aerial Tatsumaki
  Senpu kyaku, Aerial Tatsumaki Senpukyaku.
- **Dragonlash Kick** / 龙尾腿 (Ken); aliases: 龙尾, 龙尾脚, 大飞脚, Dragonlash, lash.
- **Jinrai Kick** / 迅雷腿 (Ken); aliases: 迅雷, 迅雷脚, Jinrai, Crazy Kick.
- **Kazekama Shin Kick** / 风镰踢 (Ken).
- **Gorai Axe Kick** / 轰雷落 (Ken).
- **Senka Snap Kick** / 闪火踢 (Ken).
- **Kasai Thrust Kick** / 火碎踢 (Ken).

#### Ken Super Move

- **Dragonlash Flame** / 龙尾烈脚 (Ken); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Shippu Jinrai-kyaku** / 疾风迅雷腿 (Ken); aliases: SA2, 二气, 2气, Shippu Jinrai
  kyaku, Shippu Jinraikyaku, SA 2, SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Shinryu Reppa** / 神龙烈破 (Ken); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Ken Unique Move

- **Quick Dash** / 奋迅腿 (Ken); aliases: 5kk, 双脚.
- **Emergency Stop** / 急停止 (Ken); aliases: 5lk, 轻脚.
- **Thunder Kick** / 紫电踵落 (Ken); aliases: 中段, 砸猪头.
- **Forward Step Kick** / 前踏踢 (Ken); aliases: 5hk, 重脚.
- **Chin Buster** / 下颚双连 (Ken); aliases: mp>hp, 中拳>重拳.
- **Triple Flash Kicks** / 闪光连腿 (Ken); aliases: mk>mk>hk, 中脚>中脚>重脚.

#### Ken Throw Move

- **Knee Strikes** / 抓膝踢 (Ken).
- **Hell Wheel** / 地狱车 (Ken).

### Blanka / 布兰卡

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/blanka/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#blanka).

#### Blanka Special Move

- **Electric Thunder** / 雷霆放电 (Blanka).
- **Rolling Attack** / 回旋撞 (Blanka).
- **Vertical Rolling Attack** / 上冲回旋撞 (Blanka); aliases: up ball, upball.
- **Backstep Rolling Attack** / 后翻回旋撞 (Blanka); aliases: rainbow, rainbow ball.
- **Aerial Rolling Attack** / 空中回旋撞 (Blanka).
- **Wild Hunt** / 野兽捕猎摔 (Blanka).
- **Blanka-chan Bomb** / 小布兰卡炸弹 (Blanka); aliases: doll, dolls, Blanka doll,
  Blanka chan Bomb, Blankachan Bomb.
- **Rolling Cannon** / 回旋炮弹 (Blanka).

#### Blanka Super Move

- **Shout of Earth** / 大地狂啸 (Blanka); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Lightning Beast** / 电光猛兽 (Blanka); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Ground Shave Cannonball** / 掠地加农弹 (Blanka); aliases: SA3, 三气, 3气, CA, SA 3,
  SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### Blanka Unique Move

- **Rock Crusher** / 岩石打击 (Blanka); aliases: 中段, 砸猪头.
- **Double Knee Bombs** / 双膝炸弹 (Blanka); aliases: 6mk, 前中脚.
- **Wild Edge** / 野兽利刃 (Blanka); aliases: 4mk, 后中脚.
- **Wild Nail** / 野兽锋爪 (Blanka); aliases: 6hp, 前重拳.
- **Amazon River Run** / 亚马逊河流冲 (Blanka); aliases: 3hp, 前下重拳.
- **Coward Crouch** / 胆怯俯身 (Blanka); aliases: 2pp, 下双拳.
- **Wild Lift** / 野兽上抛 (Blanka); aliases: 5p, 拳.
- **Raid Jump** / 突袭跳 (Blanka); aliases: 5k, 脚.
- **Surprise Forward Hop** / 惊乍前跳 (Blanka); aliases: 6kkk, 前三脚.
- **Surprise Back Hop** / 惊乍后跳 (Blanka); aliases: 4kkk, 后三脚.

#### Blanka Throw Move

- **Wild Fang** / 野兽獠牙 (Blanka).
- **Jungle Flip** / 丛林翻转 (Blanka).
- **Wild Bites** / 野兽啃咬 (Blanka).

### Dhalsim / 达尔西姆

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/dhalsim/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#dhalsim).

#### Dhalsim Special Move

- **Yoga Fire** / 瑜伽火球 (Dhalsim).
- **Yoga Arch** / 瑜伽弧 (Dhalsim).
- **Yoga Flame** / 瑜伽烈焰 (Dhalsim).
- **Yoga Blast** / 瑜伽爆炎 (Dhalsim).
- **Yoga Comet** / 瑜伽彗星 (Dhalsim).
- **Yoga Float** / 瑜伽漂浮 (Dhalsim); aliases: float.
- **Aerial Yoga Float** / 空中瑜伽漂浮 (Dhalsim); aliases: float.
- **Yoga Teleport** / 瑜伽瞬移 (Dhalsim).
- **Aerial Yoga Teleport** / 空中瑜伽瞬移 (Dhalsim).

#### Dhalsim Super Move

- **Yoga Inferno** / 瑜伽炼狱 (Dhalsim); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Yoga Sunburst** / 瑜伽日炙 (Dhalsim); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Merciless Yoga** / 瑜伽忘慈悲 (Dhalsim); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### Dhalsim Unique Move

- **Yoga Uppercut** / 瑜伽上勾拳 (Dhalsim); aliases: 4mp, 后中拳.
- **Yoga Lance** / 瑜伽长矛 (Dhalsim); aliases: 4hp, 后重拳.
- **Nirvana Punch** / 涅槃拳 (Dhalsim); aliases: 1hp, 后下重拳.
- **Agile Kick** / 灵敏踢 (Dhalsim); aliases: 1lk, 后下轻脚.
- **Divine Kick** / 合掌踢 (Dhalsim); aliases: 4mk, 后中脚.
- **Thrust Kick** / 刺踢 (Dhalsim); aliases: 1mk, 后下中脚.
- **Yoga Mountain** / 瑜伽山 (Dhalsim); aliases: 4hk, 后重脚.
- **Karma Kick** / 因果踢 (Dhalsim); aliases: 1hk, 后下重脚.
- **Yoga Mummy** / 锥钻头 (Dhalsim); aliases: 2lp, 下轻拳.
- **Drill Kick** / 锥钻踢 (Dhalsim); aliases: drill, 2lk, 下轻脚, 2mk, 下中脚, 2hk, 下重脚.

#### Dhalsim Throw Move

- **Yoga Smash** / 瑜伽猛击 (Dhalsim).
- **Yoga Throw** / 瑜伽摔 (Dhalsim).
- **Yoga Splash** / 瑜伽泼 (Dhalsim).

### E. Honda / 本田

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/ehonda/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#ehonda).

#### E. Honda Special Move

- **Hundred Hand Slap** / 百裂张手 (E. Honda).
- **Sumo Headbutt** / 超级头槌 (E. Honda); aliases: headbutt, head butt.
- **Sumo Smash** / 超级百贯落 (E. Honda); aliases: buttslam, butt slam, 压顶.
- **Oicho Throw** / 大银杏投 (E. Honda).
- **Sumo Dash** / 相扑移步 (E. Honda).
- **Teppo Triple Slap** / 铁炮掌 (E. Honda).
- **Taiho Cannon Lift** / 大炮 (E. Honda).
- **Neko Damashi** / 相扑猫骗 (E. Honda).
- **Sumo Spirit** / 相扑魂 (E. Honda).

#### E. Honda Super Move

- **Show of Force** / 气势爆碎 (E. Honda); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Ultimate Killer Head Ram** / 超级鬼无双 (E. Honda); aliases: SA2, 二气, 2气, SA 2,
  SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **The Final Bout** / 千秋乐 (E. Honda); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### E. Honda Unique Move

- **Harai Kick** / 横扫踢 (E. Honda); aliases: 6hk, 前重脚.
- **Power Stomp** / 相扑力足 (E. Honda); aliases: 中段, 砸猪头.
- **Flying Sumo Press** / 相扑飞身压 (E. Honda); aliases: 中段, 砸猪头.
- **Double Slaps** / 双连张手 (E. Honda); aliases: lp>mp, 轻拳>中拳.
- **Toko Shizume** / 地镇 (E. Honda); aliases: 中段, 砸猪头.

#### E. Honda Throw Move

- **Saba Ori** / 相扑鲭折 (E. Honda).
- **Tawara Throw** / 土台投 (E. Honda).

### Dee Jay / 迪杰

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/deejay/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#deejay).

#### Dee Jay Special Move

- **Air Slasher** / 破空飞刃 (Dee Jay).
- **Jackknife Maximum** / 屈体极点踢 (Dee Jay).
- **Roll Through Feint** / 佯动旋转步 (Dee Jay).
- **Quick Rolling Sobat** / 快速翻身后旋踢 (Dee Jay); aliases: sobat, rolling sobat.
- **Double Rolling Sobat** / 双翻后旋踢 (Dee Jay); aliases: sobat, rolling sobat.
- **Machine Gun Uppercut** / 机枪上勾拳 (Dee Jay); aliases: 贝贝, MGU.
- **Jus Cool** / 保持酷爽 (Dee Jay).
- **Funky Slicer** / 放克刀锋腿 (Dee Jay).
- **Waning Moon** / 残月 (Dee Jay).
- **Maximum Strike** / 极点上踢 (Dee Jay).
- **Juggling Dash** / 杂耍前冲 (Dee Jay).
- **Juggling Sway** / 花招摇摆 (Dee Jay).

#### Dee Jay Super Move

- **The Greatest Sobat** / 极炫后旋踢 (Dee Jay); aliases: SA1, 一气, 1气, SA 1, SA-1,
  LV1, LV.1, LVL1, Level 1, LV 1.
- **Lowkey Sunrise Festival** / 日出音乐节·低调 (Dee Jay); aliases: SA2, 二气, 2气, CA2,
  SA 2, SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Marvelous Sunrise Festival** / 日出音乐节·超凡 (Dee Jay); aliases: 音符连击, CA2, SA 2,
  SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Headliner Sunrise Festival** / 日出音乐节·极点 (Dee Jay); aliases: 音符连击, CA2, SA 2,
  SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Climactic Strike** / 激昂重拳 (Dee Jay); aliases: SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **Encore Beat** / 返场节拍 (Dee Jay); aliases: SA 2, SA-2, LV2, LV.2, LVL2, Level
  2, LV 2.
- **Weekend Pleasure** / 周末狂欢夜 (Dee Jay); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### Dee Jay Unique Move

- **Knee Shot** / 飞膝撞 (Dee Jay); aliases: 中段, 砸猪头.
- **Sunrise Heel** / 日出脚踝踢 (Dee Jay); aliases: 6mk, 前中脚.
- **Face Breaker** / 破脸 (Dee Jay); aliases: 4hk, 后重脚.
- **Threebeat Combo** / 3拍连招 (Dee Jay); aliases: lp>mk>mk, 轻拳>中脚>中脚.
- **Dee Jay Special** / 迪·杰特色 (Dee Jay); aliases: mp>hp>hk, 中拳>重拳>重脚.
- **Funky Dance** / 放克舞 (Dee Jay); aliases: mp>mp>hp, 中拳>中拳>重拳.
- **Funky Dance Feint** / 放克舞·假动作 (Dee Jay); aliases: mp>mp>4hp, 中拳>中拳>后重拳.
- **Party in the Air** / 空中聚会 (Dee Jay); aliases: 中段, 砸猪头.
- **Speedy Maracas** / 砂槌节奏 (Dee Jay); aliases: 22pp, 下下双拳.

#### Dee Jay Throw Move

- **Diss Track** / 蹬踩·节拍 (Dee Jay).
- **Flip Throw** / 翻转摔 (Dee Jay).

### Manon / 曼侬

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/manon/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#manon).

#### Manon Special Move

- **Manège Doré** / 金色圆周转 (Manon); aliases: command grab, Manege Dore.
- **Rond-point** / 环岛点 (Manon); aliases: Rond point, Rondpoint.
- **Dégagé** / 代噶热动作 (Manon); aliases: Degage.
- **Renversé** / 芭蕾回旋 (Manon); aliases: hitgrab, hit grab, Renverse.
- **Grand Fouetté** / 32圈挥舞转 (Manon); aliases: Grand Fouette.

#### Manon Super Move

- **Arabesque** / 阿拉贝斯克舞姿 (Manon); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Étoile** / 明星舞者 (Manon); aliases: SA2, 二气, 2气, Etoile, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Pas de Deux** / 双人舞 (Manon); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Manon Unique Move

- **Révérence** / 屈膝礼 (Manon); aliases: Reverence, 4hp, 后重拳.
- **Tomoe Derrière** / 巴拉后 (Manon); aliases: Tomoe Derriere, 3hk, 前下重脚.
- **À Terre** / 地面动作 (Manon); aliases: mp>mk, 中拳>中脚.
- **En Haut** / 高位舞步 (Manon); aliases: 中段, 砸猪头.
- **Temps Lié** / 重心转移 (Manon); aliases: Temps Lie, hp>hp, 重拳>重拳.
- **Allongé** / 阿隆热动作 (Manon); aliases: Allonge, 2hp>hp, 下重拳>重拳.

#### Manon Throw Move

- **Ouchi Gari** / 大内刈 (Manon).
- **Uchi Mata** / 内股 (Manon).

#### Manon Character State

- **Medals** / 奖牌 (Manon).

### Marisa / 玛丽莎

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/marisa/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#marisa).

#### Marisa Special Move

- **Gladius** / 罗马短剑 (Marisa); aliases: 罗马剑, 蓄力罗马剑.
- **Dimachaerus** / 双剑角斗士 (Marisa).
- **Phalanx** / 方阵战型 (Marisa); aliases: Superman Punch, 超人拳.
- **Quadriga** / 四马战车 (Marisa); aliases: 飞踹.
- **Scutum** / 罗马塔盾 (Marisa).
- **Tonitrus** / 雷鸣 (Marisa).
- **Procella** / 暴风雨 (Marisa).
- **Enfold** / 环抱 (Marisa).

#### Marisa Super Move

- **Javelin of Marisa** / 玛丽莎标枪 (Marisa); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Meteorite** / 陨石 (Marisa); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Goddess of the Hunt** / 狩猎女神 (Marisa); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### Marisa Unique Move

- **Marisa Style** / 玛丽莎风格 (Marisa); aliases: [hp], 蓄力重拳, [hk], 蓄力重脚.
- **Light Two Hitter** / 轻双连 (Marisa); aliases: lp>lp, 轻拳>轻拳.
- **Medium Two Hitter** / 中双连 (Marisa); aliases: mp>mp, 中拳>中拳.
- **Heavy Two Hitter** / 重双连 (Marisa); aliases: hp>hp, 重拳>重拳.
- **Volare Combo** / 飞空组合技 (Marisa); aliases: 中段, 砸猪头.
- **Caelum Arc** / 天空之弧 (Marisa); aliases: 中段, 砸猪头.
- **Magna Bunker** / 伟大地堡 (Marisa); aliases: 4hp, 后重拳.
- **Novacula Swipe** / 利刃猛击 (Marisa); aliases: 6mp>hp, 前中拳>重拳.
- **Novacula Thrust** / 利刃连射 (Marisa); aliases: 6mp>hk, 前中拳>重脚.
- **Malleus Breaker** / 重锤连打 (Marisa); aliases: 中段, 砸猪头.
- **Falx Crusher** / 方阵摧毁 (Marisa); aliases: 6hk>6hk, 前重脚>前重脚.

#### Marisa Throw Move

- **Mounted Grace** / 优雅骑乘 (Marisa).
- **Ponte Milvio** / 米尔维奥桥 (Marisa).

### JP / JP

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/jp/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#jp).

#### JP Special Move

- **Triglav** / 三头神特里格拉夫 (JP); aliases: 地刺.
- **Stribog** / 风神斯特利伯格 (JP).
- **Departure** / 出行 (JP); aliases: portal, portals, 传送门.
- **Departure: Window** / 出行·窗口 (JP); aliases: Departure Window.
- **Departure: Shadow** / 出行·暗影 (JP); aliases: Departure Shadow.
- **Amnesia** / 失忆 (JP); aliases: 摊手.
- **Torbalan** / 怪物托尔巴兰 (JP).
- **Embrace** / 抱拥 (JP).

#### JP Super Move

- **Chornobog** / 黑神切尔纳伯格 (JP); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Lovushka** / 陷阱 (JP); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **Interdiction** / 禁止 (JP); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3, LV.3,
  LVL3, Level 3, LV 3.

#### JP Unique Move

- **Guillotinna** / 断头台 (JP); aliases: 中段, 砸猪头.
- **Malice** / 恶作剧 (JP); aliases: 3hp, 前下重拳.
- **Bylina** / 俄罗斯史诗 (JP); aliases: 6hk, 前重脚.
- **Grom Strelka** / 雷箭 (JP); aliases: 4mp>mp, 后中拳>中拳.
- **Zilant** / 龙兽吉兰特 (JP); aliases: hk>hp, 重脚>重拳.
- **Zilant Mid** / 龙兽吉兰特·中 (JP); aliases: 中段, 砸猪头.
- **Zilant Low** / 龙兽吉兰特·下 (JP); aliases: hk>hp>hk, 重脚>重拳>重脚.

#### JP Throw Move

- **Ravina** / 雪崩 (JP).
- **Uragan** / 暴风 (JP).
- **Tornado** / 龙卷风 (JP).

### Zangief / 桑吉尔夫

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/zangief/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#zangief).

#### Zangief Special Move

- **Double Lariat** / 双截旋风掌 (Zangief); aliases: lariat.
- **Screw Piledriver** / 螺旋打桩机 (Zangief); aliases: SPD.
- **Borscht Dynamite** / 罗宋汤爆炸 (Zangief); aliases: air SPD.
- **Russian Suplex** / 俄式过背摔 (Zangief).
- **Siberian Express** / 西伯利亚快车 (Zangief); aliases: running bear grab.
- **Tundra Storm** / 冻原风暴 (Zangief).

#### Zangief Super Move

- **Aerial Russian Slam** / 空中俄式抱摔 (Zangief); aliases: SA1, 一气, 1气, SA 1, SA-1,
  LV1, LV.1, LVL1, Level 1, LV 1.
- **Cyclone Lariat** / 飓风双截掌 (Zangief); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Bolshoi Storm Buster** / 大剧院风暴炸弹摔 (Zangief); aliases: SA3, 三气, 3气, CA, SA 3,
  SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### Zangief Unique Move

- **Hellstab** / 地狱刺 (Zangief); aliases: 3mp, 前下中拳.
- **Knee Hammer** / 膝槌 (Zangief); aliases: 6mk, 前中脚.
- **Headbutt** / 头槌 (Zangief); aliases: 6hp, 前重拳.
- **Cyclone Wheel Kick** / 旋风轮转踢 (Zangief); aliases: 中段, 砸猪头.
- **Smetana Dropkick** / 酸奶油飞身踢 (Zangief); aliases: 3hk, 前下重脚.
- **Flying Body Press** / 飞身压 (Zangief); aliases: 中段, 砸猪头.
- **Flying Headbutt** / 空中头槌 (Zangief); aliases: 中段, 砸猪头.
- **Machine Gun Chops** / 机枪手刀 (Zangief); aliases: mp>mp>mp, 中拳>中拳>中拳.
- **Power Stomps** / 能量踩踏 (Zangief); aliases: 22mk>mk>mk, 下下中脚>中脚>中脚.

#### Zangief Throw Move

- **Bodyslam** / 抱摔 (Zangief).
- **Capture Suplex** / 抓捕过背摔 (Zangief).
- **German Suplex** / 德式拱桥摔 (Zangief).
- **Spinebuster** / 脊背重摔 (Zangief).
- **Russian Drop** / 俄式坠击 (Zangief).
- **Brain Buster** / 脑部重摔 (Zangief).

### Lily / 莉莉

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/lily/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#lily).

#### Lily Special Move

- **Condor Wind** / 秃鹰风 (Lily); aliases: wind.
- **Condor Spire** / 秃鹰尖 (Lily); aliases: spire.
- **Tomahawk Buster** / 战斧灭 (Lily).
- **Condor Dive** / 秃鹰潜 (Lily).
- **Condor Dive (Follow-up)** / 秃鹰潜 (Lily); aliases: Condor Dive (Follow up),
  Condor Dive (Followup).
- **OD Condor Dive** / 斗爆秃鹰潜 (Lily).
- **Mexican Typhoon** / 墨西哥台风 (Lily).

#### Lily Super Move

- **Breezing Hawk** / 轻风鹰 (Lily); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Thunderbird** / 雷鸟 (Lily); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Soaring Thunderbird** / 空中雷鸟 (Lily); aliases: SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **Raging Typhoon** / 暴怒台风 (Lily); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Lily Unique Move

- **Ridge Thrust** / 冲断岭 (Lily); aliases: 中段, 砸猪头.
- **Horn Breaker** / 角骨破 (Lily); aliases: 4hp, 后重拳.
- **Great Spin** / 大回旋 (Lily); aliases: 中段, 砸猪头.
- **Double Arrow** / 双发箭 (Lily); aliases: 中段, 砸猪头.
- **Desert Storm** / 沙漠风暴 (Lily); aliases: 6hp>hp>hp, 前重拳>重拳>重拳.

#### Lily Throw Move

- **Canyon Throw** / 峡谷摔 (Lily).
- **Falling Cliff** / 落崖坠 (Lily).

#### Lily Character State

- **Wind Stock** / 风绕 (Lily); aliases: wind stocks, windstacks.

### Cammy / 嘉米

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/cammy/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#cammy).

#### Cammy Special Move

- **Spiral Arrow** / 螺旋飞箭 (Cammy); aliases: 地箭.
- **Cannon Spike** / 神枪机兵 (Cammy).
- **Quick Spin Knuckle** / 快旋反转拳 (Cammy); aliases: spin knuckle.
- **Cannon Strike** / 机兵突击 (Cammy); aliases: divekick, dive kick.
- **Hooligan Combination** / 流氓组合技 (Cammy); aliases: hooligan.
- **Razor's Edge Slicer** / 下铲刀锋腿 (Cammy); aliases: Razors Edge Slicer, Razor’s
  Edge Slicer.
- **Reverse Edge** / 倒翻刀锋腿 (Cammy).
- **Fatal Leg Twister** / 夺命旋风腿 (Cammy).
- **Silent Step** / 暗中佯动 (Cammy).

#### Cammy Super Move

- **Spin Drive Smasher** / 螺旋驱动碎 (Cammy); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Killer Bee Spin** / 杀人蜂回旋 (Cammy); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Aerial Killer Bee Spin** / 空中杀人蜂回旋 (Cammy); aliases: SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Delta Red Assault** / 红色三角洲强袭 (Cammy); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### Cammy Unique Move

- **Lift Uppercut** / 上袭勾拳 (Cammy); aliases: 4mp, 后中拳.
- **Delayed Ripper** / 延时死神 (Cammy); aliases: 6hk, 前重脚.
- **Assault Blade** / 强袭利刃 (Cammy); aliases: 4hk, 后重脚.
- **Lift Combination** / 上袭组合技 (Cammy); aliases: 4mp>hk, 后中拳>重脚.
- **Swing Combination** / 摇摆组合技 (Cammy); aliases: hp>hk, 重拳>重脚.

#### Cammy Throw Move

- **Rough Landing** / 粗暴摔地 (Cammy).
- **Delta Throw** / 三角洲绞颈摔 (Cammy).
- **Leg Scissors Choke** / 双腿剪刀绞 (Cammy).

### Rashid / 拉希德

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/rashid/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#rashid).

#### Rashid Special Move

- **Spinning Mixer** / 回旋搅 (Rashid); aliases: mixer.
- **Eagle Spike** / 雄鹰踢 (Rashid).
- **Whirlwind Shot** / 旋风踢射 (Rashid); aliases: tornado.
- **Arabian Cyclone** / 阿拉伯飓风 (Rashid).
- **Wing Stroke** / 鹰翼式 (Rashid).
- **Rolling Assault** / 翻滚奇袭 (Rashid).
- **Nail Assault** / 痛踢奇袭 (Rashid).
- **Arabian Skyhigh** / 阿拉伯高空 (Rashid).

#### Rashid Super Move

- **Super Rashid Kick** / 超级拉希德踢 (Rashid); aliases: SA1, 一气, 1气, SA 1, SA-1,
  LV1, LV.1, LVL1, Level 1, LV 1.
- **Ysaar** / 龙卷风 (Rashid); aliases: SA2, 二气, 2气, tornado, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Altair** / 飞翔之鹰 (Rashid); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3, LV.3,
  LVL3, Level 3, LV 3.

#### Rashid Unique Move

- **Run** / 奔跑 (Rashid); aliases: 66[6], 前前长按前.
- **Backup** / 后手 (Rashid); aliases: 6p, 前拳.
- **Tempest Moon** / 风暴之月 (Rashid); aliases: 6k, 前脚.
- **Flapping Spin** / 鹰翼旋 (Rashid); aliases: 6mp, 前中拳.
- **Beak Assault** / 鹰喙袭 (Rashid); aliases: 中段, 砸猪头.
- **Crescent Kick** / 新月踢 (Rashid); aliases: 6hk, 前重脚.
- **Blitz Strike** / 闪电击 (Rashid); aliases: 中段, 砸猪头.
- **Aerial Shot** / 凌空射 (Rashid); aliases: 中段, 砸猪头.
- **Rising Kick** / 升空踢 (Rashid); aliases: mp>hk, 中拳>重脚.
- **Side Flip** / 侧边翻转 (Rashid); aliases: 6kk, 前双脚.
- **Front Flip** / 前跳翻转 (Rashid); aliases: 4kk, 后双脚, 5kk, 双脚, 6kk, 前双脚.
- **Wall Jump** / 三角跳 (Rashid); aliases: 9, 前上.

#### Rashid Throw Move

- **Riding Glider** / 驾乘滑冲 (Rashid).
- **Sunset Drop** / 落日坠击 (Rashid).
- **Desert Slider** / 沙漠滑行 (Rashid).

#### Rashid Character State

- **Air Current** / 气流 (Rashid).

### A.K.I. / 阿鬼

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/aki/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#aki).

#### A.K.I. Special Move

- **Nightshade Pulse** / 紫烟炮 (A.K.I.); aliases: bubble.
- **Nightshade Chaser** / 紫烟追 (A.K.I.).
- **Orchid Spring** / 紫泡泉 (A.K.I.).
- **Toxic Wreath** / 紫泡撒 (A.K.I.).
- **Serpent Lash** / 蛇头鞭 (A.K.I.); aliases: whip.
- **Cruel Fate** / 凶袭突 (A.K.I.).
- **Snake Step** / 蛇轻功 (A.K.I.).
- **Sinister Slide** / 恶鬼蛇行 (A.K.I.).
- **Venomous Fang** / 猛毒牙 (A.K.I.).
- **Heel Strike** / 蛇连咬 (A.K.I.).
- **Entrapment** / 雁字缠 (A.K.I.).

#### A.K.I. Super Move

- **Deadly Implication** / 死尸累累 (A.K.I.); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Tainted Talons** / 紫烟裂爪 (A.K.I.); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Claws of Ya Zi** / 睚眦 (A.K.I.); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### A.K.I. Unique Move

- **Pu Lao** / 蒲牢 (A.K.I.); aliases: 中段, 砸猪头.
- **Chi Wen** / 螭吻 (A.K.I.); aliases: 6hp, 前重拳.
- **Qiu Niu** / 囚牛 (A.K.I.); aliases: 6hk, 前重脚.
- **Gong Fu** / 蚣蝮 (A.K.I.); aliases: 中段, 砸猪头.
- **Hun Dun** / 混沌 (A.K.I.); aliases: lp>lp, 轻拳>轻拳.
- **Qiong Qi** / 穷奇 (A.K.I.); aliases: hp>hp, 重拳>重拳.

#### A.K.I. Throw Move

- **Whisper** / 赑屃 (A.K.I.).
- **Gluttony** / 饕餮 (A.K.I.).

#### A.K.I. Character State

- **Toxic Blossom** / 毒破裂 (A.K.I.).

### Ed / 爱德

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/ed/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#ed).

#### Ed Special Move

- **Psycho Spark** / 精神力闪光 (Ed).
- **Psycho Shoot** / 精神力反射 (Ed).
- **Psycho Uppercut** / 精神力上勾拳 (Ed).
- **Psycho Blitz** / 精神力闪攻 (Ed).
- **Psycho Flicker** / 精神力闪刺拳 (Ed); aliases: flicker, snatcher.
- **Kill Rush (Forward)** / 诛杀步 (前方) (Ed); aliases: 诛杀步.
- **Kill Switch Break** / 诛杀开关·破碎 (Ed).
- **Kill Switch Chaser** / 诛杀开关·追逐 (Ed).
- **Kill Rush (Backward)** / 诛杀步 (后方) (Ed); aliases: 诛杀步.

#### Ed Super Move

- **Psycho Storm** / 精神力风暴 (Ed); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Psycho Cannon** / 精神力炮弹 (Ed); aliases: SA2, 二气, 2气, 煤球, SA2煤球, SA 2, SA-2,
  LV2, LV.2, LVL2, Level 2, LV 2.
- **Psycho Chamber** / 精神力空间 (Ed); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Ed Unique Move

- **Psycho Knuckle** / 精神力冲拳 (Ed); aliases: [hp], 蓄力重拳.
- **Cobra Punch** / 眼镜蛇拳 (Ed); aliases: 6hp, 前重拳.
- **Flicker Combination** / 闪刺组合技 (Ed); aliases: lk>lk>lk, 轻脚>轻脚>轻脚.
- **Body Blow Combination** / 上体组合拳 (Ed); aliases: mp>hp, 中拳>重拳.
- **Hitman Combination** / 杀手组合技 (Ed); aliases: mk>mk>hp, 中脚>中脚>重拳.
- **Low Smash Combination** / 低重击组合技 (Ed); aliases: 2hk>hp, 下重脚>重拳.

#### Ed Throw Move

- **Face Buster** / 脸部炸弹摔 (Ed).
- **Rib Crusher** / 肋骨粉碎摔 (Ed).

### Akuma / 豪鬼

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/gouki_akuma/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#gouki).

#### Akuma Special Move

- **Gou Hadoken** / 豪波动拳 (Akuma).
- **Zanku Hadoken** / 斩空波动拳 (Akuma).
- **Gou Shoryuken** / 豪升龙拳 (Akuma).
- **Tatsumaki Zanku-kyaku** / 龙卷斩空腿 (Akuma); aliases: Tatsu, Tatsumaki Zanku
  kyaku, Tatsumaki Zankukyaku.
- **Aerial Tatsumaki Zanku-kyaku** / 空中龙卷斩空腿 (Akuma); aliases: air Tatsu, Aerial
  Tatsumaki Zanku kyaku, Aerial Tatsumaki Zankukyaku.
- **Adamant Flame** / 金刚灼火 (Akuma).
- **Demon Raid** / 百鬼袭 (Akuma); aliases: Demon Flip.
- **Demon Low Slash** / 百鬼豪斩 (Akuma).
- **Demon Guillotine** / 百鬼豪冲 (Akuma).
- **Demon Blade Kick** / 百鬼豪刃 (Akuma).
- **Demon Swoop** / 百鬼潜影 (Akuma).
- **Demon Gou Zanku** / 百鬼豪斩空 (Akuma).
- **Demon Gou Rasen** / 百鬼豪螺旋 (Akuma).
- **Ashura Senku** / 阿修罗闪空 (Akuma); aliases: teleport.
- **Oboro Throw** / 胧 (Akuma).

#### Akuma Super Move

- **Messatsu Gohado** / 灭杀豪波动 (Akuma); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Tenma Gozanku** / 天魔豪斩空 (Akuma); aliases: SA 1, SA-1, LV1, LV.1, LVL1, Level
  1, LV 1.
- **Empyrean's End** / 崩天劫火 (Akuma); aliases: SA2, 二气, 2气, Empyreans End,
  Empyrean’s End, SA 2, SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Sip of Calamity** / 祸坏 (Akuma); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.
- **Shun Goku Satsu** / 瞬狱杀 (Akuma); aliases: Raging Demon, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Akuma Unique Move

- **Skull Splitter** / 头盖破杀 (Akuma); aliases: 中段, 砸猪头.
- **Resso Snap Kick** / 裂枪脚 (Akuma); aliases: 6mk, 前中脚.
- **Rago High Kick** / 罗豪脚 (Akuma); aliases: 4hk, 后重脚.
- **Viscera Piercer** / 六腑穿 (Akuma); aliases: mp>mp, 中拳>中拳.
- **Bone Crusher Axe Kick** / 骸斩 (Akuma); aliases: 中段, 砸猪头.
- **Kikoku Combination** / 鬼哭连击 (Akuma); aliases: 6hp>6hp>hk, 前重拳>前重拳>重脚.
- **Tenmaku Blade Kick** / 天魔空刃腿 (Akuma); aliases: 2mk, 下中脚.

#### Akuma Throw Move

- **Goshoha** / 豪冲破 (Akuma).
- **Shuretto** / 朱裂刀 (Akuma).

### M. Bison / 维加

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/vega_mbison/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#vega).

#### M. Bison Special Move

- **Psycho Crusher Attack** / 精神力旋冲击 (M. Bison); aliases: 电钻.
- **Double Knee Press** / 双膝爆 (M. Bison); aliases: Scissor Kick, Scissor Kicks,
  剪刀脚, 重剪脚, 重双膝爆.
- **Backfist Combo** / 反手拳连招 (M. Bison).
- **Shadow Rise** / 影升 (M. Bison).
- **Head Press** / 头部踏压 (M. Bison).
- **Somersault Skull Diver** / 空翻头骨落 (M. Bison).
- **Devil Reverse** / 逆魔破 (M. Bison).

#### M. Bison Super Move

- **Knee Press Nightmare** / 膝爆梦魇 (M. Bison); aliases: SA1, 一气, 1气, SA 1, SA-1,
  LV1, LV.1, LVL1, Level 1, LV 1.
- **Psycho Punisher** / 精神力惩罚者 (M. Bison); aliases: SA2, 二气, 2气, SA 2, SA-2,
  LV2, LV.2, LVL2, Level 2, LV 2.
- **Unlimited Psycho Crusher** / 终极精神力旋冲 (M. Bison); aliases: SA3, 三气, 3气, CA,
  SA 3, SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### M. Bison Unique Move

- **Psycho Hammer** / 精神重锤 (M. Bison); aliases: 中段, 砸猪头.
- **Evil Knee** / 邪恶之膝 (M. Bison); aliases: 4hk, 后重脚.
- **Hover Kick** / 滑铲踢 (M. Bison); aliases: 3hk, 前下重脚.
- **Shadow Hammer** / 重影锤 (M. Bison); aliases: 中段, 砸猪头.
- **Shadow Spear** / 邪影矛 (M. Bison); aliases: mp>2hk, 中拳>下重脚.
- **Hell Attack** / 地狱攻击 (M. Bison); aliases: mp>mp, 中拳>中拳.

#### M. Bison Throw Move

- **Deadly Throw** / 夺命摔 (M. Bison).
- **Death Tower** / 死亡之塔 (M. Bison).

### Terry / 特瑞

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/terry/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#terry).

#### Terry Special Move

- **Power Wave** / 能量波 (Terry).
- **Round Wave** / 圆波 (Terry).
- **Quick Burn** / 快速燃烧 (Terry).
- **Burning Knuckle** / 燃烧指节 (Terry); aliases: Burn Knuckle.
- **Power Charge** / 能量冲锋 (Terry).
- **Crack Shoot** / 崩裂喷射 (Terry).
- **Rising Tackle** / 升龙摔 (Terry).

#### Terry Super Move

- **Buster Wolf** / 非凡之狼 (Terry); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Power Geyser** / 能量喷泉 (Terry); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Twin Geyser** / 双重能量喷泉 (Terry); aliases: SA 2, SA-2, LV2, LV.2, LVL2, Level
  2, LV 2.
- **Triple Geyser** / 三重能量喷泉 (Terry); aliases: SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **Rising Fang** / 升龙牙 (Terry); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Terry Unique Move

- **Hammer Punch** / 重锤拳 (Terry); aliases: 中段, 砸猪头.
- **Power Drive** / 能量驱动 (Terry); aliases: mp>hp, 中拳>重拳.
- **Power Shoot** / 能量投篮 (Terry); aliases: mp>hk, 中拳>重脚.
- **Power Dunk** / 能量灌篮 (Terry); aliases: mp>hk>hk, 中拳>重脚>重脚.
- **Passing Sway** / 穿越摇摆 (Terry); aliases: mp>mk, 中拳>中脚.
- **Jumping Lariat** / 跳跃臂勾 (Terry); aliases: mp>mk>mp, 中拳>中脚>中拳.
- **Jumping Knee** / 跳跃膝撞 (Terry); aliases: mp>mk>mk, 中拳>中脚>中脚.
- **Fire Kick** / 火焰踢 (Terry); aliases: 2mk>2hk, 下中脚>下重脚.

#### Terry Throw Move

- **Grasping Upper** / 强袭投 (Terry).
- **Buster Throw** / 破坏投 (Terry).

### Mai / 舞

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/mai/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#mai).

#### Mai Special Move

- **Kachousen** / 花蝶扇 (Mai); aliases: fan, fans.
- **Midare Kachousen** / 乱花蝶扇 (Mai).
- **Ryuuenbu** / 龙炎舞 (Mai).
- **Hissatsu Shinobi Bachi** / 必杀忍蜂 (Mai).
- **Hishou Ryuuenjin** / 飞翔龙炎阵 (Mai); aliases: DP.
- **Musasabi no Mai** / 鼯鼠之舞 (Mai).

#### Mai Super Move

- **Kagerou no Mai** / 阳炎之舞 (Mai); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Chou Hissatsu Shinobi Bachi** / 超必杀忍蜂 (Mai); aliases: SA2, 二气, 2气, SA 2,
  SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Air Chou Hissatsu Shinobi Bachi** / 空中超必杀忍蜂 (Mai); aliases: SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Shiranui Ryuu: Enbu Ada Zakura** / 不知火流·炎舞仇樱 (Mai); aliases: SA3, 三气, 3气,
  CA, Shiranui Ryuu Enbu Ada Zakura, SA 3, SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### Mai Unique Move

- **Senkotsu Uchi** / 扇骨打 (Mai); aliases: 中段, 砸猪头.
- **Hien Ren Kyaku** / 飞燕连脚 (Mai); aliases: lk>lk>lk, 轻脚>轻脚>轻脚.
- **Hoshi Kujaku** / 星孔雀 (Mai); aliases: 4hk>hk, 后重脚>重脚.

#### Mai Throw Move

- **Shiranui Gourin** / 不知火刚临 (Mai).
- **Fuusha Kuzushi** / 风车崩 (Mai).
- **Yume Zakura** / 梦樱 (Mai).

#### Mai Character State

- **Flame Stock** / 忍焰 (Mai).

### Elena / 艾琳娜

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/elena/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#elena).

#### Elena Special Move

- **Rhino Horn** / 犀角踢 (Elena).
- **Scratch Wheel** / 轮刮踢 (Elena).
- **Lynx Song** / 连结之歌 (Elena).
- **Leopard Snap** / 花豹迅击 (Elena).
- **Harvest Circle** / 圆弧收割 (Elena).
- **Mallet Smash** / 猛锤踢 (Elena).
- **Lynx Whirl** / 连结回旋 (Elena).
- **Spinning Scythe** / 旋转镰刀 (Elena).
- **Moon Glider** / 半月弧影踢 (Elena).

#### Elena Super Move

- **Meteor Volley** / 流星凌空踢 (Elena); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Revival Dance** / 复苏之歌 (Elena); aliases: SA2, 二气, 2气, 回血超必杀, 回血必杀, SA 2,
  SA-2, LV2, LV.2, LVL2, Level 2, LV 2.
- **Song of the Grasslands** / 草原之歌 (Elena); aliases: SA3, 三气, 3气, CA, SA 3,
  SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### Elena Unique Move

- **Slide** / 滑铲 (Elena); aliases: 3hk, 前下重脚.
- **Round Arch** / 圆弧踢 (Elena); aliases: 4hk, 后重脚.
- **Starling Beak** / 椋鸟喙啄 (Elena); aliases: mp>mp, 中拳>中拳.
- **Handstand Whip** / 倒立腿鞭 (Elena); aliases: 中段, 砸猪头.
- **Hind Kick** / 后蹄踢 (Elena); aliases: mk>hk, 中脚>重脚.
- **Fluttering Lark** / 云雀振翅 (Elena); aliases: 2mk>hk, 下中脚>重脚.
- **Turning Tail** / 回旋尾鞭 (Elena); aliases: hp>hp, 重拳>重拳.
- **Trunk Slap** / 象鼻掴打 (Elena); aliases: 6hp>hp>hp, 前重拳>重拳>重拳.
- **Soaring Raid** / 翱翔奇袭 (Elena); aliases: lp>mk, 轻拳>中脚.
- **Raptor Range** / 猛禽突击 (Elena); aliases: 中段, 砸猪头.

#### Elena Throw Move

- **Leg Tackle** / 腿锁摔 (Elena).
- **Leg Lift Throw** / 腿举抛 (Elena).

### Sagat / 沙加特

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/sagat/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#sagat).

#### Sagat Special Move

- **High Tiger Shot** / 猛虎波 (Sagat).
- **Low Tiger Shot** / 下段猛虎波 (Sagat).
- **Tiger Uppercut** / 猛虎升龙破 (Sagat).
- **Tiger Knee Crush** / 猛虎跳膝撞 (Sagat).
- **Tiger Nexus** / 猛虎连结 (Sagat).
- **Mighty Tiger** / 猛虎威击 (Sagat).
- **Greedy Tiger** / 猛虎贪婪 (Sagat).
- **Nova Tiger** / 猛虎新星 (Sagat).

#### Sagat Super Move

- **Tiger Cannon** / 猛虎炮 (Sagat); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Savage Tiger** / 残暴之虎 (Sagat); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Savage Tiger Raid** / 残暴之虎突袭 (Sagat); aliases: SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **Savage Tiger Zenith** / 残暴之虎巅峰 (Sagat); aliases: SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Savage Tiger Pendulum** / 残暴之虎摆荡 (Sagat); aliases: SA 2, SA-2, LV2, LV.2,
  LVL2, Level 2, LV 2.
- **Savage Tiger Stomp** / 残暴之虎重锤 (Sagat); aliases: SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **Tiger Vanquisher** / 猛虎征服者 (Sagat); aliases: SA3, 三气, 3气, CA, SA 3, SA-3,
  LV3, LV.3, LVL3, Level 3, LV 3.

#### Sagat Unique Move

- **Tiger Heavy Elbow** / 猛虎重砸肘 (Sagat); aliases: 中段, 砸猪头.
- **Tiger Monolith** / 猛虎巨石 (Sagat); aliases: 4hp, 后重拳.
- **Low Step Kick** / 前踏低扫踢 (Sagat); aliases: 6lk, 前轻脚.
- **High Step Kick** / 前踏高扫踢 (Sagat); aliases: 6hk, 前重脚.
- **Middle Step Kick** / 前踏中扫踢 (Sagat); aliases: mk>hk, 中脚>重脚.
- **Tiger Sting** / 猛虎扎 (Sagat); aliases: hp>hk, 重拳>重脚.
- **Tiger Slash** / 猛虎斩 (Sagat); aliases: 2mp>hp, 下中拳>重拳.
- **Tiger Rise** / 猛虎升 (Sagat); aliases: 2mp>hk, 下中拳>重脚.

#### Sagat Throw Move

- **Tiger Hang** / 猛虎悬 (Sagat).
- **Tiger Carry** / 猛虎摔 (Sagat).

### C. Viper / 深红毒蛇

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/cviper/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#cviper).

#### C. Viper Special Move

- **Thunder Dash** / 雷电掴打 (C. Viper); aliases: TK, Thunder Knuckle.
- **Tracer Combination** / 追踪组合技 (C. Viper).
- **Feint** / 假动作 (C. Viper).
- **Burning Kick** / 烈焰踢 (C. Viper); aliases: Burn Kick.
- **Knuckled Pursuit** / 追击冲拳 (C. Viper).
- **Double Burn** / 双重灼烧 (C. Viper).
- **Aerial Burning Kick** / 空中烈焰踢 (C. Viper).
- **Seismic Hammer** / 震地重锤 (C. Viper); aliases: seismo.
- **Focus Force** / 蓄能之力 (C. Viper).

#### C. Viper Super Move

- **Limit Decoupler** / 弹击步 (C. Viper); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1,
  LV.1, LVL1, Level 1, LV 1.
- **Mission Complete** / 任务终结 (C. Viper); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Hard Luck Rejector** / 厄运排斥者 (C. Viper); aliases: SA3, 三气, 3气, CA, SA 3,
  SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### C. Viper Unique Move

- **Viper Elbow** / 毒蛇肘击 (C. Viper); aliases: 中段, 砸猪头.
- **Double Kick** / 双连踢 (C. Viper); aliases: 6hk, 前重脚.
- **High Jump** / 大跳跃 (C. Viper); aliases: 29, 下前上, 28, 下上.

#### C. Viper Throw Move

- **High Impulse** / 过载脉冲 (C. Viper).
- **Thunder Cradle** / 闪电怀抱 (C. Viper).

### Alex / 阿里克斯

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/alex/movelist); [Chinese
community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#alex).

#### Alex Special Move

- **Flash Axe** / 闪光手斧 (Alex).
- **Flash Chop** / 闪光手刀 (Alex).
- **Aerial Knee Smash** / 空中膝撞 (Alex).
- **Power Bomb** / 炸弹摔 (Alex); aliases: Pwr Bomb.
- **Hyper Bomb** / 超级炸弹 (Alex).

#### Alex Super Move

- **Raging Spear** / 狂怒飞冲 (Alex); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Sledgecross Hammer** / 交叉猛摔 (Alex); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Omega Wing Buster** / 最终臂摔 (Alex); aliases: SA 2, SA-2, LV2, LV.2, LVL2,
  Level 2, LV 2.
- **The Final Prison** / 终极捕获 (Alex); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Alex Unique Move

- **Prowler Stance** / 破坏姿势 (Alex); aliases: 2pp, 下双拳.
- **Low Rush** / 前滑步 (Alex); aliases: 6, 前.
- **Low Retreat** / 后滑步 (Alex); aliases: 4, 后.
- **Slashing Elbow** / 肘斩 (Alex); aliases: 6p, 前拳, 6lp, 前轻拳, 6mp, 前中拳, 6hp, 前重拳.
- **Palm Jab** / 掌刺 (Alex); aliases: 5lp, 轻拳.
- **Shoulder Launcher** / 肩撞 (Alex); aliases: 5mp, 中拳.
- **Heavy Lariat** / 重臂勾 (Alex); aliases: 5hp, 重拳.
- **Tactical Hop** / 策略跳 (Alex); aliases: 5lk, 轻脚.
- **Air Stampede** / 空落踩 (Alex); aliases: 中段, 砸猪头.
- **Sweep Combination** / 扫腿组合技 (Alex); aliases: hk>hk, 重脚>重脚.
- **Hyper Takedown** / 超级放倒 (Alex); aliases: lp+lk, 轻拳+轻脚.
- **Dangerous Armbar** / 危险肘固 (Alex); aliases: 2lp+lk, 下轻拳+轻脚.
- **Chop** / 手刀 (Alex); aliases: 中段, 砸猪头.
- **Oblique Stomp** / 斜踩 (Alex); aliases: 4mk, 后中脚.
- **Flying Cross Chop** / 飞身交叉劈 (Alex); aliases: 2hp, 下重拳.
- **Palm Strikes** / 掌击 (Alex); aliases: mp>hp, 中拳>重拳.
- **Twisted Drop** / 螺旋坠 (Alex); aliases: 2lk>2hk, 下轻脚>下重脚.

#### Alex Throw Move

- **Arm Lock** / 臂锁 (Alex).
- **Guillotine Hammer** / 断头重锤 (Alex).
- **Illegal Knees** / 犯规膝撞 (Alex).

### Ingrid / 英格丽德

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/ingrid/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#ingrid).

#### Ingrid Special Move

- **Sun Shot** / 日射 (Ingrid); aliases: Sunshot.
- **Sun Flare** / 日耀 (Ingrid); aliases: Sunflare.
- **Solar Burst** / 日焰 (Ingrid).
- **Sun Rise** / 日射踢 (Ingrid).
- **Sun Veil** / 太阳面纱 (Ingrid).
- **Vanishing Sun** / 日隐技 (Ingrid).

#### Ingrid Super Move

- **Shining Sun** / 骄阳照耀 (Ingrid); aliases: SA1, 一气, 1气, SA 1, SA-1, LV1, LV.1,
  LVL1, Level 1, LV 1.
- **Order of the Sun** / 烈日秩序 (Ingrid); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Cosmic Ray** / 宇宙射线 (Ingrid); aliases: SA3, 三气, 3气, CA, SA 3, SA-3, LV3,
  LV.3, LVL3, Level 3, LV 3.

#### Ingrid Unique Move

- **Sun Bright** / 曦光 (Ingrid); aliases: 中段, 砸猪头.
- **Halo Flight** / 光轮飞劈 (Ingrid); aliases: 6hp, 前重拳.
- **Pretty Heel Kick** / 空旋踝踢 (Ingrid); aliases: mp>mk, 中拳>中脚.
- **Glowing Touch** / 发光触碰 (Ingrid); aliases: 4mk>hp, 后中脚>重拳.
- **Luminous Uppercut** / 明亮上段击 (Ingrid); aliases: 4hp>hp, 后重拳>重拳.
- **Satellite Leap** / 卫星跳踢 (Ingrid); aliases: 中段, 砸猪头.

#### Ingrid Throw Move

- **Strange Knuckle** / 奇异拳 (Ingrid).
- **Gravity Drop** / 重力摔 (Ingrid).

#### Ingrid Character State

- **Sun Crest** / 太阳符纹 (Ingrid); aliases: Suncrest, 印记.

### Yasmine / 亚思敏

Source: [Capcom command
list](https://www.streetfighter.com/6/zh-hans/character/yasmine/movelist);
[Chinese community
reference](https://www.spmoves.com/sp1/street_fighter_6/sf6_chs.html#yasmine).

#### Yasmine Special Move

- **Daloy ng Tubig** / 激流连击 (Yasmine).
- **Alon** / 涌浪 (Yasmine).
- **Talim ng Hangin** / 旋风刃 (Yasmine).
- **Mukha ng Langit** / 天相显容 (Yasmine).
- **Ulan** / 骤雨 (Yasmine).
- **Kulog** / 落雷 (Yasmine).
- **Lipad ng Agila** / 雕王飞踢 (Yasmine).
- **Pangil sa Likuran** / 蛇牙回噬 (Yasmine).
- **Linya ng Liwanag** / 光芒轨迹 (Yasmine).

#### Yasmine Super Move

- **Hiwa ng Kalangitan** / 螺旋空斩 (Yasmine); aliases: SA1, 一气, 1气, SA 1, SA-1,
  LV1, LV.1, LVL1, Level 1, LV 1.
- **Nakatagong Lakas** / 潜藏之力 (Yasmine); aliases: SA2, 二气, 2气, SA 2, SA-2, LV2,
  LV.2, LVL2, Level 2, LV 2.
- **Pamumukadkad ng Sampaguita** / 茉莉绽放 (Yasmine); aliases: SA3, 三气, 3气, CA, SA
  3, SA-3, LV3, LV.3, LVL3, Level 3, LV 3.

#### Yasmine Unique Move

- **Hiwang Pababa** / 下旋裂爪 (Yasmine); aliases: 中段, 砸猪头.
- **Walis na Pabagsak** / 旋风扫腿 (Yasmine); aliases: 4hk, 后重脚.
- **Kidlat na Hiwa** / 闪电斩击 (Yasmine); aliases: lp>lp, 轻拳>轻拳.
- **Tatlong Hiwa** / 三连斩击 (Yasmine); aliases: mp>mp, 中拳>中拳.
- **Sunod-sunod na Sipa** / 多段连踢 (Yasmine); aliases: Sunod sunod na Sipa,
  Sunodsunod na Sipa, mk>mk>hk, 中脚>中脚>重脚.
- **Kumbinasyong Pampabagsak** / 倒地组合技 (Yasmine); aliases: 2mk>hk, 下中脚>重脚.

#### Yasmine Throw Move

- **Pigil-Ulo** / 破颅重击 (Yasmine); aliases: Pigil Ulo, PigilUlo.
- **Hila-Kamay** / 牵引连击 (Yasmine); aliases: Hila Kamay, HilaKamay.

#### Yasmine Character State

- **Bayani Mode** / 英雄模式 (Yasmine); aliases: Bayani.

## Expansion sources

- [Capcom current roster](https://www.streetfighter.com/6/zh-hans/character) —
  live roster, checked October 8, 2026; historical inclusion is recorded
  separately.
- [Capcom Yasmine
  launch](https://news.capcomusa.com/2026/08/03/activate-bayani-mode-as-yasmine-launches-today-in-street-fighter-6/)
  — confirms August 3, 2026 inclusion.
- [Capcom official Steam
  announcements](https://steamcommunity.com/app/1364780/announcements/) — future
  Year 4 releases are excluded.
- [SPMoves linked move-name
  reference](https://www.spmoves.com/sp1/street_fighter_6/sf6.html) —
  intermediate name pairing only; no Japanese or traditional Chinese aliases
  added.
Each character-specific section links its own official command list. The machine
configuration stores the corresponding source IDs and blank review fields. No
current frame counts, damage values, or patch adjustments were copied into this
vocabulary.

## Super Art levels and Critical Art

SA1, SA2, and SA3 identify Super Art levels, not specific character moves
without subject context. The Chinese meter nicknames can also describe a
resource amount. They must not be confused with Drive Gauge stocks.

- **SA1 / 一气 / 1气**: Level 1 Super Art; with Ryu context (as an example), Shinku
  Hadoken / 真空波动拳.
- **SA2 / 二气 / 2气**: Level 2 Super Art; with Ryu context (as an example), Shin
  Hashogeki / 真波掌击. Its charge levels are a separate concept.
- **SA3 / 三气 / 3气**: Level 3 Super Art; with Ryu context (as an example), Shin
  Shoryuken / 真升龙拳.
- **CA / SA3 / 三气**: In Chinese community feedback, normalize these move
  nicknames to the same Level 3 Super Art family; with Ryu context (as an
  example), Shin Shoryuken / 真升龙拳. Strict Critical Art terminology still
  identifies an enhanced variant when explicitly stated.

For example, a statement that the player has three stocks remaining describes
Super Gauge. A request to weaken Ryu SA3 or bare CA describes the same move
family under the project Chinese community convention. Neither nickname by
itself establishes an enhanced variant.

## Project Chinese community convention

Source: user instruction in this project chat. Bare CA and SA3 are treated as
the same Level 3 Super Art family when analyzing Chinese community feedback.
This convention does not change official mechanics or imply that every use of CA
describes the enhanced variant. Preserve original evidence.

## Configuration structure and runtime use

- Top-level metadata identifies the game, target patch, languages, collection
  status, and schema version. The patch label does not make this a numerical
  frame-data database.
- `policy` stores interpretation constraints; `sources` stores provenance keyed
  by source ID.
- `entries` contains concepts with stable `id`, English `canonical_name`,
  `chinese_label`, `category`, `scope`, aliases, optional Classic notation,
  notes, source IDs, and pending human review fields.
- Each alias carries its language, kind, and provenance. Some aliases also carry
  context requirements or a normalized target ID.
- `ambiguous_aliases` contains candidate concept IDs and context-dependent
  resolution guidance.
- `numpad_directions` and `notation_rules` explain input notation.
  `universal_categories` identifies categories that apply to all characters.
  `community_normalization` records Chinese community CA-to-SA3 conventions.
  `roster` and `roster_policy` freeze target-version inclusion;
  `character_state` is the category for subject-specific modes and resources.

The smoke-test runner uses this file only when `--glossary` is selected. It
retrieves lexical candidates from each comment, filters character-specific
candidates by explicitly matched subject labels, keeps subject-free SA level
aliases universal, adds candidates referenced by matching ambiguity records, and
supplies a compact reference containing policy, selected concepts, ambiguity
guidance, and community normalization to the model. It does not rewrite the
comment, automatically resolve short aliases, or infer a character from a
universal normal move. Pending nickname aliases remain visible as candidates but
do not establish hard subject scope. Alias kinds and context restrictions are
supplied to the model. Source and human-review metadata are preserved in the run
snapshot but are not used to score the model. Subject matching is a lexical
heuristic and still requires semantic review. Input-notation tables remain
configuration for future parsing; the current runner does not implement a full
notation parser.

Each run freezes the glossary, cases, patch context, and prompt, records a
glossary hash, and saves complete rendered requests and raw responses. Model
output still requires semantic review: vocabulary recognition alone does not
establish the requested balance direction or prove patch facts.

## Community alias expansion and manual review

The October 8 alias expansion is recorded in [alias-review.md](alias-review.md).
New aliases are candidates with blank per-alias review fields. Observed
community words, historical nicknames, and generated notation/spelling variants
are explicitly distinguished. The collection deliberately retains overloaded
descriptions and branch-unspecified supers for review. No usage-frequency or
completeness claim is made.

New universal concepts needed to interpret the collected shorthand:

- **Level 1 Super Art** / 一气超必杀 (universal); aliases: SA1, SA 1, 一气, 1气, 1级超必杀,
  SA-1, LV1, LV.1, LVL1, Level 1, LV 1, 1格大招, 1气大招.
- **Level 2 Super Art** / 二气超必杀 (universal); aliases: SA2, SA 2, 二气, 2气, 2级超必杀,
  SA-2, LV2, LV.2, LVL2, Level 2, LV 2, 2格大招, 2气大招.
- **Level 3 Super Art** / 三气超必杀 (universal); aliases: SA3, SA 3, 三气, 3气, 3级超必杀,
  CA, 三气大招, SA-3, LV3, LV.3, LVL3, Level 3, LV 3, 3格大招, 3气大招.
- **Dragon Punch-type Move** / 升龙类招式 (universal); aliases: DP, Dragon Punch, 升龙,
  Dragon Punch type Move, Dragon Punchtype Move.
- **Target Combo** / 目标连段 (universal); aliases: TC, 特定连段, TC连段, 固定连段.
- **Hard Knockdown** / 强制倒地 (universal); aliases: HKD, 不可受身.
- **Delay** / 延迟 (universal); aliases: dl., 延迟释放, 放帧.
- **Reversal** / 反转技 (universal); aliases: wake-up reversal, 凹, 起身凹.
- **Safe Jump** / 安全跳 (universal); aliases: safejump.
- **Option Select** / 复合 (universal); aliases: OS, option-select.
- **Delayed Throw Tech** / 延迟拆投 (universal); aliases: delay tech, delayed tech,
  延迟拆.
- **Frame Trap** / 帧陷阱 (universal); aliases: frametrap, 帧数陷阱.
- **Spacing Trap** / 差合陷阱 (universal).
- **Teabagging** / 茶包 (universal); aliases: teabag, tea bagging.
- **Total Frames** / 总帧 (universal); aliases: total duration.
- **Hit Advantage** / 命中优势 (universal); aliases: on-hit advantage, 命中有利.
- **Block Advantage** / 防御优势 (universal); aliases: on-block advantage, 防御有利.
- **Perfect Victory** / 完美胜利 (universal); aliases: perfect, pf., 完美.
