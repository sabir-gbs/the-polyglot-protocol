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
