# Frozen 100-comment agent silver review

This is **agent review**, not independent human gold. The selected existing
comments were read in full and annotated with written relevance reasons. There
are 50 English and 50 Chinese comments, 90 related, eight unrelated and two
uncertain. Sampling was stratified by the old admission outcome and deliberately
includes known failures, so label prevalence does not represent the full corpus.

`labels.jsonl` binds immutable source IDs to exact original-text SHA-256 hashes.
It stores related/unrelated/uncertain, reasons, selected clear character/direction
expectations, numerical requests and error categories. Character expectations
are intentionally non-exhaustive: unlisted claims cannot be scored as false
positives. `source:Arjun` means only a source-literal identity; official identity
and patch applicability are not verified. Tier statements are topic-related
without automatically requesting a buff/nerf. Historical balance patches are
related without being new change requests. Accessibility and pure input-learning
discussion are unrelated unless a competitive strength/fairness opinion appears.

The fixed 70/30 development/holdout split keeps previously inspected forced
failure cases in development. Threshold calibration reads development only.
The remaining holdout is within-project silver, not a blind external evaluation.
Uncertain labels are excluded from binary relevance metrics and counted explicitly.
Future corrections require a new version and documented reasons, not silent
editing of this frozen set. Source data stays in the existing local raw dataset.

Independent human double annotation/adjudication remains necessary before using
these labels to claim model accuracy or production precision/recall.
