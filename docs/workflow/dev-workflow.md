# Development Workflow

## Purpose

This document defines the required operating workflow for add, change, and
update requests handled from the repository root where this skill is being
used.

- Use superpowers skills, Context7, and related skills for every
  add/change/update request.
- Do not use OpenSpec in this workflow.
- Treat this workflow as the default delivery contract unless a higher-priority
  user instruction overrides part of it explicitly.

## Prerequisite Checks

Before planning starts, check for the local presence of:

1. CloakBrowser
2. Lighthouse
3. `obra/superpowers`
4. Context7

Current required versions:

- CloakBrowser Python package: `0.3.30`
- CloakBrowser Chromium binary: `146.0.7680.177.5`
- Playwright Python dependency used by CloakBrowser: `1.60.0`
- Lighthouse CLI: `13.3.0`
- `obra/superpowers`: `5.1.0`
- Context7 CLI (`ctx7`): `0.4.4`
- Node.js for workflow CLIs: Active LTS `24.16.0`

Use fresh local evidence for each check, such as version output, command
resolution, or a verified local install path. Record the evidence in the
workflow-run audit log.

Typical evidence examples:

- CloakBrowser package: `.venv/bin/python -m pip show cloakbrowser`
- CloakBrowser binary: `.venv/bin/python -c "from cloakbrowser import binary_info; print(binary_info())"`
- CloakBrowser smoke test: launch headless, open a `data:` URL, read title/text,
  and close the browser
- Lighthouse: `lighthouse --version`
- Context7: `ctx7 --version` or another verified local Context7 install check
- `obra/superpowers`: a verified local install path or tool resolution, plus
  version evidence when available

If one or more prerequisites are missing:

- install the missing prerequisite first
- record the exact evidence that showed it was missing
- record the installation command or installation path used
- continue only after the prerequisite is installed and re-verified with fresh
  local evidence
- if installation fails or is impossible in the current scope, record that
  result as the blocker before continuing, unless a higher-priority user
  instruction explicitly changes that behavior

## Guidance Priority

Apply repository guidance in this order:

1. Direct user request for the current task
2. `docs/workflow/dev-workflow.md`
3. `AGENTS.md`
4. `language-guidelines.md`
5. `docs/languages/python/python.md`
6. `docs/languages/typescript/typescript.md`
7. `CLAUDE.md`
8. Other repository docs and scripts

If two guidance files overlap, keep all content and resolve the conflict in
favor of the higher-priority source.

## Workflow Self-Application

When this workflow document or other guidance files are updated, this workflow
applies to that work too.

- Store workflow-run artifacts under `docs/workflow/`.
- Use kebab-case filenames without dates, such as
  `<request-slug>-<artifact>.md`.
- Treat guidance-only requests as first-class workflow runs with the same plan,
  audit, verification, and final-pass requirements.

## Artifact Locations And Naming

Create these artifacts for every change request unless a higher-priority user
instruction explicitly changes the location:

- plan: `docs/workflow/<request-slug>-plan.md`
- implementation plan:
  `docs/workflow/<request-slug>-implementation-plan.md`
- execution plan:
  `docs/workflow/<request-slug>-execution-plan.md`
- audit log: `docs/workflow/<request-slug>-audits.md`

The audit log must contain:

- planning audit rounds
- coding audit rounds
- guidance-file audit rounds when guidance files changed
- verification evidence
- final-pass notes

## Required Skills And Inputs

- Invoke applicable superpowers skills before acting. Typical defaults are
  `using-superpowers`, `writing-plans`, `verification-before-completion`,
  `requesting-code-review`, `benchmark`, `qa`, and related workflow skills.
- Use Context7 to confirm current framework, library, browser, or tooling
  guidance when the request touches external technology.
- Use repository-local guidance and scripts before inventing new workflow steps.
- Use `language-guidelines.md` whenever the request involves language choice,
  code generation, runtime defaults, toolchain installation, or dependency
  upgrades. Read the relevant file under `docs/languages/` before generating
  language-specific code. Default operational scripts to Python unless the
  repository already standardizes on another script runner.
- For refactor requests, read the relevant language file's
  `## Refactoring Playbook` and identify which playbook item applies before
  editing code. If more than one applies, keep each item scoped and verified
  separately.
- Run `python scripts/validate-workspace.py` after guidance or documentation
  changes unless the file is unavailable because the task is outside this
  workspace.
