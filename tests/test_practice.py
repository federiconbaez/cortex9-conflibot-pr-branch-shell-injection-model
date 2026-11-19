"""Answers to PRACTICE.md."""
import unittest
from pathlib import Path
from c9conflibot import gitcmd


class Practice(unittest.TestCase):
    def test_level_1_plain(self):
        self.assertEqual(gitcmd.analyze("pre", "main")["outcome"], "CLEAN")

    def test_level_2_semicolon(self):
        self.assertEqual(
            gitcmd.analyze("pre", "main;id")["outcome"], "SHELL_METACHAR")

    def test_level_3_v1_argv(self):
        r = gitcmd.analyze("v1", "main;id")
        self.assertEqual(r["outcome"], "ARGV_SAFE")
        self.assertFalse(r["shell"])
        self.assertTrue(r["head_ref_in_git"])

    def test_level_4_v2_numeric(self):
        r = gitcmd.analyze("v2", "main;id", pull_number=7, target_number=8)
        self.assertEqual(r["outcome"], "NUMERIC_REF")
        self.assertFalse(r["head_ref_in_git"])

    def test_level_5_target_ref(self):
        r = gitcmd.analyze("pre", "clean-head", "main", "other;id")
        self.assertEqual(r["outcome"], "SHELL_METACHAR")

    def test_level_6_observation(self):
        text = Path("LIMITATIONS.md").read_text(encoding="utf-8")
        self.assertIn("o01", text)


if __name__ == "__main__":
    unittest.main()
