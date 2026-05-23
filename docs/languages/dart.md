# Dart

Use Dart for Dart packages, command-line tools, and Flutter applications. Use
Flutter only when the project is already Flutter or the user asks for it.

## Runtime And Package Management

- Use stable Dart, currently `3.12.0`.
- Preserve `pubspec.yaml`, lockfiles, and existing package layout.
- Keep Flutter SDK requirements separate from plain Dart requirements.

## Tooling

```sh
dart --version
dart pub get
dart format .
dart analyze
dart test
```

## Generation Rules

Prefer strong types, immutable data where practical, null-safety, and explicit
async error handling. Keep widgets small in Flutter and separate UI from domain
logic.

## Source Documentation And Comments

Use Dart documentation comments (`///`) for public libraries, classes, methods,
widgets, and package APIs. Document async behavior, thrown exceptions, state
ownership, and widget responsibilities. Use inline comments for non-obvious
layout, platform, and lifecycle decisions; avoid comments that restate code.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Project Discovery And Structure

Before generating Dart, inspect `pubspec.yaml`, SDK constraints, package layout,
Flutter usage, state management, routing, tests, and analyzer settings. Preserve
library boundaries, widget structure, and generated-code conventions.

## Design Patterns And Architecture

Prefer immutable models, small widgets, services, repositories at I/O
boundaries, and framework-native state patterns. Use Provider, Bloc, Riverpod,
or MVVM only when the project already uses them or the complexity warrants it.
Avoid rebuilding large widget trees unnecessarily.
## Algorithmic Complexity And Dynamic Programming

Document complexity for collection transforms, isolates, and UI-facing data
flows. Prefer `O(n)` passes, maps/sets, lazy iterables, and indexed lookups over
nested scans. Use dynamic programming only with clear state, transitions, base
cases, and memory bounds. Keep expensive work out of Flutter build methods and
measure before adding complex caching.

## Senior Architecture Decisions

In Flutter or Dart clients, prefer local state, repositories, offline cache, and
bounded background work before adding distributed patterns. Use queues on the
server side or through platform services for durable background processing.
Document cache invalidation, retry policy, cancellation, telemetry, and
idempotency for sync flows and external API calls.

## Concurrency Parallelism And Hardware Acceleration

Use async/await for I/O and isolates for CPU-bound work that would block the UI or event loop. Keep isolate messages small enough that transfer overhead is worth it. In Flutter, keep build methods cheap and move heavy work off the UI isolate. Use GPU through Flutter rendering or specialized plugins only when profiling shows CPU rendering or compute is the bottleneck.


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
