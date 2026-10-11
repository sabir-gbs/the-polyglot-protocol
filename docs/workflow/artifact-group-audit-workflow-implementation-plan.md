# Artifact Group Audit Workflow Implementation Plan

## Request Summary

Add the per-artifact-group dual-auditor audit workflow as a standalone standard
and wire it into the existing workflow guidance and validation.

## Success Criteria

- `docs/workflow/artifact-group-audit-workflow.md` exists and covers scope,
  roles, procedure, output contract, criteria sources, log requirements, and
  blockers.
- `dev-workflow.md` has an `Artifact-Group Dual-Auditor Gate` section, a
  guidance-priority entry, an audit-log bullet, and a final-pass item.
- `SKILL.md` has a required workflow step, a core rule, and a reference-map
  entry.
- The validator fails when the doc or a reference to it is missing.

## Affected Files Systems URLs And Environments

- `docs/workflow/artifact-group-audit-workflow.md` (new)
- `docs/workflow/dev-workflow.md`
- `SKILL.md`
- `readme.md`
- `docs/AGENTS.md`
- `scripts/validate-workspace.py`
- `scripts/score-audit-gate.py` and `tests/test-score-audit-gate.py` (follow-up)
- Node pin files: `docs/language-guidelines.md`, `docs/languages/javascript.md`,
  `docs/languages/typescript.md`, `docs/languages/typescript/typescript.md`

## Required Skills And External References

- `the-polyglot-protocol`; Python rules in `docs/languages/python/python.md`
  apply to the validator change.
- Context7: `N/A`.

## Implementation Steps

1. Write the standalone workflow doc.
2. Insert the gate section after `Post-Codegen Protocol Audit` in
   `dev-workflow.md`, and update guidance priority, audit-log contents, and the
   final pass list.
3. Add the step, rule, and reference entry to `SKILL.md`, renumbering the
   validation step.
4. Add index entries to `readme.md` and `docs/AGENTS.md`.
5. Add `check_audit_workflow_references` to `scripts/validate-workspace.py` and
   call it from `main`.
6. Run validation, a negative validation, and `git diff --check`.

## Validation Rollback And Risk

- Positive run: `python scripts/validate-workspace.py` must print `PASS`.
- Negative run: move the new doc aside, expect `FAIL` naming the missing doc,
  then restore it.
- `git diff --check` must be clean.
- Rollback: revert edits and remove new files.

## Refactoring Playbook

`N/A`; no refactor.

## Baseline URL KPI Docker Lighthouse CloakBrowser Deployment

All `N/A`; docs-only change. See the plan for evidence.
