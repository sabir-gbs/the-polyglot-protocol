# C Sharp

Use C# for .NET applications, services, libraries, tools, Unity projects, or
repositories that already use the .NET ecosystem.

## Runtime And Project Management

- Use current .NET LTS, currently `.NET 10.0.8`, unless the project targets a
  specific supported runtime.
- Preserve solution layout, project files, and package management conventions.
- Enable nullable reference types for new projects.

## Tooling

```sh
dotnet --info
dotnet restore
dotnet format
dotnet test
```

## Generation Rules

Use async APIs correctly, propagate cancellation tokens, keep public contracts
stable, and avoid reflection-heavy or dynamic code unless justified. Use
structured logging and dependency injection only where the project already does.

## Source Documentation And Comments

Use XML documentation comments for public classes, methods, records,
properties, events, and library APIs. Document cancellation behavior, exceptions,
nullability, threading, and side effects. Use inline comments for intent,
workarounds, and non-obvious framework behavior; avoid repeating method names.

## Project Discovery And Structure

Before generating C#, inspect the solution, project files, target framework,
nullable settings, analyzers, dependency injection setup, tests, and package
versions. Preserve namespaces, layering, async conventions, and public contracts.

## Design Patterns And Architecture

Use dependency injection, Options, Repository, Mediator, or CQRS only when the
project already benefits from those boundaries. Prefer records, interfaces,
small services, and async methods with cancellation. Avoid reflection-heavy,
container-driven, or inheritance-heavy designs in simple code.
## Algorithmic Complexity And Dynamic Programming

Document complexity for non-trivial LINQ, collection, and async pipelines.
Prefer `O(n)` passes, dictionaries, hash sets, spans, streaming, and indexed
queries over repeated enumeration. Use dynamic programming only when overlapping
subproblems exist; define state and memory use. Avoid hidden multiple
enumerations and allocation-heavy LINQ in hot paths.

## Senior Architecture Decisions

Use built-in .NET hosting, background services, channels, queues, and dependency
injection only where they create clear boundaries. Message queues need
idempotent handlers, retry limits, poison-message handling, correlation IDs,
metrics, and health checks. Prefer database transactions or synchronous calls
when they are simpler and meet latency/reliability needs.

## Concurrency Parallelism And Hardware Acceleration

Use `async`/`await` for I/O-bound work and avoid blocking thread-pool threads. Use `Parallel`, channels, background services, or dedicated workers for measured CPU-bound work with bounded concurrency and cancellation tokens. Use GPU libraries only for large numeric, image, or ML workloads. Track queue length, latency, exceptions, cancellation, and resource saturation.


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
