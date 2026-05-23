# Repository Guidelines

## Shortest Reliable Path First

Before adding infrastructure, configuring extra services, or debugging a complex path, deeply search for the simplest supported solution. Prefer direct, built-in capabilities when they meet the goal. Example: for RustDesk over Tailscale, enable TCP direct connection on each machine and connect with the literal Tailscale IP before building or troubleshooting a RustDesk ID/relay server path.

## Project Structure & Module Organization

This is a documentation workspace. Keep the folder organized at all times: group related files, remove temporary files, and give new directories clear names and purpose.

Root guides:

- `PYTHON.md`: Python runtime, portability, security, and testing guidance.
- `TYPESCRIPT.md`: TypeScript and JavaScript runtime, tooling, style, and testing guidance.
- `language-guidelines.md`: Language selection, default toolchains, and cross-language code generation rules.
- `docs/languages/`: Individual guidance files for Bash, C, C#, C++, CSS, Dart, Go, HTML, Java, JavaScript, Kotlin, Lua, PHP, Python, R, Ruby, Rust, Shopify Liquid, SQL, Swift, TypeScript, and Zig.
- `dev-workflow.md`: Required workflow for add, change, and update requests.
- `AGENTS.md`: Contributor-facing repository guide and index of rules.

There are no source, test, asset, package, or build directories. If code is added later, use top-level directories such as `src/`, `tests/`, `docs/`, and `assets/`.

## Guidance Documents & Rules

Check guidance before changing files. Use `dev-workflow.md` for the operating process, `language-guidelines.md` for language choice and default toolchains, the relevant file under `docs/languages/` before generating language-specific code, `PYTHON.md` for Python code and scripts, and `TYPESCRIPT.md` only when TypeScript or JavaScript is required. When adding rule documents, reference them here.

## Build, Test, and Development Commands

No project build system is configured. Use documentation checks before submitting changes:

```sh
python scripts/validate-workspace.py
find . -maxdepth 2 -type f | sort
python -m pip --version
```

Use `python scripts/validate-workspace.py` as the primary local validation command. Use `find` to confirm contents. Use runtime checks when relevant: `python --version`, `node --version`, or `npm --version`.

## Coding Style & Naming Conventions

Write Markdown with concise headings, direct instructions, and fenced command blocks. Use kebab-case for new filenames, such as `agent-notes.md` or `build-script.py`; never put dates in filenames. Prefer ASCII punctuation and avoid machine-specific absolute paths.

Use Python as the default language for repository scripts. Script work must follow `PYTHON.md`, `language-guidelines.md`, and `dev-workflow.md`. Use platform-native languages for platform code such as WordPress PHP or Shopify Liquid, but keep operational automation in Python unless existing repo tooling clearly provides a better path.

## Testing Guidelines

There is no automated test suite. For documentation-only changes, verify Markdown structure, links, headings, commands, and file references. If code is introduced, add tests beside the code or under `tests/`, use descriptive kebab-case filenames, and document the test command here.

## Commit & Pull Request Guidelines

This directory has no Git history, so no repository-specific commit convention can be inferred. Use short, imperative commit subjects when Git is initialized, such as `Add repository contributor guide`.

Pull requests should include a summary, reason for the change, files touched, and verification performed. Link related issues when available. Include screenshots only for rendered documentation or future user interfaces.

## Agent-Specific Instructions

Read `dev-workflow.md` before making add, change, script, or update requests in this workspace. Treat unsupported workflow steps as explicit `N/A` items with evidence rather than inventing build, deployment, or Git actions.
