# Polyglot Protocol Upgrade Plan

Status: **draft for maintainer review. No fixes from this plan have been applied.**

## Request Summary

Run the artifact-group dual-auditor gate across the whole repository with round
1 as the deepest sweep, to find information that is outdated, wrong, missing, or
worth optimizing. This plan ranks every finding and gives a recommendation for
each decision that needs the maintainer.

## Round 1 Gate Results

Seven artifact groups, two independent read-only auditors per group
(`sol-auditor` on Codex `gpt-6.1-sol`, `opus-auditor` on Opus). Totals were
re-added by `scripts/score-audit-gate.py`. Gate: mean of `85` or more with no
`CRITICAL`.

| Group | Scope | sol | opus | Mean | CRITICAL (sol / opus) | Gate |
|---|---|---:|---:|---:|---|---|
| G1 | Entry and adapter docs | 69 | 66 | 67.5 | 4 / 1 | FAIL |
| G2 | Workflow and policy docs | 56 | 57 | 56.5 | 6 / 2 | FAIL |
| G3 | Python guidance | pending | 66 | n/a | pending / 4 | not scored |
| G4 | TypeScript and JavaScript guidance | 67 | 69 | 68.0 | 3 / 2 | FAIL |
| G5 | Systems and scripting languages | 71 | 68 | 69.5 | 0 / 0 | FAIL |
| G6 | Application and data languages | 72 | 68 | 70.0 | 1 / 0 | FAIL |
| G7 | Validator scripts and tests | 57 | 62 | 59.5 | 6 / 2 | FAIL |

Both auditors agreed within 2 to 5 points on every scored group, which is a
good sign the scores are not noise. The `sol-auditor` run for G3 had not
finished when this plan was written, so G3 findings come from `opus-auditor`
only.

## Independent Verification

Auditor claims were checked against primary sources before ranking. Confirmed:

- Latest versions from `pypi.org`, `registry.npmjs.org`, `go.dev/dl`,
  `static.rust-lang.org`, `ziglang.org`, `cran.r-project.org`, `lua.org/ftp`,
  `php.net`, `ruby-lang.org`, the Dart and .NET release feeds, the Adoptium API,
  and the Node `Release/schedule.json`.
- `obra/superpowers` has no `benchmark` or `qa` skill (checked against the
  GitHub contents API for `skills/`).
