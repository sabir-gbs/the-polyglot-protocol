# Model-Agnostic Roles Audit Log

Date: 2026-10-11
Branch: `feat/model-agnostic-roles` (HEAD `a4c9637`)
Scope: Plan A of model-agnostic audit roles (Tasks 1-5 implementation, Task 6 verification and this log).

This log records real evidence only. It does not claim a score. See "Deviations" for what was not run.

## Commits

Output of `git log --oneline 937671165..HEAD`:

```text
a4c9637 Collapse adapters to point at SKILL.md and profiles
9f7554d Make audit workflow roles capability-based and model-neutral
94437b2 Add role resolution and harness reference
c3d25cf Skip hidden directories when checking workspace filenames
7846d4d Add profile format, validator checks, and default profiles
b6d0f82 Reject undecodable auditor and lock files with exit 2
7fe3df5 Harden audit gate scorer and add degraded independence mode
```

## Verification

Run from the repository root on 2026-10-11, before this log was committed.

### Scorer tests

```text
$ python -B tests/test-score-audit-gate.py 2>&1 | tail -3
Ran 31 tests in 0.013s

OK
```

### Validator tests

```text
$ python -B tests/test-validate-workspace.py 2>&1 | tail -3
Ran 14 tests in 0.001s

OK
```

### Workspace validator

```text
$ python -B scripts/validate-workspace.py 2>&1 | tail -6
language guidance validation: PASS
language files: 22
language readmes: 22
operational files: 11
score: 100/100
workspace validation: PASS
exit=0
```

The `score: 100/100` line is hardcoded validator output (upgrade plan P0-10), not an audit score for this change.

### Diff check

```text
$ git diff --check && echo "diff-check: clean"
diff-check: clean
```

### Gate re-score of a real round 1 pair (G6)

The hardened scorer was run against two real round 1 auditor outputs from the scratchpad, with `--independence full`.

```text
$ python -B scripts/score-audit-gate.py out-sol-G6.txt out-opus-G6.txt --independence full; echo exit=$?
out-sol-G6.txt: re-added total 72/100
  CRITICAL docs/languages/swift.md:18 Bare `swift format` reads standard input instead of formatting project files and can wait indefinitely -> supply explicit source paths, e.g. `swift format --in-place --recursive Sources Tests`; exclude generated/dependency directories ([official formatter documentation](https://github.com/swiftlang/swift-format#command-line-usage)).
out-opus-G6.txt: re-added total 68/100
mean: 70.0/100 threshold: 85
GATE: FAIL (independence=full, threshold=85)
exit=1
```

Result matches the expected `GATE: FAIL` and `exit=1`. Mean `70.0` matches the earlier mean. No `invalid input:` line was printed: both real auditor outputs parse under the hardened scorer.

## Per-task review

Built from the SDD ledger (`.superpowers/sdd/model-agnostic-roles-implementation-plan/progress.md`). Per-task review was done by a reviewer subagent separate from the implementer.

| Task | Implementer commits | Spec compliant | Quality | Critical / Important / Minor | Fix rounds | Outcome |
|---|---|---|---|---|---|---|
| 1. Scorer hardening and degraded independence | `7fe3df5`, fix `b6d0f82` | Yes | No quality verdict stated in the ledger; review recorded clean after the fix | 0 / 1 / 4 (the ledger lists four deferred minor entries; the fourth was added after the fix round) | 1 of 5 (1 addressed, 0 open) | Complete. Important finding: `UnicodeDecodeError` exited 1 instead of 2; fixed in `b6d0f82` (31 tests passing). |
| 2. Profile format and validator checks | `7846d4d`, fix `c3d25cf` | Yes | Approved | 0 / 0 / 7 | 1 of 5 (ruling-based fix: skip hidden directories; 14 tests passing) | Complete. Implementer reported DONE_WITH_CONCERNS: the intended model-name check failed until Task 4. |
| 3. Role resolution and harness reference | `94437b2` | Yes (byte-identical to brief) | Approved | 0 / 0 / 7 | 0 | Complete. |
| 4. Capability-based, model-neutral audit workflow | `9f7554d` | Yes (five files verbatim to brief) | Approved | 0 / 0 / 6 | 0 | Complete. Validator PASS; model-neutral grep clean. |
| 5. Adapters collapse | `a4c9637` | Yes (six files verbatim) | Approved | 0 / 1 (out of diff, pre-existing) / 5 | 0 | Complete. The Important finding is upgrade plan P0-1, left to that plan. |

