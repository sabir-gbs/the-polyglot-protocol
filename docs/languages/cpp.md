# C++

Use C++ for performance-sensitive systems, native libraries, engines, and
projects that already use C++. Prefer Python for operational scripts around C++
projects.

## Standard And Toolchain

- Use C++23 for new code when supported; otherwise preserve the project standard.
- Prefer CMake or Meson when the project has no build system.
- Use RAII and standard library facilities before custom resource management.

## Tooling

```sh
c++ --version
cmake --build build
ctest --test-dir build
clang-format -i path/to/file.cpp
clang-tidy path/to/file.cpp
```

## Generation Rules

Avoid owning raw pointers, unchecked casts, hidden global state, and manual
memory management unless required. Use sanitizers and tests for concurrency,
lifetime, parsing, and boundary-heavy changes.

## Source Documentation And Comments

Document public APIs, templates with non-obvious constraints, ownership,
lifetime, exception guarantees, threading guarantees, and ABI expectations. Use
comments for invariants, synchronization, custom allocators, and unsafe casts.
Avoid comments that duplicate type names or obvious RAII behavior.

## Test-First Red Green Refactor

For bug fixes and behavior changes, write or identify a failing test first, make
the smallest change to pass, then refactor with tests green. If a test cannot be
added, document the manual verification and why automated coverage is not
practical.

## Project Discovery And Structure

Before generating C++, inspect build files, standard level, compiler flags,
namespaces, tests, public headers, ABI constraints, allocator conventions, and
threading model. Preserve module/header layout, ownership style, and existing
library choices.

## Design Patterns And Architecture

Prefer RAII, value types, templates, composition, and standard library
algorithms. Use Strategy, Adapter, Builder, or Factory when they simplify
variation or isolate dependencies. Avoid inheritance-heavy designs, heap
allocation, type erasure, and virtual dispatch in performance-sensitive paths
unless justified.
## Algorithmic Complexity And Dynamic Programming

State complexity for algorithms and container choices. Prefer `O(n)` traversal,
standard algorithms, hash maps/sets, sorted vectors, and cache-friendly storage
over nested scans. Use dynamic programming only for overlapping subproblems;
define state, transition, base cases, and memory layout. Avoid heap churn and
virtual dispatch in hot DP or graph loops unless measured.

## Senior Architecture Decisions

Use queues, thread pools, actors, or event loops only when they simplify
concurrency and provide bounded memory, backpressure, cancellation, and graceful
shutdown. Prefer proven libraries over custom brokers. Document ownership,
thread-safety, retry behavior, metrics, and failure recovery. Avoid architecture
that hides allocations or contention in hot paths.

## Concurrency Parallelism And Hardware Acceleration

Use `std::jthread`, futures, thread pools, atomics, and coroutines only with clear ownership, cancellation, synchronization, and lifetime rules. Prefer data-parallel algorithms or SIMD for CPU-bound work after profiling. Use CUDA, HIP/SYCL, Vulkan compute, or other GPU paths only for large parallel workloads where transfer cost is measured. Test races and shutdown paths.


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
