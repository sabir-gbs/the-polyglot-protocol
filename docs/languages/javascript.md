# JavaScript

Use JavaScript only when the project is already JavaScript-only, the runtime
requires it, or the user explicitly requests it. Prefer TypeScript for new
JavaScript-family code.

## Runtime And Package Management

- Target Node.js Active LTS `24.16.0` for server, CLI, and tooling code.
- Preserve the existing package manager and module system.
- Use ESM for new standalone JavaScript unless CommonJS is required.

## Tooling

```sh
node --version
npm --version
npm ci
npm run lint
npm test
```

## Generation Rules

Use JSDoc types when TypeScript is not available. Avoid implicit globals,
prototype mutation, unhandled promises, and dynamic `eval`-style code. Keep
browser code compatible with the declared browser matrix.

## Source Documentation And Comments

Use JSDoc for exported APIs, complex callbacks, event payloads, and JavaScript
that lacks TypeScript type coverage. Document browser assumptions, async error
behavior, side effects, and public contracts. Use inline comments for intent,
workarounds, and security-sensitive behavior; do not narrate obvious statements.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Project Discovery And Structure

Before generating code, inspect `package.json`, lockfile, module type, bundler
or runtime config, lint rules, test runner, and browser support. Preserve
CommonJS versus ESM, existing folder layout, event conventions, and dependency
style.

## Design Patterns And Architecture

Prefer plain functions, modules, closures, and object literals before classes.
Use Adapter for browser/runtime differences, Strategy for replaceable behavior,
and Pub/Sub only when event-driven code already exists. Avoid patterns that hide
control flow or add allocation overhead in hot browser paths.
## Algorithmic Complexity And Dynamic Programming

Document complexity for non-trivial loops, transforms, and request handlers.
Prefer `O(n)` passes, `Map`/`Set`, object indexes, streaming, or precomputed
lookups over nested scans. Use memoization or dynamic programming only when
inputs repeat overlapping subproblems. Avoid hidden quadratic behavior in DOM
updates, rendering, event handlers, and hot Node.js paths.

## Senior Architecture Decisions

For browser JavaScript, keep architecture local: progressive enhancement,
bounded state, request cancellation, and cache invalidation. For Node.js, use
message queues only for background work, fan-out, retries, or decoupling that a
synchronous path cannot handle. Require idempotent consumers, bounded retries,
dead-letter paths, metrics, and clear ownership of each event.

## Concurrency Parallelism And Hardware Acceleration

Use promises and async I/O for waiting work, not CPU parallelism. Use Node worker threads, child processes, or Web Workers only for measured CPU-heavy tasks. Use WebGL/WebGPU for graphics, ML, or large data workloads only when data transfer and browser support are acceptable. Keep event loops responsive and add cancellation, backpressure, and timeout handling.


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
