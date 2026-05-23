from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "docs" / "languages"

LANGUAGE_FILES = {
    "bash.md",
    "c.md",
    "c-sharp.md",
    "cpp.md",
    "css.md",
    "dart.md",
    "go.md",
    "html.md",
    "java.md",
    "javascript.md",
    "kotlin.md",
    "lua.md",
    "php.md",
    "python.md",
    "r.md",
    "ruby.md",
    "rust.md",
    "shopify-liquid.md",
    "sql.md",
    "swift.md",
    "typescript.md",
    "zig.md",
}

LANGUAGE_README_DIRS = {name.removesuffix(".md") for name in LANGUAGE_FILES}

OPERATIONAL_FILES = {
    "decision-matrix.md",
    "do-not-generate-policy.md",
    "examples.md",
    "install-version-commands.md",
    "language-file-template.md",
    "maintenance-policy.md",
    "pre-codegen-checklist.md",
    "readme.md",
    "scoring-rubric.md",
    "score-report.md",
    "top-llm-coding-nuances.md",
}

REQUIRED_SECTIONS = [
    "## Tooling",
    "## Generation Rules",
    "## Source Documentation And Comments",
    "## Test-First Red Green Refactor",
    "## Refactoring Playbook",
    "## Project Discovery And Structure",
    "## Design Patterns And Architecture",
    "## Algorithmic Complexity And Dynamic Programming",
    "## Senior Architecture Decisions",
    "## Concurrency Parallelism And Hardware Acceleration",
    "## Senior Decision Checklist",
    "## Final Senior Guardrails",
    "## LLM Coding Guardrails",
]

SENIOR_LABELS = [
    "Security Threat Modeling And Abuse Cases",
    "Data Modeling And Persistence",
    "API Contracts And Compatibility",
    "Error Handling And Recovery",
    "Observability And Operability",
    "Testing Strategy By Risk",
    "Performance Budgets And Profiling",
    "Dependency And Supply-Chain Governance",
    "Configuration And Environment Strategy",
    "Release Migration And Rollback Strategy",
    "Accessibility And Internationalization",
    "Privacy Compliance And Data Governance",
]

FINAL_LABELS = [
    "Code Review Checklist",
    "Refactoring Rules",
    "Generated And AI-Assisted Code Rules",
    "Platform And OS Integration",
    "Serialization And Wire Formats",
    "Time Date Locale And Money",
    "Resource Lifecycle",
    "Build And Packaging Strategy",
]

REFACTORING_LABELS = [
    "Characterization Refactor",
    "Extract And Isolate",
    "Rename For Domain Clarity",
    "Simplify Control Flow",
    "Dead Code And Dependency Pruning",
    "Boundary Refactor",
    "Performance Refactor",
    "Compatibility-Preserving Migration",
    "Concurrency Refactor",
    "Architecture De-Escalation",
]


def is_kebab_case(name: str) -> bool:
    stem = name.removesuffix(".md").removesuffix(".py")
    return stem == stem.lower() and "_" not in stem and " " not in stem


def main() -> int:
    errors: list[str] = []

    actual_language_files = {path.name for path in LANG_DIR.glob("*.md")} & LANGUAGE_FILES
    missing_language_files = sorted(LANGUAGE_FILES - actual_language_files)
    if missing_language_files:
        errors.append(f"missing language files: {missing_language_files}")

    missing_language_readmes = sorted(
        slug for slug in LANGUAGE_README_DIRS if not (LANG_DIR / slug / "readme.md").exists()
    )
    if missing_language_readmes:
        errors.append(f"missing language readmes: {missing_language_readmes}")

    actual_operational_files = {path.name for path in LANG_DIR.glob("*.md")} & OPERATIONAL_FILES
    missing_operational_files = sorted(OPERATIONAL_FILES - actual_operational_files)
    if missing_operational_files:
        errors.append(f"missing operational files: {missing_operational_files}")

    for path in sorted(LANG_DIR.glob("*.md")):
        if not is_kebab_case(path.name):
            errors.append(f"filename is not kebab-case: {path}")
        text = path.read_text(encoding="utf-8")
        if not any(line.startswith("#") for line in text.splitlines()):
            errors.append(f"missing markdown heading: {path}")

    for name in sorted(LANGUAGE_FILES):
        path = LANG_DIR / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            count = text.count(section)
            if count != 1:
                errors.append(f"{name}: expected one {section!r}, found {count}")
        for label in SENIOR_LABELS + FINAL_LABELS + REFACTORING_LABELS:
            if label not in text:
                errors.append(f"{name}: missing label {label!r}")

    if errors:
        print("language guidance validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("language guidance validation: PASS")
    print(f"language files: {len(LANGUAGE_FILES)}")
    print(f"language readmes: {len(LANGUAGE_README_DIRS)}")
    print(f"operational files: {len(OPERATIONAL_FILES)}")
    print("score: 100/100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
