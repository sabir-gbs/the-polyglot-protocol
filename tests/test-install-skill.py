from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("install_skill", ROOT / "scripts" / "install-skill.py")
assert SPEC is not None and SPEC.loader is not None
INSTALL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = INSTALL
SPEC.loader.exec_module(INSTALL)

NAME = "the-polyglot-protocol"
KEPT_WORKFLOW = ["artifact-group-audit-workflow.md", "dev-workflow.md", "role-resolution.md"]


class InstallSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name).resolve()

    def use_source(self, source: Path) -> None:
        # Point the installer at a small fake repo so a bug cannot touch the real one.
        original = INSTALL.ROOT
        INSTALL.ROOT = source
        self.addCleanup(setattr, INSTALL, "ROOT", original)

    def fake_source(self, base: Path) -> Path:
        source = base / NAME
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text(f"name: {NAME}\n", encoding="utf-8")
        return source

    def test_default_targets_use_the_paths_agents_load(self) -> None:
        targets = {agent: path.as_posix() for agent, path in INSTALL.DEFAULT_TARGETS.items()}
        self.assertTrue(targets["opencode"].endswith(f".config/opencode/skills/{NAME}"))
        self.assertTrue(targets["codex"].endswith(f".agents/skills/{NAME}"))

    def test_copy_skips_tests_run_logs_and_env_files(self) -> None:
        target = self.tmp / "skills" / NAME
        INSTALL.copy_project(target, force=False)
        self.assertFalse((target / "tests").exists())
        self.assertFalse((target / ".superpowers").exists())
        workflow = sorted(path.name for path in (target / "docs" / "workflow").iterdir())
        self.assertEqual(workflow, KEPT_WORKFLOW)

        source = self.fake_source(self.tmp / "fake")
        (source / ".env.test").write_text("secret", encoding="utf-8")
        (source / "docs").mkdir()
        (source / "docs" / ".env").write_text("secret", encoding="utf-8")
        self.use_source(source)
        fake_target = self.tmp / "out" / NAME
        INSTALL.copy_project(fake_target, force=False)
        names = {path.name for path in fake_target.rglob("*")}
        self.assertFalse({name for name in names if name.startswith(".env")})
        self.assertIn("SKILL.md", names)

    def test_force_refuses_a_directory_with_no_skill_file(self) -> None:
        self.use_source(self.fake_source(self.tmp / "src"))
        target = self.tmp / "skills" / NAME
        target.mkdir(parents=True)
        (target / "precious.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(SystemExit):
            INSTALL.copy_project(target, force=True)
        self.assertTrue((target / "precious.txt").exists())

    def test_force_refuses_wrong_name_the_source_and_its_parent(self) -> None:
        outer = self.fake_source(self.tmp / "outer")
        source = self.fake_source(outer)
        self.use_source(source)
        wrong_name = self.tmp / "skills" / "other"
        wrong_name.mkdir(parents=True)
        (wrong_name / "SKILL.md").write_text("x", encoding="utf-8")
        (wrong_name / "keep.txt").write_text("keep", encoding="utf-8")
        for target in (wrong_name, source, outer):
            with self.subTest(target=str(target)):
                with self.assertRaises(SystemExit):
                    INSTALL.copy_project(target, force=True)
        self.assertTrue((wrong_name / "keep.txt").exists())
        self.assertTrue((source / "SKILL.md").exists())
        self.assertTrue((outer / "SKILL.md").exists())

    def test_installed_copy_validates_itself(self) -> None:
        target = self.tmp / "skills" / NAME
        INSTALL.copy_project(target, force=False)
        # A copy that holds this test file would run it again and loop forever.
        self.assertFalse((target / "tests").exists())
        result = subprocess.run(
            [sys.executable, "-B", "scripts/validate-workspace.py"],
            cwd=target, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("workspace validation: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
