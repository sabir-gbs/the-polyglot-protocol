# TypeScript

Use TypeScript for new JavaScript-family product code unless the existing
project is JavaScript-only. `typescript/typescript.md` is the authoritative deep
guide.

## Runtime And Package Management

- Target Node.js Active LTS `24.16.0` for server, CLI, build, and test code.
- Use the package manager implied by the lockfile.
- Prefer ESM for new projects.
- Pin dependencies through the lockfile and avoid global installs.

## Tooling

```sh
node --version
npm --version
npm ci
npm run typecheck
npm run lint
npm test
```

## Generation Rules

Enable strict TypeScript. Avoid `any`, unchecked casts, implicit globals, and
runtime behavior hidden by unnecessary transpilation. Preserve framework
patterns, workspace boundaries, and existing test runners.

## Source Documentation And Comments

Use TSDoc for exported functions, classes, types, hooks, components, and public
package APIs. Document runtime contracts, generic constraints, side effects,
thrown errors, and compatibility assumptions. Use comments for non-obvious
state transitions, browser/platform workarounds, and security decisions; avoid
comments that repeat names or obvious control flow.

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

Before generating code, inspect `package.json`, lockfile, `tsconfig.json`,
framework config, source layout, tests, and existing import style. Preserve the
package manager, workspace boundaries, routing conventions, component model,
state management, and public exports.

## Design Patterns And Architecture

Prefer typed functions, small modules, composition, discriminated unions, and
framework-native patterns. Use Adapter for external APIs, Strategy for
replaceable behavior, Factory for complex object creation, and Repository only
when a data boundary already exists. Avoid class-heavy patterns in UI code
unless the framework requires them.
## Algorithmic Complexity And Dynamic Programming

For non-trivial data transforms, document time and space complexity. Prefer
`O(n)` array passes, `Map`/`Set`, indexed records, streaming, or memoized pure
functions over repeated scans. Use dynamic programming only when repeated
subproblems exist; type the state, transition, and result shape. Avoid quadratic
work in render paths, reducers, request handlers, and browser interactions.

## Senior Architecture Decisions

In browser code, avoid distributed architecture inside the client; use
framework-native state, cache, and data-fetching patterns. In Node.js services,
use queues for slow tasks, webhooks, fan-out, and retryable external calls.
Require idempotency keys, retry limits, dead-letter handling, observability, and
backpressure. Do not add CQRS, event sourcing, or brokers when a transaction or
single service call is enough.

## Concurrency Parallelism And Hardware Acceleration

Use async I/O for network and filesystem work. In Node.js, use worker threads or separate services for CPU-bound work only after profiling. In browsers, use Web Workers for CPU-heavy work and WebGL/WebGPU only for graphics, ML, or large data parallelism where transfer cost is justified. Require cancellation, backpressure, and avoid blocking render or event loops.


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
