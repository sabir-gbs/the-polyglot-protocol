# Round One P0 Fixes Implementation Plan (Wave 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the round 1 P0 findings that live outside the language guidance files: the installer, broken required paths, nonexistent skills, false score claims, and the false changelog entry.

**Architecture:** Six tasks. Task 4 runs first. Task 5 (comment pass) runs after Tasks 1, 3 and 4. Task 6 (basic rule and comment rule in the protocol's guidance) runs last. Task 7 is optional hardening and is not planned. Task 1 rewrites `scripts/install-skill.py` as an allowlist installer with target guards, staged replacement, and `--dry-run`, with tests, and updates the readme install section. Task 2 applies exact text replacements to documents. Task 3 removes the hardcoded score and corrects the changelog entry.

**Tech Stack:** Python 3.14 standard library (`argparse`, `shutil`, `pathlib`, `unittest`, `subprocess`), Markdown.

**Spec:** `docs/workflow/polyglot-protocol-upgrade-plan.md` (items P0-1 to P0-11, P0-13 already done in Plan A). Wave 2 (language guidance files P0-14 to P0-25) is a separate plan, written after the per-language `sol-auditor` runs finish so those runs are not invalidated.

## Global Constraints

- Default operational scripts to Python; standard library only; no new dependency.
- Filenames are kebab-case with no digits or dates.
- Do not claim `100/100` as a measured score anywhere. A requirement that an audit target `100/100` is not a claim and stays.
- Validators report `PASS` or `FAIL`.
- Do not touch any file under `docs/languages/<language>.md`, `docs/languages/<language>/`, or the deep guides. Those belong to Wave 2.
- Tests are `unittest` files named `tests/test-*.py` and run as `python tests/<file>`.
- Code comments and docstrings use plain US English at about a 6th grade reading level.
  Technical terms are fine. Say why, not what. No filler, hype, edit narration, banners,
  or emoji. Banned in comments: "note that", "it's worth noting", "importantly",
  "robust", "seamless", "leverage", "comprehensive", "ensure that", "simply".
  Keep sentences under about 20 words. Every code-writing dispatch repeats this rule.
- `python -B scripts/validate-workspace.py` must end with `workspace validation: PASS` at the end of every task.
- Installer: a refusal raises `SystemExit` with a message (exit `1`), as the existing script does.

## Out Of Scope

- P0-12 (`security.md` private reporting) is a GitHub repository setting. No file change is correct until it is enabled. The maintainer enables it in Settings, Code security, Private vulnerability reporting.
- Language-file items P0-14 to P0-25 (Wave 2).

## File Structure

| File | Responsibility |
|---|---|
| `scripts/install-skill.py` | Correct target paths, guard on force replace, skip junk |
| `tests/test-install-skill.py` | Five tests: paths, junk skipped, force guards, installed copy validates |
| `readme.md` | Install commands, quick start, validation output, project status |
| `docs/languages/index.md`, `maintenance-policy.md`, `pre-codegen-checklist.md`, `docs/AGENTS.md`, `docs/workflow/dev-workflow.md`, `SKILL.md` | Path and skill-name corrections |
| `scripts/validate-language-guidance.py` | Remove the hardcoded score |
| `contributing.md`, `docs/languages/score-report.md` | Remove the score claim |
| `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md` | Dated correction note |

---

### Task 1: Fix installer target paths, guard force replace, skip junk files

Minimal path. Desired effects, and only these:

- E1: `--agent opencode` and `--agent codex` install where those agents load skills.
- E2: `--force` can never delete an unrelated directory.
- E3: the installed copy has no secrets, caches, run scratch, tests, or plan and audit logs.
- E4: the readme one-liners work on a second run.

Targeted edits to the existing `scripts/install-skill.py`. No `--dry-run`, no staging
directory, no backup, no allowlist, no new flags. Accepted residual: a copy that fails
halfway leaves a partial install, and re-running with `--force` fixes it.

**Files:**
- Modify: `scripts/install-skill.py` (targeted edits)
- Create: `tests/test-install-skill.py` (five tests)
- Modify: `readme.md` (Quick Start and One-Line Install only)

**Interfaces:**
- Consumes: the existing `copy_project(target, *, force)`, `DEFAULT_TARGETS`, `EXCLUDES`.
- Produces: the same CLI; `copy_project` raises `SystemExit` when a replace is unsafe.

- [ ] **Step 1: Write the failing tests**

Create `tests/test-install-skill.py`:

```python
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("install_skill", ROOT / "scripts" / "install-skill.py")
assert SPEC is not None and SPEC.loader is not None
INSTALL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = INSTALL
SPEC.loader.exec_module(INSTALL)

NAME = "the-polyglot-protocol"


class InstallSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name).resolve()
        self.target = self.base / "skills" / NAME

    def test_default_targets_use_the_paths_agents_read(self) -> None:
        targets = {k: v.as_posix() for k, v in INSTALL.DEFAULT_TARGETS.items()}
        self.assertTrue(targets["opencode"].endswith(f".config/opencode/skills/{NAME}"))
        self.assertTrue(targets["codex"].endswith(f".agents/skills/{NAME}"))

    def test_copy_skips_tests_scratch_and_run_logs(self) -> None:
        INSTALL.copy_project(self.target, force=False)
        self.assertFalse((self.target / "tests").exists())
        self.assertFalse((self.target / ".superpowers").exists())
        kept = sorted(p.name for p in (self.target / "docs" / "workflow").iterdir())
        self.assertEqual(
            kept,
            ["artifact-group-audit-workflow.md", "dev-workflow.md", "role-resolution.md"],
        )

    def test_force_refuses_a_directory_that_is_not_a_skill_install(self) -> None:
        self.target.mkdir(parents=True)
        (self.target / "keep.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(SystemExit):
            INSTALL.copy_project(self.target, force=True)
        self.assertTrue((self.target / "keep.txt").exists())

    def test_force_refuses_wrong_name_and_the_source_tree(self) -> None:
        other = self.base / "other"
        other.mkdir()
        for bad in (other, ROOT, ROOT.parent):
            with self.subTest(target=str(bad)):
                with self.assertRaises(SystemExit):
                    INSTALL.copy_project(bad, force=True)

    def test_installed_copy_validates_itself(self) -> None:
        INSTALL.copy_project(self.target, force=False)
        result = subprocess.run(
            [sys.executable, "-B", "scripts/validate-workspace.py"],
            cwd=self.target, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("workspace validation: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -B tests/test-install-skill.py 2>&1 | tail -8`
Expected: FAIL. The path test fails on the old defaults, and the copy test finds `tests` in the copy.

- [ ] **Step 3: Make the edits to `scripts/install-skill.py`**

1. In `DEFAULT_TARGETS`, set `codex` to `Path.home() / ".agents" / "skills" / "the-polyglot-protocol"` and `opencode` to `Path.home() / ".config" / "opencode" / "skills" / "the-polyglot-protocol"`. Leave `claude-code` alone.
2. Add `SKILL_NAME = "the-polyglot-protocol"` near the top, and extend `EXCLUDES` with `".superpowers"`, `"tests"`, `".pytest_cache"`, `".mypy_cache"`, `".ruff_cache"`, `"node_modules"`.
3. Add `WORKFLOW_KEEP = {"dev-workflow.md", "artifact-group-audit-workflow.md", "role-resolution.md"}`.
4. Replace the `ignore` function inside `copy_project` with:

```python
    def ignore(directory: str, names: list[str]) -> set[str]:
        skip = {n for n in names if n in EXCLUDES or n.startswith(".env")}
        if Path(directory).name == "workflow":
            skip |= {n for n in names if n not in WORKFLOW_KEEP}
        return skip
```

5. Add this function above `copy_project`, and call `check_replace_target(target)` right before the existing `shutil.rmtree(target)` (inside the branch where the target exists and `force` is set):

```python
def check_replace_target(target: Path) -> None:
    """Refuse to delete a directory that is not an earlier install of this skill."""
    resolved = target.resolve()
    if resolved.name != SKILL_NAME:
        raise SystemExit(f"refusing to replace {resolved}: its name must be {SKILL_NAME}")
    if resolved == ROOT or ROOT.is_relative_to(resolved):
        raise SystemExit(f"refusing to replace {resolved}: it holds the source repository")
    if not (resolved / "SKILL.md").is_file():
        raise SystemExit(f"refusing to replace {resolved}: no SKILL.md, so it is not an earlier install")
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -B tests/test-install-skill.py 2>&1 | tail -4`
Expected: `Ran 5 tests` and `OK`. If `test_installed_copy_validates_itself` fails because an excluded file is read by the validator, remove only that name from the exclusion and report which one.

- [ ] **Step 5: Edit the readme**

In `readme.md`, replace the Quick Start sentence about copying an adapter with:

```markdown
Use the skill folder directly from an agent that supports local skill folders,
or install it with the commands below. Install the whole skill folder. Adapter
files link to `SKILL.md` and `profiles/`, so an adapter copied on its own
cannot find them.
```

Replace each one-line install so it clones into a fresh temporary directory and does not use `--force`. The Codex one becomes:

```sh
d=$(mktemp -d) && git clone https://github.com/sabir-gbs/the-polyglot-protocol.git "$d" && python "$d/scripts/install-skill.py" --agent codex
```

Do the same for `claude-code`, `opencode`, and the custom `--target` form. After the commands add:

```markdown
Add `--force` to replace an existing install. It only replaces a previous
install of this skill, and the target directory must be named
`the-polyglot-protocol`. On Windows, create a directory yourself instead of
using `$(mktemp -d)`.
```

- [ ] **Step 6: Verify**

Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.
Run: `python -B scripts/install-skill.py --target /tmp/skills --force; echo exit=$?`
Expected: a refusal message and a non-zero exit (no directory is touched).

- [ ] **Step 7: Commit**

```bash
git add scripts/install-skill.py tests/test-install-skill.py readme.md
git commit -m "Fix installer target paths, guard force replace, and skip junk files"
```

---

### Task 2: Broken required paths and nonexistent skills

**Files:**
- Modify: `docs/languages/index.md`, `docs/languages/maintenance-policy.md`, `docs/languages/pre-codegen-checklist.md`, `docs/AGENTS.md`, `docs/workflow/dev-workflow.md`, `SKILL.md`

**Interfaces:**
- Consumes: nothing.
- Produces: corrected references. No code interfaces.

Apply each replacement exactly once. If an old string is not found exactly once in its file, stop and report BLOCKED with the text you searched for.

- [ ] **Step 1: `docs/languages/index.md`**

Replace `` `../../language-guidelines.md` `` with `` `../language-guidelines.md` ``.

- [ ] **Step 2: `docs/languages/maintenance-policy.md`**

Replace `- Update \`language-guidelines.md\` when language selection or default policy` with `- Update \`docs/language-guidelines.md\` when language selection or default policy`.

- [ ] **Step 3: `docs/languages/pre-codegen-checklist.md`**

Replace `3. Read \`language-guidelines.md\`.` with `3. Read \`docs/language-guidelines.md\`.`

- [ ] **Step 4: `docs/AGENTS.md`**

Replace every occurrence of `` `language-guidelines.md` `` that is not already preceded by `docs/` with `` `docs/language-guidelines.md` `` (three occurrences: the index bullet, the "Check guidance" paragraph, and the Python script-language paragraph). Do not touch `../../language-guidelines.md` forms anywhere.

- [ ] **Step 5: `docs/workflow/dev-workflow.md`**

Make these four replacements:

1. `5. \`language-guidelines.md\`` becomes `5. \`docs/language-guidelines.md\``
2. `- Use \`language-guidelines.md\` whenever the request involves language choice,` becomes `- Use \`docs/language-guidelines.md\` whenever the request involves language choice,`
3. `8. \`CLAUDE.md\`` becomes `8. \`adapters/claude-code/CLAUDE.md\``
4. In the Guidance-File Audit Loop sentence, `` `AGENTS.md`, `CLAUDE.md`, or another `` becomes `` `AGENTS.md`, `adapters/claude-code/CLAUDE.md`, or another ``

Then fix the nonexistent skills:

5. Replace `` `requesting-code-review`, `benchmark`, `qa`, and related workflow skills. `` with `` `requesting-code-review`, and related workflow skills. ``
6. Replace `- Use the superpowers QA workflow for frontend validation.` with `- Use the \`verification-before-completion\` skill and the CloakBrowser checks below for frontend validation.`

- [ ] **Step 6: `SKILL.md`**

Replace this exact block:

````markdown
10. Run validation when this skill folder is available:

```sh
python scripts/validate-workspace.py
```
````

with:

````markdown
10. Run validation from the skill root (the folder that contains this file). It
    checks the protocol repository itself, not the project you are generating
    code for:

```sh
python scripts/validate-workspace.py
```
````

- [ ] **Step 7: Verify**

Run: `grep -rnE "(^|[^/a-z-])language-guidelines\.md" docs/AGENTS.md docs/workflow/dev-workflow.md docs/languages/pre-codegen-checklist.md docs/languages/maintenance-policy.md docs/languages/index.md | grep -v "docs/language-guidelines.md" || echo "no bare references"`
Expected: `no bare references`.
Run: `grep -nE "\`benchmark\`|\`qa\`|superpowers QA" docs/workflow/dev-workflow.md || echo "no nonexistent skills"`
Expected: `no nonexistent skills`.
Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.

- [ ] **Step 8: Commit**

```bash
git add docs/languages/index.md docs/languages/maintenance-policy.md docs/languages/pre-codegen-checklist.md docs/AGENTS.md docs/workflow/dev-workflow.md SKILL.md
git commit -m "Fix broken required paths and nonexistent skill references"
```

---

### Task 3: Remove the hardcoded score claim and correct the changelog entry

Minimal path. Desired effects: the validator no longer prints a score it did not
compute, no document presents it as a measured score, and the false changelog claims
are corrected. No new test file: the grep below proves the effect.

**Files:**
- Modify: `scripts/validate-language-guidance.py`, `readme.md`, `contributing.md`, `docs/languages/score-report.md`, `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md`

**Interfaces:**
- Consumes: nothing.
- Produces: a validator that prints `PASS` or `FAIL` with counts and no numeric score.

- [ ] **Step 1: Remove the score line**

In `scripts/validate-language-guidance.py`, delete the line `    print("score: 100/100")` and nothing else.

- [ ] **Step 2: Update the documents**

`readme.md`: in the "Expected result" text block, delete the line `score: 100/100` (keep the other five lines). Replace `Current validation score: \`100/100\`.` with:

```markdown
Current validation status: structural checks `PASS` (22 language files, 22
language readmes, 11 operational files). This is a structural check, not a
rubric score. Rubric scores are recorded per audit under `docs/workflow/`.
```

`contributing.md`: replace `Do not submit changes that reduce the validation score below \`100/100\`.` with `Do not submit changes that make \`python scripts/validate-workspace.py\` fail.`

`docs/languages/score-report.md`: replace the two lines

```markdown
## Current Status

Score: `100/100`
```

with

```markdown
## Current Status

Structural validation: `PASS`. This is a structural check, not a rubric score.
```

Leave `SKILL.md` and `dev-workflow.md` alone: their `100/100` is the audit target, which is a requirement, not a claim.

- [ ] **Step 3: Correct the changelog entry**

Append this section to the end of `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md`:

```markdown

## Correction (2026-10-11)

Checked against the repository on 2026-10-11, several statements above are not
true. They stay for history and are corrected here.

- **Docstrings.** The entry says `validate-workspace.py` and
  `validate-language-guidance.py` use strict Google-style docstrings with
  `Args:`, `Returns:`, `Raises:` and complexity sections.
  `validate-language-guidance.py` has no docstrings. In `validate-workspace.py`
  the module docstring sits after the imports, so Python does not use it.
- **Packaged copy.** The entry describes a `the-polyglot-protocol/` skill
  package and sync checks against it. That directory has never existed in this
  repository's git history (`git log --all -- 'the-polyglot-protocol/*'` is
  empty), so those checks never run.
- **Standard.** The entry cites `docs/PYTHON.md`. That file does not exist. The
  Python guidance is `docs/languages/python/python.md`.
- **Verification command.** The entry lists
  `(cd the-polyglot-protocol && python scripts/validate-workspace.py)` as run.
  That cannot have run, because the directory does not exist.
- **Audit scores.** The `100/100` results in the sibling artifacts for this
  change are not supported by the evidence above. Do not rely on them.
```

- [ ] **Step 4: Verify**

Run: `python -B scripts/validate-language-guidance.py | grep -c "100/100"`
Expected: `0`.
Run: `grep -rn "100/100" readme.md contributing.md docs/languages/score-report.md scripts/validate-language-guidance.py || echo "no score claims"`
Expected: `no score claims`.
Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate-language-guidance.py readme.md contributing.md docs/languages/score-report.md docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md
git commit -m "Remove hardcoded validator score and correct false changelog claims"
```

---

### Task 4: Close the scorer decoration bypass and fix stale audit-log lines

Carried from the Plan A whole-branch re-review (Important, load-bearing): the scorer
treats a contract line as reserved only when it is decorated with characters from a
fixed list, so a CRITICAL finding written as `1. **FINDING CRITICAL**`, `+ FINDING ...`,
`1) FINDING ...`, a bullet `•`, a table row, brackets, parentheses, an emoji prefix, or
`_FINDING_` is silently ignored and the gate can PASS. Run this task FIRST.

**Files:**
- Modify: `scripts/score-audit-gate.py` (the `RESERVED_RE` constant only, and a comment if needed)
- Modify: `tests/test-score-audit-gate.py` (add tests)
- Modify: `docs/workflow/model-agnostic-roles-audits.md` (stale statements only)

**Interfaces:**
- Consumes: the existing decorated-line handling in `parse_audit` (a line that matches `RESERVED_RE` but does not begin with the keyword at column 0 raises `InvalidInputError`, exit 2).
- Produces: the same CLI and exit codes; a stricter detector.

- [ ] **Step 1: Write the failing tests**

Add these tests to `ScoreAuditGateTest` in `tests/test-score-audit-gate.py`:

```python
    def test_exotic_decorations_of_contract_lines_are_invalid(self) -> None:
        decorated = [
            "+ FINDING CRITICAL a.md:3 x",
            "1. **FINDING CRITICAL** a.md:3 x",
            "1) FINDING CRITICAL a.md:3 x",
            "\u2022 FINDING CRITICAL a.md:3 x",
            "| FINDING CRITICAL | a.md:3 | x |",
            "(FINDING CRITICAL a.md:3 x)",
            "[FINDING CRITICAL] a.md:3 x",
            "\u26a0\ufe0f FINDING CRITICAL a.md:3 x",
            "_FINDING CRITICAL_ a.md:3 x",
            "- TOTAL: 100/100",
            "> VERDICT extra: 10/10",
        ]
        for line in decorated:
            with self.subTest(line=line):
                text = audit_text([10] * 10) + line + "\n"
                self.assertEqual(self.run_gate(text, audit_text([10] * 10))[0], INVALID_CODE)

    def test_ordinary_prose_that_mentions_the_words_is_ignored(self) -> None:
        prose = [
            "VERDICTS above were checked twice.",
            "TOTALLY fine.",
            "- Finding the root cause took a while.",
            "1. Total cost was low.",
            "**Total** effort was small.",
            "Note: the finding list is above.",
        ]
        text = audit_text([10] * 10) + "\n".join(prose) + "\n"
        self.assertEqual(self.run_gate(text, audit_text([10] * 10))[0], PASS_CODE)
