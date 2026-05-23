# Per-Language Examples Audits

## Scope

Add language-specific best-practice examples to every individualized language
file and enforce the section through validation.

## Guidance-File Audit Rounds

### Round 1

Score: `94/100`

Findings:

- `docs/languages/examples.md` contained useful cross-language examples.
- Individualized language files did not include concrete language-specific
  bad/good examples.

Fixes:

- Added `## Best Practice Examples` to all 22 individualized language files.
- Added three concise bad/good examples per language covering idiomatic
  boundaries, errors, safety, performance, accessibility, or persistence.

### Round 2

Score: `98/100`

Findings:

- The validator, template, scoring rubric, and score report did not yet require
  or describe the new examples section.

Fixes:

- Added `## Best Practice Examples` to required validator sections.
- Updated the language file template, scoring rubric, and score report.

### Round 3

Score: `100/100`

Evidence:

```sh
python scripts/validate-workspace.py
git diff --check
```

Result:

- `language guidance validation: PASS`
- `language files: 22`
- `language readmes: 22`
- `operational files: 11`
- `score: 100/100`
- `workspace validation: PASS`
- `git diff --check` returned no whitespace errors.

## Final Notes

Per-language examples now live directly in each `docs/languages/*.md` file so
agents do not need to infer language-specific best practices from the generic
examples document alone.
