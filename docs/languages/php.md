# PHP

Use PHP for WordPress, Laravel, Symfony, Composer packages, and repositories
that already use PHP. Use Python for operational scripts unless the project has
documented PHP automation.

## Runtime And Package Management

- Use supported PHP releases; latest verified release is `8.5.6`.
- Use Composer and preserve `composer.lock`.
- Follow WordPress Coding Standards in WordPress projects.

## Tooling

```sh
php -v
composer install
composer test
vendor/bin/phpunit
vendor/bin/phpcs
```

## Generation Rules

Use strict types when compatible, parameterized database access, escaped output,
nonce/capability checks in WordPress, and explicit validation for request data.
Never interpolate untrusted input into SQL, shell commands, or HTML.

## Source Documentation And Comments

Use PHPDoc for public classes, functions, methods, hooks, filters, complex array
shapes, and APIs where native types are insufficient. In WordPress, document
hook names, expected arguments, capability checks, and escaping assumptions. Use
comments for security-sensitive behavior; avoid restating obvious PHP syntax.

## Project Discovery And Structure

Before generating PHP, inspect `composer.json`, framework or WordPress
structure, autoloading, coding standards, tests, hooks, database access, and
template conventions. Preserve namespaces, plugin/theme layout, service
registration, and escaping/validation patterns.

## Design Patterns And Architecture

Use framework-native controllers, services, middleware, events, and dependency
injection where present. In WordPress, prefer hooks, small service classes, and
clear capability boundaries. Avoid generic enterprise patterns when procedural
theme or plugin conventions are clearer and faster.
## Algorithmic Complexity And Dynamic Programming

Document complexity for collection processing, database loops, and request
handlers. Prefer `O(n)` passes, associative-array indexes, database indexes, and
bulk queries over nested PHP loops or N+1 queries. Use dynamic programming only
for real overlapping subproblems and keep memory bounded for web requests.
Explain unavoidable non-linear work.

## Senior Architecture Decisions

For WordPress and PHP apps, prefer platform hooks, cron, framework jobs, and
database transactions before adding brokers. Use queues for slow email, media,
webhooks, imports, and retryable integrations. Consumers must be idempotent,
bounded, observable, and protected from duplicate delivery. Avoid long work in
web requests and prevent N+1 database behavior.

## Concurrency Parallelism And Hardware Acceleration

Keep web requests short and avoid manual threading in PHP. Use queues, cron, framework workers, or process managers for background and parallel work. Bound worker concurrency and make jobs idempotent. Use database and cache concurrency controls explicitly. GPU work should run in external services or CLI workers, not ordinary request handlers.


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
