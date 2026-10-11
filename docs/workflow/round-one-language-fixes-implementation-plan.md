# Round One Language Fixes Implementation Plan (Wave 2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the language guidance statements that make generated code fail to build, run, or stay secure. These are the verified P0 items from the round one audit and the CRITICAL findings from the per-language audits.

**Architecture:** Four tasks, grouped by file so each dispatch has one clear surface. Each item is a small targeted edit with a named primary source the implementer confirms before editing.

**Tech Stack:** Markdown only. No code files change.

**Spec:** `docs/workflow/polyglot-protocol-upgrade-plan.md` (P0-14 to P0-25) and the per-language audit findings (CRITICAL severity).

## Basic Rule And Scope

The protocol's basic rule is the minimal path, with the minimal change, that produces the desired effect. Each item below names its desired effect. Make only that edit.

In scope: wrong commands, wrong configuration, wrong facts, and missing security guidance that can make generated code insecure.

Out of scope, and left for the maintainer to approve separately:
- the version-pin refresh (upgrade plan tier P1, decision D2);
- the roughly 1,900 MAJOR and MINOR per-language findings (wording, duplication, completeness);
- moving the shared boilerplate out of the 22 language files (decision D3).

## Global Constraints

- Markdown edits only. Do not touch any `.py` file.
- Filenames unchanged. No new files.
- Every new or changed factual statement is confirmed against a primary source first (vendor docs, language spec, registry, or release notes). Write the source URL in your report. If a claim cannot be confirmed, do not add it; report it as UNVERIFIED.
- Do not invent flags, package names, versions, or configuration keys.
- Code comments inside new examples follow the protocol comment rule: plain US English at about a 6th grade level, technical terms fine, say why not what, no filler.
- Keep each new bullet short, in the same style as its neighbors.
- Do not claim `100/100` anywhere.
- `python -B scripts/validate-workspace.py` must end with `workspace validation: PASS`. The language validator requires each section header to appear exactly once, so do not rename or duplicate section headers.
- Commit only the files named in the task.

## Task Order

Tasks 3 and 4 touch files whose `sol-auditor` reads already finished. Tasks 1 and 2 touch the two deep guides, and their last two `sol-auditor` halves must finish first. Run 3, 4, then 1, 2.

---

### Task 1: TypeScript deep guide and readme

**Desired effect:** a project scaffolded from the guide type-checks, lints, and builds without errors, and the refresh rule cannot silently install an incompatible TypeScript.

**Files:**
- Modify: `docs/languages/typescript/typescript.md`
- Modify: `docs/languages/typescript/readme.md`

| # | Location (audit line) | Required change | Source to confirm |
|---|---|---|---|
| P0-14 | `typescript.md:~261` and the starter `devDependencies` near `:913-921` | The ESLint config imports `@eslint/js` but the starter dependencies omit it, and ESLint 10 no longer depends on it. Add `"@eslint/js"` to the dependency list and the pinned-baseline sentence near `:120`, with the version from the npm registry (`@eslint/js` latest at audit time was `10.0.1`). | registry.npmjs.org/@eslint/js and the typescript-eslint getting-started page |
| P0-15 | `typescript.md:~178` (tsconfig baseline) | With TypeScript 6, `types` defaults to `[]`, so Node globals and `node:*` imports fail to type-check. Add `"types": ["node"]` for Node targets and say why in one short sentence. | devblogs.microsoft.com/typescript/announcing-typescript-6-0 |
| P0-16 | `typescript.md:~178,~212,~906` | `declaration: false` leaves `declarationMap: true`, which the compiler rejects. Say to turn both off together. Also add `rootDir`, `outDir` and `include` to the baseline (or say to use a separate test tsconfig) so `tsc -p` does not write `.js` and `.d.ts` files beside the sources. | typescriptlang.org/tsconfig |
| CRIT-TS-1 | `typescript.md:~222` | "Bundler projects may use `moduleResolution: Bundler`" applied to the `module: NodeNext` baseline does not compile, because `NodeNext` requires `moduleResolution: NodeNext`. State that `Bundler` must be paired with `module: ESNext` or `Preserve`, and change both options together. | typescriptlang.org/tsconfig#moduleResolution |
| CRIT-TS-2 | `readme.md:12` and the refresh rule near `typescript.md:~127-129` | "Verify current stable versions" with no caveat can pull `typescript@latest`, which is `7.0.x`, while `typescript-eslint` declares a peer range that stops below `6.1.0`. Add one sentence: stay on the `6.0.x` line until `typescript-eslint` supports a newer major; check the peer range before bumping. | registry.npmjs.org/typescript-eslint/latest (peerDependencies) |

- [ ] **Step 1:** For each row, open the source and confirm the claim. Note the exact current values.
- [ ] **Step 2:** Make the edit. Keep it to the one statement.
- [ ] **Step 3:** Run `python -B scripts/validate-workspace.py 2>&1 | tail -3`. Expected: `workspace validation: PASS`.
- [ ] **Step 4:** Run `git diff --stat` and confirm only the two files changed and the diff is small.
- [ ] **Step 5:** Commit: `git add docs/languages/typescript/typescript.md docs/languages/typescript/readme.md && git commit -m "Fix TypeScript baseline config, ESLint dependency, and version caveat"`

