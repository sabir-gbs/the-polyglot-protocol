# Pre-Codegen Checklist

Run this checklist before generating or editing code.

## Required Steps

1. Read `docs/workflow/dev-workflow.md`.
2. Read `AGENTS.md`.
3. Read `language-guidelines.md`.
4. Read `docs/languages/decision-matrix.md`.
5. Read the relevant individualized language file.
6. Read `docs/languages/python/python.md` for Python scripts or `docs/languages/typescript/typescript.md` for TypeScript and
   JavaScript work.
7. Inspect the repository structure, package files, lockfiles, tests, and
   existing conventions.
8. Identify whether the task is product code, operational script, migration,
   configuration, documentation, or deployment work.
9. Check `docs/languages/do-not-generate-policy.md` for hard stops.
10. State assumptions, validation commands, rollback notes, and justified `N/A`
    items in the workflow artifacts.

## Completion Gate

Do not edit code until the relevant guidance is read, the repo conventions are
known, and the workflow plan has passed the required audit round.
