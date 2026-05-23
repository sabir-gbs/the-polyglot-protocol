# The Polyglot Protocol

A senior-engineer protocol for polyglot code generation, architecture, testing,
security, performance, and agent validation.

This project packages a portable skill for Codex, Claude Code, OpenCode, and
other skill-capable coding agents. It helps agents make disciplined coding
decisions across languages without inventing APIs, skipping repository
discovery, overengineering, or ignoring validation.

## What It Includes

- `SKILL.md`: skill entrypoint
- `docs/languages/`: individualized guidance for 22 languages
- `docs/languages/<language>/readme.md`: human-readable quality,
  completeness, and accuracy decisions for each language
- `docs/language-guidelines.md`: language selection and default-script policy
- `docs/dev-workflow.md`: planning, audit, validation, and `N/A` rules
- `scripts/validate-workspace.py`: full local validation
- `adapters/`: lightweight guidance and human-readable README files for Codex,
  Claude Code, and OpenCode

## Quick Start

Use the skill folder directly from an agent that supports local skill folders,
or copy the relevant adapter into the target agent's expected guidance location.

Validate the project:

```sh
python scripts/validate-workspace.py
```

Expected result:

```text
language guidance validation: PASS
language files: 22
language readmes: 22
operational files: 11
score: 100/100
workspace validation: PASS
```

## Language Coverage

Bash, C, C#, C++, CSS, Dart, Go, HTML, Java, JavaScript, Kotlin, Lua, PHP,
Python, R, Ruby, Rust, Shopify Liquid, SQL, Swift, TypeScript, and Zig.

## Core Principles

- Preserve existing repository conventions.
- Default operational scripts to Python unless the project already has a better
  native script runner.
- Use platform-native languages for product surfaces.
- Prefer the shortest reliable supported path.
- Verify dependency, runtime, and API claims from local code or official docs.
- Treat unsupported checks as explicit `N/A` items with evidence.

## Human-Readable Decision Guides

Each language has a dedicated README folder, for example:

- `docs/languages/python/readme.md`
- `docs/languages/typescript/readme.md`
- `docs/languages/rust/readme.md`

These README files summarize the decisions that control codegen quality,
completeness, and accuracy. The full enforceable rules remain in the matching
top-level language file such as `docs/languages/python.md`.

Each coding environment adapter also has a README:

- `adapters/codex/readme.md`
- `adapters/claude-code/readme.md`
- `adapters/opencode/readme.md`

## Project Status

Current validation score: `100/100`.

See `docs/languages/score-report.md` for the score report and
`docs/languages/scoring-rubric.md` for the rubric.

## License

Copyright (C) 2026 Growth by Sabir Inc.

Licensed under the Apache License, Version 2.0 (`Apache-2.0`). Commercial and
non-commercial use are permitted under the license terms.
