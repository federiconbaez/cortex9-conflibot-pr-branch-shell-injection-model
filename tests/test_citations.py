"""Every line citation in this repo is checked against the saved diff.

Citation form everywhere: ``<tag>:L<n>`` or ``<tag>:L<n>-<m>``, where
``<tag>`` is the 8-hex prefix of the fix commit. ``sources/diffs.tsv`` maps
each tag to the saved official diff copied into ``sources/`` and its SHA-256;
``citations.tsv`` is the single table of cited ranges with the SHA-256 of
each range.

Normalisation of a range's hash: take lines ``start``..``end`` of the diff
file exactly as stored (no ``cat -n`` number prefix, no stripping, any
trailing whitespace kept), join them with ``\n``, no final newline, and hash
the UTF-8 bytes.

The in-repo copies are always checked. Optional: ``C9_DIFF`` (one path, or
several joined with os.pathsep) must be byte-identical to an in-repo copy.
"""
import csv
import hashlib
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAGGED = re.compile(r"\b([0-9a-f]{8}):L(\d+)(?:-(\d+))?\b")
BARE = re.compile(r"\bL\d+\b")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SKIP_DIRS = {".git", "sources", "__pycache__", "node_modules"}
SKIP_FILES = {"LICENSE", "test_citations.py", "test_citations.js"}
TEXT_EXT = {".py", ".js", ".md", ".json", ".csv", ".tsv", ".yml", ".toml",
            ".txt", ""}


def _read_tsv(path: Path) -> list:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


DIFFS = {r["tag"]: r for r in _read_tsv(ROOT / "sources/diffs.tsv")}
ROWS = _read_tsv(ROOT / "citations.tsv")
TABLE = {(r["tag"], int(r["start"]), int(r["end"])) for r in ROWS}


def range_sha256(lines: list, start: int, end: int) -> str:
    return hashlib.sha256(
        "\n".join(lines[start - 1:end]).encode("utf-8")).hexdigest()


def _lines(tag: str) -> list:
    return (ROOT / "sources" / DIFFS[tag]["file"]).read_text(
        encoding="utf-8").splitlines()


def _tracked_text_files():
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in
                                  p.relative_to(ROOT).parts):
            continue
        if p.name in SKIP_FILES or p.suffix not in TEXT_EXT:
            continue
        yield p


class CitationTable(unittest.TestCase):
    def test_tables_are_well_formed(self):
        self.assertTrue(DIFFS)
        for tag, r in DIFFS.items():
            self.assertRegex(tag, r"^[0-9a-f]{8}$")
            self.assertRegex(r["sha256"], HEX64)
            self.assertRegex(
                r["url"],
                rf"^https://github\.com/.+/commit/{tag}[0-9a-f]{{32}}\.diff$",
            )
            self.assertTrue((ROOT / "sources" / r["file"]).is_file())
        self.assertTrue(ROWS)
        self.assertEqual(len(TABLE), len(ROWS), "duplicate range")
        for r in ROWS:
            self.assertIn(r["tag"], DIFFS)
            self.assertTrue(1 <= int(r["start"]) <= int(r["end"]))
            self.assertRegex(r["sha256"], HEX64)
            self.assertTrue(r["what"].strip())

    def test_saved_diffs_match_their_sha256(self):
        for tag, r in DIFFS.items():
            data = (ROOT / "sources" / r["file"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), r["sha256"], tag)

    def test_every_cited_range_matches_the_saved_diff(self):
        for r in ROWS:
            tag, a, b = r["tag"], int(r["start"]), int(r["end"])
            with self.subTest(cite=f"{tag}:L{a}-{b}"):
                lines = _lines(tag)
                self.assertTrue(1 <= a <= b <= len(lines),
                                f"range past end ({len(lines)} lines)")
                self.assertEqual(range_sha256(lines, a, b), r["sha256"])

    def test_every_citation_in_the_repo_is_in_the_table(self):
        seen = 0
        for p in _tracked_text_files():
            text = p.read_text(encoding="utf-8")
            for m in TAGGED.finditer(text):
                tag, a = m.group(1), int(m.group(2))
                b = int(m.group(3) or a)
                seen += 1
                with self.subTest(file=str(p.relative_to(ROOT)), cite=m.group(0)):
                    self.assertIn((tag, a, b), TABLE)
            for m in BARE.finditer(TAGGED.sub("", text)):
                self.fail(f"{p.relative_to(ROOT)}: untagged citation {m.group(0)}")
        self.assertGreater(seen, 0)


class ExternalDiff(unittest.TestCase):
    def test_c9_diff_matches_the_in_repo_copy(self):
        raw = os.environ.get("C9_DIFF", "")
        paths = [p for p in raw.split(os.pathsep) if p]
        if not paths or not all(Path(p).is_file() for p in paths):
            self.skipTest(
                "external check SKIPPED: C9_DIFF is "
                + (f"'{raw}', not existing file(s)" if raw else "not set")
                + "; the in-repo copies in sources/ are still fully checked")
        for p in paths:
            sha = hashlib.sha256(Path(p).read_bytes()).hexdigest()
            tags = [t for t, r in DIFFS.items() if r["sha256"] == sha]
            self.assertEqual(len(tags), 1, f"{p}: sha256 {sha} matches no diff")
            copy = ROOT / "sources" / DIFFS[tags[0]]["file"]
            self.assertEqual(Path(p).read_bytes(), copy.read_bytes())


if __name__ == "__main__":
    unittest.main()
