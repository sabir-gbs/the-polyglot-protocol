# SQL

Use SQL for database schemas, migrations, queries, views, indexes, and reports.
Choose the database dialect before generating SQL.

## Dialect Selection

Identify the target first: PostgreSQL, SQLite, MySQL/MariaDB, SQL Server,
Oracle, DuckDB, BigQuery, Snowflake, or another engine. Do not mix dialect
features without a compatibility reason.

## Tooling

```sh
psql --version
sqlite3 --version
mysql --version
```

Use the project's migration tool, formatter, and test database when available.

## Generation Rules

Use parameterized queries from application code. Add reversible migrations when
possible, explicit constraints, indexes with query-plan evidence for risky
paths, and transaction boundaries. Never concatenate untrusted input into SQL.

## Source Documentation And Comments

Comment migrations with intent, data-impact, rollback notes, locking risk, and
expected runtime for large tables. Document views, complex queries, non-obvious
indexes, constraints, and dialect-specific behavior. Avoid comments that simply
repeat table or column names.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Refactoring Playbook

- **Characterization Refactor**: capture current behavior with tests before changing legacy, risky, or poorly understood code.
- **Extract And Isolate**: extract functions, modules, classes, or components only when it reduces duplication, isolates an external system, or clarifies a real boundary.
- **Rename For Domain Clarity**: rename symbols when names hide intent; keep scope narrow and update tests, docs, and public references deliberately.
- **Simplify Control Flow**: flatten nested conditionals, remove duplicated branches, and replace clever logic with direct readable logic.
- **Dead Code And Dependency Pruning**: remove unused code, imports, flags, config, assets, and dependencies only after search and test evidence.
- **Boundary Refactor**: move validation, serialization, authorization, persistence, and external API calls to explicit boundaries.
- **Performance Refactor**: optimize for lower complexity, lower allocation, or better I/O only with a measured bottleneck or obvious pathological cost.
- **Compatibility-Preserving Migration**: add compatibility first, migrate callers or data, verify both paths, then remove the old path in a separate cleanup.
- **Concurrency Refactor**: introduce async, threads, workers, queues, GPU, or parallelism only after profiling and with cancellation, backpressure, and race tests.
- **Architecture De-Escalation**: remove unnecessary factories, inheritance, brokers, abstractions, or frameworks when simpler code satisfies the contract.

## Project Discovery And Structure

Before generating SQL, identify the database dialect, migration tool, schema
layout, naming conventions, transaction behavior, data volume, indexes,
permissions, and rollback process. Preserve existing migration ordering and
application query boundaries.

## Design Patterns And Architecture

Use normalization, constraints, indexes, views, materialized views, stored
procedures, and partitioning only when they match access patterns and database
capabilities. Avoid abstract schemas, generic EAV models, and premature
denormalization without query-plan evidence.
## Algorithmic Complexity And Dynamic Programming

Reason about complexity through indexes, joins, cardinality, query plans, and
data volume. Prefer indexed `O(log n)` lookups, set-based operations, window
functions, and linear scans only when appropriate. Avoid row-by-row procedural
loops and N+1 application queries. Recursive CTEs or dynamic-programming-like
queries require clear bounds, explain plans, and test data at realistic scale.

## Senior Architecture Decisions

Use the database for consistency, constraints, set-based work, transactions, and
indexes. Use queues for work that should happen after commit, can be retried, or
must be decoupled from request latency. Prefer an outbox pattern for reliable
event publication. Avoid triggers, stored procedures, or distributed
transactions unless they simplify consistency and are observable.

## Concurrency Parallelism And Hardware Acceleration

Use database concurrency deliberately: transactions, isolation levels, locks, indexes, batch sizes, and query plans. Prefer set-based operations over application-side threading. Avoid long transactions and lock escalation. Use parallel query features only when the database planner chooses them or evidence supports them. GPU acceleration is database/vendor-specific and requires proof.


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
