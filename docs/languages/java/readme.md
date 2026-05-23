# Java Codegen Decisions

Purpose: JVM services, libraries, and enterprise applications.

Use this README as the human-readable summary for `java.md`. The full rules live in `../java.md`.

## Quality Controls

- Inspect the existing repository structure, toolchain, tests, and conventions before generating code.
- Preserve the project's language style, package manager, formatter, and test runner.
- Use native documentation, validation, and error-handling conventions for Java.
- Add only justified dependencies and verify current stable versions from official or primary sources.

## Completeness Controls

- Update code, tests, docs, configuration, exports, and packaging together when the change requires it.
- Cover source documentation, project structure, design patterns, algorithmic complexity, senior architecture decisions, concurrency, and final guardrails.
- Include rollback, migration, compatibility, and `N/A` notes when a workflow step does not apply.

## Accuracy Controls

- Do not invent APIs, flags, package names, runtime behavior, or framework conventions.
- Verify claims against local files or official documentation.
- Prefer the shortest reliable supported path before adding infrastructure or abstraction.
- Run `python scripts/validate-workspace.py` from the project root after guidance changes.

## Read Next

- Full language guide: `../java.md`
- Decision matrix: `../decision-matrix.md`
- Hard stops: `../do-not-generate-policy.md`
- LLM guardrails: `../top-llm-coding-nuances.md`
