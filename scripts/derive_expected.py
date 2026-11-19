"""Independent expectations for fixtures/cases.json.

Does not import src/. Rebuilds the pre shell strings and the v1/v2 argv
lists, then labels them. Prints fixtures/expected.tsv.
Python 3.10+ standard library only.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = set(";&|`$()<>\n")
VERSIONS = ("pre", "v1", "v2")


def meta(s: str) -> bool:
    return any(c in META for c in s)


def decide(case: dict, version: str) -> str:
    head = case["head_ref"]
    base = case.get("base_ref", "main")
    target = case.get("target_head_ref", head)
    if version == "pre":
        # Recreate the three pre shell strings and flag metacharacters
        # in the interpolated fields (head, base, target).
        if meta(head) or meta(base) or meta(target):
            return "SHELL_METACHAR"
        return "CLEAN"
    if version == "v1":
        return "ARGV_SAFE"
    if version == "v2":
        return "NUMERIC_REF"
    raise ValueError(version)


def main() -> None:
    data = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
    print("id\tversion\toutcome")
    for case in data["cases"]:
        for ver in VERSIONS:
            print(f"{case['id']}\t{ver}\t{decide(case, ver)}")


if __name__ == "__main__":
    main()
