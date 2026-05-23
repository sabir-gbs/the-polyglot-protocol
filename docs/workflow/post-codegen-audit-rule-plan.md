# Post-Codegen Audit Rule Plan

## Request Summary

Add a protocol rule requiring every generated codebase to be audited against
The Polyglot Protocol after code generation, with a final criterion-level score
reported against the rubric. The target outcome is `100/100` for every
criterion unless an explicitly documented blocker prevents it.

## Success Criteria

- The top-level skill workflow requires a post-codegen compliance audit.
- The development workflow states when and how to run the audit.
- The audit requires criterion-level scoring against
  `docs/languages/scoring-rubric.md`.
- The audit requires concrete gaps, fixes, validation evidence, and justified
  `N/A` items.
- `python scripts/validate-workspace.py` passes after the guidance change.

## Affected Files Systems URLs And Environments

- `SKILL.md`
- `docs/workflow/dev-workflow.md`
- `docs/workflow/post-codegen-audit-rule-plan.md`
- `docs/workflow/post-codegen-audit-rule-implementation-plan.md`
- `docs/workflow/post-codegen-audit-rule-execution-plan.md`
- `docs/workflow/post-codegen-audit-rule-audits.md`
- No application URLs are affected.
- No Docker, deployment, database, or runtime service is affected.

## Required Skills And External References

- Skill: `the-polyglot-protocol`
- Local docs: `docs/workflow/dev-workflow.md`,
  `docs/language-guidelines.md`, `docs/languages/scoring-rubric.md`,
  `docs/languages/pre-codegen-checklist.md`, and
  `docs/languages/do-not-generate-policy.md`
- Context7: `N/A`; no external framework, library, browser API, or tooling
  behavior is changed.

## Validation Rollback And Risk

- Validation: `python scripts/validate-workspace.py`
- Rollback: revert the edits to `SKILL.md`, `docs/workflow/dev-workflow.md`,
  and these workflow artifacts.
- Risk: wording could be too vague and leave audit timing or score reporting
  implicit. Mitigation: add explicit final-pass rules and reference the rubric.

## Refactoring Playbook

`N/A`; this is a guidance change, not a code refactor.

## Baseline URL KPI Docker Lighthouse CloakBrowser Deployment

- Docker: `N/A`; this repository has no application container for this docs-only
  change.
- Lighthouse: `N/A`; no local web review URL is affected.
- CloakBrowser UI validation: `N/A`; this is non-frontend guidance.
- Deployment: `N/A`; no deployable service is changed.
