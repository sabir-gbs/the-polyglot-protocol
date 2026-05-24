# README Featured Image Plan

## Request Summary

Add the generated Polyglot Protocol banner as the featured image on the GitHub
project page by storing it as a repository asset and referencing it from the
top-level README.

## Success Criteria

- The generated PNG is copied into the repository with a stable kebab-case name.
- The top-level README renders the image directly under the project title.
- Existing unrelated untracked files remain untouched.
- Workspace validation passes.

## Scope

- Add `assets/polyglot-protocol-featured.png`.
- Update `readme.md`.
- Add workflow artifacts under `docs/workflow/`.

## Validation And N/A Items

- Run `python scripts/validate-workspace.py`.
- Docker: N/A, README asset-only change.
- Lighthouse: N/A, no live web app URL is involved.
- CloakBrowser UI validation: N/A, no interactive UI is changed.
- Deployment: N/A, no deployment requested.

## Rollback

Remove the README image reference and delete the copied asset plus workflow
artifacts for this request.
