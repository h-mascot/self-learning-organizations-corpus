# Task Plan: Engineering/QA Corpus Lane

## Goal
Deliver a committed, migration-safe corpus platform with canonical structure/schema, validation, generated documentation/statistics, CI, and regression coverage while preserving all current evidence.

## Phases
- [x] Phase 1: Inventory repository, data, and existing tooling before migration
- [x] Phase 2: Define canonical contracts and migration design
- [x] Phase 3: Implement tooling, safe migration, generated artifacts, and CI
- [x] Phase 4: Add and run regression tests; audit repository data
- [x] Phase 5: Checkpoint engineering progress, review diff, and commit

## Key Questions
1. What formats, paths, and metadata are already present and must remain compatible?
2. Which files can be migrated automatically without losing evidence or breaking links?
3. How should counted versus rejected sources be represented and verified?
4. What remaining data incompatibilities prevent a fully clean audit?

## Decisions Made
- Preserve raw source content and use a manifest for every path migration.
- Treat generated statistics and README sections as reproducible outputs of the validator.
- Use `sources/<platform>/<accepted|rejected>/` so exclusions remain preserved and auditable.
- Hash the exact Markdown body; migration manifests additionally hash each complete legacy file.

## Errors Encountered
- Generated CSVs initially used Python's platform-default CRLF terminator, which `git diff --check` reported as trailing whitespace; generators now explicitly use deterministic LF and artifacts were regenerated.

## Status
**Complete** - Preservation hashes, tests, corpus audit, generated-file reproducibility, and staged diff checks pass; committing the coherent engineering lane.
