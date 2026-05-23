# Top LLM Coding Nuances

This document applies to the user-provided top coding LLM set. Do not depend on
model rankings or marketing claims; apply these failure-mode guardrails to every
model.

## Common Failure Modes

- **Invented APIs**: verify package names, function signatures, flags,
  configuration keys, and cloud services against local code or official docs.
- **Skipped repository discovery**: inspect source layout, lockfiles, tests,
  configs, and existing conventions before generating code.
- **Overengineering**: prefer the shortest reliable supported path; avoid queues,
  frameworks, services, and design patterns until requirements justify them.
- **Under-testing**: add or run tests that match risk; do not claim correctness
  from type checks alone.
- **Unsafe concurrency**: require cancellation, bounds, backpressure, race
  safety, and shutdown behavior before adding threads, workers, or async flows.
- **Weak migrations**: plan compatibility, backfills, rollback, indexing, and
  data validation before schema or persistence changes.
- **Dependency drift**: verify current stable versions and licenses before
  installing or pinning dependencies.
- **Security blind spots**: validate inputs, protect secrets, avoid injection,
  and document trust boundaries.
- **Partial implementation**: update docs, tests, configs, exports, packaging,
  and operational notes when the code change requires them.
- **False confidence**: record assumptions, evidence, and unsupported `N/A`
  decisions instead of pretending unsupported checks passed.

## Required Behavior

Before writing code, the model must read `pre-codegen-checklist.md`,
`do-not-generate-policy.md`, the relevant language file, and local project
conventions. After writing code or guidance, run
`python scripts/validate-workspace.py` when this workspace is in scope.
