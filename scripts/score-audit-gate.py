"""Score the artifact-group dual-auditor gate.

Reads two auditor output files that follow the output contract in
docs/workflow/artifact-group-audit-workflow.md, re-adds each criterion score
instead of trusting the advertised total, and applies the gate rule: the mean
total must reach the threshold for the independence mode and no auditor may
raise a CRITICAL finding.

Independence comes from a lock file (--lock) when given, otherwise from
--independence, otherwise it defaults to full. Thresholds: full 85,
degraded 90. A threshold below the floor, or above 100, is rejected.

Exit codes: 0 gate passed, 1 gate failed, 2 invalid input.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

CRITERIA_COUNT = 10
THRESHOLDS = {"full": 85, "degraded": 90}
# A line is a reserved contract line if ANY of these patterns matches, however
# it is decorated or prefixed. The strict shapes below only match at column 0,
# so a reserved line that is not a clean column-0 contract line is rejected
# (exit 2) instead of silently ignored. Listing prefixes can never be complete,
# so the patterns key on the contract tokens themselves:
#   1. an ALL-CAPS keyword after any run of non-word characters, underscores,
#      or numeric list markers ("1.", "1)");
#   2. a FINDING (any case) followed by an ALL-CAPS severity word, anywhere;
#   3. a verdict-shaped fragment ("VERDICT ...: 9/10"), anywhere;
#   4. a total-shaped fragment ("TOTAL: 90/100"), anywhere.
# Mixed-case severity words ("Finding Critical") are intentionally prose,
# because the contract is ALL CAPS; so is lower-case running text.
RESERVED_PATTERNS = (
    re.compile(r"^(?:[\W_]|\d+[.)])*(?:VERDICT|TOTAL|FINDING)\b"),
    re.compile(r"\b(?i:finding)[ \t]+[\W_]*(?:CRITICAL|MAJOR|MINOR)\b"),
    re.compile(r"\bVERDICT\b[^\n]*:\s*\d+/10\b"),
    re.compile(r"\bTOTAL\b\s*:\s*\d+/100\b"),
)
VERDICT_RE = re.compile(r"^VERDICT (?P<name>.+?): (?P<score>\d+)/10\s*$")
TOTAL_RE = re.compile(r"^TOTAL: (?P<total>\d+)/100\s*$")
FINDING_RE = re.compile(r"^FINDING (?P<severity>CRITICAL|MAJOR|MINOR) (?P<where>\S+) (?P<text>.+?)\s*$")


def is_reserved(line: str) -> bool:
    """Return True if the line looks like a contract line in any decoration."""
    return any(pattern.search(line) for pattern in RESERVED_PATTERNS)


class InvalidInputError(ValueError):
    """Raised when an auditor output, lock file, or option is invalid."""


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
    def names(self) -> frozenset[str]:
        return frozenset(self.scores)

    @property
    def criticals(self) -> list[tuple[str, str, str]]:
        return [item for item in self.findings if item[0] == "CRITICAL"]


def parse_audit(path: Path) -> AuditResult:
    """Parse one auditor output file.

    Any line that looks like a contract line (see RESERVED_PATTERNS), even one
    that is indented, decorated, or prefixed, must match the contract exactly
    at column 0.

    Complexity: O(n) in the number of lines.

    Raises:
        InvalidInputError: if a reserved-prefix line is malformed, a criterion
            repeats, a score is out of range, or the criterion count is wrong.
    """
    scores: dict[str, int] = {}
    advertised: int | None = None
    findings: list[tuple[str, str, str]] = []

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise InvalidInputError(f"cannot decode {path} as UTF-8: {error.reason}") from error

    for number, line in enumerate(text.splitlines(), 1):
        if not is_reserved(line):
            continue
        if match := VERDICT_RE.match(line):
            name, score = match["name"], int(match["score"])
            if name in scores:
                raise InvalidInputError(f"{path}:{number}: duplicate criterion {name!r}")
            if not 0 <= score <= 10:
                raise InvalidInputError(f"{path}:{number}: score out of range for {name!r}: {score}")
            scores[name] = score
        elif match := TOTAL_RE.match(line):
            advertised = int(match["total"])
        elif match := FINDING_RE.match(line):
            findings.append((match["severity"], match["where"], match["text"]))
        else:
            raise InvalidInputError(f"{path}:{number}: malformed contract line: {line[:80]!r}")

    if len(scores) != CRITERIA_COUNT:
        raise InvalidInputError(f"{path}: expected {CRITERIA_COUNT} VERDICT lines, found {len(scores)}")
    return AuditResult(path=path, scores=scores, advertised_total=advertised, findings=findings)


def load_lock(path: Path) -> tuple[str, dict[str, object]]:
    """Read the independence mode and role map from a lock file.

    Raises:
        InvalidInputError: if the file is unreadable, not JSON, has an unknown
            independence value, or assigns one model to both auditors.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise InvalidInputError(f"cannot read lock file {path}: {error}") from error
    except UnicodeDecodeError as error:
        raise InvalidInputError(f"cannot decode lock file {path} as UTF-8: {error.reason}") from error
    if not isinstance(data, dict):
        raise InvalidInputError(f"lock file {path} must contain a JSON object")
    mode = data.get("independence")
    if not isinstance(mode, str) or mode not in THRESHOLDS:
        raise InvalidInputError(f"lock file {path}: independence must be one of {sorted(THRESHOLDS)}")
    roles = data.get("roles")
    if isinstance(roles, dict):
        models = [
            roles[key].get("model")
            for key in ("auditor_a", "auditor_b")
            if isinstance(roles.get(key), dict)
        ]
        if len(models) == 2 and models[0] is not None and models[0] == models[1]:
            raise InvalidInputError("lock file assigns the same model to both auditors")
    return mode, data


