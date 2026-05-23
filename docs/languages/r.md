# R

Use R for statistical analysis, reproducible research, reporting, and projects
that already use R.

## Runtime And Dependency Management

- Use stable R, currently `4.6.0`, unless the project or platform pins another
  version.
- Use `renv` for dependency isolation.
- Keep data, scripts, reports, and generated artifacts separated.

## Tooling

```sh
R --version
Rscript -e 'renv::restore()'
Rscript -e 'styler::style_dir()'
Rscript -e 'lintr::lint_dir()'
Rscript -e 'testthat::test_dir("tests")'
```

## Generation Rules

Be explicit about column types, encodings, locale, time zones, and missing
values. Avoid hidden global state and set seeds for randomized analysis.

## Source Documentation And Comments

Use roxygen2 comments for package functions, datasets, parameters, return
values, examples, and exported objects. In scripts and notebooks, document data
sources, statistical assumptions, filtering rationale, seeds, and reproducibility
constraints. Avoid comments that merely describe assignment syntax.

## Project Discovery And Structure

Before generating R, inspect project layout, `renv.lock`, package structure,
notebooks, data directories, report targets, tests, and style tooling. Preserve
data provenance, analysis pipeline boundaries, and reproducibility conventions.

## Design Patterns And Architecture

Prefer pure functions, explicit data frames, pipelines, and small package
functions. Use S3/S4/R6 only when the project already uses them or stateful
objects are truly needed. Avoid hidden global options and mutation-heavy designs
that make analysis irreproducible.
## Algorithmic Complexity And Dynamic Programming

Document complexity for data transformations and statistical routines. Prefer
vectorized operations, joins, grouping, and indexed data structures over nested
R loops. Use dynamic programming only when recurrence state is clear and memory
use is acceptable. For large data, document row counts, memory expectations, and
when to move work to database, data.table, or compiled code.

## Senior Architecture Decisions

R should usually consume queued or scheduled work rather than host production
brokers. For analytics pipelines, use reproducible batch jobs, durable inputs,
checkpointed outputs, and explicit retry/idempotency rules. Move orchestration,
backpressure, and long-running queue workers to Python, the database, or a
workflow scheduler.

## Concurrency Parallelism And Hardware Acceleration

Use vectorization first, then parallel packages or batch schedulers for measured CPU-bound work. Keep random seeds, chunking, and result ordering reproducible. Use GPU packages only for large matrix, ML, or numeric workloads where data transfer overhead is justified. Avoid parallelism that exceeds memory capacity or makes analysis non-reproducible.


## Senior Decision Checklist

- **Security Threat Modeling And Abuse Cases**: identify trust boundaries, validate all inputs, protect secrets, avoid injection and unsafe deserialization, and apply least privilege for this language surface.
- **Data Modeling And Persistence**: define ownership, schema or shape, indexes, migrations, serialization, retention, and compatibility before changing stored data.
- **API Contracts And Compatibility**: preserve public signatures, request/response schemas, events, error formats, pagination, and versioning unless a breaking change is explicit.
- **Error Handling And Recovery**: separate retryable, user-correctable, and terminal failures; add timeouts, fallback behavior, cleanup, and clear error reporting.
- **Observability And Operability**: emit useful logs, metrics, traces, correlation IDs, health signals, and runbook notes for production-relevant behavior.
- **Testing Strategy By Risk**: match tests to risk with unit, integration, property, fuzz, race, load, snapshot, or end-to-end tests as appropriate; avoid mocks that hide contract failures.
- **Performance Budgets And Profiling**: set budgets for latency, memory, startup, bundle size, query count, render cost, or throughput; profile before optimizing.
- **Dependency And Supply-Chain Governance**: add dependencies only with justification, lock exact versions, check licenses and vulnerabilities, and prefer standard library or platform APIs.
- **Configuration And Environment Strategy**: validate config at startup, keep secrets out of source, document defaults, and preserve local/stage/prod parity.
- **Release Migration And Rollback Strategy**: plan safe rollout, backward compatibility, data backfills, feature flags, rollback paths, and cleanup after migration.
- **Accessibility And Internationalization**: for user-facing surfaces, support keyboard access, readable text, locale-aware formatting, translation boundaries, and inclusive defaults.
- **Privacy Compliance And Data Governance**: minimize PII, redact logs, enforce retention/deletion rules, protect consent boundaries, and document audit-sensitive data flows.


## Final Senior Guardrails

- **Code Review Checklist**: block changes that lack clear correctness, security, test, performance, compatibility, or maintainability evidence.
- **Refactoring Rules**: refactor only with preserved behavior, small reviewable steps, characterization tests for risky code, and no unrelated churn.
- **Generated And AI-Assisted Code Rules**: verify generated APIs, dependencies, licenses, and claims against source docs; remove hallucinated options and unused code.
- **Platform And OS Integration**: handle filesystem, permissions, signals, services, shells, installers, encodings, and platform differences explicitly.
- **Serialization And Wire Formats**: validate schemas, preserve backward compatibility, define encoding, version formats, and reject malformed input safely.
- **Time Date Locale And Money**: use timezone-aware UTC internally, handle DST and locale formatting deliberately, and never use binary floats for money.
- **Resource Lifecycle**: close files, sockets, database handles, locks, processes, and transactions deterministically; support cancellation and cleanup on failure.
- **Build And Packaging Strategy**: keep builds reproducible, outputs minimal, metadata accurate, artifacts verifiable, and target platforms explicit.


## LLM Coding Guardrails

Apply `top-llm-coding-nuances.md` before generating code in this language. Verify APIs, flags, package names, runtime behavior, and tool output against local files or official docs before relying on them. Preserve existing project conventions, avoid speculative rewrites, and choose the shortest reliable supported path. Do not add dependencies, queues, concurrency, GPU paths, migrations, or design patterns without evidence, tests, rollback notes, and documented tradeoffs.
