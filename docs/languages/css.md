# CSS

Use CSS for presentation, layout, responsive behavior, animations, and design
system implementation. Keep behavior in HTML or JavaScript only when CSS cannot
express it reliably.

## Standards And Browser Support

- Follow the project's browser support matrix.
- Use modern CSS when supported by the matrix.
- Preserve existing methodology such as BEM, CSS modules, Tailwind, or scoped
  component styles.

## Tooling

```sh
npm run lint
npm run build
```

## Generation Rules

Use semantic class names, responsive constraints, accessible focus states, and
stable sizing for fixed-format controls. Avoid one-off color drift, layout
overlap, excessive specificity, and viewport-scaled font sizes.

## Source Documentation And Comments

Comment design tokens, layout constraints, browser workarounds, accessibility
requirements, and intentional specificity. Group related rules with clear
section comments only when the stylesheet is large enough to benefit. Do not add
comments that simply restate selectors or property names.

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

## Best Practice Examples

- Bad: fix layout with hard-coded pixel offsets. Good: use semantic structure,
  flex/grid, responsive constraints, and tested breakpoints.
- Bad: duplicate color and spacing values everywhere. Good: use existing design
  tokens or scoped custom properties with clear fallback behavior.
- Bad: hide content visually without accessibility intent. Good: preserve
  readable contrast, focus states, reduced-motion support, and text flow.

## Project Discovery And Structure

Before generating CSS, inspect existing styling approach, tokens, breakpoints,
component boundaries, browser matrix, reset/base styles, and build pipeline.
Preserve naming conventions, cascade layers, utility systems, and design-system
variables.

## Design Patterns And Architecture

Use design tokens, component-scoped styles, cascade layers, and utility classes
only when they match the project. Prefer simple selectors and low specificity.
Avoid abstract class systems, deep nesting, and animation/layout techniques that
hurt rendering performance.
## Algorithmic Complexity And Dynamic Programming

CSS does not use dynamic programming. Treat performance in terms of selector
matching, layout, paint, and animation cost. Prefer simple selectors, contained
layouts, transform/opacity animations, and stable dimensions. Avoid deeply
nested selectors, layout thrashing triggers, and rules that require excessive
DOM structure to remain performant.

## Senior Architecture Decisions

CSS architecture should stay within design-system boundaries: tokens,
components, cascade layers, and predictable overrides. Do not encode application
state machines or queue-like behavior in CSS. For complex state, use semantic
HTML and the project's JavaScript/TypeScript state model. Avoid styling systems
that require excessive DOM or runtime class churn.

## Concurrency Parallelism And Hardware Acceleration

CSS has no application threads or dynamic programming. Treat GPU use as browser compositing: prefer transform and opacity animations, avoid layout-triggering animations, and use `will-change` sparingly. Keep selectors and DOM dependencies simple so the browser can parallelize style, layout, paint, and compositing efficiently.


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
