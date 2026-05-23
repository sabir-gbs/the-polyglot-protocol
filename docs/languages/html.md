# HTML

Use HTML for document structure and accessible user interface semantics. Pair it
with CSS for presentation and JavaScript or TypeScript only for behavior that
cannot be handled declaratively.

## Standards

- Follow WHATWG HTML living standards and the project's browser matrix.
- Use semantic elements before generic `div` or `span`.
- Keep forms, buttons, labels, headings, and landmarks accessible.

## Tooling

```sh
npm run lint
npm run build
```

## Generation Rules

Keep heading order logical, controls keyboard-operable, images described when
meaningful, and form errors tied to inputs. Avoid inline event handlers and
layout tables unless the content is truly tabular.

## Source Documentation And Comments

Use HTML comments sparingly for template boundaries, server-rendered insertion
points, accessibility rationale, and integration hooks. Do not leave large
commented-out markup. Avoid comments that duplicate visible text or describe
obvious element names.

## Project Discovery And Structure

Before generating HTML, inspect templates, components, routing, server-rendering
or static-generation conventions, accessibility patterns, and browser support.
Preserve semantic structure, naming conventions, partials/includes, and existing
data attributes used by scripts or tests.

## Design Patterns And Architecture

Use semantic composition, reusable partials/components, progressive enhancement,
and accessible landmarks. Avoid div-heavy component patterns, hidden behavior
hooks without documentation, and markup structures that force expensive CSS or
JavaScript work.
## Algorithmic Complexity And Dynamic Programming

HTML does not implement dynamic programming. Reduce runtime complexity by
keeping markup semantic, shallow enough for maintainable styling, and compatible
with progressive enhancement. Avoid repeated duplicate markup that forces
quadratic JavaScript traversal or expensive CSS selectors. Use data attributes
only when they support clear, indexed behavior.

## Senior Architecture Decisions

HTML should express document structure, not distributed architecture. Keep async
behavior, queues, caching, and retries in the application layer. Use semantic
markup that supports progressive enhancement, observability hooks such as stable
data attributes, and accessible loading/error states without duplicating state
machines in markup.

## Concurrency Parallelism And Hardware Acceleration

HTML has no threads or GPU execution model. Design markup so browser rendering can stay efficient: semantic structure, lazy loading, responsive media, and minimal DOM depth. Use attributes that support JavaScript workers or GPU-backed rendering cleanly, but keep concurrency decisions in JavaScript/TypeScript and rendering decisions in CSS/canvas/WebGL layers.


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