- ESLint 10 no longer depends on `@eslint/js`; ESLint 9 does.
- TypeScript 6.0 defaults `types` to `[]` (Microsoft's announcement post).
- `typescript-eslint` 8.71.1 requires `typescript >=4.8.4 <6.1.0`.
- OpenCode's global skill path is `~/.config/opencode/skills`; `.opencode/skills`
  is project-level only. Codex lists `$HOME/.agents/skills`.
- Private vulnerability reporting is disabled on the repo
  (`{"enabled":false}`), and GitHub detects the license as `NOASSERTION`.
- `scripts/` modules have no module docstring (the string after the imports is
  not a docstring), and the packaged `the-polyglot-protocol/` directory never
  existed in git history.
- About 39% of all language-guidance lines (1,122 of 2,814) are shared
  boilerplate that appears in at least 20 of 22 files.

Not independently verified: Unity runtime level, ktlint and detekt plugin IDs,
the Rails default test framework, SQL client commands, and MariaDB `mysql`
symlinks. These stay marked `UNVERIFIED` in the findings.

## Priority 0: Breaks Users Or States Something Untrue

Do these first. Each one makes a user's command fail, installs something
unusable, or asserts evidence that does not exist.

| # | Fix | Where | Recommendation |
|---|---|---|---|
| P0-1 | OpenCode installer targets a directory OpenCode never reads, so install reports success and the skill never loads | `scripts/install-skill.py:13`, `readme.md:166` | Change the default to `~/.config/opencode/skills/the-polyglot-protocol`. Both auditors rated this `CRITICAL`; verified. |
| P0-2 | Codex installer targets a deprecated path | `scripts/install-skill.py:11`, `readme.md:154` | Change the default to `~/.agents/skills/the-polyglot-protocol`. Keep `~/.codex/skills` only behind an explicit `--target`. |
| P0-3 | `--force` runs `shutil.rmtree` on any target with no guard, and deletes the old install before the copy succeeds | `scripts/install-skill.py:19-32` | Refuse targets that are the repo, its parents, `$HOME`, or lack a `SKILL.md` named `the-polyglot-protocol`. Copy to a staging directory first, then swap. Add `--dry-run`. Remove `--force` from the readme one-liners. |
| P0-4 | Installer copies `.env*`, caches, `tests/`, and 40+ plan and audit logs into the agent skill directory | `scripts/install-skill.py:16` | Copy an allowlist only: `SKILL.md`, `docs/languages/`, `docs/language-guidelines.md`, `docs/workflow/dev-workflow.md`, `docs/workflow/artifact-group-audit-workflow.md`, `scripts/`, `adapters/`. |
| P0-5 | One-liner installs clone to a fixed `/tmp/the-polyglot-protocol`, so a second run fails | `readme.md:154-172` | Use `mktemp -d`, and note Windows needs a different form. |
| P0-6 | Required reading paths point at a file that does not exist (`language-guidelines.md` at the root) | `docs/workflow/dev-workflow.md:68,117`, `docs/languages/index.md:4`, `docs/languages/maintenance-policy.md:23`, `docs/languages/pre-codegen-checklist.md:9`, `docs/AGENTS.md:15,25,43` | Use `docs/language-guidelines.md` everywhere, and `../language-guidelines.md` from `docs/languages/`. |
| P0-7 | `CLAUDE.md` is in the guidance-priority list and the guidance-file audit trigger, but no root file exists | `docs/workflow/dev-workflow.md:71,330` | Point at `adapters/claude-code/CLAUDE.md`, or drop the entry. |
| P0-8 | Validation command is `../../scripts/validate-workspace.py` in six adapter files, and bare `python scripts/...` in `SKILL.md`; both fail depending on the working directory, and `SKILL.md` never says it checks the protocol repo, not the user's code | six adapter files, `SKILL.md:33` | Say "from the skill root", or use `${CLAUDE_SKILL_DIR}` for Claude Code. State what the script validates. |
| P0-9 | Workflow requires superpowers `benchmark` and `qa` skills that do not exist | `docs/workflow/dev-workflow.md:113,372` | Replace with real skills (`verification-before-completion`, `requesting-code-review`) and name CloakBrowser as the QA mechanism. |
| P0-10 | Hardcoded `score: 100/100` is printed by the validator and repeated as a measured score | `scripts/validate-language-guidance.py:161`, `readme.md:188,227`, `SKILL.md:50,70`, `contributing.md:21`, `docs/languages/score-report.md:5` | Replace with `structural validation: PASS`. Reserve numeric scores for rubric audits with recorded evidence. |
| P0-11 | An older changelog entry claims Google-style docstrings and a packaged copy that never existed, and cites a verification command that cannot have run | `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md:10,50` | Verified false. Correct the entry in place with a dated correction note. Do not delete it; the history is useful. |
| P0-12 | `security.md` sends reporters to a public issue because private reporting is disabled | `security.md:9` | Enable private vulnerability reporting in repo settings (one click), or add a private contact. This is a repo setting I cannot change from here. |
| P0-13 | Scorer accepts malformed input and can pass bad reports: malformed `FINDING CRITICAL` is ignored, an eleventh `VERDICT` is accepted, `--threshold 0` passes zero scores, criterion names are never compared | `scripts/score-audit-gate.py:60,90` | My bug from earlier in this session. Reject unknown lines that start with a reserved prefix, require identical criterion names from both auditors, and reject thresholds below `85` or above `100`. Add tests for each. |

### Wrong Commands And Config In Guidance (also P0)

These produce failing builds or unsafe code if followed literally.

| # | Fix | Where | Recommendation |
|---|---|---|---|
| P0-14 | `@eslint/js` imported but not in the template dev dependencies | `typescript/typescript.md:261,913-921` | Add `@eslint/js@10.0.1`. Verified. |
| P0-15 | TypeScript 6 baseline has no `types`, so `process` and `node:*` fail to type-check | `typescript/typescript.md:178` | Add `"types": ["node"]`. Verified. |
| P0-16 | `declaration: false` leaves `declarationMap: true`, which the compiler rejects; no `outDir` or `rootDir`, so `tsc` writes `.js` beside sources | `typescript/typescript.md:178,212,906` | Disable `declarationMap` together with `declaration`; add `rootDir`, `outDir`, `include`. |
| P0-17 | `python -m pip-audit` cannot work (hyphen) | `python/python.md:1062` | `python -m pip_audit`. Verified the module is `pip_audit`. |
| P0-18 | ruff `S` rules flag every `assert` in the guide's own tests | `python/python.md:214,216,624` | Add `"tests/**" = ["S101"]`. |
| P0-19 | `str.masked` does not exist | `python/python.md:1242` | Remove, or point to the `mask_*` helpers at `:1249`. |
| P0-20 | "Safe" `git clone` example is open to option injection | `python/python.md:1265` | `["git", "clone", "--", user_url]` plus a URL scheme allowlist. |
| P0-21 | Example pin `requests==2.32.3` is affected by CVE-2024-47081 | `python/python.md:160` | Use `requests==2.34.2` (verified current). |
| P0-22 | scrypt `n=16384` is below OWASP's minimum; Argon2id missing; bcrypt 72-byte limit undocumented; `secure_delete` overwrite gives false assurance | `python/python.md:1174-1297` | Raise scrypt to `N=2^17`, add Argon2id as ask-first, document the bcrypt limit, drop the overwrite claim in favor of encryption at rest. |
| P0-23 | Bare `swift format` reads stdin and hangs in CI | `swift.md:18` | `swift format lint --recursive Sources Tests`. Both auditors flagged it. |
| P0-24 | `cmake --build build` has no configure step; `cargo audit` and `govulncheck` shown without install | `c.md:17`, `cpp.md:18`, `rust.md:19`, `go.md:20` | Add the configure and install steps so each tooling block runs on a clean checkout. |
| P0-25 | `testthat::test_dir("tests")` is wrong for package layouts | `r.md:20` | `Rscript -e 'testthat::test_local()'`. |

## Priority 1: Outdated Versions

All values below were confirmed against primary sources on 2026-10-11.

| Item | Current in repo | Verified now | Notes |
|---|---|---|---|
| Python | `3.14.5` | `3.14.8` (patch), `3.15.0` (released 2026-10-09) | Recommend keep the `3.14` floor, name `3.14.8`, and treat `3.15` as next target until dependency wheels catch up. |
| Node.js | `24.21.0` Active LTS | `24.21.0`; Node 24 enters Maintenance `2026-10-20`; Node 26 becomes Active LTS `2026-10-28` | Add the transition dates and re-pin on 2026-10-28. Do not move to 26 yet; today it is Current. |
| TypeScript | `6.0.3` | npm latest is `7.0.2` | Stay on `6.0.x`. `typescript-eslint` 8.71.1 requires `<6.1.0`. State this reason in the doc so the "refresh" rule does not break installs. |
| Rust | `1.95.0` | `1.99.0` | |
| Go | `1.26.3` | `1.27.2` (latest `1.26` patch `1.26.9`) | |
| Zig | `0.16.0` | `0.17.0` | Pre-1.0; also fix stale `async` guidance. |
| Lua | `5.5.0` | `5.5.1` | |
| PHP | `8.5.6` | `8.5.11` (security release) | |
| Ruby | `3.4.9` as "stable" | `4.0.7` is stable; `3.4.11` is latest 3.4 | The "stable" claim is wrong, not just old. |
| R | `4.6.0` | `4.6.1` | |
| Dart | `3.12.0` | `3.13.5` | |
| .NET | `10.0.8` LTS | `10.0.12` LTS | .NET 8 and 9 end support `2026-11-10`; add a warning. |
| Kotlin | `2.3.21` | `2.4.21` | |
| Java | "current LTS" (no number) | JDK `25` LTS; `27` latest feature | Give the number. |
| Swift | "current stable" (no number) | `6.4.0` per auditor, not independently verified | Verify before pinning. |
| pip / uv | `26.1.1` / `0.11.16` | `26.2.1` / `0.13.0` | |
| ruff / mypy | `0.15.14` / `2.1.0` | `0.17.0` / `2.4.0` | |
| pytest / pytest-cov | `9.0.3` / `7.1.0` | `9.1.1` / `7.1.0` | |
| build / pip-audit | `1.5.0` / `2.10.0` | `1.6.1` / `2.10.1` | |
| eslint / typescript-eslint | `10.4.0` / `8.59.4` | `10.12.0` / `8.71.1` | |
| prettier / tsx | `3.8.3` / `4.22.3` | `3.9.10` / `4.23.15` | |
| vitest | `4.1.7` | `5.0.3` (4.x line `4.1.11`) | Major; recommend `4.1.11` until you choose to move. |
| @types/node | `24.12.4` | `24.19.2` (24.x line) | |
| Playwright / axe | `1.60.0` / `4.11.3` | `1.64.0` / `4.13.0` (Python `1.63.0`) | |
| Lighthouse / ctx7 | `13.3.0` / `0.4.4` | `13.5.0` / `0.6.0` | |
| CloakBrowser | `0.3.30` | `0.6.1` | Chromium binary pin cannot be verified without installing. |
| obra/superpowers | `5.1.0` | `7.0.0` (released 2026-10-10) | Major, one day old. |

**Recommendation for the pins as a whole:** keep exactly one dated table in
`docs/language-guidelines.md` with a verified-on date per row, and have every
language file say "see the baseline table". The table header currently claims
`2026-05-23` but lists Node `24.21.0`, which did not exist until 2026-09-07, so
the date is false for part of the table. This removes about 15 places that drift
independently.

For the workflow tool pins (`dev-workflow.md`): relabel them "minimum tested",
not "required". As written they contradict the repo's own rule to verify
current versions before pinning.

## Priority 2: Version-Gated And Factual Corrections

Smaller than P0 but each is a wrong statement a model would reproduce.

| Fix | Where |
|---|---|
| `itertools.batched` is 3.12, not "3.14+" | `python/python.md:790` |
| PEP 695 `class C[T]` syntax is 3.12, not "3.14+" | `python/python.md:321` |
| `optparse` is not deprecated | `python/python.md:971` |
| `lib2to3` and `tkinter.tix` were removed in 3.13, with other PEP 594 removals; list them | `python/python.md:975` |
| `ruff format` is "near-identical" to Black, not identical | `python/python.md:205` |
| `memory_profiler` is no longer maintained; use stdlib `tracemalloc` | `python/python.md:870` |
| Python summary file contradicts the deep guide on threads, the GIL, and commands | `docs/languages/python.md:19,105` |
| Structured concurrency is still preview in JDK 25 and needs `--enable-preview` | `java.md:93` |
| .NET 8 and 9 end of support is 2026-11-10 | `c-sharp.md:8` |
| Corepack is no longer bundled from Node 25 | `typescript/typescript.md:46` |
| "Native fetch has no default timeout" is inaccurate; it has no overall deadline | `typescript/typescript.md:1136` |
| Node release schedule wording predates the new yearly cadence | `typescript/typescript.md:22` |
| `process`-style flags redundant with `strict`, and `consistent-type-imports` needs `no-import-type-side-effects` | `typescript/typescript.md:183,276` |
| `pre-codegen-checklist.md` says "the required audit round", conflicting with three rounds | `docs/languages/pre-codegen-checklist.md:25` |
| `scoring-rubric.md` is scoped to language files but used for whole codebases | `dev-workflow.md:212`, `scoring-rubric.md:3` |
| `language-file-template.md` omits labels the validator requires | `docs/languages/language-file-template.md` |
| Shopify theme directory list omits `blocks/` | `shopify-liquid.md:9` |
| Bash: macOS ships Bash 3.2; no test runner or formatter named | `bash.md:10,15` |
| Lua: no guidance for sandboxing untrusted chunks | `lua.md:22` |
| Zig: `build.zig.zon` not mentioned | `zig.md:10` |
| `python -m pip --version` is not a documentation check | `docs/AGENTS.md:34` |
| `docs/AGENTS.md` says no test, asset, or build directories and no Git history; both false | `docs/AGENTS.md:21,51` |
| RustDesk and Tailscale example is unrelated to this repo | `docs/AGENTS.md:5` |
| "OAC Framework" has no link and an unclear name | `readme.md:17,57,91,107` |
| License detected as `NOASSERTION` because of a preamble before the Apache text | `license.md` |
| Language readmes link to bare `<lang>.md`, which resolves wrongly | 22 readmes, line 5 |
| Validator docstring cites `docs/PYTHON.md`; module docstrings are after imports so `__doc__` is `None` | `scripts/*.py` |
| Test file uses `unittest.TestCase`, which `python/python.md` forbids | `tests/test-score-audit-gate.py` |

## Priority 3: Structure And Optimization

Lower urgency, high long-term value. Several need a policy decision first.

| Fix | Impact | Recommendation |
|---|---|---|
| Move shared boilerplate (Refactoring Playbook, Test-First, Senior Checklist, Final Guardrails, LLM Guardrails) into one shared doc | About 1,100 lines (39%) of language guidance, and the main drift risk | Do it, but see decision D3: the validator currently requires each section in every file. |
| Collapse the 22 language readmes and the 6 adapter files | About 700 duplicated lines | Reduce each adapter to "Read `SKILL.md` and follow its Required Workflow". Reduce readmes to Purpose plus links. |
| Merge `docs/AGENTS.md` into root `AGENTS.md` | Codex and OpenCode load `AGENTS.md` from the project root, so `docs/AGENTS.md` is not seen in normal use | Merge and delete `docs/AGENTS.md`. |
| Remove dead packaged-copy code from the validator | `validate-workspace.py:46-85` always returns `[]` | Delete both functions and calls. |
| Add a Markdown path-resolution check to the validator | The whole class of broken links in P0-6 passes validation today | Small check; closes the gap that let these through. |
| Fix validator rigor: whole-heading matches, shared kebab-case helper, `timeout=` on subprocesses, skip every `.gitignore`d directory | Prevents false passes and a `.pytest_cache` false failure | Do alongside P0-10. |
| Shorten the two copies of the gate procedure (`dev-workflow.md` vs the standalone doc) to a pointer plus the `85` threshold | Removes duplicated rules | Do. |
| Move the 200-line Dry-Run Audit Mode out of `typescript/typescript.md` | Shortens the main guide | Optional. |
| Add language-specific release and versioning lines (Go `/vN`, Rust semver, C ABI, Zig breaking changes) | Replaces generic text with useful text | Optional. |
| Normalize Markdown spacing (missing blank line before `## Algorithmic Complexity...` in every language file) | Cosmetic | Do with a formatter pass. |

## Decisions For The Maintainer

| ID | Decision | Recommendation |
|---|---|---|
| D1 | Should the `85` gate replace the `100/100` and `10/10` completion rules? | **No.** Keep the gate as the per-group checkpoint, as written. Round 1 scored 56 to 72 on every group, so a lenient completion rule would be unsafe right now. |
| D2 | Pin to latest verified versions, or to versions the workflow has been run against? | **Pin latest for language and package baselines** (they are reference values for generated code, and verification is just a registry lookup). **Keep tool pins as "minimum tested"** (CloakBrowser, Lighthouse, ctx7, superpowers) because they have not been run here, and superpowers `7.0.0` is a day-old major. |
| D3 | Move shared boilerplate out of the 22 language files? | **Yes, to one shared doc,** and change the validator contract in the same commit so each file links to it. This is the single biggest quality gain. It does mean the "each section present exactly once" contract changes. |
| D4 | Node: stay on 24 or move to 26? | **Stay on `24.21.0` today, add the transition dates, and re-pin to 26 on 2026-10-28** when it becomes Active LTS. |
| D5 | Python floor: `3.14` or `3.15`? | **Keep `3.14`, name `3.14.8`, mark `3.15` as next.** It has been out two days. |
| D6 | TypeScript 7? | **No.** Document that `6.0.x` is held back by `typescript-eslint`'s peer range. |
| D7 | Which Python file is canonical, `python.md` or `python/python.md`? | **`python/python.md`** (already described as authoritative). Make the top-level file a short summary with no conflicting commands. Same for TypeScript. |
| D8 | Keep `docs/AGENTS.md`? | **Merge into root `AGENTS.md`** and delete it. |
| D9 | Correct or remove the changelog entry with false claims? | **Correct in place** with a dated note, so the history stays honest. |
| D10 | Enable private vulnerability reporting? | **Yes.** It is a repo setting, and it is the fastest fix for `security.md`. |

## Suggested Order Of Work

1. P0-13 scorer fixes (so the gate itself is trustworthy for later rounds).
2. P0-1 to P0-5 installer.
3. P0-6 to P0-12 broken paths, nonexistent skills, false scores and claims.
4. P0-14 to P0-25 wrong commands in guidance.
5. P1 pins in one table, then link every language file to it.
6. P2 factual corrections.
7. P3 structure, after D3 is decided.
8. Re-run the gate on each group as round 2, then round 3, and record scores in
   `docs/workflow/polyglot-protocol-upgrade-audits.md`.

## Validation Rollback And Risk

- Validation: `python scripts/validate-workspace.py`, then the gate per group.
- Rollback: each priority tier is separable; commit per tier so any tier can be
  reverted without the others.
- Risk: D3 changes a validator contract and touches 22 files at once.
  Mitigation: do it as its own commit with a before and after validator run.
- Risk: version pins move again before this lands. Mitigation: record the
  verified-on date per row and re-check on the day of the commit.

## Refactoring Playbook

`N/A`; this is a guidance and tooling change, not a code refactor, except the
installer and scorer which follow `docs/languages/python/python.md`.

## Baseline URL KPI Docker Lighthouse CloakBrowser Deployment

All `N/A`; no web surface, container, or deployment is affected.
