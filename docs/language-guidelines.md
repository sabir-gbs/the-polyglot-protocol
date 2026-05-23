# Language Guidelines

This guide removes guesswork from code generation across languages. Use it with
`docs/workflow/dev-workflow.md`, `AGENTS.md`, `docs/languages/python/python.md`, and `docs/languages/typescript/typescript.md`.

## Per-Language Files

Use `docs/languages/` for language-specific instructions:

- `docs/languages/decision-matrix.md`
- `docs/languages/do-not-generate-policy.md`
- `docs/languages/examples.md`
- `docs/languages/install-version-commands.md`
- `docs/languages/language-file-template.md`
- `docs/languages/maintenance-policy.md`
- `docs/languages/pre-codegen-checklist.md`
- `docs/languages/readme.md`
- `docs/languages/scoring-rubric.md`
- `docs/languages/score-report.md`
- `docs/languages/top-llm-coding-nuances.md`
- `docs/languages/bash.md`
- `docs/languages/c.md`
- `docs/languages/c-sharp.md`
- `docs/languages/cpp.md`
- `docs/languages/css.md`
- `docs/languages/dart.md`
- `docs/languages/go.md`
- `docs/languages/html.md`
- `docs/languages/java.md`
- `docs/languages/javascript.md`
- `docs/languages/kotlin.md`
- `docs/languages/lua.md`
- `docs/languages/php.md`
- `docs/languages/python.md`
- `docs/languages/r.md`
- `docs/languages/ruby.md`
- `docs/languages/rust.md`
- `docs/languages/shopify-liquid.md`
- `docs/languages/sql.md`
- `docs/languages/swift.md`
- `docs/languages/typescript.md`
- `docs/languages/zig.md`

## Language Selection Order

1. Preserve the repository's existing language, framework, package manager,
   formatter, test runner, and layout.
2. Use platform-native languages for platform code: Shopify Liquid for Shopify
   themes, PHP for WordPress plugins/themes, Kotlin for Android, Swift for iOS,
   SQL for database migrations and queries, and HTML/CSS for web documents.
3. Use Python for operational scripts, automation, audits, migrations, file
   processing, and glue code, even in WordPress, Shopify, JavaScript, or compiled
   language repositories, unless the repo already has a better native script
   runner.
4. Before adding a toolchain, dependency, service, or custom implementation,
   search for the shortest reliable supported path and document the source.
5. Read the relevant file under `docs/languages/` before generating code.
6. Verify current stable versions from official sources before pinning or
   upgrading. Do not rely on memory for modern tool versions.

## Universal Rules

- Prefer stable production releases over preview, beta, nightly, or development
  channels.
- Keep dependencies minimal, exact, locked, and justified.
- Use the language's standard formatter, linter, type checker, and test runner.
- Treat warnings, unsafe code, unchecked casts, globals, shell injection, SQL
  injection, and unbounded I/O as defects until proven necessary.
- Keep code portable across Windows, macOS, Fedora, and Ubuntu unless the project
  explicitly narrows the target.
- Use structured parsers and APIs instead of ad hoc string manipulation.
- Store generated workflow artifacts under `docs/workflow/` with kebab-case
  filenames and no dates.

## Current Stable Baselines

These baselines were verified from official or primary sources on 2026-05-23.
Re-check before each upgrade or new project.

| Area | Baseline | Verification source |
|---|---:|---|
| Python | `3.14.5+` target; follow `docs/languages/python/python.md` | python.org and `docs/languages/python/python.md` |
| Node.js | Active LTS `24.16.0` | `https://nodejs.org/dist/index.json` |
| TypeScript | `6.0.3` | npm registry `typescript/latest` |
| Go | `1.26.3` | `https://go.dev/dl/?mode=json` |
| Rust | `1.95.0` stable | Rust stable channel metadata |
| Zig | `0.16.0` stable | Zig download index |
| PHP | `8.5.6` | php.net releases |
| Ruby | `3.4.9` | ruby-lang.org release/cache |
| R | `4.6.0` | CRAN `R-4` source index |
| Lua | `5.5.0` | lua.org FTP index |
| Dart | `3.12.0` | Dart stable archive metadata |
| .NET/C# | `.NET 10.0.8` LTS | Microsoft release metadata |
| Kotlin | `2.3.21` | JetBrains Kotlin GitHub releases |
| Java | Current vendor LTS JDK | Verify with Adoptium, Oracle, or distro source |
| Swift | Current stable Swift/Xcode toolchain | Verify with swift.org or Xcode release notes |
| SQL | Dialect-specific | Verify against the target database |
| HTML/CSS | Living standards plus browser matrix | WHATWG, W3C, MDN, caniuse |
| Shopify Liquid | Shopify platform version | Shopify developer docs |
| Bash | System shell version | Local `/bin/bash --version` when Bash is required |

