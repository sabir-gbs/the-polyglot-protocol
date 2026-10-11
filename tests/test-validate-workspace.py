from __future__ import annotations

import importlib.util
import sys
import tempfile
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
        "fallback": {role: {"harness": "h1", "model": f"model-{role}"} for role in VW.ROLES},
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

    def test_missing_fallback_role_is_an_error(self) -> None:
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

    # --- structure: wrong types are errors, never exceptions --------------
    def assert_error_mentioning(self, data: object, fragment: str) -> None:
        errors, _ = VW.validate_profile(data, TODAY)
        self.assertTrue(any(fragment in e for e in errors), (fragment, errors))

    def test_non_object_containers_are_errors(self) -> None:
        for key in ("harnesses", "constraints", "pins", "fallback"):
            for bad in ([], "text", 5, None):
                with self.subTest(key=key, bad=bad):
                    data = good_profile()
                    data[key] = bad
                    self.assert_error_mentioning(data, key)

    def test_sources_must_be_a_list_of_strings(self) -> None:
        for bad in ("https://example.org", {}, [1], ["ok", None]):
            with self.subTest(bad=bad):
                data = good_profile()
                data["sources"] = bad
                self.assert_error_mentioning(data, "sources")

    def test_allowed_providers_must_be_a_list(self) -> None:
        for bad in ("opencode", {}, 5, None):
            with self.subTest(bad=bad):
                data = good_profile()
                data["constraints"]["allowed_providers"] = bad  # type: ignore[index]
                self.assert_error_mentioning(data, "allowed_providers")

    def test_fallback_harness_and_model_must_be_non_empty_strings(self) -> None:
        for field in ("harness", "model"):
            for bad in ("", "  ", 5, None, [], {}):
                with self.subTest(field=field, bad=bad):
                    data = good_profile()
                    data["fallback"]["worker"][field] = bad  # type: ignore[index]
                    self.assert_error_mentioning(data, f"fallback.worker {field}")

    def test_fallback_entry_that_is_not_an_object_is_an_error(self) -> None:
        data = good_profile()
        data["fallback"]["worker"] = "claude"  # type: ignore[index]
        self.assert_error_mentioning(data, "fallback.worker")

    def test_harness_entry_must_be_an_object_with_a_string_command(self) -> None:
        for bad in ([], "tool", None, {"roles": ["worker"]}, {"command": 5, "roles": []}, {"command": "", "roles": []}):
            with self.subTest(bad=bad):
                data = good_profile()
                data["harnesses"]["h1"] = bad  # type: ignore[index]
                self.assert_error_mentioning(data, "harnesses.h1")

    def test_harness_roles_must_be_a_list_of_known_roles(self) -> None:
        for bad in ("worker", {}, 5, ["janitor"], ["worker", 3], None):
            with self.subTest(bad=bad):
                data = good_profile()
                data["harnesses"]["h1"]["roles"] = bad  # type: ignore[index]
                self.assert_error_mentioning(data, "harnesses.h1 roles")

    def test_list_valued_harness_does_not_raise(self) -> None:
        data = good_profile()
        data["harnesses"] = ["h1"]
        data["fallback"]["worker"]["harness"] = ["h1"]  # type: ignore[index]
        errors, warnings = VW.validate_profile(data, TODAY)
        self.assertTrue(errors)
        self.assertIsInstance(warnings, list)

    def test_unhashable_fallback_harness_does_not_raise(self) -> None:
        data = good_profile()
        data["fallback"]["worker"]["harness"] = {"a": 1}  # type: ignore[index]
        errors, _ = VW.validate_profile(data, TODAY)
        self.assertTrue(errors)

    def test_same_model_for_both_auditors_is_an_error(self) -> None:
        data = good_profile()
        data["fallback"]["auditor_a"]["model"] = "same"  # type: ignore[index]
        data["fallback"]["auditor_b"]["model"] = "same"  # type: ignore[index]
        self.assert_error_mentioning(data, "same model")

    def test_different_models_for_both_auditors_are_accepted(self) -> None:
        data = good_profile()
        data["fallback"]["auditor_a"]["model"] = "one"  # type: ignore[index]
        data["fallback"]["auditor_b"]["model"] = "two"  # type: ignore[index]
        self.assertEqual(VW.validate_profile(data, TODAY), ([], []))

    def test_shipped_profiles_have_no_errors(self) -> None:
        paths = sorted((ROOT / "profiles").glob("*.md"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(profile=path.name):
                data = VW.extract_profile_json(path.read_text(encoding="utf-8"))
                errors, _ = VW.validate_profile(data, date.today())
                self.assertEqual(errors, [])


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


class CheckFilesHiddenDirectoryTest(unittest.TestCase):
    def test_hidden_directories_are_skipped(self) -> None:
        original_root = VW.ROOT
        self.addCleanup(setattr, VW, "ROOT", original_root)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".hidden").mkdir()
            (root / ".hidden" / "Bad_File1.md").write_text("# x\n", encoding="utf-8")
            (root / "visible").mkdir()
            (root / "visible" / "Bad_File2.md").write_text("# x\n", encoding="utf-8")
            VW.ROOT = root
            errors = VW.check_files()
        rules = ("uppercase", "numbered filename", "kebab-case")
        filename_errors = [e for e in errors if any(rule in e for rule in rules)]
        self.assertFalse(any(".hidden/Bad_File1.md" in e for e in filename_errors))
        self.assertTrue(any("visible/Bad_File2.md" in e for e in filename_errors))


if __name__ == "__main__":
    unittest.main()
