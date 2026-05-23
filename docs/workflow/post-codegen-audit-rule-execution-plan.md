# Post-Codegen Audit Rule Execution Plan

## Request Summary

Implement the protocol rule that generated code must receive a final compliance
audit against The Polyglot Protocol, targeting `100/100` for every rubric
criterion and reporting the final score.

## Success Criteria

- Required rule is present in `SKILL.md`.
- Detailed audit procedure is present in `docs/workflow/dev-workflow.md`.
- Audit artifacts record planning, implementation, verification, and final
  review evidence.
- Workspace validation passes.

## Affected Files Systems URLs And Environments

- Guidance files: `SKILL.md`, `docs/workflow/dev-workflow.md`
- Workflow artifacts: this plan set and audit log
- No application runtime, data store, Docker image, URL, or deployment target is
  affected.

## Execution Steps

1. Complete three planning audit rounds.
2. Patch `SKILL.md` and `docs/workflow/dev-workflow.md`.
3. Record coding and guidance-file audit rounds.
4. Run `python scripts/validate-workspace.py`.
5. Run `git diff --check`.
6. Perform a final post-change review against the request and rubric.

## Validation Rollback And Risk

- Validation commands:
  - `python scripts/validate-workspace.py`
  - `git diff --check`
- Rollback command if required: revert the specific changed files from version
  control or remove the new workflow artifact files.
- Risk is wording ambiguity. Verify the final text requires timing, target
  score, criterion-level reporting, remediation, and blocker handling.

## Refactoring Playbook

`N/A`; this is not a refactor.

## Baseline URL KPI Docker Lighthouse CloakBrowser Deployment

- Docker: `N/A`, docs-only repository change.
- Lighthouse: `N/A`, no web URL.
- CloakBrowser: `N/A`, no UI surface changed.
- Deployment: `N/A`, no deployable service changed.
