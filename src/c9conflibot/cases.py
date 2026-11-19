"""Fixture loading shared by tests and scripts/gen_results.py."""
from __future__ import annotations

import json
from pathlib import Path

from . import gitcmd

ROOT = Path(__file__).resolve().parents[2]


def load() -> list:
    data = (ROOT / "fixtures/cases.json").read_text(encoding="utf-8")
    return json.loads(data)["cases"]


def run(case: dict, version: str) -> dict:
    return gitcmd.analyze(
        version,
        case["head_ref"],
        case.get("base_ref", "main"),
        case.get("target_head_ref", case["head_ref"]),
        int(case.get("pull_number", 1)),
        int(case.get("target_number", 2)),
    )
