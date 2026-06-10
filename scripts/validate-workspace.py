from __future__ import annotations

import subprocess
import sys
from pathlib import Path

"""
Workspace validation script for the Polyglot Protocol.

Enforces naming, structure, and (when present) packaged skill language guidance
contract checks. Follows Google-style docstrings and explicit complexity per
docs/PYTHON.md.
"""

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_UPPERCASE = {"AGENTS.md", "CLAUDE.md", "SKILL.md"}
ADAPTER_READMES = {
    ROOT / "adapters" / "codex" / "readme.md",
    ROOT / "adapters" / "claude-code" / "readme.md",
    ROOT / "adapters" / "opencode" / "readme.md",
}


def is_kebab_case(path: Path) -> bool:
    stem = path.name.removesuffix(path.suffix)
    return stem == stem.lower() and "_" not in stem and " " not in stem


def run_language_validator() -> list[str]:
    script = ROOT / "scripts" / "validate-language-guidance.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        return ["language guidance validator failed"]
    return []


def run_packaged_language_validator() -> list[str]:
    """Additionally validate the language guidance inside the packaged skill.

    This ensures the the-polyglot-protocol/ copy receives the full contract checks.
    """
    packaged_script = ROOT / "the-polyglot-protocol" / "scripts" / "validate-language-guidance.py"
    if not packaged_script.exists():
        return []

    result = subprocess.run(
        [sys.executable, str(packaged_script)],
        cwd=ROOT / "the-polyglot-protocol",
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print("--- packaged skill language guidance ---\n" + result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        return ["packaged skill language guidance validator failed"]
    return []


def check_skill_package_sync() -> list[str]:
    """Guard against drift between root scripts and packaged skill copies."""
    errors: list[str] = []
    root_scripts = ROOT / "scripts"
    pkg_scripts = ROOT / "the-polyglot-protocol" / "scripts"

    if not (root_scripts.exists() and pkg_scripts.exists()):
        return errors

    for name in ("validate-workspace.py", "validate-language-guidance.py"):
        root_f = root_scripts / name
        pkg_f = pkg_scripts / name
        if pkg_f.exists() and root_f.read_bytes() != pkg_f.read_bytes():
            errors.append(f"packaged skill script is out of sync with root: {name}")
    return errors


def check_files() -> list[str]:
    errors: list[str] = []
    for path in sorted(ADAPTER_READMES):
        if not path.exists():
            errors.append(f"missing adapter readme: {path.relative_to(ROOT)}")
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".venv" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".sh"}:
            continue
        if any(char.isupper() for char in path.name) and path.name not in ALLOWED_UPPERCASE:
            errors.append(f"uppercase filename is not allowed: {path.relative_to(ROOT)}")
        if any(char.isdigit() for char in path.stem):
            errors.append(f"date-like or numbered filename is not allowed: {path.relative_to(ROOT)}")
        if not is_kebab_case(path) and path.name not in ALLOWED_UPPERCASE:
            errors.append(f"filename is not kebab-case: {path.relative_to(ROOT)}")
        if path.suffix == ".md":
            text = path.read_text(encoding="utf-8")
            if not any(line.startswith("#") for line in text.splitlines()):
                errors.append(f"markdown file has no heading: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = run_language_validator()
    errors.extend(run_packaged_language_validator())
    errors.extend(check_files())
    errors.extend(check_skill_package_sync())

    if errors:
        print("workspace validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("workspace validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
