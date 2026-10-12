# Changelog

All notable changes to The Polyglot Protocol are recorded here. The newest
entry is first. Dates use `YYYY-MM-DD`.

## Unreleased: model-agnostic audit gate and round one fixes

Branch `feat/model-agnostic-roles`, 2026-10-11. This is a large change. It adds
an audit gate, makes the audit roles work with any capable model, and fixes
the problems a full audit of the repository found. Each section says what
changed and why. The last sections say what was not done and where the known
limits are.

### Why this change exists

The protocol's default workflow uses Claude Code with Codex. Users who run
OpenCode or another harness with open-weight models (DeepSeek, Kimi, GLM and
others) need the same quality gate without being tied to one model name. New
models also appear often, so the protocol describes roles by capability and
keeps model names in small profile files that are easy to replace.

### Changes to the required workflow

These change what a user of the protocol is told to do.

- `SKILL.md` has a new step 9: split work into artifact groups and pass each
  group through the dual-auditor gate. Validation is now step 10, and it says
  to run from the skill root and that it checks the protocol repository, not
  the project being generated.
- `docs/workflow/dev-workflow.md` has a new "Artifact-Group Dual-Auditor Gate"
  section, a new item in the final pass, and the audit workflow in its guidance
  priority list.
- `docs/workflow/dev-workflow.md`, "Git And Release Controls": the rule to use
  `GITHUB_PAT` strictly and to refuse cached credentials is replaced. Git and
  GitHub operations now use `gh auth`, checked with `gh auth status`, and
  personal access tokens are not used. The rule that a token is never written
  into a remote, repository config, shell history, or document is kept.
  Earlier audit logs still mention `GITHUB_PAT` because they record what was
  true at the time.
- `contributing.md`: "Do not submit changes that reduce the validation score
  below `100/100`" is now "Do not submit changes that make
  `python scripts/validate-workspace.py` fail". The validator has no score.
- `readme.md`: the one-line install commands use `mktemp -d` instead of a fixed
  `/tmp` folder and no longer pass `--force`. Adding `--force` replaces an
  existing install. A Windows note was added.

### Added

**Audit gate (per artifact group, two independent auditors)**
- `docs/workflow/artifact-group-audit-workflow.md`: the procedure. An
  orchestrator splits work into artifact groups. Two auditors from different
  model families score each group. Only the orchestrator edits files; auditors
  and workers are read-only. The gate passes when the mean of the two totals is
  at least `85` and no auditor raised a CRITICAL finding. A group that still
  fails after gate round 3 stops and is reported to the maintainer.
- `scripts/score-audit-gate.py`: the scorer. It reads two auditor outputs,
  adds up each criterion score itself, and ignores the total the auditor
  wrote. Exit codes: `0` gate passed, `1` gate failed, `2` invalid input. The
  scorer does not count rounds; that is a workflow rule.
- Degraded independence mode for harnesses that have only one model family.
  It is labeled in the audit log and needs a mean of at least `90`.
- Output contract: exactly ten `VERDICT <criterion>: n/10` lines and any
  number of `FINDING <CRITICAL|MAJOR|MINOR> file:line text` lines. A
  `TOTAL: n/100` line is optional and advisory. The scorer ignores it. A
  contract line that is malformed, indented, or decorated (bulleted, quoted,
  bold, numbered) makes the scorer exit `2` instead of being skipped.

**Model-agnostic roles**
- `docs/workflow/model-agnostic-roles-design.md`: the approved design. Four
  roles by capability: orchestrator, auditor A, auditor B, worker.
- `docs/workflow/role-resolution.md`: harness classes, what a harness must
  provide, a table of observed harnesses (12 rows: 11 harnesses and one model
  runner), and rules for unknown harnesses.
- `profiles/default.md`, `profiles/opencode-open-weights.md`,
  `profiles/template.md`: where model names belong. Each profile holds a JSON
  block that the validator checks.
- Adapters for Claude Code, Codex, and OpenCode now point to `SKILL.md` and
  the profiles instead of repeating the rules.

**Validator and tests**
- `scripts/validate-workspace.py` now also checks: profile structure; that
  `SKILL.md`, the dev workflow, and the audit workflow name no model; that
  `SKILL.md`, the dev workflow, `readme.md`, and `docs/AGENTS.md` link the
  audit workflow; that the audit workflow, the dev workflow, and `SKILL.md`
  state the `85` threshold; that the scorer file exists; and that the script
  tests pass.
- New tests: 39 for the scorer, 26 for the validator, 5 for the installer.
  All use the standard library `unittest`.

