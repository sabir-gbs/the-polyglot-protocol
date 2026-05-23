# Claude Code Environment Decisions

Use this adapter when applying The Polyglot Protocol in Claude Code-style
coding agents.

## Quality Controls

- Read `../../SKILL.md` and `CLAUDE.md` before code generation.
- Keep human-readable explanations concise and tied to files changed.
- Preserve repository conventions and avoid speculative rewrites.

## Completeness Controls

- Use the decision matrix and hard-stop policy before choosing a language or
  dependency.
- Read the relevant individualized language guide under
  `../../docs/languages/`.
- Include verification evidence and known `N/A` items.

## Accuracy Controls

- Verify APIs, commands, and package versions before relying on them.
- Validate with:

```sh
python ../../scripts/validate-workspace.py
```
