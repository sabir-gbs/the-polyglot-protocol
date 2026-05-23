# Language Guidance README

This directory turns language choice and code generation into an explicit,
auditable process.

## How To Use This Directory

1. Read `../../dev-workflow.md`.
2. Read `../../language-guidelines.md`.
3. Read `decision-matrix.md`.
4. Read `pre-codegen-checklist.md`.
5. Read the individualized language file for the code being generated.
6. Check `do-not-generate-policy.md` before editing.
7. Use `scoring-rubric.md` when adding or changing guidance.

## Organization

- Individual language files define language-specific rules.
- Operational docs define how to choose, score, validate, and maintain guidance.
- `examples.md` gives concrete good/bad patterns.
- `score-report.md` records the current validation status.

## Validation

Run:

```sh
python scripts/validate-workspace.py
python scripts/validate-language-guidance.py
```

The workspace validator runs the language validator and repository naming and
Markdown heading checks. The language validator checks required sections,
required labels, filenames, and operational documents.