- Record every justified `N/A` decision explicitly in the plan, audits, and
  final report. `N/A` is allowed only when a step is objectively impossible for
  the request or repository.

## N/A And Blocker Rules

- Never fabricate a Docker URL, Lighthouse run, CloakBrowser UI flow, deployment
  step, or Git action just to satisfy the checklist.
- For every unsupported step, record:
  `status`, `reason`, `evidence`, and `follow-up requirement if scope changes`.
- If the directory is not a Git repository, record commit and push as blocked
  rather than pretending they were completed.
- If the repository has no local web app or review URL, mark Docker review
  deployment and Lighthouse comparison as `N/A` with the local evidence that
  supports that conclusion.
- If the change is docs-only or otherwise non-frontend, mark frontend CloakBrowser
  UI validation as `N/A` and run only the relevant local verification that the
  repository can actually support.

## Planning Artifacts

For every change request, create all three planning artifacts before
implementation starts:

1. A plan
2. An implementation plan
3. An execution plan

Each planning artifact must include:

- request summary and success criteria
- affected files, systems, URLs, and environments
- required skills and external references
- validation, rollback, and risk notes
- relevant language refactoring playbook item when the request is a refactor or
  includes refactoring
- baseline URL selection and KPI capture plan when Lighthouse applies
- Docker, Lighthouse, CloakBrowser, and deployment expectations

## Planning Audit Loop

Run exactly three audit rounds on the planning artifacts before coding.

### Planning Audit Criteria

Score each criterion from `0` to `10` for a total score out of `100`.

1. Request coverage
2. Instruction compliance
3. Technical accuracy
4. Completeness of file and system touchpoints
5. Dependency and tooling readiness
6. Risk, rollback, and failure handling
7. Verification and test design
8. Performance baseline and comparison plan
9. Docker, environment, and deployment clarity
10. Documentation and reviewer usability

### Planning Audit Rules

- Round 1: score and revise
- Round 2: score and revise again
- Round 3: must reach `100/100`
- If round 3 is below `100/100`, the planning artifacts are not approved and
  must be revised until a replacement round 3 reaches `100/100`
- Do not execute code until the planning audits are complete
- Record criterion-level scores, total score, concrete findings, and the fixes
  applied between rounds

## Execution Rules

- Fully execute the execution plan once planning is approved.
- Do not skip planned verification, review, or deployment steps without
  explicitly documenting why.
- Keep the execution log aligned with the plan so later code audits can compare
  intent versus outcome.
- Record execution progress in the execution plan itself or in the audit log.

## Lighthouse Baseline And Regression Control

Before executing new code, establish a Lighthouse baseline for the local Docker
review URL.

Required baseline process:

1. Build the latest local image and start the local Docker development
   environment.
2. Identify the exact review URL that will be audited.
3. Run Lighthouse against that URL and save artifacts with kebab-case filenames
   that do not include dates. Put run timestamps inside the artifact content,
   including JSON output.
4. Capture at least `TBT` and `TTI` in the baseline notes.

Required post-change process:

1. Rebuild the latest image again.
2. Redeploy the updated image to the local Docker development environment.
3. Re-run Lighthouse against the same URL under the same conditions.
4. Compare post-change `TBT` and `TTI` against the baseline.
5. Treat any regression in `TBT` or `TTI` as a blocking issue unless the user
   explicitly approves it.

Use repeatable runs when practical so the comparison reflects stable results
rather than one noisy sample. When timing variance matters, use the same run
count before and after the change and compare median `TBT` and median `TTI`.

If no local web URL exists for the request, record Lighthouse as `N/A` with the
repository evidence that explains why no valid baseline can be produced.

## Docker Development Environment

- Always build the latest image before review.
- Always deploy that image to the local Docker development environment.
- Always provide the relevant local Docker test or review URLs.
- Prefer explicit image tags, compose files, profiles, and service names in the
  execution plan.
- Do not rely on stale containers or untracked local state as evidence.

If the repository does not define a local image or Docker development stack,
record Docker deployment and review URLs as `N/A` instead of inventing them.

## Coding Audit Loop

After coding is complete, run exactly three more audit rounds comparing the
executed code against the approved plans.

### Coding Audit Criteria

Score each criterion from `0` to `10` for a total score out of `100`.

