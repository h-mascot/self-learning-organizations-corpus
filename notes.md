# Notes: Corpus Goal 1

## Engineering/QA lane

- Six legacy ID-only YouTube transcripts were migrated into canonical source records.
- Five initial seeds are relevant; `fVut0ceg2IY` is an unrelated OpenTable ad and remains preserved as quarantined evidence.
- Canonical path: `sources/<platform>/<accepted|rejected>/<date>--<title>--<publisher>--<stable-id>.md`.
- Accepted transcripts must be non-empty, timestamped, and reach at least 80% of declared duration.
- Initial verification passed 10/10 tests with 5 validated relevant sources and 1 rejected source.

## Research lane

- Exa and authenticated GitHub CLI were usable; X retrieval lacked authentication.
- Perplexity had no configured CLI/MCP/key; direct API returned HTTP 401 and blocker proof is preserved.
- OpenAI/GPT web research completed through authenticated Codex web search.
- The initial 200-item Crossref topic-by-facet matrix remains useful discovery evidence but did not satisfy the recursive-loop gate.
- A corrective run replaced that drifted matrix with a separately validated 200-loop dependent research DAG while preserving the original evidence.

## YouTube lane

- The `goal/youtube` worker began with 6 transcripts, 5 relevant candidates, missing seed `I9c8STV7Hnw`, and unrelated seed `fVut0ceg2IY`.
- 25 reproducible queries yielded 478 unique candidates.
- Caption retrieval hit HTTP 429, so the pipeline used Groq Whisper ASR fallback; both available models enforce 7,200 audio-seconds/hour.
- Chrome cookies and the recommended EJS component did not recover YouTube access; the final probe still returned HTTP 429 and “Sign in to confirm you’re not a bot.”
- 64 relevant timestamped transcripts passed the worker validator, including `I9c8STV7Hnw`.
- `yk2o6Sj3XQk` (repeated “Thank you”) and `dFIM6WcjYEc` (individual memory-training advertisement) were quarantined.
- 47 attempted/unresolved sources remain materialized in `research/progress/youtube-failures.jsonl`.
- Raw caption/ASR evidence, quarantine records, and failure ledgers are retained.
