# Unique Move Alias Review

Reference checked: October 8, 2026. Target experiment patch: August 3, 2026.
Live Capcom properties have not been independently matched to the historical
patch. All decisions remain blank.

Rules: overhead moves receive 中段 and 砸猪头. Other moves receive lowercase
numpad/button notation and simplified Chinese direction/button labels. Existing
aliases are retained. Target combos use complete sequences; movement-only
actions use their actual direction inputs. Neutral buttons use 5. Stance,
airborne, proximity, hold, and resource conditions are stored separately in JSON
and shown below.

A Mid hit qualifies even when other hits are High or Low. The labels do not
imply every hit is overhead. Generic 中段 can still refer to the universal
overhead concept. Shared input aliases require character and move context.

Coverage: 31 characters, 244 entries; 51 with an overhead hit; 510 new alias
mappings.

## Ryu Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/ryu/frame); [Capcom command
list](https://www.streetfighter.com/6/character/ryu/movelist).

### Ryu: Collarbone Breaker

- Entry: `ryu.collarbone` / 锁骨破
- Observed properties: \*MidHigh
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: Already present
- Conditions: None specified
- Property note: Second hit becomes an overhead only when the first hit whiffs.
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ryu: Solar Plexus Strike

- Entry: `ryu.solar` / 鸠尾碎
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ryu: Short Uppercut

- Entry: `ryu.uppercut` / 上突
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ryu: Axe Kick

- Entry: `ryu.axe` / 踵落
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ryu: Whirlwind Kick

- Entry: `ryu.whirlwind` / 旋风腿
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ryu: High Double Strike

- Entry: `ryu.double` / 上段二连击
- Observed properties: High
- Complete input: hp>hk
- Required aliases: hp>hk, 重拳>重脚
- Newly added: hp>hk, 重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ryu: Fuwa Triple Strike

- Entry: `ryu.fuwa` / 不破三连击
- Observed properties: High
- Complete input: mp>lk>hk
- Required aliases: mp>lk>hk, 中拳>轻脚>重脚
- Newly added: mp>lk>hk, 中拳>轻脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Luke Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/luke/frame); [Capcom command
list](https://www.streetfighter.com/6/character/luke/movelist).

### Luke: Rawhide

- Entry: `luke.unique.rawhide` / 生皮鞭
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Luke: Suppressor

- Entry: `luke.unique.suppressor` / 枪械消音器
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Luke: Outlaw Kick

- Entry: `luke.unique.outlaw_kick` / 亡命踢
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Luke: Double Impact

- Entry: `luke.unique.double_impact` / 双连冲击
- Observed properties: High
- Complete input: 6hp>hp
- Required aliases: 6hp>hp, 前重拳>重拳
- Newly added: 6hp>hp, 前重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Luke: Triple Impact

- Entry: `luke.unique.triple_impact` / 三连冲击
- Observed properties: High
- Complete input: lp>mp>hp
- Required aliases: lp>mp>hp, 轻拳>中拳>重拳
- Newly added: lp>mp>hp, 轻拳>中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Luke: Nose Breaker

- Entry: `luke.unique.nose_breaker` / 鼻破
- Observed properties: High
- Complete input: 2mk>2hp
- Required aliases: 2mk>2hp, 下中脚>下重拳
- Newly added: 2mk>2hp, 下中脚>下重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Luke: Snapback Combo

- Entry: `luke.unique.snapback_combo` / 回返连击
- Observed properties: High
- Complete input: mp>mp>mp>mp
- Required aliases: mp>mp>mp>mp, 中拳>中拳>中拳>中拳
- Newly added: mp>mp>mp>mp, 中拳>中拳>中拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Jamie Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/jamie/frame); [Capcom command
list](https://www.streetfighter.com/6/character/jamie/movelist).

### Jamie: Tensei Kick

- Entry: `jamie.unique.tensei_kick` / 天晴腿
- Observed properties: High
- Complete input: 2kk
- Required aliases: 2kk, 下双脚
- Newly added: 2kk, 下双脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Phantom Sway

- Entry: `jamie.unique.phantom_sway` / 幻醉舞
- Observed properties: High, No attack property shown
- Complete input: 2hk>hk>p
- Required aliases: 2hk>hk>p, 下重脚>重脚>拳
- Newly added: 2hk>hk>p, 下重脚>重脚>拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Falling Star Kick

- Entry: `jamie.unique.falling_star_kick` / 落星腿
- Observed properties: Mid
- Complete input: 6mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Hermit's Elbow

- Entry: `jamie.unique.hermit_s_elbow` / 仙姑肘
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Senei Kick

- Entry: `jamie.unique.senei_kick` / 旋影腿
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Bitter Strikes

- Entry: `jamie.unique.bitter_strikes` / 锐钟打
- Observed properties: High
- Complete input: lp>lk>mp
- Required aliases: lp>lk>mp, 轻拳>轻脚>中拳
- Newly added: lp>lk>mp, 轻拳>轻脚>中拳
- Conditions: (Drink level 1 or higher)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Full Moon Kick

- Entry: `jamie.unique.full_moon_kick` / 圆月腿
- Observed properties: Mid, High, No attack property shown
- Complete input: 6mk>mk>p
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (Drink level 2 or higher)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Intoxicated Assault

- Entry: `jamie.unique.intoxicated_assault` / 酩酊袭
- Observed properties: High
- Complete input: 4hp>hp>hk
- Required aliases: 4hp>hp>hk, 后重拳>重拳>重脚
- Newly added: 4hp>hp>hk, 后重拳>重拳>重脚
- Conditions: (Drink level 3 or higher)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Jamie: Ransui Haze

- Entry: `jamie.unique.ransui_haze` / 乱醉旋
- Observed properties: High, No attack property shown
- Complete input: 6hk>4hk>p
- Required aliases: 6hk>4hk>p, 前重脚>后重脚>拳
- Newly added: 6hk>4hk>p, 前重脚>后重脚>拳
- Conditions: (Drink level 4 or higher)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Chun-Li Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/chunli/frame); [Capcom command
list](https://www.streetfighter.com/6/character/chunli/movelist).

### Chun-Li: Swift Thrust

- Entry: `chunli.unique.swift_thrust` / 追刺拳
- Observed properties: High
- Complete input: 4mp / 6mp
- Required aliases: 4mp, 后中拳, 6mp, 前中拳
- Newly added: 4mp, 后中拳, 6mp, 前中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Hakkei

- Entry: `chunli.unique.hakkei` / 发劲
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Water Lotus Fist

- Entry: `chunli.unique.water_lotus_fist` / 水莲掌
- Observed properties: Mid
- Complete input: 3hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Yokusen Kick

- Entry: `chunli.unique.yokusen_kick` / 翼旋腿
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Falling Crane

- Entry: `chunli.unique.falling_crane` / 鹤脚落
- Observed properties: Mid
- Complete input: 3hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Yoso Kick

- Entry: `chunli.unique.yoso_kick` / 鹰爪腿
- Observed properties: High
- Complete input: 2mk / 2mk>2mk>2mk
- Required aliases: 2mk, 下中脚, 2mk>2mk>2mk, 下中脚>下中脚>下中脚
- Newly added: 2mk, 下中脚, 2mk>2mk>2mk, 下中脚>下中脚>下中脚
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Wall Jump

- Entry: `chunli.unique.wall_jump` / 三角跳
- Observed properties: No attack property shown
- Complete input: 9
- Required aliases: 9, 前上
- Newly added: 9, 前上
- Conditions: (During a jump); (Must be near a wall)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Soaring Eagle Punches

- Entry: `chunli.unique.soaring_eagle_punches` / 鹰嘴连拳
- Observed properties: Mid
- Complete input: hp>hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Serenity Stream

- Entry: `chunli.unique.serenity_stream` / 行云流水
- Observed properties: No attack property shown
- Complete input: 214p
- Required aliases: 214p, 下后下后拳
- Newly added: 214p, 下后下后拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Orchid Palm

- Entry: `chunli.unique.orchid_palm` / 兰华
- Observed properties: High
- Complete input: 5lp
- Required aliases: 5lp, 轻拳
- Newly added: 5lp, 轻拳
- Conditions: (During Serenity Stream)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Snake Strike

- Entry: `chunli.unique.snake_strike` / 长蛇打
- Observed properties: Low
- Complete input: 5mp
- Required aliases: 5mp, 中拳
- Newly added: 5mp, 中拳
- Conditions: (During Serenity Stream)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Lotus Fist

- Entry: `chunli.unique.lotus_fist` / 莲掌
- Observed properties: \*MidHigh
- Complete input: 5hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During Serenity Stream)
- Property note: Second hit becomes an overhead only when the first hit whiffs.
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Forward Strike

