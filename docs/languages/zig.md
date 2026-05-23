# Zig

Use Zig for systems code, low-level tooling, cross-compilation, and repositories
that already use Zig.

## Runtime And Build

- Use stable Zig, currently `0.16.0`.
- Avoid master or nightly unless the user explicitly accepts instability.
- Preserve `build.zig`, package structure, and target matrix.

## Tooling

```sh
zig version
zig fmt .
zig build
zig test path/to/file.zig
```

## Generation Rules

Handle errors explicitly, keep allocation ownership clear, avoid hidden global
state, and test comptime-heavy code. Document target assumptions and allocator
lifetimes.

## Source Documentation And Comments

Use doc comments for public declarations, modules, build options, allocator
contracts, and target assumptions. Comment comptime behavior, ownership,
sentinel and alignment assumptions, error-set intent, and FFI boundaries. Avoid
comments that restate simple declarations.

## Project Discovery And Structure

Before generating Zig, inspect `build.zig`, target matrix, module layout,
allocator conventions, error sets, tests, and C interop. Preserve allocation
ownership, target-specific branches, and build options.

## Design Patterns And Architecture

Prefer explicit structs, functions, comptime parameters, and error unions. Use
interface-like vtables or tagged unions only when variation is required. Avoid
hidden allocation, generic indirection, and comptime complexity that slows builds
without measurable benefit.
## Algorithmic Complexity And Dynamic Programming

State complexity and allocation behavior for non-trivial algorithms. Prefer
`O(n)` loops, slices, bounded arrays, hash maps, and explicit preallocation over
nested scans. Use dynamic programming only with explicit state layout, allocator
choice, base cases, and memory bounds. Avoid hidden allocation and excessive
comptime work in hot or frequently built paths.

## Senior Architecture Decisions

Keep systems architecture explicit: bounded queues, clear allocator ownership,
known thread lifetimes, cancellation, and shutdown paths. Prefer simple event
loops or proven brokers over custom distributed infrastructure. Queue consumers
need idempotency, backpressure, retry bounds, and observability hooks without
hidden allocation.

## Concurrency Parallelism And Hardware Acceleration

Use threads, event loops, atomics, and async patterns only with explicit ownership, allocator strategy, cancellation, and shutdown behavior. Bound worker queues and avoid hidden allocation. Use SIMD, GPU APIs, or accelerators only after profiling and when transfer and setup costs are justified. Test races, memory safety, and platform-specific paths.


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
