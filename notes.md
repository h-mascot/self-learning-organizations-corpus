# Notes: Corpus Goal 1

## Engineering/QA lane
- Six legacy ID-only YouTube transcripts were migrated into canonical source records.
- Five are relevant; `fVut0ceg2IY` is an unrelated OpenTable ad and remains preserved as rejected evidence.
- Canonical path: `sources/<platform>/<accepted|rejected>/<date>--<title>--<publisher>--<stable-id>.md`.
- Accepted transcripts must be non-empty, timestamped, and reach at least 80% of declared duration.
- Initial verification: 10/10 tests passed; 6 records valid; 5 validated relevant; 1 rejected.

## Research lane
- Exa and authenticated GitHub CLI were usable.
- X retrieval lacked authentication in this worker environment.
- Perplexity had no configured CLI/MCP/key; direct API probe returned HTTP 401 and blocker proof is preserved.
- OpenAI/GPT web research completed through authenticated Codex web search.
- Crossref returned 200 evidence-bearing query artifacts across 20 topics and 10 facets.
- Manager audit: these 200 artifacts form a predetermined query matrix, not the requested recursive chain from prior findings. They remain useful discovery evidence but do not satisfy the final recursive-loop gate until corrected by a follow-up worker.