- Entry: `chunli.unique.forward_strike` / 前击
- Observed properties: Low
- Complete input: 5lk
- Required aliases: 5lk, 轻脚
- Newly added: 5lk, 轻脚
- Conditions: (During Serenity Stream)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Senpu Kick

- Entry: `chunli.unique.senpu_kick` / 仙风
- Observed properties: Low
- Complete input: 5mk
- Required aliases: 5mk, 中脚
- Newly added: 5mk, 中脚
- Conditions: (During Serenity Stream)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Chun-Li: Tenku Kick

- Entry: `chunli.unique.tenku_kick` / 天空腿
- Observed properties: High
- Complete input: 5hk
- Required aliases: 5hk, 重脚
- Newly added: 5hk, 重脚
- Conditions: (During Serenity Stream)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Guile Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/guile/frame); [Capcom command
list](https://www.streetfighter.com/6/character/guile/movelist).

### Guile: Full Bullet Magnum

- Entry: `guile.unique.full_bullet_magnum` / 马格南满弹
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Burning Straight

- Entry: `guile.unique.burning_straight` / 燃烧直拳
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Spinning Back Knuckle

- Entry: `guile.unique.spinning_back_knuckle` / 回旋反手拳
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp, 前重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Knee Bazooka

- Entry: `guile.unique.knee_bazooka` / 飞膝火箭炮
- Observed properties: High
- Complete input: 4lk
- Required aliases: 4lk, 后轻脚
- Newly added: 4lk, 后轻脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Rolling Sobat

- Entry: `guile.unique.rolling_sobat` / 翻身后旋踢
- Observed properties: High
- Complete input: 4mk / 6mk
- Required aliases: 4mk, 后中脚, 6mk, 前中脚
- Newly added: 4mk, 后中脚, 6mk, 前中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Reverse Spin Kick

- Entry: `guile.unique.reverse_spin_kick` / 倒旋踢
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Guile High Kick

- Entry: `guile.unique.guile_high_kick` / 古烈上段踢
- Observed properties: High
- Complete input: 3hk
- Required aliases: 3hk, 前下重脚
- Newly added: 3hk, 前下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Recoil Cannon

- Entry: `guile.unique.recoil_cannon` / 反冲加农
- Observed properties: High
- Complete input: mp>4hp
- Required aliases: mp>4hp, 中拳>后重拳
- Newly added: mp>4hp, 中拳>后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Double Shot

- Entry: `guile.unique.double_shot` / 双射
- Observed properties: High
- Complete input: 2mp>2mp
- Required aliases: 2mp>2mp, 下中拳>下中拳
- Newly added: 2mp>2mp, 下中拳>下中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Drake Fang

- Entry: `guile.unique.drake_fang` / 龙牙连打
- Observed properties: Mid
- Complete input: 2mk>6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Guile: Phantom Cutter

- Entry: `guile.unique.phantom_cutter` / 魅影切割
- Observed properties: High
- Complete input: 2hk>3hk
- Required aliases: 2hk>3hk, 下重脚>前下重脚
- Newly added: 2hk>3hk, 下重脚>前下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Kimberly Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/kimberly/frame); [Capcom command
list](https://www.streetfighter.com/6/character/kimberly/movelist).

### Kimberly: Water Slicer Slide

- Entry: `kimberly.unique.water_slicer_slide` / 水漂腿
- Observed properties: Low
- Complete input: 3mk
- Required aliases: 3mk, 前下中脚
- Newly added: 3mk, 前下中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Windmill Kick

- Entry: `kimberly.unique.windmill_kick` / 风车踢
- Observed properties: Mid
- Complete input: 4hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Hisen Kick

- Entry: `kimberly.unique.hisen_kick` / 飞箭踢
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Step Up

- Entry: `kimberly.unique.step_up` / 藩篱越
- Observed properties: No attack property shown
- Complete input: 7 / 8 / 9
- Required aliases: 7, 后上, 8, 上, 9, 前上
- Newly added: 7, 后上, 8, 上, 9, 前上
- Conditions: (After Hisen Kick)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Elbow Drop

- Entry: `kimberly.unique.elbow_drop` / 肘落
- Observed properties: High
- Complete input: 2mp
- Required aliases: 2mp, 下中拳
- Newly added: 2mp, 下中拳
- Conditions: (At the peak of a forward jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Bushin Tiger Fangs

- Entry: `kimberly.unique.bushin_tiger_fangs` / 武神虎连牙
- Observed properties: High
- Complete input: mp>hp
- Required aliases: mp>hp, 中拳>重拳
- Newly added: mp>hp, 中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Bushin Prism Strikes

- Entry: `kimberly.unique.bushin_prism_strikes` / 武神天架拳
- Observed properties: High
- Complete input: lp>mp>hp>hk
- Required aliases: lp>mp>hp>hk, 轻拳>中拳>重拳>重脚
- Newly added: lp>mp>hp>hk, 轻拳>中拳>重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Bushin Hellchain

- Entry: `kimberly.unique.bushin_hellchain` / 武神狱锁拳
- Observed properties: High
- Complete input: lp>mp>2hp>hk
- Required aliases: lp>mp>2hp>hk, 轻拳>中拳>下重拳>重脚
- Newly added: lp>mp>2hp>hk, 轻拳>中拳>下重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Kimberly: Bushin Hellchain Throw

- Entry: `kimberly.unique.bushin_hellchain_throw` / 武神狱锁投
- Observed properties: High
- Complete input: lp>mp>2hp>2hk
- Required aliases: lp>mp>2hp>2hk, 轻拳>中拳>下重拳>下重脚
- Newly added: lp>mp>2hp>2hk, 轻拳>中拳>下重拳>下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Juri Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/juri/frame); [Capcom command
list](https://www.streetfighter.com/6/character/juri/movelist).

### Juri: Kyosesho

- Entry: `juri.unique.kyosesho` / 狂背掌
- Observed properties: High
- Complete input: 6mp
- Required aliases: 6mp, 前中拳
- Newly added: 6mp, 前中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Juri: Senkai Kick

- Entry: `juri.unique.senkai_kick` / 歼回腿
- Observed properties: Mid
- Complete input: 6mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Juri: Renko Kicks

- Entry: `juri.unique.renko_kicks` / 连克腿
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp, 前重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Juri: Korenzan

- Entry: `juri.unique.korenzan` / 钩镰斩
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Juri: Death Crest

- Entry: `juri.unique.death_crest` / 死纹踢
- Observed properties: High
- Complete input: mp>4hp>hp
- Required aliases: mp>4hp>hp, 中拳>后重拳>重拳
- Newly added: mp>4hp>hp, 中拳>后重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Ken Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/ken/frame); [Capcom command
list](https://www.streetfighter.com/6/character/ken/movelist).

### Ken: Quick Dash

- Entry: `ken.unique.quick_dash` / 奋迅腿
- Observed properties: No attack property shown
- Complete input: 5kk
- Required aliases: 5kk, 双脚
- Newly added: 5kk, 双脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ken: Emergency Stop

- Entry: `ken.unique.emergency_stop` / 急停止
- Observed properties: No attack property shown
- Complete input: 5lk
- Required aliases: 5lk, 轻脚
- Newly added: 5lk, 轻脚
- Conditions: (During Quick Dash)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ken: Thunder Kick

- Entry: `ken.unique.thunder_kick` / 紫电踵落
- Observed properties: Mid
- Complete input: 5mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During Quick Dash)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ken: Forward Step Kick

- Entry: `ken.unique.forward_step_kick` / 前踏踢
- Observed properties: High
- Complete input: 5hk
- Required aliases: 5hk, 重脚
- Newly added: 5hk, 重脚
- Conditions: (During Quick Dash)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ken: Chin Buster

- Entry: `ken.unique.chin_buster` / 下颚双连
- Observed properties: High
- Complete input: mp>hp
- Required aliases: mp>hp, 中拳>重拳
- Newly added: mp>hp, 中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ken: Triple Flash Kicks

- Entry: `ken.unique.triple_flash_kicks` / 闪光连腿
- Observed properties: High
- Complete input: mk>mk>hk
- Required aliases: mk>mk>hk, 中脚>中脚>重脚
- Newly added: mk>mk>hk, 中脚>中脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Blanka Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/blanka/frame); [Capcom command
list](https://www.streetfighter.com/6/character/blanka/movelist).

### Blanka: Rock Crusher

- Entry: `blanka.unique.rock_crusher` / 岩石打击
- Observed properties: \*MidHigh
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Property note: Second hit becomes an overhead only when the first hit whiffs.
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Double Knee Bombs

- Entry: `blanka.unique.double_knee_bombs` / 双膝炸弹
- Observed properties: High
- Complete input: 6mk
- Required aliases: 6mk, 前中脚
- Newly added: 6mk, 前中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Wild Edge

- Entry: `blanka.unique.wild_edge` / 野兽利刃
- Observed properties: High
- Complete input: 4mk
- Required aliases: 4mk, 后中脚
- Newly added: 4mk, 后中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Wild Nail

- Entry: `blanka.unique.wild_nail` / 野兽锋爪
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp, 前重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Amazon River Run

- Entry: `blanka.unique.amazon_river_run` / 亚马逊河流冲
- Observed properties: Low
- Complete input: 3hp
- Required aliases: 3hp, 前下重拳
- Newly added: 3hp, 前下重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Coward Crouch

- Entry: `blanka.unique.coward_crouch` / 胆怯俯身
- Observed properties: No attack property shown
- Complete input: 2pp
- Required aliases: 2pp, 下双拳
- Newly added: 2pp, 下双拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Wild Lift

- Entry: `blanka.unique.wild_lift` / 野兽上抛
- Observed properties: High
- Complete input: 5p
- Required aliases: 5p, 拳
- Newly added: 5p, 拳
- Conditions: (During Coward Crouch)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Raid Jump

- Entry: `blanka.unique.raid_jump` / 突袭跳
- Observed properties: No attack property shown
- Complete input: 5k
- Required aliases: 5k, 脚
- Newly added: 5k, 脚
- Conditions: (During Coward Crouch)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Surprise Forward Hop

- Entry: `blanka.unique.surprise_forward_hop` / 惊乍前跳
- Observed properties: No attack property shown
- Complete input: 6kkk
- Required aliases: 6kkk, 前三脚
- Newly added: 6kkk, 前三脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Blanka: Surprise Back Hop

- Entry: `blanka.unique.surprise_back_hop` / 惊乍后跳
- Observed properties: No attack property shown
- Complete input: 4kkk
- Required aliases: 4kkk, 后三脚
- Newly added: 4kkk, 后三脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Dhalsim Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/dhalsim/frame); [Capcom command
list](https://www.streetfighter.com/6/character/dhalsim/movelist).

### Dhalsim: Yoga Uppercut

- Entry: `dhalsim.unique.yoga_uppercut` / 瑜伽上勾拳
- Observed properties: High
- Complete input: 4mp
- Required aliases: 4mp, 后中拳
- Newly added: 4mp, 后中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Yoga Lance

- Entry: `dhalsim.unique.yoga_lance` / 瑜伽长矛
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Nirvana Punch

- Entry: `dhalsim.unique.nirvana_punch` / 涅槃拳
- Observed properties: High
- Complete input: 1hp
- Required aliases: 1hp, 后下重拳
- Newly added: 1hp, 后下重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Agile Kick

- Entry: `dhalsim.unique.agile_kick` / 灵敏踢
- Observed properties: Low
- Complete input: 1lk
- Required aliases: 1lk, 后下轻脚
- Newly added: 1lk, 后下轻脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Divine Kick

- Entry: `dhalsim.unique.divine_kick` / 合掌踢
- Observed properties: High
- Complete input: 4mk
- Required aliases: 4mk, 后中脚
- Newly added: 4mk, 后中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Thrust Kick

- Entry: `dhalsim.unique.thrust_kick` / 刺踢
- Observed properties: Low
- Complete input: 1mk
- Required aliases: 1mk, 后下中脚
- Newly added: 1mk, 后下中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Yoga Mountain

- Entry: `dhalsim.unique.yoga_mountain` / 瑜伽山
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Karma Kick

- Entry: `dhalsim.unique.karma_kick` / 因果踢
- Observed properties: Low
- Complete input: 1hk
- Required aliases: 1hk, 后下重脚
- Newly added: 1hk, 后下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Yoga Mummy

- Entry: `dhalsim.unique.yoga_mummy` / 锥钻头
- Observed properties: High
- Complete input: 2lp
- Required aliases: 2lp, 下轻拳
- Newly added: 2lp, 下轻拳
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dhalsim: Drill Kick

- Entry: `dhalsim.unique.drill_kick` / 锥钻踢
- Observed properties: High
- Complete input: 2lk / 2mk / 2hk
- Required aliases: 2lk, 下轻脚, 2mk, 下中脚, 2hk, 下重脚
- Newly added: 2lk, 下轻脚, 2mk, 下中脚, 2hk, 下重脚
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## E. Honda Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/ehonda/frame); [Capcom command
list](https://www.streetfighter.com/6/character/ehonda/movelist).

### E. Honda: Harai Kick

- Entry: `honda.unique.harai_kick` / 横扫踢
- Observed properties: Low
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### E. Honda: Power Stomp

- Entry: `honda.unique.power_stomp` / 相扑力足
- Observed properties: Mid
- Complete input: 3hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### E. Honda: Flying Sumo Press

- Entry: `honda.unique.flying_sumo_press` / 相扑飞身压
- Observed properties: Mid
- Complete input: 2mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a forward jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### E. Honda: Double Slaps

- Entry: `honda.unique.double_slaps` / 双连张手
- Observed properties: High
- Complete input: lp>mp
- Required aliases: lp>mp, 轻拳>中拳
- Newly added: lp>mp, 轻拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### E. Honda: Toko Shizume

- Entry: `honda.unique.toko_shizume` / 地镇
- Observed properties: Mid
- Complete input: mp>3hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Dee Jay Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/deejay/frame); [Capcom command
list](https://www.streetfighter.com/6/character/deejay/movelist).

### Dee Jay: Knee Shot

- Entry: `deejay.unique.knee_shot` / 飞膝撞
- Observed properties: Mid
- Complete input: 2lk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a forward jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Sunrise Heel

- Entry: `deejay.unique.sunrise_heel` / 日出脚踝踢
- Observed properties: High
- Complete input: 6mk
- Required aliases: 6mk, 前中脚
- Newly added: 6mk, 前中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Face Breaker

- Entry: `deejay.unique.face_breaker` / 破脸
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Threebeat Combo

- Entry: `deejay.unique.threebeat_combo` / 3拍连招
- Observed properties: High
- Complete input: lp>mk>mk
- Required aliases: lp>mk>mk, 轻拳>中脚>中脚
- Newly added: lp>mk>mk, 轻拳>中脚>中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Dee Jay Special

- Entry: `deejay.unique.dee_jay_special` / 迪·杰特色
- Observed properties: High
- Complete input: mp>hp>hk
- Required aliases: mp>hp>hk, 中拳>重拳>重脚
- Newly added: mp>hp>hk, 中拳>重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Funky Dance

- Entry: `deejay.unique.funky_dance` / 放克舞
- Observed properties: High
- Complete input: mp>mp>hp
- Required aliases: mp>mp>hp, 中拳>中拳>重拳
- Newly added: mp>mp>hp, 中拳>中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Funky Dance Feint

- Entry: `deejay.unique.funky_dance_feint` / 放克舞·假动作
- Observed properties: No attack property shown
- Complete input: mp>mp>4hp
- Required aliases: mp>mp>4hp, 中拳>中拳>后重拳
- Newly added: mp>mp>4hp, 中拳>中拳>后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Party in the Air

- Entry: `deejay.unique.party_in_the_air` / 空中聚会
- Observed properties: Mid
- Complete input: mp>hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Dee Jay: Speedy Maracas

- Entry: `deejay.unique.speedy_maracas` / 砂槌节奏
- Observed properties: No attack property shown
- Complete input: 22pp
- Required aliases: 22pp, 下下双拳
- Newly added: 22pp, 下下双拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Manon Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/manon/frame); [Capcom command
list](https://www.streetfighter.com/6/character/manon/movelist).

### Manon: Révérence

- Entry: `manon.unique.reverence` / 屈膝礼
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Manon: Tomoe Derrière

- Entry: `manon.unique.tomoe_derriere` / 巴拉后
- Observed properties: High
- Complete input: 3hk
- Required aliases: 3hk, 前下重脚
- Newly added: 3hk, 前下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Manon: À Terre

- Entry: `manon.unique.a_terre` / 地面动作
- Observed properties: High
- Complete input: mp>mk
- Required aliases: mp>mk, 中拳>中脚
- Newly added: mp>mk, 中拳>中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Manon: En Haut

- Entry: `manon.unique.en_haut` / 高位舞步
- Observed properties: High, Mid
- Complete input: 4mk>mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Manon: Temps Lié

- Entry: `manon.unique.temps_lie` / 重心转移
- Observed properties: High
- Complete input: hp>hp
- Required aliases: hp>hp, 重拳>重拳
- Newly added: hp>hp, 重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Manon: Allongé

- Entry: `manon.unique.allonge` / 阿隆热动作
- Observed properties: High
- Complete input: 2hp>hp
- Required aliases: 2hp>hp, 下重拳>重拳
- Newly added: 2hp>hp, 下重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Marisa Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/marisa/frame); [Capcom command
list](https://www.streetfighter.com/6/character/marisa/movelist).

### Marisa: Marisa Style

- Entry: `marisa.unique.marisa_style` / 玛丽莎风格
- Observed properties: No attack property shown
- Complete input: [hp] / [hk]
- Required aliases: [hp], 蓄力重拳, [hk], 蓄力重脚
- Newly added: [hp], 蓄力重拳, [hk], 蓄力重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Light Two Hitter

- Entry: `marisa.unique.light_two_hitter` / 轻双连
- Observed properties: High
- Complete input: lp>lp
- Required aliases: lp>lp, 轻拳>轻拳
- Newly added: lp>lp, 轻拳>轻拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Medium Two Hitter

- Entry: `marisa.unique.medium_two_hitter` / 中双连
- Observed properties: High
- Complete input: mp>mp
- Required aliases: mp>mp, 中拳>中拳
- Newly added: mp>mp, 中拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Heavy Two Hitter

- Entry: `marisa.unique.heavy_two_hitter` / 重双连
- Observed properties: High
- Complete input: hp>hp
- Required aliases: hp>hp, 重拳>重拳
- Newly added: hp>hp, 重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Volare Combo

- Entry: `marisa.unique.volare_combo` / 飞空组合技
- Observed properties: Mid
- Complete input: mp>mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Caelum Arc

- Entry: `marisa.unique.caelum_arc` / 天空之弧
- Observed properties: Mid
- Complete input: 2hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a neutral jump); (During a neutral jump); Hold the final
  attack button
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Magna Bunker

