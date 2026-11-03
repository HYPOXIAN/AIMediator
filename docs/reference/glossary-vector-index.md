# Glossary vector index

- Type: Reference
- Status: Active
- Updated: 2026-11-03
- Applies to: `data/processed/glossary-vectors/`; `aimediator.glossary_vectors`

The index uses every entry and every alias in `data/glossary.json`, including
pending candidates. Index inclusion does not approve a candidate. The separate
`~/Archives/AIMediator/docs-data/low-alias-review.*` proposals are not imported.

Each glossary entry is one retrieval document containing its identity, character,
category, English and Chinese names, all alias objects and their restrictions,
notation, super level and notes. The complete source entry is retained alongside
its embedding. Global policies, ambiguity records and sources are saved in
`context.json` for downstream RAG resolution. Do not interpret vector similarity
as approval or as proof of character identity.

Configuration comes from `.env` (or same-name environment variables):
`EMBEDDING_API_KEY`, `EMBEDDING_API_URL`, `EMBEDDING_MODEL`. A URL ending in
`/chat/completions` is adapted to the same service's `/embeddings` route; the
configuration file is not changed. Credentials are not saved to index metadata.
The API receives the glossary documents and any search query submitted.

Requires Python and NumPy. From the project root:

```bash
python scripts/glossary_vectors.py build
python scripts/glossary_vectors.py search '隆的波掌击' --scope Ryu --top-k 5
```

The build stores data in `data/processed/glossary-vectors/`:

- `current.json`: active version identity, published only after a complete build.
- `versions/<identity>/vectors.npy`: L2-normalized float32 embedding matrix.
- `versions/<identity>/records.json`: source entries and embedding texts, aligned
  row-for-row with the matrix.
- `versions/<identity>/context.json`: full glossary-level policies and ambiguity
  records, including sources.
- `versions/<identity>/manifest.json`: model, endpoint, actual dimensions, counts,
  source hash, file checksums, query instruction and build time.
- `batches/<identity>/`: resumable embedding batches and reported API usage.

The index is an exact cosine-search vector space implemented with NumPy; no
external database service is required at this corpus size. Query vectors use the
same model and endpoint and an explicit Qwen-style retrieval instruction. Search
returns full source records with similarity scores. `--scope` filters results to
the selected character plus universal concepts. Without a scope, shared terms
may retrieve multiple characters. The command does not generate an answer.

Re-running the build resumes completed batches for identical source content,
model and endpoint. Changing the glossary creates a separate version. Search
checks model/endpoint consistency and index file integrity. Existing indexes are
snapshots; rebuild after source edits. Keep the ambiguity/policy context and
candidate status when integrating results with a generator.

API reference: [OpenRouter embeddings](https://openrouter.ai/docs/api/api-reference/embeddings/create-embeddings).
