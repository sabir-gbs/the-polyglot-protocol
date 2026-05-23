# Language Guidance Maintenance Policy

Keep language guidance current, organized, and source-backed.

## Update Triggers

- New language file added
- Runtime or toolchain version changes
- Dependency baseline changes
- User adds a new rule
- A failed implementation exposes missing guidance
- Official platform guidance changes

## Version Checks

Before updating version numbers, verify from official or primary sources such
as language release metadata, package registries, vendor docs, or framework
docs. Do not rely on memory for modern tool versions.

## Review Requirements

- Update `docs/languages/index.md` when files are added or renamed.
- Update `language-guidelines.md` when language selection or default policy
  changes.
- Run the scoring rubric after guidance changes.
- Record workflow artifacts under `docs/workflow/`.
- Preserve kebab-case filenames and never put dates in filenames.
