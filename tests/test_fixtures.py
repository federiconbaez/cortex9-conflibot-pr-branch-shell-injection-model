import unittest
from c9conflibot import cases, gitcmd

DATA = cases.load()
EXPECTED = {}
for line in (cases.ROOT / "fixtures/expected.tsv").read_text(
        encoding="utf-8").splitlines()[1:]:
    cid, ver, outcome = line.split("\t")
    EXPECTED[(cid, ver)] = outcome
VERSIONS = gitcmd.VERSIONS


class Fixtures(unittest.TestCase):
    def test_expected_covers_everything(self):
        self.assertEqual(len(EXPECTED), len(DATA) * len(VERSIONS))

    def test_model_derivation_and_hand_labels_agree(self):
        for c in DATA:
            for v in VERSIONS:
                with self.subTest(case=c["id"], version=v):
                    got = cases.run(c, v)["outcome"]
                    self.assertEqual(got, EXPECTED[(c["id"], v)])
                    self.assertEqual(got, c["expected"][v])

    def test_acceptance_pos_flip(self):
        for c in DATA:
            if c["class"] != "pos":
                continue
            pre = cases.run(c, "pre")
            v1 = cases.run(c, "v1")
            v2 = cases.run(c, "v2")
            self.assertEqual(pre["outcome"], "SHELL_METACHAR", c["id"])
            self.assertTrue(pre["shell"], c["id"])
            self.assertEqual(v1["outcome"], "ARGV_SAFE", c["id"])
            self.assertFalse(v1["shell"], c["id"])
            self.assertEqual(v2["outcome"], "NUMERIC_REF", c["id"])
            self.assertFalse(v2["shell"], c["id"])
            self.assertTrue(v1["head_ref_in_git"], c["id"])
            self.assertFalse(v2["head_ref_in_git"], c["id"])

    def test_acceptance_negatives(self):
        for c in DATA:
            if c["class"] != "neg":
                continue
            self.assertEqual(cases.run(c, "pre")["outcome"], "CLEAN", c["id"])
            self.assertEqual(cases.run(c, "v1")["outcome"], "ARGV_SAFE", c["id"])
            self.assertEqual(cases.run(c, "v2")["outcome"], "NUMERIC_REF", c["id"])
            self.assertFalse(cases.run(c, "v2")["head_ref_in_git"], c["id"])


if __name__ == "__main__":
    unittest.main()
