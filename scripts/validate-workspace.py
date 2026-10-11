from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
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

ROLES = ("orchestrator", "auditor_a", "auditor_b", "worker")
LICENCE_POLICIES = ("any", "permissive", "commercial-ok")
PROFILE_KEYS = ("name", "harnesses", "constraints", "pins", "fallback", "verified_on", "sources")
CONSTRAINT_KEYS = ("allowed_providers", "max_cost_per_mtok", "licence_policy", "local_only")
STALE_DAYS = 30
MODEL_NAME_RE = re.compile(r"Sonnet|Opus|Haiku|gpt-|Gemini|Kimi|GLM|DeepSeek|Qwen|MiMo")
MODEL_NEUTRAL_DOCS = (
    "docs/workflow/artifact-group-audit-workflow.md",
    "docs/workflow/dev-workflow.md",
    "SKILL.md",
)


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


def run_script_tests() -> list[str]:
    """Run the stdlib unittest files under tests/."""
    errors: list[str] = []
    for test_file in sorted((ROOT / "tests").glob("test-*.py")):
        result = subprocess.run(
            [sys.executable, "-B", str(test_file)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            print(result.stderr, end="", file=sys.stderr)
            errors.append(f"script tests failed: {test_file.relative_to(ROOT)}")
    return errors


def check_audit_workflow_references() -> list[str]:
    """Require the artifact-group audit workflow doc, its references, and a
    consistent gate threshold in every file that states it.

    Complexity: O(f) in the number of checked files.
    """
    errors: list[str] = []
    doc = ROOT / "docs" / "workflow" / "artifact-group-audit-workflow.md"
    if not doc.exists():
        return [f"missing workflow doc: {doc.relative_to(ROOT)}"]
    scorer = ROOT / "scripts" / "score-audit-gate.py"
    if not scorer.exists():
        errors.append(f"missing gate scorer: {scorer.relative_to(ROOT)}")

    needle = "artifact-group-audit-workflow.md"
    threshold = "`85`"
    dev_workflow = ROOT / "docs" / "workflow" / "dev-workflow.md"
    skill = ROOT / "SKILL.md"
    referrers = (skill, dev_workflow, ROOT / "readme.md", ROOT / "docs" / "AGENTS.md")
    threshold_files = {doc, dev_workflow, skill}

    for path in referrers:
        if not path.exists():
            errors.append(f"missing guidance file: {path.relative_to(ROOT)}")
        elif needle not in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)} does not reference {needle}")
    for path in sorted(threshold_files):
        if path.exists() and threshold not in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)} does not state gate threshold {threshold}")
    return errors


def extract_profile_json(text: str) -> object:
    """Return the parsed first ```json fenced block of a profile file.

    Raises:
        ValueError: if there is no block or it is not valid JSON.
    """
    match = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if match is None:
        raise ValueError("no ```json block found")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON: {error}") from error


def validate_profile(data: object, today: date) -> tuple[list[str], list[str]]:
    """Validate a parsed profile and return (errors, warnings).

    A verified_on date older than STALE_DAYS is a warning, not an error.
    """
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["profile must be a JSON object"], warnings
    for key in PROFILE_KEYS:
        if key not in data:
            errors.append(f"missing key: {key}")
    constraints = data.get("constraints")
    if isinstance(constraints, dict):
        for key in CONSTRAINT_KEYS:
            if key not in constraints:
                errors.append(f"missing constraints key: {key}")
        if constraints.get("licence_policy") not in LICENCE_POLICIES:
            errors.append(f"licence_policy must be one of {list(LICENCE_POLICIES)}")
    harnesses = data.get("harnesses")
    fallback = data.get("fallback")
    if isinstance(fallback, dict):
        for role in ROLES:
            entry = fallback.get(role)
            if not isinstance(entry, dict) or "harness" not in entry or "model" not in entry:
                errors.append(f"fallback.{role} needs harness and model")
            elif isinstance(harnesses, dict) and entry["harness"] not in harnesses:
                errors.append(f"fallback.{role} uses undeclared harness {entry['harness']!r}")
    verified = data.get("verified_on")
    if isinstance(verified, str):
        try:
            age = (today - date.fromisoformat(verified)).days
        except ValueError:
            errors.append("verified_on must be an ISO date (YYYY-MM-DD)")
        else:
            if age > STALE_DAYS:
                warnings.append(f"verified_on is {age} days old (over {STALE_DAYS} days); re-verify")
    elif "verified_on" in data:
        errors.append("verified_on must be an ISO date (YYYY-MM-DD)")
    return errors, warnings


def check_profiles() -> list[str]:
    """Validate every profiles/*.md file; print staleness warnings."""
    errors: list[str] = []
    profile_dir = ROOT / "profiles"
    if not profile_dir.is_dir():
        return ["missing directory: profiles/"]
    for path in sorted(profile_dir.glob("*.md")):
        rel = path.relative_to(ROOT)
        try:
            data = extract_profile_json(path.read_text(encoding="utf-8"))
        except ValueError as error:
            errors.append(f"{rel}: {error}")
            continue
        problems, warnings = validate_profile(data, date.today())
        errors.extend(f"{rel}: {problem}" for problem in problems)
        for warning in warnings:
            print(f"WARNING {rel}: {warning}")
    for required in ("default.md", "template.md"):
        if not (profile_dir / required).exists():
            errors.append(f"missing profile: profiles/{required}")
    return errors


def find_model_names(text: str) -> list[str]:
    """Return model-family tokens found in text, in order of appearance."""
    return MODEL_NAME_RE.findall(text)


def check_core_docs_model_neutral() -> list[str]:
    """Core workflow docs must not name a model; names live in profiles/."""
    errors: list[str] = []
    for name in MODEL_NEUTRAL_DOCS:
        path = ROOT / name
        if not path.exists():
            continue
        hits = find_model_names(path.read_text(encoding="utf-8"))
        if hits:
            errors.append(f"{name} names models {sorted(set(hits))}; move them to profiles/")
    return errors


def check_files() -> list[str]:
    errors: list[str] = []
    for path in sorted(ADAPTER_READMES):
        if not path.exists():
            errors.append(f"missing adapter readme: {path.relative_to(ROOT)}")
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part.startswith(".") for part in path.relative_to(ROOT).parts):
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
    errors.extend(check_audit_workflow_references())
    errors.extend(run_script_tests())
    errors.extend(check_profiles())
    errors.extend(check_core_docs_model_neutral())
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