---

### Task 2: Python deep guide

**Desired effect:** the commands in the guide run, the examples pass the guide's own lint rules, and the security examples are safe as written.

**Files:**
- Modify: `docs/languages/python/python.md`

| # | Location (audit line) | Required change | Source to confirm |
|---|---|---|---|
| P0-17 | `python.md:~1062` | `python -m pip-audit` cannot work (a module name has no hyphen). Use `python -m pip_audit`. Also make the same fix anywhere else the `-m` form appears. | github.com/pypa/pip-audit |
| P0-18 | `python.md:~214,~216,~624` | The `S` ruff rules flag every `assert`, including the guide's own tests. Add `"tests/**" = ["S101"]` to the per-file ignores in both places. | docs.astral.sh/ruff/rules/assert |
| P0-19 | `python.md:~1242` | Remove the instruction to use `str.masked`, which does not exist. If a replacement is wanted, point to the guide's own `mask_*` helpers nearby. | docs.python.org/3/library/stdtypes.html |
| P0-20 | `python.md:~1265` | The "safe" `git clone` example is open to option injection. Put `--` before the URL in the argument list, and add one sentence to allow only expected URL schemes. | git-scm.com/docs/git-clone |
| P0-21 | `python.md:~160` | `requests==2.32.3` is affected by CVE-2024-47081. Use the current patched version from the PyPI page and change the range floor to `2.32.4`. | pypi.org/project/requests and the GitHub advisory |
| P0-22 | `python.md:~1174-1297` | scrypt `n=16384` is below the OWASP minimum, Argon2id is missing, the bcrypt 72-byte limit is undocumented, and `secure_delete` (overwrite then unlink) gives false assurance. Raise scrypt to the OWASP value and note `maxmem`; add Argon2id as the first choice to ask about; state the bcrypt limit; replace the overwrite claim with "use encryption at rest". | cheatsheetseries.owasp.org Password Storage Cheat Sheet; pypi.org/project/bcrypt; NIST SP 800-88 |
| CRIT-PY-2 | `python.md:~1263` (next to the `git clone` example) | The argument-list subprocess advice omits that on Windows a `.bat` or `.cmd` file is run through the command shell even when `shell=False`, so untrusted arguments can still inject commands. Add one sentence: do not pass untrusted arguments to `.bat` or `.cmd` files; call the real executable instead. | docs.python.org/3/library/subprocess.html (Windows and security notes) |
| CRIT-PY-1 | `python.md:~790` and `~321` | `itertools.batched` is Python 3.12, not "3.14+", and PEP 695 generic class syntax is 3.12. Correct both version labels. | docs.python.org/3/library/itertools.html and docs.python.org/3/whatsnew/3.12.html |

- [ ] **Step 1:** For each row, confirm the claim at its source and note exact values.
- [ ] **Step 2:** Make the edit. One statement per row.
- [ ] **Step 3:** Run `python -B scripts/validate-workspace.py 2>&1 | tail -3`. Expected: `workspace validation: PASS`.
- [ ] **Step 4:** Run `git diff --stat`; confirm one file and a small diff.
- [ ] **Step 5:** Commit: `git add docs/languages/python/python.md && git commit -m "Fix Python guide commands, lint config, and security examples"`

---

### Task 3: Tooling blocks in the smaller language files (batched)

**Desired effect:** each tooling block runs on a clean checkout as written.

**Files:**
- Modify: `docs/languages/swift.md`, `docs/languages/c.md`, `docs/languages/cpp.md`, `docs/languages/rust.md`, `docs/languages/go.md`, `docs/languages/r.md`, `docs/languages/dart.md`, `docs/languages/zig.md`

| File | Location | Required change | Source to confirm |
|---|---|---|---|
| `swift.md` | `:~18` | Bare `swift format` reads standard input and hangs in scripts and CI. Use `swift format lint --recursive Sources Tests` for checking and `swift format --in-place --recursive Sources Tests` for formatting. | github.com/swiftlang/swift-format |
| `c.md` | `:~17` | `cmake --build build` has no configure step on a clean checkout. Add `cmake -S . -B build` before it. | cmake.org manual (cmake(1)) |
| `cpp.md` | `:~18` | Same missing configure step before `cmake --build build` and `ctest --test-dir build`. Add `cmake -S . -B build`. | cmake.org manual |
| `rust.md` | `:~18-19` | `cargo audit` is a separate crate and fails until installed; add `cargo install cargo-audit --locked` or say to use it only when the project already does. `--all-targets` does not run doctests, which the file asks for; add `cargo test --doc`. | crates.io/crates/cargo-audit; doc.rust-lang.org/cargo/commands/cargo-test.html |
| `go.md` | `:~20` | `govulncheck ./...` has no install step. Add `go install golang.org/x/vuln/cmd/govulncheck@latest`. | go.dev/doc/tutorial/govulncheck |
| `r.md` | `:~20` | `testthat::test_dir("tests")` is wrong for package layouts. Use `Rscript -e 'testthat::test_local()'`. | testthat.r-lib.org/reference/test_dir.html |
| `dart.md` | `:~16` | `dart pub get` fails for packages that depend on the Flutter SDK. Say to use `flutter pub get` for Flutter packages and `dart pub get` for plain Dart. | dart.dev/tools/pub/cmd/pub-get |
| `zig.md` | `:~66` | Models default to `@cImport`, which is deprecated in 0.16 and removed in 0.17, so the code fails to compile. Add one bullet: do not generate `@cImport`; use the build system's translate-C step for the pinned Zig version. | ziglang.org release notes for 0.16.0 and 0.17.0 |

