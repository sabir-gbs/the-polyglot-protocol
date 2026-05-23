# Kotlin

Use Kotlin for Android, JVM services, Gradle plugins, Kotlin Multiplatform, and
repositories that already use Kotlin.

## Runtime And Build

- Use stable Kotlin, currently `2.3.21`, unless the project pins another version.
- Use the existing Gradle or Maven wrapper.
- For Android, follow Android Gradle Plugin and SDK constraints exactly.

## Tooling

```sh
./gradlew test
./gradlew ktlintCheck
./gradlew detekt
```

## Generation Rules

Prefer null-safe APIs, immutable data, sealed types for closed states, and
coroutines with structured concurrency. Avoid platform types leaking across
boundaries and keep Android UI code separated from domain logic.

## Source Documentation And Comments

Use KDoc for public classes, functions, properties, sealed hierarchies, and
library APIs. Document coroutine behavior, nullability, threading, lifecycle,
and Android platform assumptions. Use inline comments for non-obvious state,
interop, and lifecycle decisions; avoid comments that repeat signatures.

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

- Bad: use nullable values as hidden control flow. Good: model absence and
  failures with sealed classes, result types, or explicit validation.
- Bad: launch coroutines without lifecycle ownership. Good: use structured
  concurrency, cancellation, and dispatcher boundaries.
- Bad: put platform calls in business logic. Good: isolate Android/JVM services
  behind interfaces and test domain logic without platform state.

## Project Discovery And Structure

Before generating Kotlin, inspect Gradle/Maven config, Kotlin version, JVM or
Android target, package layout, coroutine usage, state management, tests, and
lint rules. Preserve existing architecture, module boundaries, and Java
interop constraints.

## Design Patterns And Architecture

Prefer data classes, sealed types, extension functions, composition, and
coroutine scopes. Use Repository, Use Case, MVVM, or Adapter where the project
already has those boundaries. Avoid over-layering small features or adding
patterns that increase allocations on Android hot paths.
## Algorithmic Complexity And Dynamic Programming

Document complexity for collection chains, coroutines, and UI state transforms.
Prefer `O(n)` passes, maps/sets, sequences where they reduce intermediate
allocations, and indexed lookups over nested scans. Use dynamic programming only
with explicit state and memory bounds. Avoid allocation-heavy chains in Android
rendering or hot coroutine paths.

## Senior Architecture Decisions

For Android, keep queues and durable background work in WorkManager or platform
services, with cancellation, retry, network constraints, and idempotency. For
JVM services, follow Java service guidance for queues, caches, transactions, and
observability. Avoid over-layered clean architecture when a simple ViewModel,
repository, or service boundary is sufficient.

## Concurrency Parallelism And Hardware Acceleration

Use coroutines for asynchronous I/O and structured concurrency. On Android, avoid blocking the main thread and use WorkManager for deferrable durable work. Use dispatchers or worker pools for CPU-bound tasks with bounded parallelism. Use GPU through platform rendering, ML, or graphics APIs only when measured benefits justify complexity and battery cost.


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
