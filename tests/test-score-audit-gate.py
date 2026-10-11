from __future__ import annotations

import contextlib
import importlib.util
import io
import json
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


def audit_text(
    scores: list[int],
    *,
    total: int | None = None,
    findings: tuple[str, ...] = (),
    names: list[str] | None = None,
) -> str:
    labels = names or [f"criterion {index}" for index in range(1, len(scores) + 1)]
    lines = [f"VERDICT {label}: {score}/10" for label, score in zip(labels, scores)]
    lines.append(f"TOTAL: {sum(scores) if total is None else total}/100")
    lines.extend(findings)
    return "\n".join(lines) + "\n"


class ScoreAuditGateTest(unittest.TestCase):
    def run_gate(self, first: str, second: str, *extra: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for name, text in (("a.txt", first), ("b.txt", second)):
                path = Path(tmp) / name
                path.write_text(text, encoding="utf-8")
                paths.append(str(path))
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = GATE.main([*paths, *extra])
            return code, buffer.getvalue()

    def run_with_lock(self, first: str, second: str, lock: dict[str, object], *extra: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            lock_path = Path(tmp) / "resolved-roles.json"
            lock_path.write_text(json.dumps(lock), encoding="utf-8")
            return self.run_gate(first, second, "--lock", str(lock_path), *extra)

    # --- existing behavior -------------------------------------------------
    def test_passes_above_threshold(self) -> None:
        text = audit_text([9] * 10)
        self.assertEqual(self.run_gate(text, text)[0], PASS_CODE)

    def test_passes_exactly_at_threshold_mean(self) -> None:
        self.assertEqual(self.run_gate(audit_text([9] * 10), audit_text([8] * 10))[0], PASS_CODE)

    def test_fails_just_below_threshold_mean(self) -> None:
        self.assertEqual(self.run_gate(audit_text([9] * 10), audit_text([8] * 9 + [7]))[0], FAIL_CODE)

    def test_critical_finding_fails_even_with_high_scores(self) -> None:
        critical = audit_text([10] * 10, findings=("FINDING CRITICAL a.md:3 unsafe command",))
        self.assertEqual(self.run_gate(critical, audit_text([10] * 10))[0], FAIL_CODE)

    def test_major_finding_does_not_block(self) -> None:
        major = audit_text([10] * 10, findings=("FINDING MAJOR a.md:3 unclear wording",))
        self.assertEqual(self.run_gate(major, audit_text([10] * 10))[0], PASS_CODE)

    def test_advertised_total_is_not_trusted(self) -> None:
        lying = audit_text([5] * 10, total=100)
        self.assertEqual(self.run_gate(lying, lying)[0], FAIL_CODE)

    def test_wrong_criterion_count_is_invalid(self) -> None:
        self.assertEqual(self.run_gate(audit_text([9] * 9), audit_text([9] * 10))[0], INVALID_CODE)

    def test_out_of_range_score_is_invalid(self) -> None:
        self.assertEqual(self.run_gate(audit_text([9] * 9 + [11]), audit_text([9] * 10))[0], INVALID_CODE)

    def test_duplicate_criterion_is_invalid(self) -> None:
        duplicate = "\n".join(["VERDICT same: 9/10"] * 10) + "\n"
        self.assertEqual(self.run_gate(duplicate, audit_text([9] * 10))[0], INVALID_CODE)

    def test_missing_file_is_invalid(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            code = GATE.main(["/nonexistent/a.txt", "/nonexistent/b.txt"])
        self.assertEqual(code, INVALID_CODE)

    # --- malformed contract lines are rejected, not ignored ---------------
    def test_negative_score_line_is_invalid(self) -> None:
        bad = audit_text([9] * 9) + "VERDICT criterion 10: -1/10\n"
        self.assertEqual(self.run_gate(bad, audit_text([9] * 10))[0], INVALID_CODE)

    def test_eleventh_verdict_line_is_invalid(self) -> None:
        extra = audit_text([9] * 10) + "VERDICT extra: 9/10\n"
        self.assertEqual(self.run_gate(extra, audit_text([9] * 10))[0], INVALID_CODE)

    def test_finding_without_location_is_invalid(self) -> None:
        bad = audit_text([10] * 10, findings=("FINDING CRITICAL",))
        self.assertEqual(self.run_gate(bad, audit_text([10] * 10))[0], INVALID_CODE)

    def test_finding_with_unknown_severity_is_invalid(self) -> None:
        bad = audit_text([10] * 10, findings=("FINDING HIGH a.md:3 problem",))
        self.assertEqual(self.run_gate(bad, audit_text([10] * 10))[0], INVALID_CODE)

    def test_free_text_word_starting_like_a_prefix_is_ignored(self) -> None:
        notes = audit_text([10] * 10) + "VERDICTS above were checked twice.\nTOTALLY fine.\n"
        self.assertEqual(self.run_gate(notes, audit_text([10] * 10))[0], PASS_CODE)

    def test_decorated_or_indented_contract_lines_are_invalid(self) -> None:
        decorated = {
            "bullet finding": "- FINDING CRITICAL a.md:3 unsafe command",
            "indented finding": "  FINDING CRITICAL a.md:3 unsafe command",
            "blockquote finding": "> FINDING CRITICAL a.md:3 unsafe command",
            "bold finding": "**FINDING CRITICAL** a.md:3 unsafe command",
            "numbered finding": "1. FINDING CRITICAL a.md:3 unsafe command",
            "decorated verdict": "- VERDICT criterion 11: 9/10",
            "decorated total": "* TOTAL: 100/100",
        }
        for label, line in decorated.items():
            with self.subTest(label):
                bad = audit_text([10] * 10) + line + "\n"
                code, out = self.run_gate(bad, audit_text([10] * 10))
                self.assertEqual(code, INVALID_CODE)
                self.assertIn("a.txt:", out)

    def test_decorated_prose_words_are_still_ignored(self) -> None:
        notes = audit_text([10] * 10) + "- VERDICTS above were checked twice.\n> TOTALLY fine.\n"
        self.assertEqual(self.run_gate(notes, audit_text([10] * 10))[0], PASS_CODE)

    # --- both auditors must score the same criteria -----------------------
    def test_different_criterion_names_are_invalid(self) -> None:
        other = audit_text([9] * 10, names=[f"other {i}" for i in range(1, 11)])
        self.assertEqual(self.run_gate(audit_text([9] * 10), other)[0], INVALID_CODE)

    # --- thresholds and independence --------------------------------------
    def test_threshold_zero_is_invalid(self) -> None:
        zero = audit_text([0] * 10)
        self.assertEqual(self.run_gate(zero, zero, "--threshold", "0")[0], INVALID_CODE)

    def test_threshold_below_full_floor_is_invalid(self) -> None:
        text = audit_text([9] * 10)
        self.assertEqual(self.run_gate(text, text, "--threshold", "84")[0], INVALID_CODE)

    def test_threshold_above_100_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        self.assertEqual(self.run_gate(text, text, "--threshold", "101")[0], INVALID_CODE)

    def test_custom_threshold_above_floor_applies(self) -> None:
        text = audit_text([9] * 10)
        self.assertEqual(self.run_gate(text, text, "--threshold", "95")[0], FAIL_CODE)

    def test_degraded_flag_raises_default_threshold(self) -> None:
        # totals 90 and 80 give mean 85: passes full, fails degraded
        first, second = audit_text([9] * 10), audit_text([8] * 10)
        self.assertEqual(self.run_gate(first, second)[0], PASS_CODE)
        self.assertEqual(self.run_gate(first, second, "--independence", "degraded")[0], FAIL_CODE)

    def test_degraded_passes_at_90(self) -> None:
        # totals 95 and 85 give mean 90
        first, second = audit_text([10] * 5 + [9] * 5), audit_text([9] * 5 + [8] * 5)
        self.assertEqual(self.run_gate(first, second, "--independence", "degraded")[0], PASS_CODE)

    def test_degraded_threshold_below_90_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        code, _ = self.run_gate(text, text, "--independence", "degraded", "--threshold", "85")
        self.assertEqual(code, INVALID_CODE)

    def test_gate_line_reports_independence(self) -> None:
        text = audit_text([10] * 10)
        _, out = self.run_gate(text, text, "--independence", "degraded")
        self.assertIn("GATE: PASS (independence=degraded, threshold=90)", out)

    def test_lock_file_sets_independence(self) -> None:
        first, second = audit_text([9] * 10), audit_text([8] * 10)
        code, out = self.run_with_lock(first, second, {"independence": "degraded"})
        self.assertEqual(code, FAIL_CODE)
        self.assertIn("independence=degraded", out)

    def test_lock_and_flag_conflict_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        code, _ = self.run_with_lock(text, text, {"independence": "full"}, "--independence", "degraded")
        self.assertEqual(code, INVALID_CODE)

    def test_lock_with_same_model_for_both_auditors_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        lock = {
            "independence": "degraded",
            "roles": {"auditor_a": {"model": "m1"}, "auditor_b": {"model": "m1"}},
        }
        self.assertEqual(self.run_with_lock(text, text, lock)[0], INVALID_CODE)

    def test_lock_with_unknown_independence_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        self.assertEqual(self.run_with_lock(text, text, {"independence": "partial"})[0], INVALID_CODE)

    def test_lock_with_non_string_independence_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        for value in ([], {}, 5, None):
            with self.subTest(value=value):
                self.assertEqual(self.run_with_lock(text, text, {"independence": value})[0], INVALID_CODE)

    def test_lock_without_independence_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        self.assertEqual(self.run_with_lock(text, text, {})[0], INVALID_CODE)

    def test_unreadable_lock_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        self.assertEqual(self.run_gate(text, text, "--lock", "/nonexistent/lock.json")[0], INVALID_CODE)

    # --- undecodable input is invalid input (exit 2), not a crash ---------
    def test_undecodable_audit_file_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "a.txt", Path(tmp) / "b.txt"
            first.write_bytes(b"\xff\xfe\x00")
            second.write_text(audit_text([10] * 10), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                code = GATE.main([str(first), str(second)])
        self.assertEqual(code, INVALID_CODE)

    def test_undecodable_lock_file_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first, second, lock = Path(tmp) / "a.txt", Path(tmp) / "b.txt", Path(tmp) / "lock.json"
            for path in (first, second):
                path.write_text(audit_text([10] * 10), encoding="utf-8")
            lock.write_bytes(b"\xff\xfe\x00")
            with contextlib.redirect_stdout(io.StringIO()):
                code = GATE.main([str(first), str(second), "--lock", str(lock)])
        self.assertEqual(code, INVALID_CODE)

    def test_exotic_decorations_of_contract_lines_are_invalid(self) -> None:
        decorated = [
            "+ FINDING CRITICAL a.md:3 x",
            "1. **FINDING CRITICAL** a.md:3 x",
            "1) FINDING CRITICAL a.md:3 x",
            "• FINDING CRITICAL a.md:3 x",
            "| FINDING CRITICAL | a.md:3 | x |",
            "(FINDING CRITICAL a.md:3 x)",
            "[FINDING CRITICAL] a.md:3 x",
            "⚠️ FINDING CRITICAL a.md:3 x",
            "_FINDING CRITICAL_ a.md:3 x",
            "- TOTAL: 100/100",
            "> VERDICT extra: 10/10",
        ]
        for line in decorated:
            with self.subTest(line=line):
                text = audit_text([10] * 10) + line + "\n"
                self.assertEqual(self.run_gate(text, audit_text([10] * 10))[0], INVALID_CODE)

    def test_contract_lines_with_letter_or_digit_decoration_are_invalid(self) -> None:
        decorated = [
            "| 1 | FINDING CRITICAL | a.md:3 | x |",
            "1.1 FINDING CRITICAL a.md:3 x",
            "#1 FINDING CRITICAL a.md:3 x",
            "1: FINDING CRITICAL a.md:3 x",
            "a) FINDING CRITICAL a.md:3 x",
            "(a) FINDING CRITICAL a.md:3 x",
            "iv. FINDING CRITICAL a.md:3 x",
            "1\ufe0f\u20e3 FINDING CRITICAL a.md:3 x",
            "\u2460 FINDING CRITICAL a.md:3 x",
            "Auditor A: FINDING CRITICAL a.md:3 x",
            "**Result:** FINDING CRITICAL a.md:3 x",
            "Step 2 - FINDING CRITICAL a.md:3 x",
            "Finding CRITICAL a.md:3 x",
            "Auditor A: VERDICT clarity: 9/10",
            "Result - TOTAL: 90/100",
        ]
        for line in decorated:
            with self.subTest(line=line):
                text = audit_text([10] * 10) + line + "\n"
                self.assertEqual(self.run_gate(text, audit_text([10] * 10))[0], INVALID_CODE)

    def test_prose_with_reserved_words_in_running_text_is_ignored(self) -> None:
        prose = [
            "finding critical issues took a while",
            "- Finding the root cause",
            "1. Total cost was low.",
            "NOTE that the TOTAL is re-added",
            "Each VERDICT line is parsed",
            "This FINDING was already reported",
            "Finding Critical is treated as prose because the contract is ALL CAPS.",
        ]
        text = audit_text([10] * 10) + "\n".join(prose) + "\n"
        self.assertEqual(self.run_gate(text, audit_text([10] * 10))[0], PASS_CODE)

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


if __name__ == "__main__":
    unittest.main()