- Entry: `marisa.unique.magna_bunker` / 伟大地堡
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: Hold the final attack button
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Novacula Swipe

- Entry: `marisa.unique.novacula_swipe` / 利刃猛击
- Observed properties: Low
- Complete input: 6mp>hp
- Required aliases: 6mp>hp, 前中拳>重拳
- Newly added: 6mp>hp, 前中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Novacula Thrust

- Entry: `marisa.unique.novacula_thrust` / 利刃连射
- Observed properties: High
- Complete input: 6mp>hk
- Required aliases: 6mp>hk, 前中拳>重脚
- Newly added: 6mp>hk, 前中拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Malleus Breaker

- Entry: `marisa.unique.malleus_breaker` / 重锤连打
- Observed properties: Mid
- Complete input: 3hp>3hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: Hold the final attack button
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Marisa: Falx Crusher

- Entry: `marisa.unique.falx_crusher` / 方阵摧毁
- Observed properties: High
- Complete input: 6hk>6hk
- Required aliases: 6hk>6hk, 前重脚>前重脚
- Newly added: 6hk>6hk, 前重脚>前重脚
- Conditions: Hold the final attack button
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## JP Unique Move Aliases

Source: [Capcom frame data](https://www.streetfighter.com/6/character/jp/frame);
[Capcom command list](https://www.streetfighter.com/6/character/jp/movelist).

### JP: Guillotinna

- Entry: `jp.unique.guillotinna` / 断头台
- Observed properties: Mid
- Complete input: 6mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### JP: Malice

- Entry: `jp.unique.malice` / 恶作剧
- Observed properties: Low
- Complete input: 3hp
- Required aliases: 3hp, 前下重拳
- Newly added: 3hp, 前下重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### JP: Bylina

- Entry: `jp.unique.bylina` / 俄罗斯史诗
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### JP: Grom Strelka

- Entry: `jp.unique.grom_strelka` / 雷箭
- Observed properties: High
- Complete input: 4mp>mp
- Required aliases: 4mp>mp, 后中拳>中拳
- Newly added: 4mp>mp, 后中拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### JP: Zilant

- Entry: `jp.unique.zilant` / 龙兽吉兰特
- Observed properties: High
- Complete input: hk>hp
- Required aliases: hk>hp, 重脚>重拳
- Newly added: hk>hp, 重脚>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### JP: Zilant Mid

- Entry: `jp.unique.zilant_mid` / 龙兽吉兰特·中
- Observed properties: Mid
- Complete input: hk>hp>hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### JP: Zilant Low

- Entry: `jp.unique.zilant_low` / 龙兽吉兰特·下
- Observed properties: Low
- Complete input: hk>hp>hk
- Required aliases: hk>hp>hk, 重脚>重拳>重脚
- Newly added: hk>hp>hk, 重脚>重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Zangief Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/zangief/frame); [Capcom command
list](https://www.streetfighter.com/6/character/zangief/movelist).

### Zangief: Hellstab

- Entry: `zangief.unique.hellstab` / 地狱刺
- Observed properties: High
- Complete input: 3mp
- Required aliases: 3mp, 前下中拳
- Newly added: 3mp, 前下中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Knee Hammer

- Entry: `zangief.unique.knee_hammer` / 膝槌
- Observed properties: High
- Complete input: 6mk
- Required aliases: 6mk, 前中脚
- Newly added: 6mk, 前中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Headbutt

- Entry: `zangief.unique.headbutt` / 头槌
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp, 前重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Cyclone Wheel Kick

- Entry: `zangief.unique.cyclone_wheel_kick` / 旋风轮转踢
- Observed properties: Mid
- Complete input: 6hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Smetana Dropkick

- Entry: `zangief.unique.smetana_dropkick` / 酸奶油飞身踢
- Observed properties: High
- Complete input: 3hk
- Required aliases: 3hk, 前下重脚
- Newly added: 3hk, 前下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Flying Body Press

- Entry: `zangief.unique.flying_body_press` / 飞身压
- Observed properties: Mid
- Complete input: 2hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Flying Headbutt

- Entry: `zangief.unique.flying_headbutt` / 空中头槌
- Observed properties: Mid
- Complete input: 8hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a neutral jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Machine Gun Chops

- Entry: `zangief.unique.machine_gun_chops` / 机枪手刀
- Observed properties: High
- Complete input: mp>mp>mp
- Required aliases: mp>mp>mp, 中拳>中拳>中拳
- Newly added: mp>mp>mp, 中拳>中拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Zangief: Power Stomps

- Entry: `zangief.unique.power_stomps` / 能量踩踏
- Observed properties: Low
- Complete input: 22mk>mk>mk
- Required aliases: 22mk>mk>mk, 下下中脚>中脚>中脚
- Newly added: 22mk>mk>mk, 下下中脚>中脚>中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Lily Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/lily/frame); [Capcom command
list](https://www.streetfighter.com/6/character/lily/movelist).

### Lily: Ridge Thrust

- Entry: `lily.unique.ridge_thrust` / 冲断岭
- Observed properties: Mid
- Complete input: 3hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Lily: Horn Breaker

- Entry: `lily.unique.horn_breaker` / 角骨破
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Lily: Great Spin

- Entry: `lily.unique.great_spin` / 大回旋
- Observed properties: Mid
- Complete input: 2hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Lily: Double Arrow

- Entry: `lily.unique.double_arrow` / 双发箭
- Observed properties: Mid
- Complete input: mp>mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Lily: Desert Storm

- Entry: `lily.unique.desert_storm` / 沙漠风暴
- Observed properties: High
- Complete input: 6hp>hp>hp
- Required aliases: 6hp>hp>hp, 前重拳>重拳>重拳
- Newly added: 6hp>hp>hp, 前重拳>重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Cammy Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/cammy/frame); [Capcom command
list](https://www.streetfighter.com/6/character/cammy/movelist).

### Cammy: Lift Uppercut

- Entry: `cammy.unique.lift_uppercut` / 上袭勾拳
- Observed properties: High
- Complete input: 4mp
- Required aliases: 4mp, 后中拳
- Newly added: 4mp, 后中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Cammy: Delayed Ripper

- Entry: `cammy.unique.delayed_ripper` / 延时死神
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Cammy: Assault Blade

- Entry: `cammy.unique.assault_blade` / 强袭利刃
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Cammy: Lift Combination

- Entry: `cammy.unique.lift_combination` / 上袭组合技
- Observed properties: High
- Complete input: 4mp>hk
- Required aliases: 4mp>hk, 后中拳>重脚
- Newly added: 4mp>hk, 后中拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Cammy: Swing Combination

- Entry: `cammy.unique.swing_combination` / 摇摆组合技
- Observed properties: High
- Complete input: hp>hk
- Required aliases: hp>hk, 重拳>重脚
- Newly added: hp>hk, 重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Rashid Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/rashid/frame); [Capcom command
list](https://www.streetfighter.com/6/character/rashid/movelist).

### Rashid: Run

- Entry: `rashid.unique.run` / 奔跑
- Observed properties: No attack property shown
- Complete input: 66[6]
- Required aliases: 66[6], 前前长按前
- Newly added: 66[6], 前前长按前
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Backup

- Entry: `rashid.unique.backup` / 后手
- Observed properties: Low
- Complete input: 6p
- Required aliases: 6p, 前拳
- Newly added: 6p, 前拳
- Conditions: (During Run)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Tempest Moon

- Entry: `rashid.unique.tempest_moon` / 风暴之月
- Observed properties: High
- Complete input: 6k
- Required aliases: 6k, 前脚
- Newly added: 6k, 前脚
- Conditions: (During Run); (from Run when coming in contact with an air
  current)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Flapping Spin

- Entry: `rashid.unique.flapping_spin` / 鹰翼旋
- Observed properties: High
- Complete input: 6mp
- Required aliases: 6mp, 前中拳
- Newly added: 6mp, 前中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Beak Assault

- Entry: `rashid.unique.beak_assault` / 鹰喙袭
- Observed properties: Mid
- Complete input: 6hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Crescent Kick

- Entry: `rashid.unique.crescent_kick` / 新月踢
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Blitz Strike

- Entry: `rashid.unique.blitz_strike` / 闪电击
- Observed properties: Mid
- Complete input: 2hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a forward jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Aerial Shot

- Entry: `rashid.unique.aerial_shot` / 凌空射
- Observed properties: Mid
- Complete input: 8hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a neutral jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Rising Kick

- Entry: `rashid.unique.rising_kick` / 升空踢
- Observed properties: High
- Complete input: mp>hk
- Required aliases: mp>hk, 中拳>重脚
- Newly added: mp>hk, 中拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Side Flip

- Entry: `rashid.unique.side_flip` / 侧边翻转
- Observed properties: No attack property shown
- Complete input: 6kk
- Required aliases: 6kk, 前双脚
- Newly added: 6kk, 前双脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Front Flip

- Entry: `rashid.unique.front_flip` / 前跳翻转
- Observed properties: No attack property shown
- Complete input: 4kk / 5kk / 6kk
- Required aliases: 4kk, 后双脚, 5kk, 双脚, 6kk, 前双脚
- Newly added: 4kk, 后双脚, 5kk, 双脚, 6kk, 前双脚
- Conditions: (During Side Flip)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Rashid: Wall Jump

- Entry: `rashid.unique.wall_jump` / 三角跳
- Observed properties: No attack property shown
- Complete input: 9
- Required aliases: 9, 前上
- Newly added: 9, 前上
- Conditions: (During a jump); (Must be near a wall)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## A.K.I. Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/aki/frame); [Capcom command
list](https://www.streetfighter.com/6/character/aki/movelist).

### A.K.I.: Pu Lao

- Entry: `aki.unique.pu_lao` / 蒲牢
- Observed properties: Mid
- Complete input: 3mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### A.K.I.: Chi Wen

- Entry: `aki.unique.chi_wen` / 螭吻
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp, 前重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### A.K.I.: Qiu Niu

- Entry: `aki.unique.qiu_niu` / 囚牛
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### A.K.I.: Gong Fu

- Entry: `aki.unique.gong_fu` / 蚣蝮
- Observed properties: Mid
- Complete input: 2hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a forward jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### A.K.I.: Hun Dun

- Entry: `aki.unique.hun_dun` / 混沌
- Observed properties: High
- Complete input: lp>lp
- Required aliases: lp>lp, 轻拳>轻拳
- Newly added: lp>lp, 轻拳>轻拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### A.K.I.: Qiong Qi

- Entry: `aki.unique.qiong_qi` / 穷奇
- Observed properties: High
- Complete input: hp>hp
- Required aliases: hp>hp, 重拳>重拳
- Newly added: hp>hp, 重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Ed Unique Move Aliases

Source: [Capcom frame data](https://www.streetfighter.com/6/character/ed/frame);
[Capcom command list](https://www.streetfighter.com/6/character/ed/movelist).

### Ed: Psycho Knuckle

- Entry: `ed.unique.psycho_knuckle` / 精神力冲拳
- Observed properties: High
- Complete input: [hp]
- Required aliases: [hp], 蓄力重拳
- Newly added: [hp], 蓄力重拳
- Conditions: Hold the final attack button
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ed: Cobra Punch

- Entry: `ed.unique.cobra_punch` / 眼镜蛇拳
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp, 前重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ed: Flicker Combination

- Entry: `ed.unique.flicker_combination` / 闪刺组合技
- Observed properties: High
- Complete input: lk>lk>lk
- Required aliases: lk>lk>lk, 轻脚>轻脚>轻脚
- Newly added: lk>lk>lk, 轻脚>轻脚>轻脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ed: Body Blow Combination

- Entry: `ed.unique.body_blow_combination` / 上体组合拳
- Observed properties: High
- Complete input: mp>hp
- Required aliases: mp>hp, 中拳>重拳
- Newly added: mp>hp, 中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ed: Hitman Combination

- Entry: `ed.unique.hitman_combination` / 杀手组合技
- Observed properties: High
- Complete input: mk>mk>hp
- Required aliases: mk>mk>hp, 中脚>中脚>重拳
- Newly added: mk>mk>hp, 中脚>中脚>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ed: Low Smash Combination

- Entry: `ed.unique.low_smash_combination` / 低重击组合技
- Observed properties: High
- Complete input: 2hk>hp
- Required aliases: 2hk>hp, 下重脚>重拳
- Newly added: 2hk>hp, 下重脚>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Akuma Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/gouki_akuma/frame); [Capcom
command list](https://www.streetfighter.com/6/character/gouki_akuma/movelist).

### Akuma: Skull Splitter

- Entry: `akuma.unique.skull_splitter` / 头盖破杀
- Observed properties: \*MidHigh
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Property note: Second hit becomes an overhead only when the first hit whiffs.
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Akuma: Resso Snap Kick

- Entry: `akuma.unique.resso_snap_kick` / 裂枪脚
- Observed properties: High
- Complete input: 6mk
- Required aliases: 6mk, 前中脚
- Newly added: 6mk, 前中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Akuma: Rago High Kick

- Entry: `akuma.unique.rago_high_kick` / 罗豪脚
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Akuma: Viscera Piercer

- Entry: `akuma.unique.viscera_piercer` / 六腑穿
- Observed properties: High
- Complete input: mp>mp
- Required aliases: mp>mp, 中拳>中拳
- Newly added: mp>mp, 中拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Akuma: Bone Crusher Axe Kick

- Entry: `akuma.unique.bone_crusher_axe_kick` / 骸斩
- Observed properties: Mid
- Complete input: mk>hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Akuma: Kikoku Combination

- Entry: `akuma.unique.kikoku_combination` / 鬼哭连击
- Observed properties: High
- Complete input: 6hp>6hp>hk
- Required aliases: 6hp>6hp>hk, 前重拳>前重拳>重脚
- Newly added: 6hp>6hp>hk, 前重拳>前重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Akuma: Tenmaku Blade Kick

- Entry: `akuma.unique.tenmaku_blade_kick` / 天魔空刃腿
- Observed properties: High
- Complete input: 2mk
- Required aliases: 2mk, 下中脚
- Newly added: 2mk, 下中脚
- Conditions: (During a forward jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## M. Bison Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/vega_mbison/frame); [Capcom
command list](https://www.streetfighter.com/6/character/vega_mbison/movelist).

### M. Bison: Psycho Hammer

- Entry: `mbison.unique.psycho_hammer` / 精神重锤
- Observed properties: Mid
- Complete input: 6hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### M. Bison: Evil Knee

- Entry: `mbison.unique.evil_knee` / 邪恶之膝
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### M. Bison: Hover Kick

- Entry: `mbison.unique.hover_kick` / 滑铲踢
- Observed properties: Low
- Complete input: 3hk
- Required aliases: 3hk, 前下重脚
- Newly added: 3hk, 前下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### M. Bison: Shadow Hammer

- Entry: `mbison.unique.shadow_hammer` / 重影锤
- Observed properties: Mid
- Complete input: mp>6hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### M. Bison: Shadow Spear

- Entry: `mbison.unique.shadow_spear` / 邪影矛
- Observed properties: Low
- Complete input: mp>2hk
- Required aliases: mp>2hk, 中拳>下重脚
- Newly added: mp>2hk, 中拳>下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### M. Bison: Hell Attack

- Entry: `mbison.unique.hell_attack` / 地狱攻击
- Observed properties: High
- Complete input: mp>mp
- Required aliases: mp>mp, 中拳>中拳
- Newly added: mp>mp, 中拳>中拳
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Terry Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/terry/frame); [Capcom command
list](https://www.streetfighter.com/6/character/terry/movelist).

### Terry: Hammer Punch

- Entry: `terry.unique.hammer_punch` / 重锤拳
- Observed properties: Mid
- Complete input: 6hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Terry: Power Drive

- Entry: `terry.unique.power_drive` / 能量驱动
- Observed properties: High
- Complete input: mp>hp
- Required aliases: mp>hp, 中拳>重拳
- Newly added: mp>hp, 中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Terry: Power Shoot

- Entry: `terry.unique.power_shoot` / 能量投篮
- Observed properties: High
- Complete input: mp>hk
- Required aliases: mp>hk, 中拳>重脚
- Newly added: mp>hk, 中拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Terry: Power Dunk

- Entry: `terry.unique.power_dunk` / 能量灌篮
- Observed properties: High
- Complete input: mp>hk>hk
- Required aliases: mp>hk>hk, 中拳>重脚>重脚
- Newly added: mp>hk>hk, 中拳>重脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Terry: Passing Sway

- Entry: `terry.unique.passing_sway` / 穿越摇摆
- Observed properties: High
- Complete input: mp>mk
- Required aliases: mp>mk, 中拳>中脚
- Newly added: mp>mk, 中拳>中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Terry: Jumping Lariat

- Entry: `terry.unique.jumping_lariat` / 跳跃臂勾
- Observed properties: High
- Complete input: mp>mk>mp
- Required aliases: mp>mk>mp, 中拳>中脚>中拳
- Newly added: mp>mk>mp, 中拳>中脚>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Terry: Jumping Knee

- Entry: `terry.unique.jumping_knee` / 跳跃膝撞
- Observed properties: High
- Complete input: mp>mk>mk
- Required aliases: mp>mk>mk, 中拳>中脚>中脚
- Newly added: mp>mk>mk, 中拳>中脚>中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Terry: Fire Kick

- Entry: `terry.unique.fire_kick` / 火焰踢
- Observed properties: High
- Complete input: 2mk>2hk
- Required aliases: 2mk>2hk, 下中脚>下重脚
- Newly added: 2mk>2hk, 下中脚>下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Mai Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/mai/frame); [Capcom command
list](https://www.streetfighter.com/6/character/mai/movelist).

### Mai: Senkotsu Uchi

- Entry: `mai.unique.senkotsu_uchi` / 扇骨打
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Mai: Hien Ren Kyaku

- Entry: `mai.unique.hien_ren_kyaku` / 飞燕连脚
- Observed properties: High
- Complete input: lk>lk>lk
- Required aliases: lk>lk>lk, 轻脚>轻脚>轻脚
- Newly added: lk>lk>lk, 轻脚>轻脚>轻脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Mai: Hoshi Kujaku

- Entry: `mai.unique.hoshi_kujaku` / 星孔雀
- Observed properties: High
- Complete input: 4hk>hk
- Required aliases: 4hk>hk, 后重脚>重脚
- Newly added: 4hk>hk, 后重脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Elena Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/elena/frame); [Capcom command
list](https://www.streetfighter.com/6/character/elena/movelist).

### Elena: Slide

- Entry: `elena.unique.slide` / 滑铲
- Observed properties: Low
- Complete input: 3hk
- Required aliases: 3hk, 前下重脚
- Newly added: 3hk, 前下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Round Arch

- Entry: `elena.unique.round_arch` / 圆弧踢
- Observed properties: High
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Starling Beak

- Entry: `elena.unique.starling_beak` / 椋鸟喙啄
- Observed properties: High
- Complete input: mp>mp
- Required aliases: mp>mp, 中拳>中拳
- Newly added: mp>mp, 中拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Handstand Whip

- Entry: `elena.unique.handstand_whip` / 倒立腿鞭
- Observed properties: Mid, High
- Complete input: 6mk>mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Hind Kick

- Entry: `elena.unique.hind_kick` / 后蹄踢
- Observed properties: High
- Complete input: mk>hk
- Required aliases: mk>hk, 中脚>重脚
- Newly added: mk>hk, 中脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Fluttering Lark

- Entry: `elena.unique.fluttering_lark` / 云雀振翅
- Observed properties: High
- Complete input: 2mk>hk
- Required aliases: 2mk>hk, 下中脚>重脚
- Newly added: 2mk>hk, 下中脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Turning Tail

- Entry: `elena.unique.turning_tail` / 回旋尾鞭
- Observed properties: High
- Complete input: hp>hp
- Required aliases: hp>hp, 重拳>重拳
- Newly added: hp>hp, 重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Trunk Slap

- Entry: `elena.unique.trunk_slap` / 象鼻掴打
- Observed properties: High
- Complete input: 6hp>hp>hp
- Required aliases: 6hp>hp>hp, 前重拳>重拳>重拳
- Newly added: 6hp>hp>hp, 前重拳>重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Soaring Raid

- Entry: `elena.unique.soaring_raid` / 翱翔奇袭
- Observed properties: High
- Complete input: lp>mk
- Required aliases: lp>mk, 轻拳>中脚
- Newly added: lp>mk, 轻拳>中脚
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Elena: Raptor Range

- Entry: `elena.unique.raptor_range` / 猛禽突击
- Observed properties: Mid
- Complete input: mp>hp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Sagat Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/sagat/frame); [Capcom command
list](https://www.streetfighter.com/6/character/sagat/movelist).

### Sagat: Tiger Heavy Elbow

- Entry: `sagat.unique.tiger_heavy_elbow` / 猛虎重砸肘
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Sagat: Tiger Monolith

- Entry: `sagat.unique.tiger_monolith` / 猛虎巨石
- Observed properties: High
- Complete input: 4hp
- Required aliases: 4hp, 后重拳
- Newly added: 4hp, 后重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Sagat: Low Step Kick

- Entry: `sagat.unique.low_step_kick` / 前踏低扫踢
- Observed properties: Low
- Complete input: 6lk
- Required aliases: 6lk, 前轻脚
- Newly added: 6lk, 前轻脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Sagat: High Step Kick

- Entry: `sagat.unique.high_step_kick` / 前踏高扫踢
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Sagat: Middle Step Kick

- Entry: `sagat.unique.middle_step_kick` / 前踏中扫踢
- Observed properties: High
- Complete input: mk>hk
- Required aliases: mk>hk, 中脚>重脚
- Newly added: mk>hk, 中脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Sagat: Tiger Sting

- Entry: `sagat.unique.tiger_sting` / 猛虎扎
- Observed properties: High
- Complete input: hp>hk
- Required aliases: hp>hk, 重拳>重脚
- Newly added: hp>hk, 重拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Sagat: Tiger Slash

- Entry: `sagat.unique.tiger_slash` / 猛虎斩
- Observed properties: High
- Complete input: 2mp>hp
- Required aliases: 2mp>hp, 下中拳>重拳
- Newly added: 2mp>hp, 下中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Sagat: Tiger Rise

- Entry: `sagat.unique.tiger_rise` / 猛虎升
- Observed properties: High
- Complete input: 2mp>hk
- Required aliases: 2mp>hk, 下中拳>重脚
- Newly added: 2mp>hk, 下中拳>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## C. Viper Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/cviper/frame); [Capcom command
list](https://www.streetfighter.com/6/character/cviper/movelist).

### C. Viper: Viper Elbow

- Entry: `cviper.unique.viper_elbow` / 毒蛇肘击
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### C. Viper: Double Kick

- Entry: `cviper.unique.double_kick` / 双连踢
- Observed properties: High
- Complete input: 6hk
- Required aliases: 6hk, 前重脚
- Newly added: 6hk, 前重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### C. Viper: High Jump

- Entry: `cviper.unique.high_jump` / 大跳跃
- Observed properties: No attack property shown
- Complete input: 29 / 28
- Required aliases: 29, 下前上, 28, 下上
- Newly added: 29, 下前上, 28, 下上
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Alex Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/alex/frame); [Capcom command
list](https://www.streetfighter.com/6/character/alex/movelist).

### Alex: Prowler Stance

- Entry: `alex.unique.prowler_stance` / 破坏姿势
- Observed properties: No attack property shown
- Complete input: 2pp
- Required aliases: 2pp, 下双拳
- Newly added: 2pp, 下双拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Low Rush

- Entry: `alex.unique.low_rush` / 前滑步
- Observed properties: No attack property shown
- Complete input: 6
- Required aliases: 6, 前
- Newly added: 6, 前
- Conditions: (During Prowler Stance)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Low Retreat

- Entry: `alex.unique.low_retreat` / 后滑步
- Observed properties: No attack property shown
- Complete input: 4
- Required aliases: 4, 后
- Newly added: 4, 后
- Conditions: (During Prowler Stance)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Slashing Elbow

- Entry: `alex.unique.slashing_elbow` / 肘斩
- Observed properties: High
- Complete input: 6p / 6lp / 6mp / 6hp
- Required aliases: 6p, 前拳, 6lp, 前轻拳, 6mp, 前中拳, 6hp, 前重拳
- Newly added: 6p, 前拳, 6lp, 前轻拳, 6mp, 前中拳, 6hp, 前重拳
- Conditions: (During Prowler Stance
Low Rush)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Palm Jab

- Entry: `alex.unique.palm_jab` / 掌刺
- Observed properties: High
- Complete input: 5lp
- Required aliases: 5lp, 轻拳
- Newly added: 5lp, 轻拳
- Conditions: (During Prowler Stance)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Shoulder Launcher

- Entry: `alex.unique.shoulder_launcher` / 肩撞
- Observed properties: High
- Complete input: 5mp
- Required aliases: 5mp, 中拳
- Newly added: 5mp, 中拳
- Conditions: (During Prowler Stance)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Heavy Lariat

- Entry: `alex.unique.heavy_lariat` / 重臂勾
- Observed properties: High, No attack property shown
- Complete input: 5hp
- Required aliases: 5hp, 重拳
- Newly added: 5hp, 重拳
- Conditions: (During Prowler Stance); (During Prowler Stance); Hold the final
  attack button
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Tactical Hop

- Entry: `alex.unique.tactical_hop` / 策略跳
- Observed properties: No attack property shown
- Complete input: 5lk
- Required aliases: 5lk, 轻脚
- Newly added: 5lk, 轻脚
- Conditions: (During Prowler Stance)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Air Stampede

- Entry: `alex.unique.air_stampede` / 空落踩
- Observed properties: Mid
- Complete input: 5mk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During Prowler Stance)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Sweep Combination

- Entry: `alex.unique.sweep_combination` / 扫腿组合技
- Observed properties: Low
- Complete input: hk>hk
- Required aliases: hk>hk, 重脚>重脚
- Newly added: hk>hk, 重脚>重脚
- Conditions: (During Prowler Stance)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Hyper Takedown

- Entry: `alex.unique.hyper_takedown` / 超级放倒
- Observed properties: Throw
- Complete input: lp+lk
- Required aliases: lp+lk, 轻拳+轻脚
- Newly added: lp+lk, 轻拳+轻脚
- Conditions: (During Prowler Stance); (When near opponent)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Dangerous Armbar

- Entry: `alex.unique.dangerous_armbar` / 危险肘固
- Observed properties: Throw
- Complete input: 2lp+lk
- Required aliases: 2lp+lk, 下轻拳+轻脚
- Newly added: 2lp+lk, 下轻拳+轻脚
- Conditions: (During Prowler Stance); (When close to a standing opponent)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Chop

- Entry: `alex.unique.chop` / 手刀
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Oblique Stomp

- Entry: `alex.unique.oblique_stomp` / 斜踩
- Observed properties: High
- Complete input: 4mk
- Required aliases: 4mk, 后中脚
- Newly added: 4mk, 后中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Flying Cross Chop

- Entry: `alex.unique.flying_cross_chop` / 飞身交叉劈
- Observed properties: High
- Complete input: 2hp
- Required aliases: 2hp, 下重拳
- Newly added: 2hp, 下重拳
- Conditions: (During a forward jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Palm Strikes

- Entry: `alex.unique.palm_strikes` / 掌击
- Observed properties: High
- Complete input: mp>hp
- Required aliases: mp>hp, 中拳>重拳
- Newly added: mp>hp, 中拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Alex: Twisted Drop

- Entry: `alex.unique.twisted_drop` / 螺旋坠
- Observed properties: Low
- Complete input: 2lk>2hk
- Required aliases: 2lk>2hk, 下轻脚>下重脚
- Newly added: 2lk>2hk, 下轻脚>下重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Ingrid Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/ingrid/frame); [Capcom command
list](https://www.streetfighter.com/6/character/ingrid/movelist).

### Ingrid: Sun Bright

- Entry: `ingrid.unique.sun_bright` / 曦光
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ingrid: Halo Flight

- Entry: `ingrid.unique.halo_flight` / 光轮飞劈
- Observed properties: High
- Complete input: 6hp
- Required aliases: 6hp, 前重拳
- Newly added: 6hp, 前重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ingrid: Pretty Heel Kick

- Entry: `ingrid.unique.pretty_heel_kick` / 空旋踝踢
- Observed properties: High
- Complete input: mp>mk
- Required aliases: mp>mk, 中拳>中脚
- Newly added: mp>mk, 中拳>中脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ingrid: Glowing Touch

- Entry: `ingrid.unique.glowing_touch` / 发光触碰
- Observed properties: High
- Complete input: 4mk>hp
- Required aliases: 4mk>hp, 后中脚>重拳
- Newly added: 4mk>hp, 后中脚>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ingrid: Luminous Uppercut

- Entry: `ingrid.unique.luminous_uppercut` / 明亮上段击
- Observed properties: High
- Complete input: 4hp>hp
- Required aliases: 4hp>hp, 后重拳>重拳
- Newly added: 4hp>hp, 后重拳>重拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Ingrid: Satellite Leap

- Entry: `ingrid.unique.satellite_leap` / 卫星跳踢
- Observed properties: Mid
- Complete input: hk>hk
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: (During a jump)
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:


## Yasmine Unique Move Aliases

Source: [Capcom frame
data](https://www.streetfighter.com/6/character/yasmine/frame); [Capcom command
list](https://www.streetfighter.com/6/character/yasmine/movelist).

### Yasmine: Hiwang Pababa

- Entry: `yasmine.unique.hiwang_pababa` / 下旋裂爪
- Observed properties: Mid
- Complete input: 6mp
- Required aliases: 中段, 砸猪头
- Newly added: 中段, 砸猪头
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Yasmine: Walis na Pabagsak

- Entry: `yasmine.unique.walis_na_pabagsak` / 旋风扫腿
- Observed properties: Low
- Complete input: 4hk
- Required aliases: 4hk, 后重脚
- Newly added: 4hk, 后重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Yasmine: Kidlat na Hiwa

- Entry: `yasmine.unique.kidlat_na_hiwa` / 闪电斩击
- Observed properties: High
- Complete input: lp>lp
- Required aliases: lp>lp, 轻拳>轻拳
- Newly added: lp>lp, 轻拳>轻拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Yasmine: Tatlong Hiwa

- Entry: `yasmine.unique.tatlong_hiwa` / 三连斩击
- Observed properties: High
- Complete input: mp>mp
- Required aliases: mp>mp, 中拳>中拳
- Newly added: mp>mp, 中拳>中拳
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Yasmine: Sunod-sunod na Sipa

- Entry: `yasmine.unique.sunod_sunod_na_sipa` / 多段连踢
- Observed properties: High
- Complete input: mk>mk>hk
- Required aliases: mk>mk>hk, 中脚>中脚>重脚
- Newly added: mk>mk>hk, 中脚>中脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:

### Yasmine: Kumbinasyong Pampabagsak

- Entry: `yasmine.unique.kumbinasyong_pampabagsak` / 倒地组合技
- Observed properties: High
- Complete input: 2mk>hk
- Required aliases: 2mk>hk, 下中脚>重脚
- Newly added: 2mk>hk, 下中脚>重脚
- Conditions: None specified
- Historical patch verified:
- Reviewer:
- Decision:
- Notes:
