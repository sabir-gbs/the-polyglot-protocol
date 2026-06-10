## Unreleased

### Added

- **Packaged skill language guidance coverage**: Running `python scripts/validate-workspace.py` from the workspace root now also executes the full language contract validation (required sections, senior labels, final guardrails, etc.) against the copy inside `the-polyglot-protocol/docs/languages/`. Output is clearly prefixed with `--- packaged skill language guidance ---`.
- **Skill package sync guard**: Added `check_skill_package_sync()` which automatically detects byte-level drift between the authoritative root validator scripts and the copies inside `the-polyglot-protocol/scripts/`. Drift now causes validation to fail.

### Changed

- **Validator script docstrings**: Both `validate-workspace.py` and `validate-language-guidance.py` (root and packaged copies) now use strict Google-style docstrings as required by `docs/PYTHON.md`:
  - Clear purpose and description
  - `Args:` sections (with types)
  - `Returns:` sections (including side effects)
  - `Raises:` sections
  - Explicit `Time complexity:` and `Space complexity:` for all functions containing loops, tree walks, content scanning, or comparisons
- These changes also apply to the mirrored copies inside the `the-polyglot-protocol/` skill package so that standalone users of the skill receive the same improvements.

### Documentation

- Created the full set of formal workflow artifacts required by `dev-workflow.md` for this guidance-related change:
  - `validate-scripts-packaged-skill-coverage-plan.md`
  - `validate-scripts-packaged-skill-coverage-implementation-plan.md`
  - `validate-scripts-packaged-skill-coverage-execution-plan.md`
  - `validate-scripts-packaged-skill-coverage-audits.md` (includes 3 rounds of planning, coding, and guidance-file audits, all reaching 100/100 on round 3)
- The previous combined summary (`validate-scripts-packaged-skill-coverage.md`) has been marked as superseded with pointers to the new formal artifacts.

### Files Changed

**Scripts (root + packaged sync):**
- `scripts/validate-workspace.py`
- `scripts/validate-language-guidance.py`
- `the-polyglot-protocol/scripts/validate-workspace.py`
- `the-polyglot-protocol/scripts/validate-language-guidance.py`

**New workflow artifacts:**
- `docs/workflow/validate-scripts-packaged-skill-coverage-plan.md`
- `docs/workflow/validate-scripts-packaged-skill-coverage-implementation-plan.md`
- `docs/workflow/validate-scripts-packaged-skill-coverage-execution-plan.md`
- `docs/workflow/validate-scripts-packaged-skill-coverage-audits.md`

**Updated historical file:**
- `docs/workflow/validate-scripts-packaged-skill-coverage.md` (superseded notice + pointers added)

### Verification

All changes were verified by re-running the skill's own validation from both contexts, plus the project's declared Python quality gates:

```sh
python scripts/validate-workspace.py
(cd the-polyglot-protocol && python scripts/validate-workspace.py)

.venv/bin/python -m ruff check ...
.venv/bin/python -m ruff format --check ...
.venv/bin/python -m mypy --strict ...
```

**Final results:**
- Both root and packaged-context runs: `language guidance validation: PASS` (22 files, 11 operational, score 100/100) + `workspace validation: PASS`
- Root run now surfaces the packaged skill language section
- ruff + mypy: clean
- Packaged script copies remain byte-identical to root

### Impact for Users of the `the-polyglot-protocol` Skill

- When using the skill **standalone** (vendored `the-polyglot-protocol/` directory): Validators are now better self-documented and the packaged language guidance receives the same deep contract checks.
- When a **host workspace** runs its root validators against a directory containing the skill: The root validator will now also audit the skill's `docs/languages/` content and will fail if the script copies have drifted.
- No breaking changes. Existing behavior is preserved or strengthened.

### Notes

- This work was itself reviewed using the `the-polyglot-protocol` skill (following its required workflow of reading `dev-workflow.md`, `PYTHON.md`, checklists, policies, and running its validator).
- Backups of the original script versions are available in the source repository under `backups/validate-scripts-pre-fix/` for anyone who needs to revert.
- Full details, audit scoring, and reproducible commands are available in the formal workflow artifacts listed above.

**Detailed notes and CHANGELOG-style entry for this change.**
