# Round One P0 Fixes Implementation Plan (Wave 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the round 1 P0 findings that live outside the language guidance files: the installer, broken required paths, nonexistent skills, false score claims, and the false changelog entry.

**Architecture:** Seven tasks. Task 4 runs first. Task 5 (comment pass) runs after Tasks 1, 3 and 4. Task 6 (rule in the protocol's guidance) and Task 7 (validator check) run last, in that order. Task 1 rewrites `scripts/install-skill.py` as an allowlist installer with target guards, staged replacement, and `--dry-run`, with tests, and updates the readme install section. Task 2 applies exact text replacements to documents. Task 3 removes the hardcoded score and corrects the changelog entry.

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
- Exit codes for the installer: `0` installed or dry-run ok, `2` refused or invalid.

## Out Of Scope

- P0-12 (`security.md` private reporting) is a GitHub repository setting. No file change is correct until it is enabled. The maintainer enables it in Settings, Code security, Private vulnerability reporting.
- Language-file items P0-14 to P0-25 (Wave 2).

## File Structure

| File | Responsibility |
|---|---|
| `scripts/install-skill.py` | Allowlist copy, target guards, staged replace, dry run |
| `tests/test-install-skill.py` | Installer behavior including a self-validation of the installed copy |
| `readme.md` | Install commands, quick start, validation output, project status |
| `docs/languages/index.md`, `maintenance-policy.md`, `pre-codegen-checklist.md`, `docs/AGENTS.md`, `docs/workflow/dev-workflow.md`, `SKILL.md` | Path and skill-name corrections |
| `scripts/validate-language-guidance.py`, `tests/test-validate-language-guidance.py` | Remove hardcoded score; test that none is printed |
| `contributing.md`, `docs/languages/score-report.md` | Remove the score claim |
| `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md` | Dated correction note |

---

### Task 1: Rewrite the installer and its readme commands

**Files:**
- Modify: `scripts/install-skill.py` (replace the whole file)
- Create: `tests/test-install-skill.py`
- Modify: `readme.md` (Quick Start and One-Line Install sections)

**Interfaces:**
- Consumes: nothing.
- Produces: `scripts/install-skill.py` CLI `install-skill.py [--agent codex|claude-code|opencode] [--target PATH] [--force] [--dry-run]`. Python API: `install(source: Path, target: Path, *, force: bool, dry_run: bool, home: Path) -> list[str]`, `InstallError`, `DEFAULT_TARGETS`, `INCLUDE`, `SKILL_NAME`.

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

NAME = INSTALL.SKILL_NAME


class InstallSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name).resolve()
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.target = self.tmp / "skills" / NAME

    def run_install(self, **kwargs: object) -> list[str]:
        options = {"force": False, "dry_run": False, "home": self.home}
        options.update(kwargs)
        return INSTALL.install(ROOT, self.target, **options)  # type: ignore[arg-type]

    def make_previous_install(self) -> None:
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_text(f"---\nname: {NAME}\n---\nold\n", encoding="utf-8")
        (self.target / "old.txt").write_text("old", encoding="utf-8")

    # --- what is copied ----------------------------------------------------
    def test_installs_the_allowlist_only(self) -> None:
        self.run_install()
        self.assertTrue((self.target / "SKILL.md").is_file())
        self.assertTrue((self.target / "docs" / "languages" / "python.md").is_file())
        self.assertTrue((self.target / "profiles" / "default.md").is_file())
        self.assertFalse((self.target / "tests").exists())
        workflow = sorted(p.name for p in (self.target / "docs" / "workflow").iterdir())
        self.assertEqual(
            workflow,
            ["artifact-group-audit-workflow.md", "dev-workflow.md", "role-resolution.md"],
        )

    def test_never_copies_env_files_or_caches(self) -> None:
        self.run_install()
        names = {p.name for p in self.target.rglob("*")}
        self.assertFalse({n for n in names if n.startswith(".env") or n == "__pycache__"})

    def test_installed_copy_validates_itself(self) -> None:
        self.run_install()
        result = subprocess.run(
            [sys.executable, "-B", "scripts/validate-workspace.py"],
            cwd=self.target, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("workspace validation: PASS", result.stdout)

    # --- target guards -----------------------------------------------------
    def test_refuses_existing_target_without_force(self) -> None:
        self.make_previous_install()
        with self.assertRaises(INSTALL.InstallError):
            self.run_install()

    def test_refuses_force_over_a_directory_that_is_not_a_previous_install(self) -> None:
        self.target.mkdir(parents=True)
        (self.target / "precious.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(INSTALL.InstallError):
            self.run_install(force=True)
        self.assertTrue((self.target / "precious.txt").exists())

    def test_refuses_target_with_wrong_leaf_name(self) -> None:
        with self.assertRaises(INSTALL.InstallError):
            INSTALL.install(ROOT, self.tmp / "skills", force=True, dry_run=False, home=self.home)

    def test_refuses_the_source_its_parents_and_children(self) -> None:
        for target in (ROOT, ROOT.parent, ROOT / "sub" / NAME):
            with self.subTest(target=str(target)):
                with self.assertRaises(INSTALL.InstallError):
                    INSTALL.install(ROOT, target, force=True, dry_run=False, home=self.home)

    def test_refuses_home_and_filesystem_root(self) -> None:
        for target in (self.home, Path(self.home.anchor)):
            with self.subTest(target=str(target)):
                with self.assertRaises(INSTALL.InstallError):
                    INSTALL.install(ROOT, target, force=True, dry_run=False, home=self.home)

    # --- replacement safety -------------------------------------------------
    def test_force_replaces_a_previous_install(self) -> None:
        self.make_previous_install()
        self.run_install(force=True)
        self.assertFalse((self.target / "old.txt").exists())
        self.assertIn("The Polyglot Protocol", (self.target / "SKILL.md").read_text(encoding="utf-8"))

    def test_failed_copy_keeps_the_previous_install(self) -> None:
        self.make_previous_install()
        original = INSTALL.copy_allowlist

        def boom(source: Path, dest: Path) -> list[str]:
            raise OSError("disk full")

        INSTALL.copy_allowlist = boom
        try:
            with self.assertRaises(OSError):
                self.run_install(force=True)
        finally:
            INSTALL.copy_allowlist = original
        self.assertTrue((self.target / "old.txt").exists())
        self.assertFalse((self.target.parent / f".{NAME}.staging").exists())

    def test_dry_run_writes_nothing(self) -> None:
        planned = self.run_install(dry_run=True)
        self.assertIn("SKILL.md", planned)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.target.parent.exists())

    # --- defaults -----------------------------------------------------------
    def test_default_targets_use_current_agent_paths(self) -> None:
        targets = {k: v.as_posix() for k, v in INSTALL.DEFAULT_TARGETS.items()}
        self.assertTrue(targets["opencode"].endswith(f".config/opencode/skills/{NAME}"))
        self.assertTrue(targets["codex"].endswith(f".agents/skills/{NAME}"))
        self.assertTrue(targets["claude-code"].endswith(f".claude/skills/{NAME}"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -B tests/test-install-skill.py 2>&1 | tail -6`
Expected: FAIL with `AttributeError: module 'install_skill' has no attribute 'SKILL_NAME'`.

- [ ] **Step 3: Write the implementation**

Replace `scripts/install-skill.py` with:

```python
"""Install The Polyglot Protocol skill into an agent's skill directory.

Copies an allowlist of skill files, not the whole repository. Refuses unsafe
targets. Replaces an existing install by staging the new copy first, so a failed
copy never loses the previous install.

Exit codes: 0 installed (or dry run), 2 refused or invalid.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "the-polyglot-protocol"

DEFAULT_TARGETS = {
    "codex": Path.home() / ".agents" / "skills" / SKILL_NAME,
    "claude-code": Path.home() / ".claude" / "skills" / SKILL_NAME,
    "opencode": Path.home() / ".config" / "opencode" / "skills" / SKILL_NAME,
}

INCLUDE = (
    "SKILL.md",
    "AGENTS.md",
    "readme.md",
    "contributing.md",
    "security.md",
    "license.md",
    "docs/AGENTS.md",
    "docs/language-guidelines.md",
    "docs/languages",
    "docs/workflow/dev-workflow.md",
    "docs/workflow/artifact-group-audit-workflow.md",
    "docs/workflow/role-resolution.md",
    "profiles",
    "scripts",
    "adapters",
)
SKIP_NAMES = {"__pycache__", ".git", ".venv", ".DS_Store"}


class InstallError(Exception):
    """Raised when a target is unsafe or the install cannot proceed."""


def _ignore(_directory: str, names: list[str]) -> set[str]:
    return {n for n in names if n in SKIP_NAMES or n.startswith(".env") or n.endswith(".pyc")}


def is_skill_install(path: Path) -> bool:
    """Return True when path holds a previous install of this skill."""
    skill = path / "SKILL.md"
    if not skill.is_file():
        return False
    return f"name: {SKILL_NAME}" in skill.read_text(encoding="utf-8", errors="replace")[:2000]


def check_target(target: Path, source: Path, *, force: bool, home: Path) -> Path:
    """Resolve and validate an install target.

    Raises:
        InstallError: for the source, its parents or children, the home
            directory, the filesystem root, a wrong leaf name, or an existing
            directory that is not a previous install.
    """
    target = target.expanduser().resolve()
    source = source.resolve()
    if target == source or source.is_relative_to(target):
        raise InstallError(f"target {target} is the source repository or one of its parents")
    if target.is_relative_to(source):
        raise InstallError(f"target {target} is inside the source repository")
    if target == home.resolve() or target == Path(target.anchor):
        raise InstallError(f"target {target} is the home directory or the filesystem root")
    if target.name != SKILL_NAME:
        raise InstallError(f"target directory name must be {SKILL_NAME!r}, got {target.name!r}")
    if target.exists():
        if not target.is_dir():
            raise InstallError(f"target {target} exists and is not a directory")
        if any(target.iterdir()):
            if not force:
                raise InstallError(f"target {target} exists; rerun with --force to replace it")
            if not is_skill_install(target):
                raise InstallError(
                    f"refusing to replace {target}: it is not a previous install of {SKILL_NAME}"
                )
    return target


def copy_allowlist(source: Path, dest: Path) -> list[str]:
    """Copy INCLUDE paths from source into dest and return the relative names."""
    copied: list[str] = []
    for rel in INCLUDE:
        src = source / rel
        if not src.exists():
            raise InstallError(f"missing source path: {rel}")
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, out, ignore=_ignore)
        else:
            shutil.copy2(src, out)
        copied.append(rel)
    return copied


def install(source: Path, target: Path, *, force: bool, dry_run: bool, home: Path) -> list[str]:
    """Install the skill and return the list of copied relative paths."""
    target = check_target(target, source, force=force, home=home)
    if dry_run:
        return list(INCLUDE)

    staging = target.parent / f".{SKILL_NAME}.staging"
    backup = target.parent / f".{SKILL_NAME}.previous"
    target.parent.mkdir(parents=True, exist_ok=True)
    for leftover in (staging, backup):
        if leftover.exists():
            shutil.rmtree(leftover)

    try:
        copied = copy_allowlist(source, staging)
        if not (staging / "SKILL.md").is_file():
            raise InstallError("staged copy has no SKILL.md")
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    if target.exists():
        target.rename(backup)
    try:
        staging.rename(target)
    except OSError:
        if backup.exists():
            backup.rename(target)
        raise
    shutil.rmtree(backup, ignore_errors=True)
    return copied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--agent", choices=sorted(DEFAULT_TARGETS), default="codex")
    parser.add_argument("--target", type=Path, help="install directory; its name must be the-polyglot-protocol")
    parser.add_argument("--force", action="store_true", help="replace a previous install of this skill")
    parser.add_argument("--dry-run", action="store_true", help="validate the target and list what would be copied")
    args = parser.parse_args(argv)

    target = args.target if args.target else DEFAULT_TARGETS[args.agent]
    try:
        copied = install(ROOT, target, force=args.force, dry_run=args.dry_run, home=Path.home())
    except InstallError as error:
        print(f"install refused: {error}", file=sys.stderr)
        return 2
    verb = "would install" if args.dry_run else "installed"
    label = f"for {args.agent}: " if not args.target else ""
    print(f"{verb} The Polyglot Protocol {label}{target} ({len(copied)} paths)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -B tests/test-install-skill.py 2>&1 | tail -5`
Expected: `Ran 12 tests` and `OK`. If `test_installed_copy_validates_itself` fails, the allowlist is missing a file the validator needs: add that path to `INCLUDE` and report which one.

- [ ] **Step 5: Replace the readme Quick Start and install commands**

In `readme.md`, replace this exact block:

```markdown
Use the skill folder directly from an agent that supports local skill folders,
or copy the relevant adapter into the target agent's expected guidance location.
```

with:

```markdown
Use the skill folder directly from an agent that supports local skill folders,
or install it with the commands below. Install the whole skill folder: the
adapter files link to `SKILL.md` and `profiles/`, so an adapter copied on its
own cannot find them.
```

Replace the whole `## One-Line Install` section (from `## One-Line Install` up to but not including `Validate the project:`) with:

````markdown
## One-Line Install

These commands clone into a fresh temporary directory, so they work on every
run, and install into the agent's global skill directory. They do not replace an
existing install.

Codex (`~/.agents/skills`):

```sh
d=$(mktemp -d) && git clone https://github.com/sabir-gbs/the-polyglot-protocol.git "$d" && python "$d/scripts/install-skill.py" --agent codex
```

Claude Code (`~/.claude/skills`):

```sh
d=$(mktemp -d) && git clone https://github.com/sabir-gbs/the-polyglot-protocol.git "$d" && python "$d/scripts/install-skill.py" --agent claude-code
```

OpenCode (`~/.config/opencode/skills`):

```sh
d=$(mktemp -d) && git clone https://github.com/sabir-gbs/the-polyglot-protocol.git "$d" && python "$d/scripts/install-skill.py" --agent opencode
```

Custom location (the directory name must be `the-polyglot-protocol`):

```sh
d=$(mktemp -d) && git clone https://github.com/sabir-gbs/the-polyglot-protocol.git "$d" && python "$d/scripts/install-skill.py" --target ~/path/to/skills/the-polyglot-protocol
```

To see what an install would do without writing anything, add `--dry-run`. To
update an existing install, add `--force`. It replaces only a previous install of
this skill, and it keeps the old copy if the new one fails to copy. On Windows,
replace `$(mktemp -d)` with a directory you create and clone into it.
````

- [ ] **Step 6: Verify**

Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.
Run: `python -B scripts/install-skill.py --agent opencode --dry-run`
Expected: a line starting `would install The Polyglot Protocol for opencode:` containing `.config/opencode/skills/the-polyglot-protocol`, exit 0.
Run: `python -B scripts/install-skill.py --target /tmp/skills --force; echo exit=$?`
Expected: `install refused:` on stderr and `exit=2`.

- [ ] **Step 7: Commit**

```bash
git add scripts/install-skill.py tests/test-install-skill.py readme.md
git commit -m "Rewrite installer with allowlist, target guards, and staged replace"
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

**Files:**
- Modify: `scripts/validate-language-guidance.py`, `readme.md`, `contributing.md`, `docs/languages/score-report.md`, `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md`
- Create: `tests/test-validate-language-guidance.py`

**Interfaces:**
- Consumes: nothing.
- Produces: a validator that prints `PASS` or `FAIL` with counts and no numeric score.

- [ ] **Step 1: Write the failing test**

Create `tests/test-validate-language-guidance.py`:

```python
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LanguageValidatorOutputTest(unittest.TestCase):
    def test_reports_pass_without_a_numeric_score(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "validate-language-guidance.py")],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("language guidance validation: PASS", result.stdout)
        self.assertNotIn("100/100", result.stdout)
        self.assertNotIn("score:", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -B tests/test-validate-language-guidance.py 2>&1 | tail -6`
Expected: FAIL with `AssertionError: '100/100' unexpectedly found`.

- [ ] **Step 3: Remove the score line**

In `scripts/validate-language-guidance.py`, delete the line `    print("score: 100/100")` and nothing else.

- [ ] **Step 4: Run it to verify it passes**

Run: `python -B tests/test-validate-language-guidance.py 2>&1 | tail -4`
Expected: `Ran 1 test` and `OK`.

- [ ] **Step 5: Update the documents**

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

- [ ] **Step 6: Correct the changelog entry**

Append this section to the end of `docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md`:

```markdown

## Correction (2026-10-11)

Verified against the repository on 2026-10-11, several statements above are not
true. They are kept for history and corrected here.

- **Docstrings.** The entry says `validate-workspace.py` and
  `validate-language-guidance.py` use strict Google-style docstrings with
  `Args:`, `Returns:`, `Raises:` and complexity sections. `validate-language-guidance.py`
  has no docstrings at all, and in `validate-workspace.py` the module docstring
  sits after the imports, so Python does not treat it as a docstring.
- **Packaged copy.** The entry describes a `the-polyglot-protocol/` skill
  package and sync checks against it. That directory has never existed in this
  repository's git history (`git log --all -- 'the-polyglot-protocol/*'` is
  empty), so those checks never run.
- **Standard.** The entry cites `docs/PYTHON.md`. That file does not exist; the
  Python guidance is `docs/languages/python/python.md`.
- **Verification command.** The entry lists `(cd the-polyglot-protocol && python scripts/validate-workspace.py)`
  as run. That command cannot have run, because the directory does not exist.
- **Audit scores.** The `100/100` audit results in the sibling artifacts for
  this change are not supported by the evidence above and should not be relied
  on.
```

- [ ] **Step 7: Verify**

Run: `python -B tests/test-validate-language-guidance.py 2>&1 | tail -3`
Expected: `OK`.
Run: `grep -rn "100/100" readme.md contributing.md docs/languages/score-report.md scripts/validate-language-guidance.py || echo "no score claims"`
Expected: `no score claims`.
Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.

- [ ] **Step 8: Commit**

```bash
git add scripts/validate-language-guidance.py tests/test-validate-language-guidance.py readme.md contributing.md docs/languages/score-report.md docs/workflow/validate-scripts-packaged-skill-coverage-changelog-entry.md
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

Run this sentence-length check:

```python
import ast, io, re, tokenize
from pathlib import Path

long_ones = []
for path in sorted(Path("scripts").glob("*.py")) + sorted(Path("tests").glob("*.py")):
    source = path.read_text(encoding="utf-8")
    texts = [tok.string.lstrip("# ") for tok in tokenize.generate_tokens(io.StringIO(source).readline) if tok.type == tokenize.COMMENT]
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node)
            if doc:
                texts.append(doc)
    for text in texts:
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if len(sentence.split()) > 25:
                long_ones.append((path.name, sentence[:80]))
print(len(long_ones), "long sentences")
for item in long_ones:
    print(item)
```

Expected: `0 long sentences`. Shorten any that are listed.

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

### Task 7: Enforce the comment rule in the validator

Run this after Task 5, so the repository's scripts and tests already comply when the check turns on.

**Files:**
- Modify: `scripts/validate-workspace.py`
- Modify: `tests/test-validate-workspace.py`

**Interfaces:**
- Consumes: the comment pass from Task 5.
- Produces: `comment_texts(source: str) -> list[tuple[int, str]]`, `comment_style_problems(source: str) -> list[str]`, `check_comment_style() -> list[str]`, and constants `COMMENT_BANNED`, `MAX_COMMENT_SENTENCE_WORDS`.

- [ ] **Step 1: Write the failing tests**

Add this class to `tests/test-validate-workspace.py`, before the `if __name__` block:

```python
class CommentStyleTest(unittest.TestCase):
    def test_flags_filler_phrases_in_comments(self) -> None:
        problems = VW.comment_style_problems("# Note that this is robust.\nx = 1\n")
        self.assertTrue(any("note that" in p for p in problems))
        self.assertTrue(any("robust" in p for p in problems))

    def test_flags_filler_in_docstrings(self) -> None:
        source = 'def f():\n    """Simply ensure that the value is set."""\n    return 1\n'
        problems = VW.comment_style_problems(source)
        self.assertTrue(any("simply" in p for p in problems))
        self.assertTrue(any("ensure that" in p for p in problems))

    def test_flags_module_docstring(self) -> None:
        problems = VW.comment_style_problems('"""A comprehensive helper."""\nx = 1\n')
        self.assertTrue(any("comprehensive" in p for p in problems))

    def test_flags_long_sentences(self) -> None:
        long_sentence = " ".join(["word"] * 30) + "."
        problems = VW.comment_style_problems(f"# {long_sentence}\nx = 1\n")
        self.assertTrue(any("words" in p for p in problems))

    def test_plain_comments_pass(self) -> None:
        source = '"""Check file names."""\n# Skip hidden folders because caches live there.\nx = 1\n'
        self.assertEqual(VW.comment_style_problems(source), [])

    def test_words_that_only_contain_a_banned_word_pass(self) -> None:
        self.assertEqual(VW.comment_style_problems("# This check gains robustness.\n"), [])

    def test_banned_words_in_string_literals_are_not_comments(self) -> None:
        self.assertEqual(VW.comment_style_problems('BANNED = ("robust", "seamless")\n'), [])

    def test_repository_scripts_and_tests_follow_the_rule(self) -> None:
        self.assertEqual(VW.check_comment_style(), [])
```

- [ ] **Step 2: Run them to verify they fail**

Run: `python -B tests/test-validate-workspace.py 2>&1 | tail -6`
Expected: FAIL with `AttributeError: module 'validate_workspace' has no attribute 'comment_style_problems'`.

- [ ] **Step 3: Write the implementation**

In `scripts/validate-workspace.py` add `import ast`, `import io` and `import tokenize` to the import block. Add these constants next to the other module constants:

```python
COMMENT_BANNED = (
    "note that",
    "worth noting",
    "it's worth",
    "importantly",
    "robust",
    "seamless",
    "seamlessly",
    "leverage",
    "comprehensive",
    "ensure that",
    "simply",
    "gracefully",
    "cutting-edge",
)
MAX_COMMENT_SENTENCE_WORDS = 25
```

Add these functions before `check_files`:

```python
def comment_texts(source: str) -> list[tuple[int, str]]:
    """Return (line, text) for each comment and docstring in Python source."""
    found: list[tuple[int, str]] = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            found.append((token.start[0], token.string.lstrip("# ").strip()))
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and node.body:
                found.append((node.body[0].lineno, doc))
    return found


def comment_style_problems(source: str) -> list[str]:
    """List filler phrases and over-long sentences in comments and docstrings."""
    problems: list[str] = []
    for line, text in comment_texts(source):
        lowered = text.lower()
        for phrase in COMMENT_BANNED:
            if re.search(rf"\b{re.escape(phrase)}\b", lowered):
                problems.append(f"line {line}: filler phrase {phrase!r}")
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if len(sentence.split()) > MAX_COMMENT_SENTENCE_WORDS:
                problems.append(f"line {line}: sentence over {MAX_COMMENT_SENTENCE_WORDS} words")
    return problems


def check_comment_style() -> list[str]:
    """Apply the plain-language comment rule to scripts/ and tests/."""
    errors: list[str] = []
    for directory in ("scripts", "tests"):
        for path in sorted((ROOT / directory).glob("*.py")):
            for problem in comment_style_problems(path.read_text(encoding="utf-8")):
                errors.append(f"{path.relative_to(ROOT)}: {problem}")
    return errors
```

In `main`, add `errors.extend(check_comment_style())` after `errors.extend(check_core_docs_model_neutral())`.

- [ ] **Step 4: Run the tests**

Run: `python -B tests/test-validate-workspace.py 2>&1 | tail -6`
Expected: `OK`. If `test_repository_scripts_and_tests_follow_the_rule` fails, list the reported problems and rewrite those comments in plain language; do not weaken the check or the word list.

- [ ] **Step 5: Verify**

Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate-workspace.py tests/test-validate-workspace.py
git commit -m "Check the plain-language comment rule in the validator"
```

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