## Per-Language Defaults

### Python

Python is the default for scripts and automation. Follow `docs/languages/python/python.md`: Python
`3.14.5+`, `venv`, exact pins, `ruff format`, `ruff`, `mypy --strict`, `pytest`,
and `pip-audit`.

### TypeScript And JavaScript

Follow `docs/languages/typescript/typescript.md`. Prefer TypeScript over JavaScript for new code, Node.js
Active LTS for server/tooling code, ESM for new packages, exact dependencies,
and package scripts over direct binary calls.

### HTML And CSS

Use semantic HTML, accessible forms/buttons, responsive CSS, and the existing
design system. Avoid JavaScript for layout that HTML/CSS can handle. Validate
against the target browser matrix.

### Shopify Liquid

Use Liquid, JSON templates, sections, snippets, and Shopify theme conventions
for storefront code. Keep operational scripts in Python unless the theme already
has a documented Node workflow.

### PHP And WordPress

Use PHP for WordPress and PHP applications. Follow Composer, PHPUnit or Pest,
PHP-CS-Fixer or PHP_CodeSniffer, and WordPress Coding Standards when applicable.
Never generate direct SQL with interpolated input.

### Rust

Use stable Rust, `cargo fmt`, `cargo clippy -- -D warnings`, and `cargo test`.
Prefer safe Rust. Document every `unsafe` block with the invariant it relies on.

### C And C++

Use C23 or C++23 for new code when the toolchain supports it; otherwise preserve
the project standard. Use `clang-format`, `clang-tidy`, sanitizers, warnings as
errors, and CMake or Meson. Avoid owning raw pointers in C++.

### Go

Use `gofmt`, `go test ./...`, `go vet`, and `govulncheck`. Keep packages small,
errors explicit, contexts propagated, and modules tidy.

### Zig

Use the latest stable Zig, `zig fmt`, `zig build`, and `zig test`. Avoid master
or nightly unless the user explicitly accepts instability.

### SQL

Choose the dialect first: PostgreSQL, SQLite, MySQL/MariaDB, SQL Server, Oracle,
DuckDB, or another target. Use migrations, parameterized queries, constraints,
indexes, query plans for risky changes, and rollback notes.

### Bash

Use Bash only for thin local glue. Prefer Python for reusable or cross-platform
automation. When Bash is required, use `set -euo pipefail`, quote expansions,
check command availability, and run ShellCheck when available.

### C Sharp

Use the current .NET LTS, nullable reference types, `dotnet format`,
`dotnet test`, analyzers, and dependency lock files for production projects.

### Java And Kotlin

Use the project's Gradle or Maven wrapper. Prefer the current LTS JDK for Java
and current stable Kotlin for Kotlin. Use JUnit, Spotless or ktlint, Detekt for
Kotlin, and explicit Android guidance for Android projects.

### Lua

Use the current stable Lua unless the host embeds LuaJIT or a fixed Lua version.
Avoid globals, use `stylua` when configured, and test with Busted or the
project's existing harness.

### Swift

Use the current stable Swift/Xcode toolchain. Prefer Swift Package Manager,
`swift-format`, XCTest, structured concurrency, and platform accessibility
rules for app code.

### Dart

Use stable Dart, `dart format`, `dart analyze`, and `dart test`. Use Flutter
only when the project is a Flutter app or the user asks for Flutter.

### Ruby

Use Bundler, exact Gemfile locks, RuboCop, and Minitest or RSpec. Avoid global
gem installs and keep Rails conventions when working inside Rails.

### R

Use `renv` for dependency isolation, `styler`, `lintr`, and `testthat`. Keep
data import/export explicit about encoding, locale, time zones, and column
types.
