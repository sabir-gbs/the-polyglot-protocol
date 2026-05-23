---
name: the-polyglot-protocol
description: Use when generating, reviewing, refactoring, or planning code in polyglot repositories and you need senior-engineer guidance for language choice, architecture, testing, security, performance, dependencies, concurrency, CPU/GPU use, release safety, and LLM coding guardrails.
---

# The Polyglot Protocol

Use this skill before code generation, code review, dependency changes,
architecture changes, or workflow changes in a repository that may involve one
or more programming languages.

## Required Workflow

1. Read `docs/workflow/dev-workflow.md` for the operating process.
2. Read `docs/language-guidelines.md` for language-selection rules.
3. Read `docs/languages/pre-codegen-checklist.md`.
4. Read `docs/languages/do-not-generate-policy.md`.
5. Read the relevant file under `docs/languages/` before generating
   language-specific code.
6. For Python scripts, also read `docs/languages/python/python.md`.
7. For TypeScript or JavaScript, also read `docs/languages/typescript/typescript.md`.
8. After code generation, audit the entire generated codebase against this
   protocol and `docs/languages/scoring-rubric.md`. Report every criterion with
   its score, remediate all gaps until every criterion reaches `10/10`, and
   report the final total score. If a criterion cannot reach `10/10`, document
   the blocker, evidence, and follow-up requirement before completion.
9. Run validation when this skill folder is available:

```sh
python scripts/validate-workspace.py
```

## Core Rules

- Default operational scripts to Python unless the repository already has a
  better native script runner.
- Preserve existing project language, framework, package manager, formatter,
  test runner, and layout.
- Use platform-native code for product surfaces: PHP for WordPress, Shopify
  Liquid for Shopify themes, Kotlin for Android, Swift for Apple apps, SQL for
  database work, and HTML/CSS/TypeScript for web surfaces.
- Prefer the shortest reliable supported path before adding infrastructure.
- Verify current tool, dependency, and runtime versions from official or primary
  sources before pinning or upgrading.
- Do not invent APIs, configuration keys, package names, services, flags, or
  framework behavior.
- Generated code is not complete until a whole-codebase protocol audit reaches
  `100/100` across the rubric, or a documented blocker explains why that target
  is impossible in the current scope.
- Treat unsupported Docker, Lighthouse, browser, deployment, Git, or CI steps as
  explicit `N/A` items with evidence.

## Reference Map

- Language choice: `docs/languages/decision-matrix.md`
- Hard stops: `docs/languages/do-not-generate-policy.md`
- Required preflight: `docs/languages/pre-codegen-checklist.md`
- Examples: `docs/languages/examples.md`
- Version checks: `docs/languages/install-version-commands.md`
- Scoring: `docs/languages/scoring-rubric.md`
- LLM failure modes: `docs/languages/top-llm-coding-nuances.md`
- Current score: `docs/languages/score-report.md`

## Adapter Files

Use the adapter files when another agent expects a specific guidance filename:

- Codex: `adapters/codex/AGENTS.md`
- Claude Code: `adapters/claude-code/CLAUDE.md`
- OpenCode: `adapters/opencode/AGENTS.md`
