from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

"""
Score the artifact-group dual-auditor gate.

Reads two auditor output files that follow the output contract in
docs/workflow/artifact-group-audit-workflow.md, re-adds each criterion score
instead of trusting the advertised total, and applies the gate rule: the mean
total must reach the threshold and no auditor may raise a CRITICAL finding.

Exit codes: 0 gate passed, 1 gate failed, 2 invalid auditor output.
"""

CRITERIA_COUNT = 10
DEFAULT_THRESHOLD = 85
VERDICT_RE = re.compile(r"^VERDICT (?P<name>.+?): (?P<score>\d+)/10\s*$")
TOTAL_RE = re.compile(r"^TOTAL: (?P<total>\d+)/100\s*$")
FINDING_RE = re.compile(r"^FINDING (?P<severity>CRITICAL|MAJOR|MINOR) (?P<where>\S+) (?P<text>.+?)\s*$")


class InvalidAuditError(ValueError):
    """Raised when an auditor output violates the output contract."""


@dataclass(frozen=True)
class AuditResult:
    """Parsed auditor output with a re-added total."""

    path: Path
    scores: dict[str, int]
    advertised_total: int | None
    findings: list[tuple[str, str, str]] = field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(self.scores.values())

    @property
    def criticals(self) -> list[tuple[str, str, str]]:
        return [item for item in self.findings if item[0] == "CRITICAL"]


def parse_audit(path: Path) -> AuditResult:
    """Parse one auditor output file.

    Complexity: O(n) in the number of lines.

    Raises:
        InvalidAuditError: if the criterion count, a score, or a name is invalid.
    """
    scores: dict[str, int] = {}
    advertised: int | None = None
    findings: list[tuple[str, str, str]] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if match := VERDICT_RE.match(line):
            name, score = match["name"], int(match["score"])
            if name in scores:
                raise InvalidAuditError(f"{path}: duplicate criterion {name!r}")
            if not 0 <= score <= 10:
                raise InvalidAuditError(f"{path}: score out of range for {name!r}: {score}")
            scores[name] = score
        elif match := TOTAL_RE.match(line):
            advertised = int(match["total"])
        elif match := FINDING_RE.match(line):
            findings.append((match["severity"], match["where"], match["text"]))

    if len(scores) != CRITERIA_COUNT:
        raise InvalidAuditError(
            f"{path}: expected {CRITERIA_COUNT} VERDICT lines, found {len(scores)}"
        )
    return AuditResult(path=path, scores=scores, advertised_total=advertised, findings=findings)


def gate_passes(results: list[AuditResult], threshold: int) -> bool:
    """Apply the gate rule with exact integer arithmetic (no float rounding)."""
    if any(result.criticals for result in results):
        return False
    return sum(result.total for result in results) >= threshold * len(results)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score the dual-auditor gate.")
    parser.add_argument("audits", nargs=2, type=Path, metavar="AUDIT_FILE")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        results = [parse_audit(path) for path in args.audits]
    except (InvalidAuditError, OSError) as error:
        print(f"invalid audit output: {error}")
        return 2

    for result in results:
        note = ""
        if result.advertised_total is not None and result.advertised_total != result.total:
            note = f" (advertised {result.advertised_total}/100, discrepancy recorded)"
        print(f"{result.path.name}: re-added total {result.total}/100{note}")
        for severity, where, text in result.criticals:
            print(f"  CRITICAL {where} {text}")

    mean = sum(result.total for result in results) / len(results)
    passed = gate_passes(results, args.threshold)
    print(f"mean: {mean:.1f}/100 threshold: {args.threshold}")
    print(f"GATE: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
