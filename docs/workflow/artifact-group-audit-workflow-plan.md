# Artifact Group Audit Workflow Plan

## Request Summary

Codify the new global audit workflow shown in the maintainer's flowchart as a
standard document, and update the workflow docs so it is discoverable and
enforced. The flowchart defines per-artifact-group work with a Sonnet 5.5
orchestrator, up to 8 `haiku-worker` agents for prep and verdict checking, two
independent read-only auditors (`sol-auditor`, `opus-auditor`) scoring 10
criteria out of 100, a mean-score gate of `85` with no `CRITICAL` finding, up to
3 rounds, and a stop-and-report outcome after round 3.

## Success Criteria

- A standalone workflow doc defines roles, procedure, output contract, gate
  rules, criteria sources, audit-log needs, and blocker handling.
- `dev-workflow.md` and `SKILL.md` reference the doc and state the gate numbers.
- Existing audit loops and the Post-Codegen Protocol Audit are preserved, with
  precedence stated explicitly.
- Index files (`readme.md`, `docs/AGENTS.md`) list the new doc.
- `python scripts/validate-workspace.py` passes and fails when the doc is
  missing.

## Decisions Made

- **Additive, not a replacement.** The `85` gate governs per-group progression.
  The `10/10` whole-codebase target in the Post-Codegen Protocol Audit and the
  per-language audits stay in force. Reason: the maintainer did not answer the
  `85` versus `100/100` question, and removing content is prohibited by the
  guidance-maintenance rules. The maintainer can flip this decision.
- **No new criteria.** Auditors reuse the existing ten-criterion sets.
- **Severity tags.** The flowchart names `CRITICAL` only. `MAJOR` and `MINOR`
  were added as non-blocking tags so the check step has a closed set to grep.

## Affected Files Systems URLs And Environments

- Add `docs/workflow/artifact-group-audit-workflow.md`
- Edit `docs/workflow/dev-workflow.md`, `SKILL.md`, `readme.md`,
  `docs/AGENTS.md`, `scripts/validate-workspace.py`
- Add the four workflow-run artifacts for this request
- No application URLs, services, containers, or deployments are affected.

## Required Skills And External References

- Skill: `the-polyglot-protocol`
- Local docs: `docs/workflow/dev-workflow.md`, `docs/languages/scoring-rubric.md`,
  `docs/languages/python/python.md`
- Context7: `N/A`; no external library, framework, or tool behavior is changed.

## Validation Rollback And Risk

- Validation: `python scripts/validate-workspace.py`, a negative run with the new
  doc removed, and `git diff --check`.
- Rollback: revert the edited files and delete the added files.
- Risk: the auditor model identifiers come from the flowchart and cannot be
  verified from this repository. Mitigation: the doc requires local
  availability checks and forbids silent substitution.
- Risk: gate numbers are repeated in three files and can drift. Mitigation: the
  validator checks that each file states the `85` threshold.

## Refactoring Playbook

`N/A`; this is a guidance change, not a code refactor.

## Baseline URL KPI Docker Lighthouse CloakBrowser Deployment

- Docker: `N/A`; docs-only change with no container stack.
- Lighthouse: `N/A`; no web URL is affected.
- CloakBrowser UI validation: `N/A`; no browser surface.
- Deployment: `N/A`; nothing deployable changes.
