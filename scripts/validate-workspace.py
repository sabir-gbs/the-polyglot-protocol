from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_UPPERCASE = {"AGENTS.md", "CLAUDE.md", "PYTHON.md", "SKILL.md", "TYPESCRIPT.md"}
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
    errors.extend(check_files())

    if errors:
        print("workspace validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("workspace validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