**Protocol rules**
- Basic rule, now the first rule in `SKILL.md` and
  `docs/language-guidelines.md`: take the minimal path, with the minimal
  change, that produces the desired effect.
- Comment rule: code comments and docstrings use plain US English at about a
  6th grade level, say why and not what, and avoid filler, hype, edit
  narration, banners, and emoji. The canonical text is in
  `docs/language-guidelines.md`. Short pointers are in `SKILL.md`, the
  pre-code checklist (new steps 11 and 12), the scoring rubric (criterion 4),
  the language file template, and the failure modes in
  `docs/languages/top-llm-coding-nuances.md`. The rule is applied by review
  and scoring. No script checks it.

**Planning records (all under `docs/workflow/`)**
- The round one upgrade plan (ranked P0 to P3 items), the implementation
  plans for each wave, and the audit logs. These are history. Some lines in
  them are out of date now (for example test counts and a hardcoded score that
  was later removed). Read the workflow and profile files above for current
  behavior.

### Changed

**Scripts**
- `scripts/install-skill.py`: the OpenCode and Codex default install paths
  are now `~/.config/opencode/skills` and `~/.agents/skills`. A forced
  replace refuses a target unless it is named `the-polyglot-protocol`, is not
  the source folder or one of its parents, and holds a `SKILL.md`. No longer
  copied: `.git`, `.venv`, caches, `.superpowers`, `node_modules`, `tests/`,
  any `.env*` file, and every `docs/workflow/` file except `dev-workflow.md`,
  `artifact-group-audit-workflow.md`, and `role-resolution.md`.
- `scripts/validate-language-guidance.py`: removed a hardcoded perfect score
  line it printed after every run. The validator checks structure, not
  quality.
- Comments and docstrings in `scripts/score-audit-gate.py`,
  `scripts/validate-workspace.py`, and two test files were rewritten to follow
  the comment rule. The code is identical, which was checked by comparing the
  syntax trees before and after. The scorer's `--help` text is its module
  docstring, so that text changed. One deliberate code change was made in its
  own commit: the validator's top note is now a real module docstring and no
  longer cites `docs/PYTHON.md`, which does not exist.

**Documentation fixes from the round one audit**
- Required paths and skill references that pointed to files or skills that do
  not exist were corrected in `docs/AGENTS.md`, the dev workflow,
  `docs/languages/index.md`, `docs/languages/maintenance-policy.md`, and
  `docs/languages/pre-codegen-checklist.md`.
- `docs/languages/score-report.md` and the readme describe the report as a
  structural check, not a quality score. The `SKILL.md` label is now
  `Current status:`.
- Node.js baselines: the Active LTS pin is now `24.21.0` (was `24.16.0`) and
  npm `11.19.0` (was `11.13.0`) in the language guidelines, the JavaScript and
  TypeScript guides, and the dev workflow.
- A correction section was added to
  `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md`
  listing claims in that earlier entry that were not true.
- Two audit records showed a local home directory. They now use `~/`.

**Language guidance**
- Tooling blocks that failed on a clean checkout were fixed for Swift (lint
  and format commands), C and C++ (configure step), Rust (`cargo test --doc`,
  `cargo install cargo-audit --locked`), Go (`govulncheck`), R
  (`testthat::test_local()`), and Dart (Flutter packages use
  `flutter pub get`). The Zig guide now says not to generate `@cImport`,
  which is deprecated in Zig 0.16 and removed in 0.17.
- Security bullets were added to the HTML, Java, Kotlin, R, and SQL files,
  and tightened after review.
- TypeScript guide: the ESLint baseline uses `@eslint/js@10.0.1` and ignores
  `dist`. The `tsconfig` sets `"types": ["node"]` and adds `rootDir`,
  `outDir`, and `include`. The guide explains `declarationMap`, the `Bundler`
  resolution pairing, and the TypeScript 6.0.x and typescript-eslint peer
  range.
- Python guide: the `pip_audit` command was fixed and the `S101` ignore is
  applied where tests live. An invented `str.masked` example was removed.
  `git clone` uses `--` before untrusted values, and a URL scheme allow-list
  comes before cloning. `requests` is pinned to 2.34.2 (versions before 2.32.4
  have CVE-2024-47081). The scrypt example uses `n=2**17` with
  `maxmem=2**28`, and Argon2id is listed first. The bcrypt 72-byte limit is
  noted, `itertools.batched` and PEP 695 syntax are marked as Python 3.12, and
  Windows batch-file subprocess risks were added. The `secure_delete`
  overwrite example was removed. The guide now says overwriting does not work
  on SSDs or on journaling and snapshot filesystems, and recommends
  encryption at rest.

