# Glossary alias reviews: conclusion record

- Type: Record
- Status: Active
- Updated: 2026-11-03
- Applies to: `src/aimediator/assets/data/glossary.json` (alias collection of
  2026-10-08, Unique Move review of 2026-10-08, low-alias search of
  2026-10-22); target patch 08.03.2026 Update

This record replaces three review dumps that used to be in the
documentation tree. The dumps are machine-generated review sheets, so they
now live in the external archive (plan section 7, decision 5; RULES.md D7).
This record states what they contained and in what state they were left.
It adds no review decision of its own.

## Reviews covered

| Review | Date | Scope | Mappings | Decisions |
| ------ | ---- | ----- | -------: | --------- |
| Community alias review (`alias-review.md`) | collected 2026-10-08 | 1582 new alias mappings, 775 distinct text/language pairs | 1582 | 418 decision fields, all blank |
| Unique Move alias review (`unique-move-alias-review.md`) | reference checked 2026-10-08 | 31 characters, 244 Unique Move entries, 51 with an overhead hit | 510 | 244 decision fields, all blank |
| Low-alias move review (`low-alias-review.md`, `low-alias-review.json`) | searched 2026-10-22 | 293 moves across 31 characters | 594 | Markdown: 594 fields, 9 filled (below); JSON: 594 fields, all blank |

Details taken from the dumps:

- **Community alias review**: 225 observed community candidates, 174
  historical candidates and 1183 generated spelling or notation variants;
  42 normal-move aliases had been removed at the user's request. Candidate
  kinds: `community_attested_candidate`, `legacy_community_candidate`,
  `editorial_spelling_candidate`, `editorial_notation_candidate`. A source
  observation does not certify a mapping.
- **Unique Move alias review**: live Capcom properties were not matched to the
  historical 2026-08-03 patch; the "Historical patch verified" fields are
  blank. Overhead moves receive the two overhead aliases; other moves receive
  numpad/button notation and simplified Chinese direction/button labels.
- **Low-alias move review**: selection was moves with at most one displayed
  explicit alias in the glossary document. Candidate kinds (JSON):
  `editorial_notation_candidate` 582, `community_attested_candidate` 5,
  `editorial_description_candidate` 4, `legacy_community_candidate` 2,
  `legacy_name_candidate` 1. The source was a community command list
  (SPMoves); the Capcom Luke movelist returned HTTP 403. The dump calls
  itself a staging area that the application does not load
  (`runtime_applied: false`).

## Status as found

No review was completed. Every decision field in the community and Unique
Move reviews is blank, and the low-alias JSON has no decision. The
low-alias Markdown, whose header says "All decisions are blank", has nine
filled decision fields that the JSON does not have. They are listed here as
written; what `p` and `np` mean is not recorded anywhere, so they are not
interpreted or applied (change record, P4-D10).

| Line | Character | Move | Entry | Candidate | Decision |
| ---: | --------- | ---- | ----- | --------- | -------- |
| 35 | Ryu | Shoryuken / `升龙拳` | `ryu.shoryuken` | `→↓↘拳` | `p` |
| 53 | Ryu | Hashogeki / `波掌击` | `ryu.hashogeki` | `↓↙←拳` | `p` |
| 65 | Ryu | Shoulder Throw / `背负投` | `ryu.forward_throw` | `(近身) 6/n+LP+LK` | `p` |
| 71 | Ryu | Shoulder Throw / `背负投` | `ryu.forward_throw` | `(近身) →/n+轻拳+轻脚` | `p` |
| 83 | Ryu | Somersault Throw / `巴投` | `ryu.back_throw` | `(近身) 4LP+LK` | `p` |
| 139 | Luke | Fatal Shot / `致命射击` | `luke.special.fatal_shot` | `斗爆版中 双拳` | `np` |
| 157 | Luke | DDT / `深度死亡摔` | `luke.special.ddt` | `斗爆版中 双拳` | `np` |
| 205 | Luke | No Chaser / `勇往直前` | `luke.special.no_chaser` | `肩撞` | `p` |
| 211 | Luke | No Chaser / `勇往直前` | `luke.special.no_chaser` | `拳` | `np` |

"Line" is the line of the decision field in the archived
`low-alias-review.md`. Reviewer and notes fields of these entries are blank.

## Effect on runtime data

- The community and Unique Move aliases are in `glossary.json` as
  candidates (`alias_collection.status` is `pending_human_review`); their
  per-alias review fields are blank. Indexing or retrieval does not approve
  them.
- The low-alias proposals were never applied to `glossary.json` or to the
  glossary document.
- `glossary.json` names this record as the `review_file` of the alias
  collection and of the Unique Move additions.

## Archived dumps

`~/Archives/AIMediator/docs-data/`, copied, verified with `sha256sum -c`
against the working files and the baseline backup, and then removed from
the project (change record, P4).

| File | Bytes | SHA256 |
| ---- | ----: | ------ |
| `alias-review.md` | 174,246 | `4320063dd22a129f9eef9f355173d0957e8798f7f144569f1aee1ed4d1fde88a` |
| `low-alias-review.json` | 328,981 | `590e83e930acfe75583d4fbf27fc1228cbd998bab5ba820d75a524aa39c17ba9` |
| `low-alias-review.md` | 204,137 | `8a825d5047c6f21daf315e926f1873b3492c8b38c3d5af70c0f3627ccc3fb594` |
| `unique-move-alias-review.md` | 81,032 | `a66b7ac51033e36b0f28b0ed6063825530f3efeac593fec6727b3d1d8c59cf6f` |

To continue a review, work on a copy of the archived dump and apply the
decisions to the per-alias records in `glossary.json` in a separate change.
