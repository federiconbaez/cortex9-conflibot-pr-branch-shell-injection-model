import ast
import unittest
from unittest import mock
import subprocess

from c9conflibot import cases, gitcmd

ROOT = cases.ROOT


class Adversarial(unittest.TestCase):
    def test_src_never_calls_popen_or_system(self):
        for f in sorted((ROOT / "src/c9conflibot").glob("*.py")):
            tree = ast.parse(f.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    fn = node.func
                    name = fn.attr if isinstance(fn, ast.Attribute) else getattr(
                        fn, "id", "")
                    self.assertNotIn(name, {"Popen", "run", "call", "system",
                                            "check_output", "getoutput",
                                            "execFile", "spawn", "exec"})

    def test_running_cases_never_touches_subprocess(self):
        boom = mock.Mock(side_effect=AssertionError("subprocess used"))
        with mock.patch.object(subprocess, "Popen", boom), \
                mock.patch.object(subprocess, "run", boom):
            for c in cases.load():
                for v in gitcmd.VERSIONS:
                    cases.run(c, v)
        boom.assert_not_called()

    def test_v1_keeps_crafted_ref_in_one_argv_slot(self):
        r = gitcmd.analyze("v1", "main;id")
        self.assertEqual(r["outcome"], "ARGV_SAFE")
        checkout = next(i for i in r["invocations"] if i["kind"] == "checkout")
        self.assertEqual(checkout["argv"], ["git", "checkout", "main;id"])

    def test_v2_uses_numeric_ref_not_branch(self):
        r = gitcmd.analyze("v2", "main;id", pull_number=42, target_number=99)
        self.assertEqual(r["outcome"], "NUMERIC_REF")
        checkout = next(i for i in r["invocations"] if i["kind"] == "checkout")
        self.assertEqual(
            checkout["argv"],
            ["git", "checkout", "--detach", "origin/pr/42"],
        )
        fmt = next(i for i in r["invocations"] if i["kind"] == "format-patch")
        self.assertIn("origin/main..origin/pr/99", fmt["argv"])
        self.assertFalse(any("main;id" in a for a in fmt["argv"]))

    def test_pre_format_patch_is_one_shell_pipe(self):
        r = gitcmd.analyze("pre", "topic", "main", "other;id")
        fmt = next(i for i in r["invocations"] if i["kind"] == "format-patch")
        self.assertEqual(fmt["mode"], "shell")
        self.assertIn("| git apply --check", fmt["command"])
        self.assertIn("origin/other;id", fmt["command"])

    def test_unknown_version(self):
        with self.assertRaises(ValueError):
            gitcmd.analyze("v9", "main")

    def test_deterministic(self):
        a = [cases.run(c, "pre")["outcome"] for c in cases.load()]
        b = [cases.run(c, "pre")["outcome"] for c in cases.load()]
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
