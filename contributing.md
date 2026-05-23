# Contributing

Contributions should keep the project portable, source-backed, and easy for
agents to apply.

## Before Editing

1. Read `SKILL.md`.
2. Read `docs/languages/pre-codegen-checklist.md`.
3. Check `docs/languages/do-not-generate-policy.md`.
4. Use `docs/languages/language-file-template.md` for language guidance changes.

## Validation

Run:

```sh
python scripts/validate-workspace.py
```

Do not submit changes that reduce the validation score below `100/100`.

## Style

- Use kebab-case filenames.
- Do not put dates in filenames.
- Keep guidance concise and action-oriented.
- Prefer official or primary sources for version and tooling claims.
- Record unsupported checks as explicit `N/A` items instead of pretending they
  passed.

## Pull Requests

Include:

- Summary of the change
- Reason for the change
- Files touched
- Validation output
- Any intentional `N/A` decisions