- [ ] **Step 1:** Confirm each row at its source. If the exact Zig 0.17 mechanism cannot be confirmed, write only the "do not generate `@cImport`" half and report the rest UNVERIFIED.
- [ ] **Step 2:** Make each edit. One statement per row.
- [ ] **Step 3:** Run `python -B scripts/validate-workspace.py 2>&1 | tail -3`. Expected: `workspace validation: PASS`.
- [ ] **Step 4:** Run `git diff --stat`; confirm exactly the eight files.
- [ ] **Step 5:** Commit: `git add docs/languages/swift.md docs/languages/c.md docs/languages/cpp.md docs/languages/rust.md docs/languages/go.md docs/languages/r.md docs/languages/dart.md docs/languages/zig.md && git commit -m "Make language tooling blocks runnable on a clean checkout"`

---

### Task 4: Missing or incomplete security guidance

**Desired effect:** a model following these files does not generate the main injection, deserialization, or secret-handling flaws for the language.

**Files:**
- Modify: `docs/languages/html.md`, `docs/languages/java.md`, `docs/languages/kotlin.md`, `docs/languages/r.md`, `docs/languages/sql.md`

Add the content inside the file's existing security-related text (the senior checklist or the existing security line). Do not add a new top-level section header, because the language validator requires a fixed section set; use a short bullet group under the existing heading that already covers security.

| File | Desired content (confirm each bullet at its source; drop any you cannot confirm) | Source |
|---|---|---|
| `html.md` | Render untrusted data only through the template engine's context-aware escaping. Never build markup by string concatenation or `innerHTML` with untrusted data. Never put untrusted data in script, style, or event-handler context. Use a Content Security Policy as defense in depth. | developer.mozilla.org (XSS, CSP); OWASP XSS Prevention Cheat Sheet |
| `java.md` | Never deserialize untrusted data with `ObjectInputStream`; if unavoidable, set an allow-list `ObjectInputFilter`. Use `PreparedStatement` for SQL. Disable external entities when parsing XML. Do not log secrets. | docs.oracle.com JDK serialization filtering guide; OWASP Deserialization Cheat Sheet |
| `kotlin.md` | Do not put secrets in source, `BuildConfig`, or resources, because APKs and JARs can be decompiled. On Android, do not export components without a permission check, and use the Keystore for keys. | developer.android.com security guidance |
| `r.md` | Never `eval(parse(text = ...))` on external input. Do not build shell commands with `paste()` into `system()`; use `system2()` with separate arguments. Use `readRDS` only on trusted files. | cran.r-project.org manual; R documentation for `readRDS` and `system2` |
| `sql.md` | Parameterized queries bind values only. Table names, column names, `ORDER BY` direction, and dynamic SQL inside procedures cannot be bound. Allow-list identifiers from a fixed set, and quote them with the database's identifier-quoting function. | OWASP SQL Injection Prevention Cheat Sheet |

- [ ] **Step 1:** For each file, find the existing security text. Add the bullets there in the file's own style. Do not add headers.
- [ ] **Step 2:** Run `python -B scripts/validate-workspace.py 2>&1 | tail -3`. Expected: `workspace validation: PASS`.
- [ ] **Step 3:** Run `git diff --stat`; confirm exactly the five files and that no `##` header was added or removed (`git diff | grep '^[+-]## '` prints nothing).
- [ ] **Step 4:** Commit: `git add docs/languages/html.md docs/languages/java.md docs/languages/kotlin.md docs/languages/r.md docs/languages/sql.md && git commit -m "Add language-specific security guidance for html, java, kotlin, r, sql"`

---

## Self-Review

**Coverage of the upgrade plan:**

| Item | Task |
|---|---|
| P0-14, P0-15, P0-16 | 1 |
| P0-17 to P0-22 | 2 |
| P0-23 (swift) | 3 |
| P0-24 (cmake, cargo audit, govulncheck) | 3 |
| P0-25 (testthat) | 3 |
| CRITICAL findings from the per-language audits | 1 (TypeScript x2), 2 (Python version labels), 3 (dart, zig), 4 (html, java, kotlin, r, sql) |

**Not in this wave, by design:** version pins (P1), the MAJOR and MINOR findings, and duplication removal.

**Risks.** The `sol-auditor` and `opus-auditor` CRITICAL claims come from model reports, so each row requires a primary-source confirmation before editing. Security bullets in Task 4 are content additions; an unconfirmed bullet is dropped, not guessed.
