# Refactoring Playbook Audits

## Scope

Add a standard 10-item refactoring playbook to every individualized language
file and require `dev-workflow.md` to reference the relevant language playbook
for refactor work.

## Guidance-File Audit Rounds

### Round 1

Score: `95/100`

Findings:

- Language files had red-green-refactor guidance but no explicit refactor type
  taxonomy.
- `dev-workflow.md` did not require agents to identify the refactor type before
  editing code.

Fixes:

- Added `## Refactoring Playbook` to all 22 individualized language files.
- Added all 10 refactor types: characterization, extract/isolate, rename,
  simplify control flow, dead code/dependency pruning, boundary, performance,
  compatibility-preserving migration, concurrency, and architecture
  de-escalation.

### Round 2

Score: `98/100`

Findings:

- The language validator did not enforce the new playbook section or labels.
- The template and scoring rubric did not mention the new requirement.

Fixes:

- Added `## Refactoring Playbook` to required language sections.
- Added all 10 refactor labels to validator enforcement.
- Updated the language template, score report, and scoring rubric.

### Round 3

Score: `100/100`

Evidence:

```sh
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

`docs/workflow/dev-workflow.md` now requires refactor requests to identify the
applicable language-specific playbook item before code edits.