Notes on counts: the Task 2, 3, 4 and 5 counts are the numbers the ledger states. The Task 1 Minor count is the number of deferred entries the ledger lists, because the ledger gives no numeric total for Task 1.

## Deferred findings

Copied verbatim from the ledger, grouped by task. Entries the ledger marks "worth fixing before merge" are flagged.


### Task 1

- Task 1: minor (deferred): indented or bulleted FINDING/VERDICT lines are silently ignored (RESERVED_RE anchored at column 0)
- Task 1: minor (deferred): a degraded lock with no `roles` map skips the same-model check (spec wants two different models)
- Task 1: minor (deferred): diagnostics go to stdout not stderr; repeated TOTAL line accepted (last wins); load_lock returns an unused second tuple element; coverage gaps (threshold 100 accepted, flag==lock accepted, non-dict lock, argparse usage error)
- Task 1: minor (deferred, same class as the fixed finding — include in final fix wave): lock with unhashable `independence` (e.g. [] or {}) raises TypeError in load_lock (`mode not in THRESHOLDS`), exit 1 + traceback; fix with isinstance(mode, str) check + test

### Task 2

- Task 2: minor (deferred, real validator false-pass): validate_profile ignores wrong-typed constraints/fallback/harnesses/pins (returns ([], []) for strings or lists)
- Task 2: minor (deferred): unhashable fallback harness value raises TypeError (entry["harness"] not in harnesses); guard with isinstance(str)
- Task 2: minor (deferred): harness command/roles not validated ({model}/{prompt_file} placeholders, roles in ROLES); extra fallback roles accepted despite test name "exactly four"; pins keys not checked; future verified_on gives no warning
- Task 2: minor (deferred): MODEL_NAME_RE has no word boundaries, is case-sensitive, omits Claude/Codex/MiniMax; matches inside ordinary words (GLMs, Opuscule)
- Task 2: minor (deferred): .polyglot/profile.md override not validated; sources not type-checked and default.md has a non-URL source; template.md fixed verified_on will warn forever
- Task 2: minor (deferred): hidden-directory skip also exempts tracked hidden dirs (.github/, .claude/) from filename checks — accepted trade-off, revisit if a tracked hidden dir gains markdown

### Task 3

