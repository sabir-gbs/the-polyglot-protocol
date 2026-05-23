# Bash

Use Bash only for thin local glue, shell startup snippets, or commands that must
run directly in a POSIX-like shell. Prefer Python for reusable, cross-platform,
or complex automation.

## Runtime

- Verify Bash when Bash-specific features are used.
- Do not assume GNU tools on macOS.
- Do not use Bash for Windows-native automation unless explicitly required.

## Tooling

```sh
bash --version
shellcheck script-name.sh
```

## Generation Rules

Start scripts with `set -euo pipefail`. Quote expansions, check command
availability, avoid parsing `ls`, use arrays for argument lists, and keep sudo
commands explicit. Add a dry-run mode for destructive or bulk operations.

## Source Documentation And Comments

Document script purpose, required environment variables, external commands,
privilege requirements, and destructive side effects at the top of reusable
scripts. Comment non-obvious quoting, traps, subshells, sudo boundaries, and
platform-specific behavior. Avoid comments that merely translate a command name.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Project Discovery And Structure

Before generating shell code, inspect existing scripts, shebangs, ShellCheck
config, Makefiles, task runners, and supported platforms. Keep reusable logic in
Python when it grows beyond simple command orchestration. Place scripts where the
repo already keeps automation and document required environment variables.

## Design Patterns And Architecture

Avoid design-pattern abstractions in Bash. Use small functions, clear command
pipelines, explicit cleanup traps, and argument parsing. For state machines,
complex parsing, retries, or cross-platform logic, switch to Python instead of
building a Bash framework.
## Algorithmic Complexity And Dynamic Programming

Do not implement dynamic programming or complex algorithms in Bash. Keep shell
work linear over files or arguments when possible. Avoid nested command
substitution loops, repeated process spawning inside large loops, and parsing
large data with shell text tricks. Move non-trivial `O(n)`, indexing, or dynamic
programming work to Python.

## Senior Architecture Decisions

Do not build queueing, orchestration, retries, or distributed workflows in Bash.
Use Bash only to invoke well-defined tools. For background jobs, scheduling,
state tracking, backpressure, or idempotent processing, use Python or an
existing scheduler/queue system. Keep shell scripts restartable and safe to run
twice.

## Concurrency Parallelism And Hardware Acceleration

Avoid complex concurrency in Bash. Use `xargs -P`, `parallel`, or background jobs only for simple independent commands with bounded parallelism and clear failure handling. Do not manage GPU work directly in shell beyond invoking tested tools. For coordination, retries, queues, or shared state, use Python or the platform scheduler.


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
