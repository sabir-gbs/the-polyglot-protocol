# Post-Codegen Audit Rule Audits

## Prerequisite Evidence

- Lighthouse: `/home/sabir/.local/bin/lighthouse`, version `13.3.0`.
- Context7: `/home/sabir/.local/bin/ctx7`, version `0.4.4`.
- Node.js: `/home/sabir/.local/bin/node`, version `v24.16.0`.
- `obra/superpowers`: `/home/sabir/.codex/superpowers/package.json`,
  version `5.1.0`.
- CloakBrowser package: missing from active Python environment:
  `WARNING: Package(s) not found: cloakbrowser`.
- CloakBrowser UI validation status: `N/A`; this is a docs-only workflow rule
  with no browser surface or review URL.

## Planning Audit Round 1

| Criterion | Score |
|---|---:|
| Request coverage | 9 |
| Instruction compliance | 9 |
| Technical accuracy | 9 |
| Completeness of file and system touchpoints | 9 |
| Dependency and tooling readiness | 9 |
| Risk, rollback, and failure handling | 9 |
| Verification and test design | 9 |
| Performance baseline and comparison plan | 10 |
| Docker, environment, and deployment clarity | 9 |
| Documentation and reviewer usability | 9 |

Total: `91/100`

Findings: the first plan needed clearer scoring-report requirements, explicit
remediation behavior for scores below `10/10`, and stronger `N/A` evidence for
frontend and deployment checks.

Fixes applied: added criterion-level score reporting, remediation language,
rollback notes, and `N/A` evidence expectations.

## Planning Audit Round 2

| Criterion | Score |
|---|---:|
| Request coverage | 10 |
| Instruction compliance | 10 |
| Technical accuracy | 10 |
| Completeness of file and system touchpoints | 10 |
| Dependency and tooling readiness | 10 |
| Risk, rollback, and failure handling | 10 |
| Verification and test design | 10 |
| Performance baseline and comparison plan | 10 |
| Docker, environment, and deployment clarity | 10 |
| Documentation and reviewer usability | 9 |

Total: `99/100`

Findings: reviewer usability still needed an explicit pointer to the source
rubric file that final reports must enumerate.

Fixes applied: added `docs/languages/scoring-rubric.md` as the required scoring
source in the implementation plan and planned guidance text.

## Planning Audit Round 3

| Criterion | Score |
|---|---:|
| Request coverage | 10 |
| Instruction compliance | 10 |
| Technical accuracy | 10 |
| Completeness of file and system touchpoints | 10 |
| Dependency and tooling readiness | 10 |
| Risk, rollback, and failure handling | 10 |
| Verification and test design | 10 |
| Performance baseline and comparison plan | 10 |
| Docker, environment, and deployment clarity | 10 |
| Documentation and reviewer usability | 10 |

Total: `100/100`

Planning approved for implementation.

## Coding Audit Round 1

| Criterion | Score |
|---|---:|
| Language selection clarity | 10 |
| Project discovery and structure clarity | 10 |
| Runtime, package, and toolchain clarity | 10 |
| Style, naming, documentation, comments, and best-practice example clarity | 10 |
| Testing, red-green-refactor, refactoring playbook, and verification clarity | 10 |
| Security, privacy, and compliance clarity | 10 |
| Algorithmic complexity and performance clarity | 10 |
| Architecture, queues, concurrency, CPU, and GPU clarity | 10 |
| Release, migration, rollback, and operability clarity | 10 |
| Dependency, configuration, resource, and packaging clarity | 10 |

Total: `100/100`

Findings: the new rule is documentation-only, introduces no runtime code,
dependencies, queues, concurrency, migrations, secrets, or generated APIs. It
keeps the scoring source local and explicit.

## Guidance-File Audit Round 1

| Criterion | Score |
|---|---:|
| Request coverage | 10 |
| Instruction compliance | 10 |
| Technical accuracy | 10 |
| Completeness of file and system touchpoints | 10 |
| Dependency and tooling readiness | 10 |
| Risk, rollback, and failure handling | 10 |
| Verification and test design | 10 |
| Performance baseline and comparison plan | 10 |
| Docker, environment, and deployment clarity | 10 |
| Documentation and reviewer usability | 10 |

Total: `100/100`

Findings: `SKILL.md` now requires post-codegen whole-codebase auditing, and
`docs/workflow/dev-workflow.md` defines the final audit loop, scoring source,
blocker handling, and required final report contents.

## Verification Evidence

- `python scripts/validate-workspace.py`: `workspace validation: PASS`
- Nested language validator output from workspace validation:
  `language guidance validation: PASS`, `score: 100/100`
- `git diff --check`: passed with no whitespace errors.

## Final-Pass Notes

The protocol now requires generated code to be audited after generation against
The Polyglot Protocol and `docs/languages/scoring-rubric.md`. The final report
must include all criteria and the final score, and completion requires
`100/100` unless an objective blocker is documented with evidence and follow-up
requirements.