- Task 3: minor (deferred, worth fixing before merge): role-resolution.md drops two spec details that affect behavior — OpenCode `mode: "subagent"` silently falls back to the default agent (read-only lost), and Antigravity `plan` mode uses read-only tools; also drops "single-family harness needs a second harness or degraded mode" **[WORTH FIXING BEFORE MERGE]**
- Task 3: minor (deferred): present-tense "is tested / is probed" while no resolver exists; validator described as covering .polyglot/profile.md but it only globs profiles/*.md; "named profile" undefined; {output_file} placeholder used by default.md not documented; fixed-model phrase wraps a line

### Task 4

- Task 4: minor (deferred, worth fixing before merge): workflow doc step 4 never says omitting --lock/--independence defaults to full (85) — a degraded run of the bare command gets the lenient bar; lock wins and conflicting --independence exits 2 also unstated **[WORTH FIXING BEFORE MERGE]**
- Task 4: minor (deferred, worth fixing before merge): N/A And Blocker Rules still say "auditor model unavailable -> stop the gate" without reconciling with degraded mode (losing the second family should degrade, only lacking two different models is a blocker) **[WORTH FIXING BEFORE MERGE]**
- Task 4: minor (deferred): Auditor Output Contract's "invalid" definition not widened to malformed lines / mismatched criterion names; "deterministic checks" not named (python scripts/validate-workspace.py); Audit Log Requirements lack independence mode and lock/profile; step 1 reflow left a short line

### Task 5

- Task 5: minor (deferred): "in the installed skill folder" gives no locator (folder name appears nowhere); validate command assumes cwd is skill root; mode:"all" rationale omitted and undated

Task 1 also carries one entry the ledger marks "include in final fix wave" (unhashable `independence` in a lock file). It is open.

## Rulings

Copied verbatim from the ledger.

- Ruling: Task 2 commit leaves `validate-workspace.py` red on purpose (model-neutral check) until Task 4 — the plan states this and the spec requires the check; tasks 2-4 run back to back — costs one intermediate failing commit if wrong.
- Ruling: `.superpowers/` excluded via .git/info/exclude (local only, not committed) — workspace was not git-ignored and implementers commit specific paths — costs nothing; reversible by deleting the line.
- Ruling: Tasks 1 Step 5 and 6 Step 2 read real round 1 outputs from the scratchpad path above (absolute) — the plan wrote `<scratchpad>` — costs a path correction if the directory is gone.
- Ruling: check_files() walks hidden dirs and trips on the git-ignored .superpowers/ scratch (digit filenames), which would break the PASS expectations in Tasks 4 and 6 — fix by skipping hidden directories in check_files (+ test); this also closes the round 1 G7 finding about .pytest_cache — dispatched as a ruling-based fix after Task 2's review — costs one small extra diff if wrong; reversible.
- Task 5: Ruling: reviewer's Important — adapters/opencode/readme.md now documents ~/.config/opencode/skills while scripts/install-skill.py:13 and readme.md:166 still install to ~/.opencode/skills (skill never loads) — is upgrade plan P0-1 (installer), pre-existing and outside Plan A's file list; left to that plan and flagged in the final summary — costs: OpenCode users following the root readme still get a non-loading install until P0-1 lands
- Ruling: Task 6 Step 3 asks for three-round planning/coding/guidance-file audit tables; a subagent cannot honestly produce independent three-round scores. The audit log instead records the real evidence — per-task SDD review verdicts, commands with output, deferred minors, rulings — and states plainly that the three-round loops in dev-workflow.md were NOT run as such (deviation). Costs: the dev-workflow audit-loop requirement is unmet for this run and says so.

## Deviations

- The three-round planning, coding, and guidance-file audit loops required by `docs/workflow/dev-workflow.md` were not run as such for this change. Per-task subagent review (spec compliance and quality) stood in for them. A final whole-branch review is planned but had not been run when this log was written. No audit score is claimed for this change.
- The dynamic resolver, dispatcher, and qualification fixture (Plan B) are not implemented. Roles are documented and the scorer enforces independence mode, but nothing resolves profiles or dispatches auditors automatically, and read-only auditing is documented rather than enforced by a snapshot.
- `score: 100/100` in the workspace validator output is hardcoded and pre-existing (upgrade plan P0-10). It is not evidence of an audit score.
- The installer OpenCode default path defect (upgrade plan P0-1) is untouched: `scripts/install-skill.py` and the root readme still install to `~/.opencode/skills` while the OpenCode adapter readme documents `~/.config/opencode/skills`.
- The deferred findings above are open. Three of them (one for Task 3, two for Task 4) are flagged as worth fixing before merge.
- The dual-auditor gate required by `SKILL.md` step 9 was not run on this branch's own artifact groups. This is N/A: no auditor dispatch was performed for Plan A. Per-task subagent review and the final whole-branch review stood in for it.
- The final whole-branch review found one Critical issue (the scorer ignored indented, bulleted, quoted, or bold `FINDING`, `VERDICT`, and `TOTAL` lines, so a decorated `CRITICAL` finding passed the gate), several Important issues (a lock file with a non-string `independence` crashed the scorer; the profile validator accepted wrong-typed containers, crashed on a list-valued harness, and allowed one model for both auditors; the OpenCode profile used an undefined `{agent}` placeholder and `--format json`; the Claude Code command left `Bash` and `NotebookEdit` able to write), and document inconsistencies with the scorer and degraded mode. A fix wave addressed them in three commits: A (scorer), B (profile validator and profiles), and C (workflow documents). That wave closes the deferred Task 1 and Task 2 findings about decorated lines, unhashable `independence`, and unvalidated profile structure, and the three findings flagged worth fixing before merge.

## Final-pass checklist

| Item | Status |
|---|---|
| Scorer tests (`tests/test-score-audit-gate.py`) | Pass, 31 tests |
| Validator tests (`tests/test-validate-workspace.py`) | Pass, 14 tests |
| `python scripts/validate-workspace.py` | `workspace validation: PASS` |
| `git diff --check` | Clean |
| Gate re-score of real round 1 pair | `GATE: FAIL (independence=full, threshold=85)`, exit 1, mean 70.0, as expected |
| Three-round audit loops | Not run as such (see Deviations) |
| Docker | N/A, docs and tooling-only change |
| Lighthouse | N/A, docs and tooling-only change |
| CloakBrowser | N/A, docs and tooling-only change |
| Deployment | Nothing deployed |
| Upgrade plan P0-13 | Marked done in `docs/workflow/polyglot-protocol-upgrade-plan.md` |
| Commit | Committed locally on `feat/model-agnostic-roles`; not pushed because `GITHUB_PAT` is not set (`echo ${GITHUB_PAT:+set}` printed nothing) |
