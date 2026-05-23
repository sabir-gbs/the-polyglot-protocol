# Organize Guidance Files Audits

## Scope

Move the deep Python, TypeScript, and development workflow guides into organized
subfolders, update all references, and add red-green-refactor guidance across
all individualized language files.

## Guidance-File Audit Rounds

### Round 1

Score: `94/100`

Findings:

- Deep guides were moved, but references still pointed at old root-level paths.
- Red-green-refactor was present only as implicit testing/refactoring guidance.
- The validator did not enforce the new red-green-refactor section.

Fixes:

- Updated references to `docs/workflow/dev-workflow.md`,
  `docs/languages/python/python.md`, and
  `docs/languages/typescript/typescript.md`.
- Added `## Test-First Red Green Refactor` to all 22 language files.
- Added the section to the language validator and language file template.

### Round 2

Score: `98/100`

Findings:

- The language score report still listed `10/10` operational governance files.
- The moved deep guides still used old title headings.

Fixes:

- Updated operational governance coverage to `11/11`.
- Renamed moved guide headings to `# Python Deep Guide` and
  `# TypeScript And JavaScript Deep Guide`.

### Round 3

Score: `100/100`

Evidence:

```sh
python scripts/validate-language-guidance.py
python scripts/validate-workspace.py
```

Result:

- `language guidance validation: PASS`
- `language files: 22`
- `language readmes: 22`
- `operational files: 11`
- `score: 100/100`
- `workspace validation: PASS`

## Final Notes

- Root-level `PYTHON.md`, `TYPESCRIPT.md`, and `docs/dev-workflow.md` are no
  longer present.
- Deep guides now live under their respective language or workflow folders.
- Red-green-refactor is now an enforced language guidance requirement.
