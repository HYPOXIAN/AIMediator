# Emotion Quantification and Evidence Isolation

- Type: Design
- Status: Active
- Updated: 2026-11-03
- Applies to: evidence-quality module v1 as implemented; written 2026-10-29
- Related: [evidence-quality.md](evidence-quality.md), the pre-implementation specification

**Project:** AI Mediator  
**Module:** Evidence Quality  
**Date:** October 29, 2026  

## 1. Purpose

The module measures the proportion of pure emotional content in a player comment and controls which parts may support balance-analysis claims. It preserves useful feedback even when the author is angry.

## 2. Processing Flow

The pipeline follows these steps:

1. Split the original comment into evidence units while preserving text and Unicode offsets.
2. Ask a language model to label source segments and identify information points.
3. Validate the labels against the original source.
4. Calculate the pure-emotion ratio and route each information point or unused segment.
5. In enforcement mode, extract claims only from eligible mechanism points.
6. Check source binding, perform a separate semantic audit, and aggregate accepted claims using unique comment IDs.

## 3. Segment Annotation

Each segment contains an exact source quote, an evidence-unit ID, and a half-open character interval `[start, end)`. Offsets use Unicode code points rather than bytes or UTF-16 units.

The model labels three separate dimensions:

- **Scope:** `character_balance`, `system_balance`, `unrelated`, or `uncertain`.
- **Content kind:** `pure_emotion`, `general_opinion`, `concrete_feedback`, `other`, or `uncertain`.
- **Emotional tone:** a Boolean indicating whether the expression is emotional.

## 4. Emotion Ratio

The model supplies annotations, not a ratio. The program calculates the measurement deterministically.

For text `x`, define `W(x)` as the number of Unicode code points whose category begins with:

- `L`: letters, including Chinese characters;
- `N`: numbers;
- `M`: combining marks;
- `S`: symbols, including many emoji.

Whitespace and punctuation are excluded. The ratio is:

```text
emotion_ratio = sum(W(segment.quote) for pure_emotion segments)
                / W(original_comment)
```

Only segments labeled `pure_emotion` enter the numerator. Segments with `emotional_tone = true` do not enter it solely because of their tone. The result therefore measures pure-emotion content share, not sentiment polarity, emotional intensity, or the probability that a comment is negative.

If the denominator is zero, the ratio is `null` and `empty_measurement` is true. Invalid annotations fail validation rather than producing a valid ratio.

The current policy sets `high_emotion_threshold` to `0.70`. A ratio at or above this value sets `high_emotion_warning`.

## 5. Evidence Isolation

Validated information points and unused segments are assigned to separate routes:

- **`exclude`:** content without usable balance information, such as pure venting, is excluded from balance analysis.
- **`opinion_only`:** general character-strength opinions or broad requests are retained as a separate opinion summary.
- **`mechanism_evidence`:** concrete character feedback with a source-bound character identity is eligible to support claims.
- **`system_evidence`:** system-balance feedback is retained separately from character evidence.
- **`review`:** unresolved context, attribution, quotation, sarcasm, or other uncertainty is queued for review.
