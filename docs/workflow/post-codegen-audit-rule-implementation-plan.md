# Post-Codegen Audit Rule Implementation Plan

## Request Summary

Add durable protocol language requiring a post-code-generation audit against The
Polyglot Protocol, with a final `100/100` target and criterion-level report.

## Success Criteria

- `SKILL.md` includes the audit as a required workflow step and core rule.
- `docs/workflow/dev-workflow.md` includes a final post-codegen audit section.
- The rule references `docs/languages/scoring-rubric.md`.
- The rule requires remediation before completion when criteria score below
  `10/10`, unless blocked and documented.

## Affected Files Systems URLs And Environments

- Edit `SKILL.md` to add the required post-codegen audit.
- Edit `docs/workflow/dev-workflow.md` to define the audit process and report
  requirements.
- Add workflow artifacts under `docs/workflow/`.
- No external systems, URLs, or runtime environments are modified.

## Required Skills And External References

- Use The Polyglot Protocol guidance already present in the repository.
- No external dependency or framework documentation is needed.

## Implementation Steps

1. Add a required workflow step in `SKILL.md` after validation.
2. Add a core rule in `SKILL.md` making the post-codegen audit mandatory.
3. Add a `Post-Codegen Protocol Audit` section in
   `docs/workflow/dev-workflow.md`.
4. Require final score reporting with all criteria from
   `docs/languages/scoring-rubric.md`.
5. Record planning, coding, guidance-file, and verification audit evidence.

## Validation Rollback And Risk

- Run `python scripts/validate-workspace.py`.
- Review `git diff --check`.
- Roll back by reverting the added section and workflow artifacts if wording is
  incorrect.
- Main risk is over-constraining non-code tasks. Mitigation: scope the rule to
  generated codebases and code generation work, while keeping objectively
  unsupported checks as documented `N/A`.

## Refactoring Playbook

`N/A`; no code refactor is planned.

## Baseline URL KPI Docker Lighthouse CloakBrowser Deployment

- No frontend, Docker, Lighthouse, browser, or deployment baseline applies.
- If future generated code has those surfaces, the post-codegen audit must
  include them according to the workflow and document any `N/A` evidence.
