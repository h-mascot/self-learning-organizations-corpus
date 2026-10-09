# 2026-10-09 Corpus Refresh Plan

## Scope
Refresh `h-mascot/self-learning-organizations-corpus` locally on branch `refresh/2026-10-09` from baseline `207ce27b193b3980d66e3b7bcadb1b9e956e9472`. Do not push or merge. Preserve July records and historical saturation evidence. Apply only corpus/research portions of runner-corpus.

## Contract
- Eligible original publication dates: 2026-07-16 through 2026-10-09 inclusive.
- Publisher/API publication proof is mandatory. Search snippets, page update dates, and repo pushes are insufficient.
- Keep accepted/rejected/duplicate/blocked decisions explicit for all 11 lanes.
- Do not claim saturation from this bounded refresh. Status ends `READY_FOR_REVIEW`, reviewer Ada pending.

## Checklist
- [x] Read runner-corpus, agent-reach, README, GOAL, schema, tools, Makefile, validators, and samples.
- [x] Freeze baseline and create durable refresh workspace.
- [ ] Search all 11 lanes with at least two query families and legal alternate routes for blocked platforms.
- [ ] Dedupe against canonical corpus before retrieval.
- [ ] Ingest accepted records only when primary evidence, date, mechanism, rights, and lane validators hold.
- [ ] Preserve rejected/duplicate/blocked candidates and receipts.
- [ ] Run `make generate`, `make test`, `make audit`, lane validators, `make check`, and `git diff --cached --check`.
- [ ] Stage intended generated changes and commit locally only.

## Progress Log
- 2026-10-09T11:59:00+01:00: Baseline frozen at `207ce27b193b3980d66e3b7bcadb1b9e956e9472`; local branch and refresh workspace initialized.

## Files Touched
- `research/refresh-20261009/`
- `docs/plans/2026-10-09-corpus-refresh.md`
- `docs/plans/ACTIVE_PLAN.md`
- `research/progress/goal-2-status.md` (refresh status update pending)

## Resume Instructions
On compaction or restart, reread `docs/plans/ACTIVE_PLAN.md`, `research/refresh-20261009/CORPUS.md`, `research/refresh-20261009/STATUS.json`, `research/refresh-20261009/manager/state.json`, and the latest lane ledgers before continuing. Do not start a second collection owner.

## Closeout Update
- 2026-10-09T12:55:00Z: Collection complete and validation green. Accepted additions by lane: academic 3, blogs 1, books 1, conferences 1, case-studies 1, github 1; youtube/x/reddit/substack/podcasts 0.
- Candidate outcomes in refresh evidence ledgers: 8 accepted, 2 rejected, 6 blocked, 0 duplicates.
- Independent generated corpus totals: 1,062 accounted records, 648 accepted relevant sources, 414 rejected, 0 canonical blocked.
- Validation: `make generate`, `make test`, `make audit`, dedicated lane validators, `make check`, and `git diff --cached --check` passed.
- Status: `READY_FOR_REVIEW`; Ada review remains pending; no push or merge performed.
