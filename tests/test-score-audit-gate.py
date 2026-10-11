from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("score_audit_gate", ROOT / "scripts" / "score-audit-gate.py")
assert SPEC is not None and SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GATE  # dataclasses resolve annotations through sys.modules
SPEC.loader.exec_module(GATE)

PASS_CODE, FAIL_CODE, INVALID_CODE = 0, 1, 2


def audit_text(scores: list[int], *, total: int | None = None, findings: tuple[str, ...] = ()) -> str:
    lines = [f"VERDICT criterion {index}: {score}/10" for index, score in enumerate(scores, 1)]
    lines.append(f"TOTAL: {sum(scores) if total is None else total}/100")
    lines.extend(findings)
    return "\n".join(lines) + "\n"


class ScoreAuditGateTest(unittest.TestCase):
    def run_gate(self, first: str, second: str, *extra: str) -> int:
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for name, text in (("sol.txt", first), ("opus.txt", second)):
                path = Path(tmp) / name
                path.write_text(text, encoding="utf-8")
                paths.append(str(path))
            return GATE.main([*paths, *extra])

    def test_passes_above_threshold(self) -> None:
        text = audit_text([9] * 10)
        self.assertEqual(self.run_gate(text, text), PASS_CODE)

    def test_passes_exactly_at_threshold_mean(self) -> None:
        # totals 90 and 80 give a mean of exactly 85
        self.assertEqual(
            self.run_gate(audit_text([9] * 10), audit_text([8] * 10)),
            PASS_CODE,
        )

    def test_fails_just_below_threshold_mean(self) -> None:
        # totals 90 and 79 give a mean of 84.5
        self.assertEqual(
            self.run_gate(audit_text([9] * 10), audit_text([8] * 9 + [7])),
            FAIL_CODE,
        )

    def test_critical_finding_fails_even_with_high_scores(self) -> None:
        critical = audit_text([10] * 10, findings=("FINDING CRITICAL a.md:3 unsafe command",))
        self.assertEqual(self.run_gate(critical, audit_text([10] * 10)), FAIL_CODE)

    def test_major_finding_does_not_block(self) -> None:
        major = audit_text([10] * 10, findings=("FINDING MAJOR a.md:3 unclear wording",))
        self.assertEqual(self.run_gate(major, audit_text([10] * 10)), PASS_CODE)

    def test_advertised_total_is_not_trusted(self) -> None:
        # advertised 100 but criterion scores re-add to 50
        lying = audit_text([5] * 10, total=100)
        self.assertEqual(self.run_gate(lying, lying), FAIL_CODE)

    def test_wrong_criterion_count_is_invalid(self) -> None:
        self.assertEqual(self.run_gate(audit_text([9] * 9), audit_text([9] * 10)), INVALID_CODE)

    def test_out_of_range_score_is_invalid(self) -> None:
        self.assertEqual(self.run_gate(audit_text([9] * 9 + [11]), audit_text([9] * 10)), INVALID_CODE)

    def test_duplicate_criterion_is_invalid(self) -> None:
        duplicate = "\n".join(["VERDICT same: 9/10"] * 10) + "\n"
        self.assertEqual(self.run_gate(duplicate, audit_text([9] * 10)), INVALID_CODE)

    def test_custom_threshold(self) -> None:
        text = audit_text([9] * 10)
        self.assertEqual(self.run_gate(text, text, "--threshold", "95"), FAIL_CODE)

    def test_missing_file_is_invalid(self) -> None:
        self.assertEqual(GATE.main(["/nonexistent/a.txt", "/nonexistent/b.txt"]), INVALID_CODE)


if __name__ == "__main__":
    unittest.main()
