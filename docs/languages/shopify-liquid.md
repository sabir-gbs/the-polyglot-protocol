# Shopify Liquid

Use Shopify Liquid for Shopify themes, sections, snippets, templates, and
storefront presentation. Use Python for operational scripts unless the theme
already uses a documented Node workflow.

## Project Structure

- Preserve `layout/`, `templates/`, `sections/`, `snippets/`, `assets/`,
  `config/`, and `locales/`.
- Use JSON templates where the theme already does.
- Keep Liquid, schema JSON, CSS, and JavaScript responsibilities separate.

## Tooling

```sh
shopify version
shopify theme check
shopify theme dev
```

## Generation Rules

Use Shopify objects and filters as documented. Escape output, avoid expensive
loops, keep section settings clear, and do not hardcode shop-specific data.
Preserve merchant-editable schema settings.

## Source Documentation And Comments

Use Liquid comments for section intent, merchant-facing assumptions, performance
tradeoffs, and theme integration boundaries. Document schema settings with clear
labels and info text. Avoid leaving commented-out markup or comments that expose
internal notes to rendered HTML.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Project Discovery And Structure

Before generating Liquid, inspect theme structure, JSON templates, sections,
snippets, settings schema, locales, assets, and Shopify app integration points.
Preserve merchant-editable settings, snippet boundaries, and existing naming.

## Design Patterns And Architecture

Use sections for merchant-configurable page blocks, snippets for reusable
rendering, and assets for behavior/presentation. Avoid nested loops, generic
snippet indirection, and app-like architecture in Liquid when simple theme
composition is faster and clearer.
## Algorithmic Complexity And Dynamic Programming

Do not implement dynamic programming in Liquid. Keep rendering loops bounded and
linear over Shopify-provided collections. Avoid nested product, variant, or
collection loops when precomputed metafields, settings, or Shopify objects can
provide direct access. Move complex computation to apps, build tooling, or
Python automation.

## Senior Architecture Decisions

Liquid themes should not implement queueing, background processing, or complex
application workflows. Use Shopify platform features, app backends, metafields,
webhooks, and build-time Python automation for durable processing. Keep theme
code focused on rendering, merchant settings, performance, and graceful fallback
when app-provided data is missing.

## Concurrency Parallelism And Hardware Acceleration

Liquid has no threading, CPU parallelism, or GPU execution model. Keep theme rendering bounded and fast. Move concurrent processing, imports, queue workers, image generation, and heavy computation to Shopify apps, platform services, or Python build automation. Do not simulate concurrency with nested snippets or large render loops.


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
