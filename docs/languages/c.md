# C

Use C for low-level systems code, embedded interfaces, ABI boundaries, or
projects that already use C. Prefer Python for operational scripts around C
projects.

## Standard And Toolchain

- Use C23 for new code when supported; otherwise preserve the project standard.
- Prefer CMake or Meson when the project has no build system.
- Compile with warnings enabled and treated as errors in CI.

## Tooling

```sh
cc --version
cmake --build build
ctest --test-dir build
clang-format -i path/to/file.c
```

## Generation Rules

Check every allocation, bounds operation, and system call. Use sanitizers for
risky changes. Keep ownership clear in names and comments. Avoid undefined
behavior, unchecked integer conversions, and string functions without bounds.

## Source Documentation And Comments

Use header comments for public functions, structs, ownership rules, lifetime
expectations, thread-safety, and error returns. Comment invariants, allocation
ownership, buffer sizes, aliasing assumptions, and intentional undefined-behavior
avoidance. Do not clutter straightforward local logic with restatement comments.

## Project Discovery And Structure

Before generating C, inspect build files, compiler flags, target platforms,
headers, ABI boundaries, memory allocation conventions, tests, and sanitizer
settings. Preserve header/source separation, naming prefixes, error conventions,
and ownership rules.

## Design Patterns And Architecture

Use lightweight patterns: opaque structs for encapsulation, function-pointer
tables for pluggable behavior, and explicit init/destroy pairs for resources.
Avoid allocation-heavy abstractions, hidden globals, and virtual-dispatch style
patterns in hot paths unless the project already uses them.
## Algorithmic Complexity And Dynamic Programming

State time and space complexity for non-trivial algorithms. Prefer cache-aware
`O(n)` scans, indexed lookup tables, sorted arrays plus binary search, or
precomputed tables over nested loops. Use dynamic programming only when state
and transitions are compact and memory bounds are explicit. Document allocation
size, overflow checks, cache behavior, and any unavoidable non-linear cost.

## Senior Architecture Decisions

Keep architecture explicit and resource-bounded. For queues, prefer bounded
in-memory queues or proven external brokers with clear ownership, locking,
backpressure, and shutdown behavior. Avoid hidden threads and unbounded buffers.
Document concurrency, memory ownership, retry policy, failure modes, and
observability hooks for production systems.

## Concurrency Parallelism And Hardware Acceleration

Use threads, atomics, locks, and event loops only with documented ownership, memory ordering, cancellation, and shutdown behavior. Prefer bounded worker pools over unbounded thread creation. Use SIMD, GPU APIs, or accelerator libraries only after profiling and when memory transfer cost is justified. Validate with sanitizers, stress tests, and benchmarks.


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
