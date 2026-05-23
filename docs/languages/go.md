# Go

Use Go for services, CLIs, networking tools, and repositories that already use
Go. Prefer Python for operational scripts unless Go is already the project
automation standard.

## Runtime And Modules

- Use stable Go, currently `1.26.3`.
- Preserve `go.mod`, module paths, and package boundaries.
- Keep `go.mod` and `go.sum` tidy.

## Tooling

```sh
go version
go fmt ./...
go test ./...
go vet ./...
govulncheck ./...
```

## Generation Rules

Return explicit errors, propagate `context.Context`, avoid package-level mutable
state, and keep interfaces small. Use table tests for parsing, validation, and
edge cases.

## Source Documentation And Comments

Use Go doc comments for every exported package, type, function, method,
constant, and variable. Start exported comments with the identifier name when
practical. Document context cancellation, error semantics, concurrency safety,
and side effects. Use inline comments for invariants and non-obvious algorithms.

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

## Best Practice Examples

- Bad: ignore returned errors with `_`. Good: handle, wrap, or deliberately
  document every error path with enough context for debugging.
- Bad: start goroutines without shutdown. Good: pass `context.Context`, bound
  work, close channels deliberately, and test cancellation.
- Bad: create broad interfaces before consumers exist. Good: define small
  interfaces at the consuming boundary and keep concrete types simple.

## Project Discovery And Structure

Before generating Go, inspect `go.mod`, package layout, internal packages,
command layout, interfaces, tests, build tags, and existing error/logging style.
Preserve package boundaries and keep new packages justified by real cohesion.

## Design Patterns And Architecture

Prefer simple functions, small interfaces at consumer boundaries, composition,
and explicit structs. Use Adapter for external services and Strategy via
interfaces when behavior must vary. Avoid generic architecture layers,
framework-style dependency injection, and premature repositories.
## Algorithmic Complexity And Dynamic Programming

State complexity for non-trivial algorithms. Prefer `O(n)` loops, maps, slices
with preallocated capacity, streaming readers, and sorted slices plus binary
search over nested scans. Use dynamic programming only when state is explicit
and memory is bounded. Avoid hidden allocations and benchmark hot algorithms
with representative inputs.

## Senior Architecture Decisions

Use goroutines, channels, worker pools, and external queues only with bounded
concurrency, context cancellation, backpressure, and graceful shutdown. Queue
consumers must be idempotent, observable, and retry-bounded with dead-letter
handling. Prefer a simple transaction or synchronous RPC when it satisfies the
reliability and latency requirement.

## Concurrency Parallelism And Hardware Acceleration

Use goroutines for concurrent I/O and worker pools for CPU-bound parallelism, always with bounded concurrency, `context.Context`, cancellation, and backpressure. Avoid sharing mutable state without synchronization. Tune `GOMAXPROCS` only with evidence. Use GPU through specialized libraries or external services only when large parallel workloads justify transfer and operational complexity.


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
