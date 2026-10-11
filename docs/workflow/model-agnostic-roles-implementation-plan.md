# Model-Agnostic Roles Implementation Plan (Plan A: Foundation)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the audit gate's roles capability-based and model-agnostic, harden the scorer, add degraded-independence mode, and ship the profile format and harness reference, without any model names in core docs.

**Architecture:** The role contract moves into `artifact-group-audit-workflow.md` as capabilities and permissions. Model names live only in `profiles/*.md` (a JSON block inside Markdown). The scorer reads one `independence` value from an optional lock file and derives its threshold from it. The dynamic resolver, dispatcher, and qualification fixture are Plan B and are out of scope here.

**Tech Stack:** Python 3.14 standard library only (`argparse`, `json`, `re`, `datetime`, `unittest`), Markdown.

**Spec:** `docs/workflow/model-agnostic-roles-design.md`

**Scope note:** The spec covers two independent subsystems. This is Plan A. Plan B (`scripts/resolve-roles.py`, `scripts/dispatch-role.py`, `qualification/`) is written after Plan A lands and after round 2 of `polyglot-protocol-upgrade-plan.md`, because it depends on the profile format and the hardened scorer.

## Global Constraints

- Default operational scripts to Python; standard library only; no new dependency.
- Filenames are kebab-case and contain no digits or dates.
- Scorer exit codes: `0` gate passed, `1` gate failed, `2` invalid input.
- Gate thresholds: `85` for `full` independence, `90` for `degraded`. A lower threshold than the floor is rejected. A threshold above `100` is rejected.
- The four roles are exactly `orchestrator`, `auditor_a`, `auditor_b`, `worker`.
- Core docs (`artifact-group-audit-workflow.md`, `dev-workflow.md`, `SKILL.md`) name no model.
- `independence` has exactly one source: the lock file when present, otherwise `--independence`, otherwise `full`.
- Profile `licence_policy` is one of `any`, `permissive`, `commercial-ok`.
- Tests are `unittest` files named `tests/test-*.py` and run as `python tests/<file>`.
- Do not claim `100/100` anywhere; validators report `PASS` or `FAIL`.

## File Structure

| File | Responsibility |
|---|---|
| `scripts/score-audit-gate.py` | Parse two auditor outputs, validate the contract, apply the gate rule |
| `tests/test-score-audit-gate.py` | Scorer behavior, including every rejection path |
| `profiles/default.md` | Default profile (Claude Code and Codex) |
| `profiles/opencode-open-weights.md` | Open-weight example profile for OpenCode |
| `profiles/template.md` | Blank profile to copy |
| `scripts/validate-workspace.py` | Adds `validate_profile`, `check_profiles`, `check_core_docs_model_neutral` |
| `tests/test-validate-workspace.py` | Tests for the three new validator functions |
| `docs/workflow/role-resolution.md` | Harness classes, capability contract, observed-harness table |
| `docs/workflow/artifact-group-audit-workflow.md` | Role contract and procedure without model names |
| `adapters/*` | Collapse to a pointer at `SKILL.md` and the profile |

---

### Task 1: Harden the scorer and add degraded independence

**Files:**
- Modify: `scripts/score-audit-gate.py` (replace the whole file)
- Modify: `tests/test-score-audit-gate.py` (replace the whole file)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `score-audit-gate.py` CLI: `score-audit-gate.py AUDIT_A AUDIT_B [--threshold N] [--independence full|degraded] [--lock PATH]`. The lock file is JSON with an `independence` key (`"full"` or `"degraded"`) and an optional `roles` map holding `auditor_a.model` and `auditor_b.model`. Python API used by tests: `main(argv: list[str] | None = None) -> int`.

- [ ] **Step 1: Write the failing tests**

Replace `tests/test-score-audit-gate.py` with:

```python
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
        self.assertEqual(GATE.main(["/nonexistent/a.txt", "/nonexistent/b.txt"]), INVALID_CODE)

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

    def test_unreadable_lock_is_invalid(self) -> None:
        text = audit_text([10] * 10)
        self.assertEqual(self.run_gate(text, text, "--lock", "/nonexistent/lock.json")[0], INVALID_CODE)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -B tests/test-score-audit-gate.py 2>&1 | tail -8`
Expected: FAIL. Several tests error with `unrecognized arguments: --independence` or assert the wrong exit code, and `test_negative_score_line_is_invalid` fails because the current scorer ignores the malformed line.

- [ ] **Step 3: Write the implementation**

Replace `scripts/score-audit-gate.py` with:

```python
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
RESERVED_RE = re.compile(r"^(VERDICT|TOTAL|FINDING)\b")
VERDICT_RE = re.compile(r"^VERDICT (?P<name>.+?): (?P<score>\d+)/10\s*$")
TOTAL_RE = re.compile(r"^TOTAL: (?P<total>\d+)/100\s*$")
FINDING_RE = re.compile(r"^FINDING (?P<severity>CRITICAL|MAJOR|MINOR) (?P<where>\S+) (?P<text>.+?)\s*$")


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

    Any line that starts with a reserved prefix must match the contract.

    Complexity: O(n) in the number of lines.

    Raises:
        InvalidInputError: if a reserved-prefix line is malformed, a criterion
            repeats, a score is out of range, or the criterion count is wrong.
    """
    scores: dict[str, int] = {}
    advertised: int | None = None
    findings: list[tuple[str, str, str]] = []

    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not RESERVED_RE.match(line):
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
    if not isinstance(data, dict):
        raise InvalidInputError(f"lock file {path} must contain a JSON object")
    mode = data.get("independence")
    if mode not in THRESHOLDS:
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -B tests/test-score-audit-gate.py 2>&1 | tail -5`
Expected: `Ran 29 tests` and `OK`.

- [ ] **Step 5: Confirm the real round 1 outputs still parse**

Run: `python -B scripts/score-audit-gate.py <scratchpad>/out-sol-G5.txt <scratchpad>/out-opus-G5.txt; echo exit=$?`
Expected: either a normal `GATE:` line, or `invalid input:` naming a malformed line in a real auditor output. If it reports a malformed line, that is a real contract violation in the auditor output, so record it in the audit log. Do not loosen the scorer.

- [ ] **Step 6: Commit**

```bash
git add scripts/score-audit-gate.py tests/test-score-audit-gate.py
git commit -m "Harden audit gate scorer and add degraded independence mode"
```

---

### Task 2: Profile format, validator checks, and the three profiles

**Files:**
- Modify: `scripts/validate-workspace.py`
- Create: `tests/test-validate-workspace.py`
- Create: `profiles/default.md`, `profiles/opencode-open-weights.md`, `profiles/template.md`

**Interfaces:**
- Consumes: nothing from Task 1.
- Produces in `scripts/validate-workspace.py`:
  - `validate_profile(data: object, today: date) -> tuple[list[str], list[str]]` returns `(errors, warnings)`.
  - `extract_profile_json(text: str) -> object` returns the parsed first ` ```json ` fenced block, and raises `ValueError` when none exists.
  - `check_profiles() -> list[str]` returns errors and prints warnings.
  - `check_core_docs_model_neutral() -> list[str]`.
  - Module constants `ROLES = ("orchestrator", "auditor_a", "auditor_b", "worker")` and `LICENCE_POLICIES = ("any", "permissive", "commercial-ok")`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test-validate-workspace.py`:

```python
from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_workspace", ROOT / "scripts" / "validate-workspace.py")
assert SPEC is not None and SPEC.loader is not None
VW = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VW
SPEC.loader.exec_module(VW)

TODAY = date(2026, 10, 11)


def good_profile() -> dict[str, object]:
    return {
        "name": "example",
        "harnesses": {"h1": {"command": "tool -m {model} {prompt_file}", "roles": ["auditor_a"]}},
        "constraints": {
            "allowed_providers": [],
            "max_cost_per_mtok": None,
            "licence_policy": "any",
            "local_only": False,
        },
        "pins": {},
        "fallback": {role: {"harness": "h1", "model": "m"} for role in VW.ROLES},
        "verified_on": "2026-10-01",
        "sources": ["https://example.org/docs"],
    }


class ValidateProfileTest(unittest.TestCase):
    def test_good_profile_has_no_errors_or_warnings(self) -> None:
        errors, warnings = VW.validate_profile(good_profile(), TODAY)
        self.assertEqual((errors, warnings), ([], []))

    def test_missing_required_key_is_an_error(self) -> None:
        data = good_profile()
        del data["fallback"]
        errors, _ = VW.validate_profile(data, TODAY)
        self.assertTrue(any("fallback" in e for e in errors))

    def test_fallback_must_cover_exactly_the_four_roles(self) -> None:
        data = good_profile()
        del data["fallback"]["worker"]  # type: ignore[index]
        errors, _ = VW.validate_profile(data, TODAY)
        self.assertTrue(any("worker" in e for e in errors))

    def test_unknown_licence_policy_is_an_error(self) -> None:
        data = good_profile()
        data["constraints"]["licence_policy"] = "whatever"  # type: ignore[index]
        errors, _ = VW.validate_profile(data, TODAY)
        self.assertTrue(any("licence_policy" in e for e in errors))

    def test_bad_date_is_an_error(self) -> None:
        data = good_profile()
        data["verified_on"] = "10/01/2026"
        errors, _ = VW.validate_profile(data, TODAY)
        self.assertTrue(any("verified_on" in e for e in errors))

    def test_old_verification_date_is_a_warning_not_an_error(self) -> None:
        data = good_profile()
        data["verified_on"] = "2026-08-01"
        errors, warnings = VW.validate_profile(data, TODAY)
        self.assertEqual(errors, [])
        self.assertTrue(any("30 days" in w for w in warnings))

    def test_fallback_harness_must_be_declared(self) -> None:
        data = good_profile()
        data["fallback"]["worker"] = {"harness": "ghost", "model": "m"}  # type: ignore[index]
        errors, _ = VW.validate_profile(data, TODAY)
        self.assertTrue(any("ghost" in e for e in errors))

    def test_non_object_profile_is_an_error(self) -> None:
        errors, _ = VW.validate_profile([], TODAY)
        self.assertTrue(errors)


class ExtractProfileJsonTest(unittest.TestCase):
    def test_extracts_first_json_block(self) -> None:
        text = "# T\n\n```json\n{\"name\": \"x\"}\n```\n"
        self.assertEqual(VW.extract_profile_json(text), {"name": "x"})

    def test_missing_block_raises(self) -> None:
        with self.assertRaises(ValueError):
            VW.extract_profile_json("# no block\n")

    def test_invalid_json_raises(self) -> None:
        with self.assertRaises(ValueError):
            VW.extract_profile_json("```json\n{bad}\n```\n")


class ModelNeutralTest(unittest.TestCase):
    def test_flags_model_family_names(self) -> None:
        self.assertEqual(VW.find_model_names("uses Sonnet and gpt-6"), ["Sonnet", "gpt-"])

    def test_clean_text_has_no_hits(self) -> None:
        self.assertEqual(VW.find_model_names("auditor A and auditor B"), [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -B tests/test-validate-workspace.py 2>&1 | tail -6`
Expected: FAIL with `AttributeError: module 'validate_workspace' has no attribute 'ROLES'`.

- [ ] **Step 3: Write the implementation**

In `scripts/validate-workspace.py`, add these imports at the top of the import block:

```python
import json
import re
from datetime import date
```

Add these definitions after the existing module constants (`ADAPTER_READMES`):

```python
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
```

Add these functions before `check_files`:

```python
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
```

In `main`, add after `errors.extend(run_script_tests())`:

```python
    errors.extend(check_profiles())
    errors.extend(check_core_docs_model_neutral())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -B tests/test-validate-workspace.py 2>&1 | tail -4`
Expected: `Ran 13 tests` and `OK`.

- [ ] **Step 5: Create `profiles/default.md`**

````markdown
# Default Profile

The default stack: Claude Code as the orchestrator session, with Codex and a
second Claude model as independent auditors. Model identifiers live only in
this file.

```json
{
  "name": "default",
  "harnesses": {
    "claude-code": {
      "command": "claude -p --model {model} --disallowedTools Edit Write < {prompt_file}",
      "roles": ["orchestrator", "auditor_b", "worker"]
    },
    "codex": {
      "command": "codex exec --sandbox read-only --skip-git-repo-check -m {model} --output-last-message {output_file} \"$(cat {prompt_file})\"",
      "roles": ["auditor_a"]
    }
  },
  "constraints": {
    "allowed_providers": [],
    "max_cost_per_mtok": null,
    "licence_policy": "any",
    "local_only": false
  },
  "pins": {},
  "fallback": {
    "orchestrator": {"harness": "claude-code", "model": "claude-sonnet-5-5"},
    "auditor_a": {"harness": "codex", "model": "gpt-6.1-sol"},
    "auditor_b": {"harness": "claude-code", "model": "claude-opus-5-5"},
    "worker": {"harness": "claude-code", "model": "claude-haiku-5-5"}
  },
  "verified_on": "2026-10-11",
  "sources": [
    "https://platform.claude.com/docs/en/about-claude/models/overview",
    "codex exec -m gpt-6.1-sol answered on the reference machine on 2026-10-11"
  ]
}
```

Auditor A and Auditor B come from different families (OpenAI and Anthropic), so
this profile runs the gate in `full` independence.
````

- [ ] **Step 6: Create `profiles/opencode-open-weights.md`**

````markdown
# OpenCode Open-Weight Profile

An example fallback for users running OpenCode with open-weight models. The
resolver replaces it when discovery works. Almost every benchmark figure behind
these choices is vendor-reported; only the DeepSWE leaderboard is independent.

Licence notes: Kimi K3, GLM-5.3, and MiniMax-M3 carry licences with revenue or
commercial-use conditions. Set `licence_policy` to `permissive` or
`commercial-ok` if that matters to you.

```json
{
  "name": "opencode-open-weights",
  "harnesses": {
    "opencode": {
      "command": "opencode run --agent {agent} --model {model} --format json \"$(cat {prompt_file})\"",
      "roles": ["orchestrator", "auditor_a", "auditor_b", "worker"]
    }
  },
  "constraints": {
    "allowed_providers": ["opencode-go", "opencode", "openrouter", "ollama"],
    "max_cost_per_mtok": null,
    "licence_policy": "any",
    "local_only": false
  },
  "pins": {},
  "fallback": {
    "orchestrator": {"harness": "opencode", "model": "opencode-go/glm-5.3"},
    "auditor_a": {"harness": "opencode", "model": "opencode-go/kimi-k3"},
    "auditor_b": {"harness": "opencode", "model": "opencode-go/deepseek-v4.1-flash"},
    "worker": {"harness": "opencode", "model": "opencode-go/mimo-v2.6-flash"}
  },
  "verified_on": "2026-10-11",
  "sources": [
    "https://opencode.ai/docs/agents/",
    "https://opencode.ai/docs/go/",
    "https://models.dev/api.json",
    "https://deepswe.datacurve.ai/"
  ]
}
```

Scripted auditors must use agents with `mode: "all"`, not `subagent`, or
`opencode run --agent` silently falls back to the default agent and loses its
read-only permissions. Auditor A and Auditor B come from different families
(Moonshot and DeepSeek), so this profile runs in `full` independence.
````

- [ ] **Step 7: Create `profiles/template.md`**

````markdown
# Profile Template

Copy this file to `.polyglot/profile.md` in your project, or into `profiles/`,
and fill it in. Every key is required.

```json
{
  "name": "my-profile",
  "harnesses": {
    "my-harness": {
      "command": "my-tool run --model {model} --prompt-file {prompt_file}",
      "roles": ["orchestrator", "auditor_a", "auditor_b", "worker"]
    }
  },
  "constraints": {
    "allowed_providers": [],
    "max_cost_per_mtok": null,
    "licence_policy": "any",
    "local_only": false
  },
  "pins": {},
  "fallback": {
    "orchestrator": {"harness": "my-harness", "model": "orchestrator-model-id"},
    "auditor_a": {"harness": "my-harness", "model": "first-auditor-model-id"},
    "auditor_b": {"harness": "my-harness", "model": "second-auditor-model-id"},
    "worker": {"harness": "my-harness", "model": "worker-model-id"}
  },
  "verified_on": "2026-10-11",
  "sources": ["https://example.org/where-you-confirmed-these-models"]
}
```

Rules: use two different model families for `auditor_a` and `auditor_b` when you
can. If you cannot, use two different models from one family and the gate runs
in degraded independence. Never use the same model for both auditors.
````

- [ ] **Step 8: Run the full validator**

Run: `python -B scripts/validate-workspace.py 2>&1 | tail -6`
Expected: `workspace validation: FAIL` with `docs/workflow/artifact-group-audit-workflow.md names models [...]`. This is the intended failure that Task 3 fixes. No profile errors should appear.

- [ ] **Step 9: Commit**

```bash
git add scripts/validate-workspace.py tests/test-validate-workspace.py profiles/
git commit -m "Add profile format, validator checks, and default profiles"
```

---

### Task 3: Role-resolution reference doc

**Files:**
- Create: `docs/workflow/role-resolution.md`

**Interfaces:**
- Consumes: the profile JSON schema from Task 2.
- Produces: the document the audit workflow links to for harness classes and the observed-harness table.

- [ ] **Step 1: Create `docs/workflow/role-resolution.md`**

```markdown
# Role Resolution

How the audit gate's four roles are filled by models, and how harnesses are
treated. The role contract itself lives in `artifact-group-audit-workflow.md`.
The design rationale is in `model-agnostic-roles-design.md`.

## Status

The profile format and the harness reference below are in force. The automatic
resolver (`scripts/resolve-roles.py`), the dispatcher
(`scripts/dispatch-role.py`), and the qualification fixture are a later plan and
are not implemented yet. Until they exist, role-to-model mapping comes from the
selected profile's `fallback` block.

## Profile Selection

1. A project profile at `.polyglot/profile.md`, if present.
2. Otherwise a named profile in `profiles/`.
3. Otherwise `profiles/default.md`.

A profile is Markdown with one ` ```json ` block. Required keys: `name`,
`harnesses`, `constraints`, `pins`, `fallback`, `verified_on`, `sources`.
`scripts/validate-workspace.py` checks them and warns when `verified_on` is
older than 30 days.

## Harness Classes

| Class | Definition | Can fill |
|---|---|---|
| Dispatchable | Runs headless with a prompt and a model, and prints the final answer | Any role |
| Session-only | Interactive or GUI only | Orchestrator only |

A user whose only harness is session-only runs the other roles sequentially in
the same session with fresh context, and the gate is always degraded.

## Model Sources Are Not Harnesses

Ollama, OpenRouter, and vendor APIs are model sources. They are reached through
a harness that supports them. A model runner with no agent loop and no file
tools cannot fill an auditor role by itself.

## Capability Contract

Each capability is tested, never assumed.

| Capability | Required for |
|---|---|
| Run headless with a prompt file | Auditor, Worker |
| Select a model per invocation | Auditor A and B from different models in one harness |
| Print the final answer to stdout | Auditor, Worker |
| Enforce read-only | Preferred; always backed by the snapshot check |
| Web tool | Auditor |
| Parallel fan-out | Worker |

A harness that cannot select a model per invocation is `fixed-model per
configuration`: it can fill one role, not several with different models.

A harness is `multi-family` when it exposes models from more than one family and
`single-family` otherwise. A multi-family harness can satisfy the independence
rule alone.

## Read-Only Is Verified

Before each auditor or worker run, snapshot the tree (for example
`git status --short` plus a hash of every modified and untracked file). After
the run, compare. Any change invalidates that run: record the changed paths and
re-dispatch once. This works for every harness, including unknown ones.

## Unknown Harnesses

Add one command template to the profile's `harnesses` block with `{model}` and
`{prompt_file}` placeholders. It must run headless and print the final answer to
stdout. Everything else is probed.

## Observed Harnesses

Observed on 2026-10-11 from each tool's own `--help` or official documentation.
Re-probe before relying on a row.

| Harness | Headless | Model per run | Read-only mechanism observed | Notes |
|---|---|---|---|---|
| Codex | `exec` | `-m` | `--sandbox read-only` (OS level) | |
| Claude Code | `-p` | `--model` | `--allowedTools`, `--disallowedTools` | |
| OpenCode | `run` | `-m provider/model` | per-agent `permission` config | Scripted auditors need `mode: "all"`; subagent depth defaults to 1 |
| Grok | `-p/--single`, `--prompt-file` | `-m` | `--allowedTools`, `--disallowed-tools` | Single family |
| Gemini CLI | `-p` | `-m` | `--approval-mode`, `--sandbox` | |
| Cursor Agent | `-p` | `--model` | `--mode plan` (planning, no edits) | |
| Pi | `-p` | `--model` | `--tools` allowlist | |
| Crush | `run` | `-m provider/model` | none observed | Relies on the snapshot check |
| Copilot | `-p` | `--model` | `--deny-tool` / `--allow-tool` rules | No OS-level read-only observed |
| ZCode | `-p` | none; session level | `--mode plan`, `--disallowed-tools` | `-p` defaults to `yolo`; fixed model per configuration |
| Antigravity (`agy`) | `-p` | `--model <slug>` | none documented | Default mode pauses for review; headless needs `permissions.allow` or `--dangerously-skip-permissions`. From documentation, not probed |
| Ollama | none | n/a | n/a | Model runner, not a harness |

## Safest Invocation

Record the least-permissive invocation observed for each role, not just any
working one. For example, launch a ZCode auditor with `--mode plan` and write
tools disallowed rather than the `-p` default.
```

- [ ] **Step 2: Verify naming rules**

Run: `python -B scripts/validate-workspace.py 2>&1 | grep -i "role-resolution\|uppercase\|kebab" || echo "no naming errors"`
Expected: `no naming errors`.

- [ ] **Step 3: Commit**

```bash
git add docs/workflow/role-resolution.md
git commit -m "Add role resolution and harness reference"
```

---

### Task 4: Capability-based audit workflow doc and wiring

**Files:**
- Modify: `docs/workflow/artifact-group-audit-workflow.md`
- Modify: `docs/workflow/dev-workflow.md`
- Modify: `SKILL.md`
- Modify: `readme.md`
- Modify: `docs/AGENTS.md`

**Interfaces:**
- Consumes: the scorer CLI (Task 1), `profiles/` (Task 2), `role-resolution.md` (Task 3).
- Produces: model-neutral docs that satisfy `check_core_docs_model_neutral`.

- [ ] **Step 1: Replace the Roles section in `artifact-group-audit-workflow.md`**

Replace this exact block:

```markdown
| Role | Model and effort | Responsibility |
|---|---|---|
| Orchestrator | Sonnet 5.5, high | Plans, dispatches, builds the artifact group and audit prompt, computes scores, applies fixes |
| `haiku-worker` (up to 8) | Haiku 5.5, max | Basic operations only: read, list, grep, copy verbatim. Never scores, judges, or edits |
| `sol-auditor` | Codex gpt-6.1-sol, high | Independent read-only audit. Scores 10 criteria out of 100 |
| `opus-auditor` | Opus 5.5, high | Independent read-only audit. Scores 10 criteria out of 100 |

Rules:

- Auditors are read-only and never edit files.
- Auditors run in parallel and must not see each other's output.
- Only the orchestrator fixes findings.
- Verify each model is available locally before dispatch. If one is not, record
  the blocker. Do not substitute a different model or self-audit silently.
```

with:

```markdown
Roles are defined by capability and permission. Which model fills a role comes
from the selected profile (see `role-resolution.md`), never from this document.

| Role | Must be able to | May touch | Count |
|---|---|---|---|
| Orchestrator | Plan long-horizon work, use tools, dispatch roles, apply fixes | Read and write; the only role that edits | 1 |
| Auditor A, Auditor B | Read many files, score ten criteria, verify facts on the web with cited sources, emit the output contract | Read-only; web allowed; no edits; no spawning | 2 |
| Worker | Read, list, grep, and copy text verbatim | Read only; no web | up to 8 |

The orchestrator is the session the user is already in. Every other role is a
command dispatched through a harness.

Rules:

- Auditors are read-only and never edit files.
- Auditors run in parallel and must not see each other's output.
- Only the orchestrator fixes findings.
- **Independence.** Auditor A and Auditor B come from different model families.
- **Capability check.** Before dispatch, confirm each model can do what its role
  needs. A model that cannot is a blocker. Do not substitute a different model
  or self-audit silently.
- **Read-only is verified.** Snapshot the tree before and after each auditor or
  worker run. Any change invalidates that run, whatever the harness claims.
- **Degraded mode.** If two families are not available, two different models from
  one family are allowed. Record `degraded independence` in the audit log. The
  pass bar rises to `90` and the deterministic checks must pass. Running the same
  model twice is a blocker.
```

- [ ] **Step 2: Update the Procedure steps**

Replace `up to 8 \`haiku-worker\` agents` with `up to 8 workers` (step 1).

Replace step 2's first sentence `\`sol-auditor\` and \`opus-auditor\` run in parallel against the same` with `Auditor A and Auditor B run in parallel against the same`.

Replace `One \`haiku-worker\` greps each auditor's verdict lines` with `One worker greps each auditor's verdict lines`.

Replace the step 4 command block and the sentence after it with:

```markdown
   ```sh
   python scripts/score-audit-gate.py <auditor-a-output> <auditor-b-output> \
     [--lock resolved-roles.json | --independence full|degraded]
   ```

   The script ignores each advertised `TOTAL`, reports any discrepancy, rejects
   malformed contract lines and mismatched criterion names, and exits `0` when
   the gate passes, `1` when it fails, and `2` when an input is invalid. Record
   its output in the audit log.
```

Replace step 5 with:

```markdown
5. **Gate.** In `full` independence the group passes when the mean is `85` or
   more. In `degraded` independence the mean must be `90` or more. In both modes
   neither auditor may raise a `CRITICAL` finding.
```

- [ ] **Step 3: Update `dev-workflow.md`**

Replace this exact block:

```markdown
1. Prep: up to 8 `haiku-worker` agents read, list, and grep the group's files.
2. Audit: `sol-auditor` and `opus-auditor` score the group independently, in
   parallel, read-only, across 10 criteria out of `100`.
3. Check: `haiku-worker` copies verdict lines and severity tags verbatim.
```

with:

```markdown
1. Prep: up to 8 workers read, list, and grep the group's files.
2. Audit: Auditor A and Auditor B, from different model families, score the
   group independently, in parallel, read-only, across 10 criteria out of `100`.
3. Check: a worker copies verdict lines and severity tags verbatim.
```

Replace `5. Gate: pass at a mean of \`85\` or more with no \`CRITICAL\` finding.` with:

```markdown
5. Gate: pass at a mean of `85` or more with no `CRITICAL` finding. When two
   model families are not available the gate runs in degraded independence and
   the bar is `90`. Models come from `profiles/`; see
   `docs/workflow/role-resolution.md`.
```

- [ ] **Step 4: Update `SKILL.md`**

In the Reference Map, after the line `- Gate scorer: \`scripts/score-audit-gate.py\`` add:

```markdown
- Role resolution and harness reference: `docs/workflow/role-resolution.md`
- Model profiles: `profiles/`
```

Replace the Core Rules bullet that begins `- An artifact group passes its audit gate at a mean score of` with:

```markdown
- An artifact group passes its audit gate at a mean score of `85` or more from
  two independent auditors with no `CRITICAL` finding (`90` when only one model
  family is available). The gate lets work continue and is not a completion
  claim. Model names live only in `profiles/`.
```

- [ ] **Step 5: Update `readme.md` and `docs/AGENTS.md`**

In `readme.md`, after the `docs/workflow/artifact-group-audit-workflow.md` bullet in "What It Includes", add:

```markdown
- `docs/workflow/role-resolution.md`: how audit roles map to models and
  harnesses
- `profiles/`: default and open-weight model profiles, and a blank template
```

In `docs/AGENTS.md`, after the `artifact-group-audit-workflow.md` index line, add:

```markdown
- `docs/workflow/role-resolution.md`: Harness classes, capability contract, and observed harnesses.
- `profiles/`: Model profiles (`default`, `opencode-open-weights`, `template`) used by the audit gate.
```

- [ ] **Step 6: Verify**

Run: `python -B scripts/validate-workspace.py 2>&1 | tail -4`
Expected: `workspace validation: PASS`, with no `names models` error.

Run: `grep -nE "Sonnet|Opus|Haiku|gpt-|haiku-worker|sol-auditor|opus-auditor" docs/workflow/artifact-group-audit-workflow.md docs/workflow/dev-workflow.md SKILL.md || echo "model-neutral"`
Expected: `model-neutral`.

- [ ] **Step 7: Commit**

```bash
git add docs/workflow/artifact-group-audit-workflow.md docs/workflow/dev-workflow.md SKILL.md readme.md docs/AGENTS.md
git commit -m "Make audit workflow roles capability-based and model-neutral"
```

---

### Task 5: Collapse the adapters

**Files:**
- Modify: `adapters/codex/AGENTS.md`, `adapters/codex/readme.md`
- Modify: `adapters/claude-code/CLAUDE.md`, `adapters/claude-code/readme.md`
- Modify: `adapters/opencode/AGENTS.md`, `adapters/opencode/readme.md`

**Interfaces:**
- Consumes: `SKILL.md` (existing), `profiles/` (Task 2).
- Produces: six short files that point at the installed skill. `validate-workspace.py` still requires the three `readme.md` files.

- [ ] **Step 1: Overwrite each guidance file**

`adapters/codex/AGENTS.md`:

```markdown
# The Polyglot Protocol (Codex)

Read `SKILL.md` in the installed skill folder and follow its Required Workflow
in order. Validate from the skill root with `python scripts/validate-workspace.py`.
The default model profile is `profiles/default.md`.
```

`adapters/claude-code/CLAUDE.md`:

```markdown
# The Polyglot Protocol (Claude Code)

Read `SKILL.md` in the installed skill folder and follow its Required Workflow
in order. Validate from the skill root with `python scripts/validate-workspace.py`.
The default model profile is `profiles/default.md`.
```

`adapters/opencode/AGENTS.md`:

```markdown
# The Polyglot Protocol (OpenCode)

Read `SKILL.md` in the installed skill folder and follow its Required Workflow
in order. Validate from the skill root with `python scripts/validate-workspace.py`.
For open-weight models use `profiles/opencode-open-weights.md`. Scripted
auditors must use agents with `mode: "all"`.
```

- [ ] **Step 2: Overwrite each readme**

`adapters/codex/readme.md`:

```markdown
# Codex Adapter

Copy or install the whole skill folder, not this file alone, because the
guidance links resolve from the skill root.

- Entry point: `SKILL.md`
- Guidance file: `AGENTS.md` (in this folder)
- Model profile: `profiles/default.md`

Validate from the skill root: `python scripts/validate-workspace.py`.
```

`adapters/claude-code/readme.md`:

```markdown
# Claude Code Adapter

Copy or install the whole skill folder, not this file alone, because the
guidance links resolve from the skill root.

- Entry point: `SKILL.md`
- Guidance file: `CLAUDE.md` (in this folder)
- Model profile: `profiles/default.md`

Validate from the skill root: `python scripts/validate-workspace.py`.
```

`adapters/opencode/readme.md`:

```markdown
# OpenCode Adapter

Copy or install the whole skill folder, not this file alone, because the
guidance links resolve from the skill root.

- Entry point: `SKILL.md`
- Guidance file: `AGENTS.md` (in this folder)
- Model profile for open-weight models: `profiles/opencode-open-weights.md`

OpenCode reads global skills from `~/.config/opencode/skills` and
`~/.agents/skills`. Validate from the skill root:
`python scripts/validate-workspace.py`.
```

- [ ] **Step 3: Verify**

Run: `python -B scripts/validate-workspace.py 2>&1 | tail -3`
Expected: `workspace validation: PASS`.

- [ ] **Step 4: Commit**

```bash
git add adapters/
git commit -m "Collapse adapters to point at SKILL.md and profiles"
```

---

### Task 6: Verification and audit log

**Files:**
- Modify: `docs/workflow/polyglot-protocol-upgrade-plan.md` (mark P0-13 done)
- Create: `docs/workflow/model-agnostic-roles-audits.md`

**Interfaces:**
- Consumes: everything above.
- Produces: the audit log for this workflow run.

- [ ] **Step 1: Run every check**

Run:

```bash
python -B tests/test-score-audit-gate.py 2>&1 | tail -3
python -B tests/test-validate-workspace.py 2>&1 | tail -3
python -B scripts/validate-workspace.py 2>&1 | tail -3
git diff --check && echo "diff-check: clean"
```

Expected: `OK` for both test files, `workspace validation: PASS`, `diff-check: clean`.

- [ ] **Step 2: Re-score a real round 1 pair with the hardened scorer**

Run: `python -B scripts/score-audit-gate.py <scratchpad>/out-sol-G6.txt <scratchpad>/out-opus-G6.txt --independence full; echo exit=$?`
Expected: `GATE: FAIL (independence=full, threshold=85)` and `exit=1`, matching the earlier mean of `70.0`. If it prints `invalid input:`, record the exact line in the audit log as a real contract violation in the auditor output.

- [ ] **Step 3: Create `docs/workflow/model-agnostic-roles-audits.md`**

Record: the date, the commands and their real output from Step 1 and Step 2, any `invalid input` lines found in real auditor outputs, the three-round planning, coding, and guidance-file audit tables scored honestly (including any criterion that cannot reach `10/10` and why), and a final-pass checklist. Do not claim `100/100` unless every criterion is `10/10` with evidence.

- [ ] **Step 4: Mark the upgrade plan item**

In `docs/workflow/polyglot-protocol-upgrade-plan.md`, change the P0-13 row's Recommendation cell to start with `Done in model-agnostic-roles Plan A.`

- [ ] **Step 5: Commit**

```bash
git add docs/workflow/model-agnostic-roles-audits.md docs/workflow/polyglot-protocol-upgrade-plan.md
git commit -m "Record model-agnostic roles verification and audit log"
```

---

## Self-Review

**Spec coverage.**

| Spec requirement | Task |
|---|---|
| Role contract, capability-based, no model names | 4 |
| Independence rule and degraded mode (`90`) | 1, 4 |
| Read-only verified by snapshot | 3, 4 (documented; enforced by the dispatcher in Plan B) |
| Scorer: lock file, floors, malformed lines, criterion names, mode on `GATE:` line | 1 |
| Profiles directory, project override, three shipped profiles | 2, 3 |
| Validator: profile fields, 30-day staleness warning | 2 |
| Core docs model-neutral | 2 (check), 4 (edits) |
| Harness classes, capability contract, observed table, unknown harness | 3 |
| Adapters collapse | 5 |
| Resolver, dispatcher, qualification fixture, lock-file writer | **Plan B** (explicitly out of scope) |

**Placeholder scan.** No `TBD`, `TODO`, or "similar to Task N". Task 6 Step 3 describes an audit log's contents because its numbers come from real runs and cannot be pre-written.

**Type and name consistency.** `resolve_mode`, `resolve_threshold`, `load_lock`, `parse_audit`, `gate_passes`, `InvalidInputError` (renamed from `InvalidAuditError`; no other file imports it). `validate_profile`, `extract_profile_json`, `find_model_names`, `check_profiles`, `check_core_docs_model_neutral`, and constants `ROLES`, `LICENCE_POLICIES` match between Task 2's tests and implementation. Roles are `orchestrator`, `auditor_a`, `auditor_b`, `worker` everywhere.

**Known interaction.** Task 2 Step 8 deliberately leaves the validator failing on the model-name check until Task 4 removes the names. Run Tasks 2, 3, and 4 in order without pausing between them.

**Risks.** The scorer now rejects malformed reserved-prefix lines. Real auditor outputs may contain a line such as `FINDING` text wrapped onto a second line starting at column 0; Task 1 Step 5 detects that on the real outputs before any gate relies on it.