def resolve_mode(cli_mode: str | None, lock_path: Path | None) -> str:
    """Return the independence mode from the lock, the flag, or the default."""
    lock_mode = load_lock(lock_path)[0] if lock_path else None
    if lock_mode and cli_mode and lock_mode != cli_mode:
        raise InvalidInputError(f"--independence {cli_mode} conflicts with lock file value {lock_mode}")
    return lock_mode or cli_mode or "full"


def resolve_threshold(mode: str, requested: int | None) -> int:
    """Return the threshold, rejecting values below the mode's floor or above 100."""
    floor = THRESHOLDS[mode]
    threshold = floor if requested is None else requested
    if threshold < floor:
        raise InvalidInputError(f"threshold {threshold} is below the {mode} floor of {floor}")
    if threshold > 100:
        raise InvalidInputError(f"threshold {threshold} is above 100")
    return threshold


def gate_passes(results: list[AuditResult], threshold: int) -> bool:
    """Apply the gate rule with exact integer arithmetic (no float rounding)."""
    if any(result.criticals for result in results):
        return False
    return sum(result.total for result in results) >= threshold * len(results)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("audits", nargs=2, type=Path, metavar="AUDIT_FILE")
    parser.add_argument("--threshold", type=int, default=None)
    parser.add_argument("--independence", choices=sorted(THRESHOLDS), default=None)
    parser.add_argument("--lock", type=Path, default=None, help="resolved-roles.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        mode = resolve_mode(args.independence, args.lock)
        threshold = resolve_threshold(mode, args.threshold)
        results = [parse_audit(path) for path in args.audits]
        if results[0].names != results[1].names:
            raise InvalidInputError("the two auditors scored different criterion names")
    except (InvalidInputError, OSError) as error:
        print(f"invalid input: {error}")
        return 2

    for result in results:
        note = ""
        if result.advertised_total is not None and result.advertised_total != result.total:
            note = f" (advertised {result.advertised_total}/100, discrepancy recorded)"
        print(f"{result.path.name}: re-added total {result.total}/100{note}")
        for _severity, where, text in result.criticals:
            print(f"  CRITICAL {where} {text}")

    mean = sum(result.total for result in results) / len(results)
    passed = gate_passes(results, threshold)
    print(f"mean: {mean:.1f}/100 threshold: {threshold}")
    print(f"GATE: {'PASS' if passed else 'FAIL'} (independence={mode}, threshold={threshold})")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
