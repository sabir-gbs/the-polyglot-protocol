# Java

Use Java for JVM services, Android-adjacent libraries, enterprise systems, and
repositories that already use Java.

## Runtime And Build

- Use the project's configured JDK. For new server projects, prefer current LTS
  JDK verified from the chosen vendor or distro source.
- Use the existing Maven or Gradle wrapper.
- Preserve package naming and module boundaries.

## Tooling

```sh
java -version
./mvnw test
./gradlew test
```

## Generation Rules

Use immutable values where practical, validate boundaries, avoid shared mutable
state, and keep exceptions meaningful. Use JUnit and the project's formatter or
Spotless/Checkstyle setup.

## Source Documentation And Comments

Use Javadoc for public classes, interfaces, records, methods, constructors, and
library APIs. Document parameters, return values, exceptions, thread-safety,
nullability, and compatibility contracts. Use inline comments for invariants,
workarounds, and complex algorithms; avoid restating obvious code.

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

Before generating Java, inspect Maven/Gradle files, JDK target, package layout,
framework conventions, dependency injection setup, tests, and static analysis.
Preserve package boundaries, public APIs, annotations, and exception style.

## Design Patterns And Architecture

Use patterns when they clarify boundaries: Builder for complex immutable
objects, Strategy for replaceable behavior, Adapter for external systems, and
Factory for controlled creation. Avoid abstract factories, deep inheritance, and
layering that adds allocations or indirection without need.
## Algorithmic Complexity And Dynamic Programming

Document complexity for algorithms, streams, and collection choices. Prefer
`O(n)` iteration, maps/sets, indexed queries, and primitive arrays in hot paths
over nested scans or boxing-heavy streams. Use dynamic programming only when
state, transition, base cases, and memory limits are clear. Avoid hidden
quadratic behavior in service and batch jobs.

## Senior Architecture Decisions

Use message queues, schedulers, transactions, caches, and dependency injection
only when they match service boundaries and operational needs. Queue consumers
need idempotency, bounded retries, dead-letter queues, correlation IDs, metrics,
and backpressure. Avoid event sourcing, CQRS, or distributed transactions unless
the domain and consistency model require them.

## Concurrency Parallelism And Hardware Acceleration

Use virtual threads or async APIs for high-concurrency I/O when the target JDK supports them. Use bounded executors, structured concurrency, and cancellation for parallel work. Use parallel streams only after profiling and only when splitting overhead is justified. Use GPU/accelerator libraries for large numeric or ML workloads with measured transfer costs and operational support.


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