### Fixed before release

None of the files below existed in a release. These are defects found by
review while building this change and fixed before it ships.

- Scorer bypass: a CRITICAL finding written with decoration (`- FINDING
  CRITICAL ...`, a quote, bold, or a number) was ignored and let the gate
  pass. It now exits `2`. Later commits widened detection (`0f38e5a`,
  `58fdcf5`).
- Scorer crash: a lock file with a non-string `independence` value raised an
  exception. It now exits `2`. Undecodable audit and lock files also exit `2`.
- Profile validator: wrong-typed JSON no longer crashes the check. A profile
  that gives both auditors the same model in `fallback` is an error. The same
  model in `pins` is not checked.
- OpenCode profile: the command used an agent name defined nowhere and a
  `--format json` flag that prints raw events. The profile now documents the
  agents to add to `opencode.json` and requires `mode: "all"`.
- Claude Code profile: the disallowed tools now include Bash and
  NotebookEdit, so read-only roles cannot write files.
- Workspace validator: hidden directories (such as `.git` and
  `.superpowers`) are skipped when checking file names.

### Security

- Read-only auditors: the workflow requires the orchestrator to snapshot the
  working tree before and after each auditor or worker run and to reject the
  run if it changed. This is a procedure in the documents. No script performs
  it yet.
- Guidance fixes above add safer defaults for untrusted input in Python
  (`git clone --`, URL scheme allow-list, password hashing parameters,
  dependency audit command), R, SQL, Java, Kotlin, and HTML.
- Scan on 2026-10-11: no secrets, tokens, or keys in the tracked files at HEAD
  or in the lines this branch adds. The current tree has no machine-specific
  paths. Earlier commits still contain a local home path in a few lines (one
  added by this branch in `8ec4ec5`, a few already on `main`), and commit
  metadata includes the maintainer's author email.

### Not done in this change

- A full version-pin refresh. Only the Node.js LTS and npm baselines and the
  `requests` example pin were updated. The other pins in the P1 table of the
  upgrade plan (Python, Go, Rust, Zig and similar) are unchanged and each
  needs a maintainer decision. Node 24 enters Maintenance on 2026-10-20 and
  the plan proposes re-pinning to Node 26 on 2026-10-28.
- About 1,900 MAJOR and MINOR findings from the per-language audits. Only the
  highest-ranked items were fixed. The individual findings are not recorded
  in the repository.
- De-duplicating the boilerplate that repeats across language files.
- The dynamic role resolver, dispatcher, and qualification probe. The design
  describes them. Today the user or the profile picks the models.
- A dry-run mode and staged replace for the installer.
- A validator check for the comment rule. The rule is applied by review and
  the scoring rubric.
- The GitHub setting for private vulnerability reporting. A maintainer must
  turn it on in the repository settings.

### Known limits

- This branch was not put through its own gate. The audit log
  `docs/workflow/model-agnostic-roles-audits.md` records the gate as `N/A`
  for these groups. Per-task and whole-branch reviews stood in. The only gate
  run on record is round 1 on the repository before these fixes, and the fixes
  were not re-scored.
- The scorer rejects a decorated line only when it contains `VERDICT`,
  `TOTAL`, or `FINDING` with a capital severity word. A CRITICAL finding
  written without the word `FINDING` (for example `- CRITICAL: a:1 text`),
  with a lowercase severity, or in mixed case is treated as prose and is not
  caught. The step where a worker greps the auditor output for CRITICAL lines
  and the orchestrator reads them is the backstop.
- Degraded independence reduces how independent the two audits are. The log
  says so and the pass mark is higher, but it is not equal to two model
  families.
- Profiles hold dated facts about harnesses. The validator warns when
  `verified_on` is more than 30 days old. A project profile at
  `.polyglot/profile.md` is not validated yet.
- `SKILL.md` says model names live only in `profiles/`. Model and harness
  names also appear in the design record and the harness table. The validator
  checks only `SKILL.md`, the dev workflow, and the audit workflow.
- The installed copy does not include `model-agnostic-roles-design.md`, which
  `role-resolution.md` mentions.
- The Go guide uses `govulncheck@latest`, a floating tag.
- Pre-existing inconsistencies that were not changed: `docs/AGENTS.md` still
  says the workspace has no source or test directories, and
  `docs/languages/python/python.md` says not to use `unittest.TestCase` while
  all three test files use `unittest`.
- Guidance changes were checked against primary sources and reviewed.
  Examples were not built or run as a test matrix.
