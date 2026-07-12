# Web/media lane record format

Each record is a UTF-8 JSON object stored under `sources/<lane>/<lifecycle>/<stable-id>.json`, where lane is one of `blogs`, `podcasts`, `books`, `conferences`, `case-studies`, or `github`, and lifecycle is `accepted`, `rejected`, or `blocked`.

Required fields:

- `schema_version`: integer `2` (lane contract aligned to GOAL.md terminology).
- `platform`: directory lane.
- `stable_id`: deterministic platform-specific or URL-derived ID.
- `title`, `creator`, `publisher`, `canonical_url`, `published_date` (ISO date or `null` with `date_precision: unknown`).
- `source_type`: article, episode, book, talk, case-study, repository, issue, or discussion.
- `status`: accepted, rejected, or blocked.
- `artifact_level`: full_text, transcript, abstract, metadata_only, or unavailable.
- `retrieved_at`: UTC ISO-8601 timestamp.
- `retrieval_method`, `provenance`, `rights_status`, and `rights_note`.
- `content_sha256`: SHA-256 of the canonical JSON serialization of `evidence`.
- `relevance_evidence`: non-empty list for accepted records.
- `evidence`: list of bounded evidence objects with `locator`, `text`, and `kind`.
- `query_ids`: identifiers into the lane query ledger.

Accepted records in every lane except books must carry bounded evidence; accepted podcasts additionally require a publisher-supplied transcript or timestamped public notes. Books may be accepted at `metadata_only`, as GOAL.md explicitly permits. `metadata_only` honestly means no complete source artifact is archived, even when bounded evidence spans support relevance.

Query attempts live in `research/web-media-acquisition/query-ledger.jsonl`; retrieval outcomes live in `research/web-media-acquisition/retrieval-ledger.jsonl`. Both are append-oriented evidence ledgers and include failures as well as successes.
