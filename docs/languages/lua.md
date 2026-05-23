# Lua

Use Lua for embedded scripting, Neovim plugins, game engines, or repositories
that already use Lua. Use the host application's Lua version when embedded.

## Runtime

- Use stable Lua, currently `5.5.0`, for standalone new code.
- Preserve LuaJIT or host-pinned versions when the runtime embeds Lua.
- Avoid globals unless the host API requires them.

## Tooling

```sh
lua -v
stylua .
busted
```

## Generation Rules

Keep modules explicit, validate table shapes at boundaries, avoid mutating
shared tables unexpectedly, and document host APIs. Use local variables by
default and tests for parser or configuration behavior.

## Source Documentation And Comments

Document module purpose, host application APIs, table shapes, expected globals,
and side effects. Use EmmyLua-style annotations when the project supports them.
Comment metatables, coroutine behavior, mutation of shared tables, and embedded
runtime assumptions; avoid comments that restate simple assignments.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Project Discovery And Structure

Before generating Lua, inspect host runtime, Lua/LuaJIT version, module loader,
plugin structure, global API, formatter, tests, and performance constraints.
Preserve module return style, table conventions, and host lifecycle hooks.

## Design Patterns And Architecture

Use tables, closures, metatables, and small modules as the primary architecture.
Use Prototype or Adapter patterns only when they match host APIs. Avoid class
frameworks, deep metatable chains, and allocation-heavy abstractions in tight
loops.
## Algorithmic Complexity And Dynamic Programming

State complexity for table-heavy algorithms. Prefer `O(n)` table iteration,
lookup tables, and precomputed state over nested loops. Use dynamic programming
only when table state remains bounded and the host runtime can tolerate the
memory. Avoid allocation-heavy closures, metatable dispatch, and string
concatenation in tight loops.

## Senior Architecture Decisions

Respect the host application's architecture. Do not invent brokers, schedulers,
or queue systems inside embedded Lua unless the host provides that extension
point. Use host events, timers, and callbacks with bounded work, clear cleanup,
and idempotent handlers. Move durable background processing to the host service
or an external system.

## Concurrency Parallelism And Hardware Acceleration

Follow the host runtime. Lua coroutines are cooperative, not CPU parallelism. Use host-provided threads, jobs, timers, or async APIs instead of inventing concurrency primitives. Keep callbacks short and bounded. Use GPU only through the host engine or native extensions, and only for workloads the host is built to accelerate.


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
