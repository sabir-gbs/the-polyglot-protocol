# README Protocol Framework Positioning Plan

## Request Summary

Add a paragraph to the top-level README near the opening section explaining why
The Polyglot Protocol is a protocol rather than a framework, and how it can
work with frameworks such as OAC Framework as a complementary quality layer.

## Success Criteria

- The paragraph appears within the first three prose paragraphs of `readme.md`.
- The text clearly distinguishes protocol standards from framework/runtime
  orchestration.
- The text explains complementary use with OAC Framework and other
  agent-control systems.
- Workspace validation passes with `python scripts/validate-workspace.py`.

## Scope

- Affected file: `readme.md`
- Workflow artifacts: this plan, implementation plan, execution plan, and audit
  log under `docs/workflow/`
- Environment: local repository only

## Required Inputs

- `SKILL.md`: read
- `docs/workflow/dev-workflow.md`: read
- `docs/language-guidelines.md`: read
- `docs/languages/pre-codegen-checklist.md`: read
- `docs/languages/do-not-generate-policy.md`: read

## Validation And N/A Items

- Run `python scripts/validate-workspace.py`.
- Docker: N/A, documentation-only change with no web app runtime.
- Lighthouse: N/A, documentation-only change with no frontend URL.
- CloakBrowser UI validation: N/A, documentation-only change with no UI flow.
- Deployment: N/A, no deployment requested.

## Rollback

Revert the README paragraph and the workflow artifacts created for this request.
