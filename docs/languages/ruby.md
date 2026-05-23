# Ruby

Use Ruby for Rails, gems, automation inside Ruby repositories, and projects that
already use Ruby. Prefer Python for cross-repository operational scripts unless
Ruby is the documented project automation path.

## Runtime And Dependency Management

- Use stable Ruby, currently `3.4.9`, unless the project pins another version.
- Use Bundler and preserve `Gemfile.lock`.
- Follow Rails conventions in Rails applications.

## Tooling

```sh
ruby -v
bundle install
bundle exec rubocop
bundle exec rspec
```

## Generation Rules

Keep public APIs small, avoid monkey patches unless the project already uses
them deliberately, validate inputs, and keep database queries parameterized.

## Source Documentation And Comments

Use YARD-style documentation for public library APIs, gems, service objects,
callbacks, and non-obvious blocks. Document parameters, return values,
exceptions, side effects, and Rails callbacks or metaprogramming. Use comments
for intent and framework workarounds; avoid restating method names.

## Project Discovery And Structure

Before generating Ruby, inspect `Gemfile`, lockfile, Rails or gem structure,
autoloading, style config, tests, and database conventions. Preserve Rails
conventions, public APIs, service boundaries, and existing metaprogramming style.

## Design Patterns And Architecture

Prefer plain objects, modules, service objects, query objects, and framework
conventions. Use Strategy, Adapter, Decorator, or Form Object only when they
clarify a real boundary. Avoid excessive metaprogramming and pattern-heavy code
that hides control flow.
## Algorithmic Complexity And Dynamic Programming

Document complexity for enumerable chains, database access, and background jobs.
Prefer `O(n)` passes, hashes/sets, preloading, indexed queries, and bulk
operations over nested loops or N+1 queries. Use dynamic programming only when
state and recurrence are clear and memory is bounded. Avoid allocation-heavy
blocks in hot paths.

## Senior Architecture Decisions

In Rails and Ruby services, use framework job systems and queues for email,
webhooks, imports, fan-out, and retryable integrations. Jobs must be idempotent,
bounded, observable, and safe under duplicate delivery. Prefer transactions and
synchronous service objects when simpler. Avoid callbacks that hide queueing or
cross-service side effects.

## Concurrency Parallelism And Hardware Acceleration

In MRI Ruby, threads help I/O but not CPU-bound Ruby code due to the GVL. Use background jobs, processes, or native extensions for CPU-bound work. Bound job concurrency and database connections. GPU work belongs in external services or native libraries. Add timeouts, idempotency, and observability for all concurrent jobs.


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