```

- [ ] **Step 2: Run them to verify the first fails**

Run: `python -B tests/test-score-audit-gate.py 2>&1 | tail -8`
Expected: FAIL in `test_exotic_decorations_of_contract_lines_are_invalid` for the decorations not in the current list (for example `+ FINDING`, `1. **FINDING CRITICAL**`).

- [ ] **Step 3: Change the detector**

In `scripts/score-audit-gate.py` replace the `RESERVED_RE` definition with:

```python
RESERVED_RE = re.compile(r"^(?:[\W_]|\d+[.)])*(VERDICT|TOTAL|FINDING)\b")
```

This treats any run of non-word characters, underscores, and numeric list markers before an ALL-CAPS contract word as decoration. Lines that merely contain the word later, or use another case (`Finding`, `Total`), are prose and stay ignored. Keep the existing rule that a matching line which does not start with the keyword at column 0 raises `InvalidInputError`.

- [ ] **Step 4: Run all scorer tests**

Run: `python -B tests/test-score-audit-gate.py 2>&1 | tail -4`
Expected: `OK`; record the `Ran N tests` number.

- [ ] **Step 5: Fix the stale audit-log statements**

In `docs/workflow/model-agnostic-roles-audits.md`:
1. Find the sentence that says Task 1 "also carries one entry" that "is open" and rewrite it to say the entry was closed by the final fix wave (commits f8d7b1f, 0958369, 59e850b).
2. Find the sentence "The deferred findings above are open" (about the three worth fixing before merge) and rewrite it to say they were addressed by the final fix wave, except those the Deviations section still lists.
3. In the Final-pass checklist, set the scorer and validator test counts to the real values: run `python -B tests/test-score-audit-gate.py` and `python -B tests/test-validate-workspace.py` and use their `Ran N tests` numbers.
Do not change any other line.

- [ ] **Step 6: Verify**

Run: `python -B tests/test-score-audit-gate.py 2>&1 | tail -3` and `python -B tests/test-validate-workspace.py 2>&1 | tail -3`
Expected: both `OK`.
Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.

- [ ] **Step 7: Commit**

```bash
git add scripts/score-audit-gate.py tests/test-score-audit-gate.py docs/workflow/model-agnostic-roles-audits.md
git commit -m "Close scorer decoration bypass and correct stale audit log lines"
```

---

### Task 5: Comments-only pass over scripts and tests

Run this after Tasks 1, 3 and 4 so it covers the new installer and the scorer.

**Files:**
- Modify: every `scripts/*.py` and `tests/*.py` file, comments and docstrings only.

**Interfaces:**
- Consumes: the code as it stands after Tasks 1, 3 and 4.
- Produces: identical behavior with plain comments. No code change of any kind.

- [ ] **Step 1: Record the starting commit**

Run: `git rev-parse HEAD` and keep the value as `BASE`.

- [ ] **Step 2: Rewrite comments and docstrings**

For every comment, docstring, and `help=` or `description=` string in the files above, apply the global comment rule. Typical fixes:

- Replace a long docstring that restates the function name with one short line.
- Remove sentences that narrate an edit or hype the result.
- Replace filler such as "ensures that", "robust", "comprehensive", "simply" with the plain fact.
- Keep technical terms, exit codes, flag names, and the `Raises:` and `Complexity:` lines where the Python guidance asks for them, but write them in short plain sentences.
- Keep every comment that explains a reason (for example why `sys.modules` is set before `exec_module`).

Do not change any statement, name, string literal used in logic, regular expression, or test assertion. Only comments and docstrings change.

- [ ] **Step 3: Prove no code changed**

Run this from the repository root, with `BASE` set to the value from Step 1:

```python
import ast, subprocess
from pathlib import Path

BASE = "<value from Step 1>"

def strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return tree

def code_dump(source):
    return ast.dump(strip_docstrings(ast.parse(source)))

changed = 0
for path in sorted(Path("scripts").glob("*.py")) + sorted(Path("tests").glob("*.py")):
    old = subprocess.run(["git", "show", f"{BASE}:{path.as_posix()}"], capture_output=True, text=True).stdout
    assert old, f"missing at BASE: {path}"
    assert code_dump(old) == code_dump(path.read_text(encoding="utf-8")), f"CODE CHANGED: {path}"
    changed += 1
print("code identical in", changed, "files")
```

Expected: `code identical in N files` and no assertion error. The one allowed exception is a `description=__doc__` or `help=` string, which are strings and appear in the AST; if the check reports a change only in such a string, list it in the report.

- [ ] **Step 4: Check the comment rule**

Run: `grep -rniE "note that|worth noting|importantly|robust|seamless|leverage|comprehensive|ensure that|simply|gracefully" scripts/*.py tests/*.py || echo "no filler words"`
Expected: `no filler words`.


- [ ] **Step 5: Verify**

Run: `python -B tests/test-score-audit-gate.py 2>&1 | tail -3`, `python -B tests/test-validate-workspace.py 2>&1 | tail -3`, `python -B tests/test-install-skill.py 2>&1 | tail -3`, `python -B tests/test-validate-language-guidance.py 2>&1 | tail -3`, then `python -B scripts/validate-workspace.py 2>&1 | tail -3`.
Expected: `OK` four times and `workspace validation: PASS`.

- [ ] **Step 6: Commit**

```bash
git add scripts tests
git commit -m "Rewrite code comments and docstrings in plain language"
```

---

### Task 6: Make the comment rule part of the protocol's guidance

The rule is a protocol requirement, not a note about one run. It goes into every
protocol-level file that states how code is written, checked, and scored.

**Files:**
- Modify: `SKILL.md`, `docs/language-guidelines.md`, `docs/languages/pre-codegen-checklist.md`, `docs/languages/scoring-rubric.md`, `docs/languages/language-file-template.md`, `docs/languages/top-llm-coding-nuances.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the rule stated once as the canonical text in `docs/language-guidelines.md`, and short pointers elsewhere. No code.

The basic rule of the protocol goes in first: take the minimal path, with the minimal
change, that produces the desired effect.

- [ ] **Step 0: The basic rule**

In `SKILL.md`, under `## Core Rules`, add this as the FIRST bullet:

```markdown
- Basic rule: take the minimal path, with the minimal change, that produces the
  desired effect. Name the effect first. Do not add features, options,
  abstractions, or checks the request does not need.
```

In `docs/language-guidelines.md`, under `## Universal Rules`, add the same bullet as the first bullet. In `docs/languages/pre-codegen-checklist.md`, add this after step `10.`, before the comment-rule step:

```markdown
11. State the desired effect and the smallest change that produces it before
    writing code.
```

and number the comment-rule step `12.` instead of `11.`.

Do not edit any `docs/languages/<language>.md` file here. Adding one line to each language file's `## Source Documentation And Comments` section is Wave 2 work.

Apply each insertion exactly once. If an anchor is not found exactly once, stop and report BLOCKED.

- [ ] **Step 1: Canonical text in `docs/language-guidelines.md`**

Under `## Universal Rules`, add this bullet at the end of the bullet list:

```markdown
- Write code comments and docstrings in plain US English at about a 6th grade
  reading level. Technical terms are fine. Say why the code does something, not
  what the next line obviously does. Leave out filler, hype, edit narration,
  banners, and emoji. `scripts/validate-workspace.py` checks this for the
  repository's own scripts and tests.
```

- [ ] **Step 2: `SKILL.md` Core Rules**

After the bullet that begins `- Do not invent APIs, configuration keys, package names, services, flags, or`, add:

```markdown
- Write code comments and docstrings in plain US English at about a 6th grade
  reading level. Technical terms are fine. No filler, hype, or edit narration.
  See `docs/language-guidelines.md`.
```

- [ ] **Step 3: `docs/languages/pre-codegen-checklist.md`**

After step `10.` (the one that ends `items in the workflow artifacts.`), add:

```markdown
11. Plan code comments and docstrings to follow the plain-language comment rule
    in `docs/language-guidelines.md`.
```

- [ ] **Step 4: `docs/languages/scoring-rubric.md`**

Under `## Scoring Rules`, add this bullet at the end of the list:

```markdown
- Criterion 4 includes the plain-language comment rule in
  `docs/language-guidelines.md`. Comments that restate the code, narrate edits,
  hype the result, or pad with filler lower that score.
```

- [ ] **Step 5: `docs/languages/language-file-template.md`**

Under `## Writing Rules`, add this bullet at the end of the list:

```markdown
- Require comments and docstrings in plain US English at about a 6th grade
  reading level, as `docs/language-guidelines.md` states.
```

- [ ] **Step 6: `docs/languages/top-llm-coding-nuances.md`**

Under `## Common Failure Modes`, add this bullet after the `**False confidence**` bullet:

```markdown
- **Slop comments**: comments that restate the code, narrate edits, hype the
  result, or pad with filler such as "note that", "robust", "seamless", or
  "ensure that". Write short, plain US English at about a 6th grade level, keep
  technical terms, and explain why, not what.
```

- [ ] **Step 7: Verify**

Run: `grep -ln "6th grade" SKILL.md docs/language-guidelines.md docs/languages/language-file-template.md docs/languages/top-llm-coding-nuances.md`
Expected: all four files listed.
Run: `grep -n "plain-language comment rule" docs/languages/pre-codegen-checklist.md docs/languages/scoring-rubric.md`
Expected: one matching line in each file.
Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.

- [ ] **Step 8: Commit**

```bash
git add SKILL.md docs/language-guidelines.md docs/languages/pre-codegen-checklist.md docs/languages/scoring-rubric.md docs/languages/language-file-template.md docs/languages/top-llm-coding-nuances.md
git commit -m "Make the plain-language comment rule part of the protocol"
```

---

### Task 7 (not planned): Enforce the comment rule in the validator

Not built by default. The protocol states the rule (Task 6) and the scoring rubric
covers it, which is the minimal path to the desired effect. A validator check that
fails on filler phrases and long sentences in `scripts/` and `tests/` is optional
hardening. Build it only if the maintainer asks.

---

## Self-Review

**Spec coverage** (`polyglot-protocol-upgrade-plan.md`):

| Item | Task |
|---|---|
| P0-1 OpenCode path | 1 |
| P0-2 Codex path | 1 |
| P0-3 `--force` guard and staged replace | 1 |
| P0-4 allowlist copy | 1 |
| P0-5 fixed `/tmp` clone | 1 |
| P0-6 broken paths | 2 |
| P0-7 `CLAUDE.md` | 2 |
| P0-8 validation command location | Plan A (adapters) and 2 (`SKILL.md`) |
| P0-9 nonexistent skills | 2 |
| P0-10 hardcoded score | 3 |
| P0-11 changelog entry | 3 |
| P0-12 `security.md` | Out of scope: repository setting |
| P0-13 scorer | Plan A, plus Task 4 closes the decoration bypass |
| P0-14 to P0-25 | Wave 2 plan |

**Placeholder scan.** No `TBD` or "similar to". Task 2 states exact old and new text for every edit.

**Consistency.** Installer names (`install`, `check_target`, `copy_allowlist`, `InstallError`, `SKILL_NAME`, `INCLUDE`, `DEFAULT_TARGETS`) match between the tests and the implementation. Test count in Task 1 Step 4 is 12; the file defines 12 test methods.

**Risks.** The allowlist must include every file the installed validator checks; the self-validation test catches an omission. The readme one-liners use `$(mktemp -d)`, which is POSIX shell, and the readme says so for Windows.
