# Rust

Use Rust for systems software, CLIs, services, WebAssembly, performance-critical
libraries, and repositories that already use Rust.

## Runtime And Package Management

- Use stable Rust, currently `1.95.0`.
- Preserve `Cargo.toml`, `Cargo.lock`, workspace layout, and feature flags.
- Use the current edition for new crates unless interoperability requires older.

## Tooling

```sh
rustc --version
cargo fmt --all
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets --all-features
cargo audit
```

## Generation Rules

Prefer safe Rust, explicit error types, and clear ownership. Document every
`unsafe` block with its invariant. Use tests for parsing, concurrency,
serialization, and boundary-heavy behavior.

## Source Documentation And Comments

Use rustdoc (`///` and `//!`) for public crates, modules, traits, structs,
functions, errors, feature flags, and examples. Include doctests for important
APIs when practical. Comment unsafe invariants, ownership subtleties, lifetime
constraints, concurrency assumptions, and FFI boundaries.

## Project Discovery And Structure

Before generating Rust, inspect `Cargo.toml`, workspace layout, features,
edition, modules, error types, tests, benches, and unsafe/FFI boundaries.
Preserve crate visibility, feature flags, public API stability, and allocation
strategy.

## Design Patterns And Architecture

Prefer traits, enums, newtypes, builders for complex construction, and typestate
only when it prevents invalid states without runtime cost. Use Adapter and
Strategy through traits where variation is required. Avoid trait-object
dispatch, boxing, or async abstraction overhead in hot paths unless justified.
## Algorithmic Complexity And Dynamic Programming

State time and space complexity for algorithms and data-structure choices.
Prefer `O(n)` iterators, slices, hash maps/sets, sorted vectors, and
preallocation over nested scans. Use dynamic programming only when state,
transition, base cases, and ownership are explicit. Consider memory layout,
borrowing, allocation count, and benchmarks for hot algorithms.

## Senior Architecture Decisions

Use async runtimes, channels, actors, and message queues only with explicit
ownership, bounded buffers, cancellation, backpressure, and graceful shutdown.
Queue consumers need idempotency, retry limits, dead-letter behavior, tracing,
and metrics. Prefer typed messages and compile-time state where it prevents
runtime failures without adding allocation or dispatch overhead.

## Concurrency Parallelism And Hardware Acceleration

Use threads, async runtimes, channels, and work-stealing libraries with explicit ownership, cancellation, bounded queues, and shutdown behavior. Prefer data parallelism through proven libraries after profiling CPU-bound work. Use GPU APIs or compute libraries only when workload size and transfer costs justify them. Let the type system prevent data races and test async cancellation paths.


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