1. Feature completeness against plan
2. Behavioral correctness
3. Regression safety
4. Test and verification coverage
5. Performance outcome versus baseline
6. UI and UX fidelity
7. DOM correctness and accessibility impact
8. Docker and environment parity
9. Documentation and operational alignment
10. Release readiness

### Coding Audit Rules

- Round 1: score and fix gaps
- Round 2: score and fix remaining gaps
- Round 3: must reach `100/100`
- If round 3 is below `100/100`, the implementation is not complete
- Keep the code-audit notes tied back to the original planning artifacts
- Record criterion-level scores, total score, concrete findings, and the fixes
  applied between rounds

## Guidance-File Audit Loop

When the change touches `docs/workflow/dev-workflow.md`, `AGENTS.md`, `CLAUDE.md`, or another
guidance file, run three guidance-file audit rounds after the edits.

### Guidance-File Audit Criteria

Score each criterion from `0` to `10` for a total score out of `100`.

1. Priority clarity
2. Instruction consistency
3. Content preservation
4. Cross-reference quality
5. Workflow discoverability
6. Local-environment accuracy
7. Security and credential safety
8. Verification guidance quality
9. Maintenance usability
10. Reviewer readability

### Guidance-File Audit Rules

- Round 1: score and revise
- Round 2: score and revise again
- Round 3: must reach `100/100`
- If round 3 is below `100/100`, the guidance update is not complete
- Keep the guidance-file audit notes in the same audit log as the planning and
  coding audits

## CloakBrowser Verification And QA

After development is confirmed `100%` complete, run verification and validation
with CloakBrowser.

CloakBrowser validation must cover:

- frontend UI and UX behavior
- DOM correctness
- advertised feature behavior
- critical user flows on the local Docker review URL
- evidence such as assertions, screenshots, and failure notes

Frontend validation rules:

- Use the superpowers QA workflow for frontend validation.
- Prefer CloakBrowser's Playwright-compatible locators and web-first assertions
  over brittle selectors.
- Use CloakBrowser as the default browser automation path. Direct Playwright is
  only a fallback when a task explicitly requires stock browser behavior,
  cross-browser coverage outside CloakBrowser, or a tool does not support
  CloakBrowser yet; record that fallback reason in the audit log.
- Verify in the browser supported by CloakBrowser on this host, currently
  stealth Chromium `146.0.7680.177.5`.
- Capture enough evidence to prove the feature works as advertised.

If no frontend or review URL exists for the request, record frontend
CloakBrowser validation as `N/A`. When browser-tool readiness still matters, run
the local CloakBrowser smoke test and record that narrower verification
honestly.

## Git And Release Controls

- Use `GITHUB_PAT` strictly for all Git operations.
- Use the token through environment-backed commands only.
- Do not use interactive Git authentication.
- Do not use cached credentials.
- Do not use alternate tokens.
- Keep credential helpers disabled for the operation if needed to enforce the
  `GITHUB_PAT` path.
- Do not write the PAT into remotes, repository config, shell history, or
  workflow documents.
- If Git actions are required but the directory is not a repository, record that
  blocker explicitly in the final pass.
- Do not deploy to live or production without explicit approval.
- When live or production deployment is approved, deploy and verify through the
  configured SSH-based production access path.

## Final Pass

After planning audits, execution, coding audits, performance comparison, QA, and
verification are complete, perform one final pass that checks:

1. plans versus shipped result
2. Docker review environment state
3. Lighthouse baseline versus post-change metrics
4. CloakBrowser validation evidence
5. documentation updates
6. local review URLs
7. deployment approval state
8. remaining risks or follow-ups

Write the final pass into the audit log for the workflow run.

## Workflow Document Maintenance

When workflow documents are updated:

- review all guidance-file updates
- reorganize the guidance files into a clear priority order
- do not remove content only to force the new order
- audit the guidance-file updates with three rounds using ten scoring criteria
- reach `100/100` by round 3
- commit and push the finalized changes after they are complete and verified

## Expected Local Capabilities

Installations vary by host. Treat these as required capability targets, not as
claims about the current machine:

- Node.js Active LTS and npm are available for workflow CLIs when needed.
- CloakBrowser, Playwright, Lighthouse, Context7, and `obra/superpowers` are
  verified before workflows that depend on them.
- Docker and Docker Compose are verified before container review workflows.
- SSH keys and OpenSSH are verified before approved SSH-based deployment flows.
- Missing capabilities are recorded as blockers or justified `N/A` items rather
  than assumed.
