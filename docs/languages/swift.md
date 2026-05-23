# Swift

Use Swift for iOS, macOS, watchOS, tvOS, Swift packages, and repositories that
already use Swift.

## Runtime And Package Management

- Use the current stable Swift or Xcode toolchain verified from swift.org or
  Xcode release notes.
- Use Swift Package Manager unless the project uses Xcode projects, CocoaPods,
  or another existing setup.
- Preserve deployment target constraints.

## Tooling

```sh
swift --version
swift format
swift test
xcodebuild test
```

## Generation Rules

Prefer value types, explicit access control, structured concurrency, and clear
error handling. Keep UI code accessible and separate business logic from views.

## Source Documentation And Comments

Use Swift documentation comments for public types, protocols, functions,
properties, packages, and framework APIs. Document actor isolation, async
behavior, errors, platform availability, and UI accessibility assumptions. Use
inline comments for intent, lifecycle, and platform workarounds only.

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

Before generating Swift, inspect package or Xcode project settings, deployment
targets, platform frameworks, concurrency model, tests, and UI architecture.
Preserve module boundaries, access control, naming, and platform availability.

## Design Patterns And Architecture

Prefer value types, protocols, extensions, actors, and SwiftUI or UIKit-native
patterns. Use MVVM, Coordinator, Adapter, or Repository only when they match the
project and improve boundaries. Avoid reference-heavy or protocol-heavy designs
in performance-sensitive code.
## Algorithmic Complexity And Dynamic Programming

Document complexity for collection transforms, UI state updates, and async
pipelines. Prefer `O(n)` passes, dictionaries/sets, lazy sequences, and
precomputed indexes over nested scans. Use dynamic programming only when state
and recurrence are clear, memory is bounded, and UI responsiveness is protected.
Benchmark hot paths and avoid copy-on-write surprises.

## Senior Architecture Decisions

For Apple clients, keep durable queueing on the server or platform background
task APIs. Use local caches, operation queues, async sequences, and actors with
cancellation, bounded work, and clear UI state. Document sync conflict handling,
retry policy, telemetry, and idempotency for network mutations.

## Concurrency Parallelism And Hardware Acceleration

Use Swift concurrency, actors, tasks, and operation queues with cancellation and main-actor boundaries. Keep UI work on the main actor and CPU-heavy work off it. Use Metal, Accelerate, Core ML, or GPU-backed frameworks only when profiling shows large numeric, image, ML, or rendering workloads benefit. Protect battery, thermal limits, and memory.


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
