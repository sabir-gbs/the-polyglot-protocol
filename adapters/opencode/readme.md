# OpenCode Environment Decisions

Use this adapter when applying The Polyglot Protocol in OpenCode-style coding
agents.

## Quality Controls

- Read `../../SKILL.md` before implementation.
- Apply the relevant language guide before code generation.
- Prefer simple, inspectable changes over hidden framework behavior.

## Completeness Controls

- Follow `../../docs/languages/pre-codegen-checklist.md`.
- Check `../../docs/languages/do-not-generate-policy.md` for hard stops.
- Keep validation commands and assumptions visible.

## Accuracy Controls

- Do not invent configuration, APIs, tool flags, or project structure.
- Validate with:

```sh
python ../../scripts/validate-workspace.py
```
