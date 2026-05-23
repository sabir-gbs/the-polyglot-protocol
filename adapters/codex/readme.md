# Codex Environment Decisions

Use this adapter when applying The Polyglot Protocol in Codex-style coding
agents.

## Quality Controls

- Read `../../SKILL.md` before code generation.
- Follow repository-local `AGENTS.md` instructions when present.
- Prefer tool-backed inspection over assumptions.
- Keep edits scoped and preserve existing user changes.

## Completeness Controls

- Use `../../docs/languages/pre-codegen-checklist.md` before editing.
- Read the relevant individualized language guide under
  `../../docs/languages/`.
- Record unsupported workflow checks as explicit `N/A` items.

## Accuracy Controls

- Do not claim tests, builds, browser checks, Docker checks, or deployments
  passed unless they actually ran.
- Validate with:

```sh
python ../../scripts/validate-workspace.py
```
