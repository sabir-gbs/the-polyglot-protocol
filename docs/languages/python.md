# Python

Use Python as the default language for operational scripts, automation, audits,
migrations, file processing, and glue code. `python/python.md` is the
authoritative deep guide.

## Runtime And Environment

- Target Python `3.14.5+`.
- Use a project `.venv`; never install packages globally.
- Invoke packages with `python -m ...`.
- Use `pathlib`, UTF-8, explicit time zones, and portable subprocess handling.

## Tooling

```sh
python --version
python -m pip install -r requirements-dev.txt
python -m ruff format .
python -m ruff check .
python -m mypy --strict .
python -m pytest
python -m pip_audit
```

## Generation Rules

Prefer stdlib before dependencies. Use `argparse` for CLIs unless the user
approves another CLI framework. Add dry-run support for destructive operations.
Keep output machine-readable where practical and send diagnostics to stderr.

## Source Documentation And Comments

Use docstrings for public modules, classes, functions, CLI entry points, and
non-obvious exceptions. Keep docstrings focused on contract, arguments, return
value, side effects, and failure modes. Use inline comments only for intent,
invariants, security decisions, portability constraints, or complex algorithms;
do not restate what the code already says.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Project Discovery And Structure

Before generating code, inspect `pyproject.toml`, `requirements*.txt`, existing
package layout, test layout, CLI entry points, and lint/type settings. Preserve
`src/` layout, module names, public APIs, and dependency policy. New reusable
code belongs in importable modules; one-off operational work belongs in small
Python scripts with clear arguments.

## Design Patterns And Architecture

Prefer plain functions, dataclasses, protocols, and small modules before
classes or frameworks. Use Strategy, Adapter, Repository, or Factory only when
they remove real branching, isolate external systems, or match existing
architecture. Avoid dependency-injection frameworks and deep inheritance unless
the project already uses them.
## Algorithmic Complexity And Dynamic Programming

State expected time and space complexity for non-trivial algorithms. Prefer
`O(n)` single-pass, streaming, dictionary/set lookups, heaps, or sorting plus
linear scans over nested loops. Use dynamic programming only for overlapping
subproblems with optimal substructure; define the state, transition, base cases,
iteration order, and memory reduction. Add tests for boundary sizes and document
any unavoidable `O(n log n)` or `O(n^2)` behavior.

## Senior Architecture Decisions

Prefer the simplest synchronous path until latency, reliability, or throughput
requires background work. Use queues for slow I/O, retries, fan-out, scheduled
jobs, and decoupling, with idempotent handlers, bounded retries, dead-letter
handling, backpressure, and structured logs. Keep transactions short, cache only
with invalidation rules, and expose metrics for queue depth, latency, failures,
and retry counts.

## Concurrency Parallelism And Hardware Acceleration

Use async I/O for many waiting network/file operations, threads for blocking I/O that cannot be made async, and processes or native extensions for CPU-bound work because of the GIL. Use GPU libraries only for large numeric, image, ML, or vector workloads where transfer overhead is justified. Require cancellation, timeouts, bounded queues, race-safe shared state, and benchmarks before adding parallelism.


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
