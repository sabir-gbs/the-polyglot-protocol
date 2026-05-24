# README Value Patterns Plan

## Request Summary

Add approved README sections inspired by the useful structure of the OAC GitHub
homepage: a comparison table, simple workflow, framework-fit section,
self-selection guidance, and a quick test.

## Success Criteria

- Add value-focused sections after `The Solution` and before `What It Includes`.
- Explain practical differences between using no protocol and using The
  Polyglot Protocol.
- Show a compact request-to-verification flow.
- Reinforce that agent frameworks handle workflow while The Polyglot Protocol
  handles the engineering bar.
- Include clear `Use` and `Skip` guidance.
- Include a quick test readers can run against their current coding agent.
- Workspace validation passes.

## Scope

- Update `readme.md`.
- Add workflow artifacts under `docs/workflow/`.

## Validation And N/A Items

- Run `python scripts/validate-workspace.py`.
- Docker: N/A, documentation-only change.
- Lighthouse: N/A, no frontend URL or rendered app changed.
- CloakBrowser UI validation: N/A, no interactive UI changed.
- Deployment: N/A, no deployment requested.

## Rollback

Remove the added README sections and delete the workflow artifacts for this
request.
