"""Offline model of conflibot git command construction, CVE-2026-55158.

Pre (wktk/conflibot < 1.2.1) interpolates pull-request branch names into
a single string and runs it through `child_process.exec` (a shell):
checkout of `head.ref` (59e255c4:L151, 0107ac6a:L173) and the
format-patch / apply pipe that interpolates `target.head.ref`
(59e255c4:L174-176, 0107ac6a:L197-199).

v1 (1.2.1, commit 59e255c49c920fd6b67471ab9ef3bf194439a3f2) keeps the
branch names but passes them as `execFile` / `spawn` argument arrays
(59e255c4:L152, 59e255c4:L181-185, 59e255c4:L244-247, 59e255c4:L265).

v2 (2.0.0, commit 0107ac6a4575ea200d0b92287ea58f975be9505d) also
references pull requests by number (`refs/pull/<n>/head`,
0107ac6a:L159-170, 0107ac6a:L175, 0107ac6a:L204-207), so attacker-
controlled branch names never reach git.

Nothing here runs git or a shell. The only command name used in
fixtures as an inert marker is `id`.
"""
from __future__ import annotations

# Shell metacharacters named by GHSA-2qvg-qr73-mqxp, plus newline.
META = set(";&|`$()<>\n")

PRE_RULE = "59e255c4:L151;59e255c4:L174-176;59e255c4:L237"
V1_RULE = "59e255c4:L152;59e255c4:L181-185;59e255c4:L244-247"
V2_RULE = "0107ac6a:L159-170;0107ac6a:L175;0107ac6a:L204-207"
VERSIONS = ("pre", "v1", "v2")


def _merge_shell(base_ref: str) -> str:
    # 59e255c4:L157-158 / 0107ac6a:L180-181
    return (
        "git -c user.name=conflibot -c user.email=dummy@conflibot.invalid "
        f"merge origin/{base_ref} --no-edit"
    )


def _merge_argv(base_ref: str) -> list[str]:
    # 59e255c4:L159-167 / 0107ac6a:L182-190
    return [
        "git",
        "-c",
        "user.name=conflibot",
        "-c",
        "user.email=dummy@conflibot.invalid",
        "merge",
        f"origin/{base_ref}",
        "--no-edit",
    ]


def has_meta(value: str) -> bool:
    return any(c in META for c in value)


def invocations(
    version: str,
    head_ref: str,
    base_ref: str,
    target_head_ref: str,
    pull_number: int,
    target_number: int,
) -> list[dict]:
    """Build the modelled git invocations. Never executed."""
    if version == "pre":
        return [
            {
                "kind": "checkout",
                "mode": "shell",
                "command": f"git checkout {head_ref}",  # 59e255c4:L151
                "argv": None,
                "tainted": {"head_ref": head_ref},
            },
            {
                "kind": "merge",
                "mode": "shell",
                "command": _merge_shell(base_ref),
                "argv": None,
                "tainted": {"base_ref": base_ref},
            },
            {
                "kind": "format-patch",
                "mode": "shell",
                "command": (
                    f"git format-patch origin/{base_ref}.."
                    f"origin/{target_head_ref} --stdout | git apply --check"
                ),  # 59e255c4:L174-176
                "argv": None,
                "tainted": {
                    "base_ref": base_ref,
                    "target_head_ref": target_head_ref,
                },
            },
        ]
    if version == "v1":
        return [
            {
                "kind": "checkout",
                "mode": "argv",
                "command": None,
                "argv": ["git", "checkout", head_ref],  # 59e255c4:L152
                "tainted": {"head_ref": head_ref},
            },
            {
                "kind": "merge",
                "mode": "argv",
                "command": None,
                "argv": _merge_argv(base_ref),
                "tainted": {"base_ref": base_ref},
            },
            {
                "kind": "format-patch",
                "mode": "argv",
                "command": None,
                "argv": [
                    "git",
                    "format-patch",
                    f"origin/{base_ref}..origin/{target_head_ref}",
                    "--stdout",
                ],  # 59e255c4:L181-185
                "tainted": {
                    "base_ref": base_ref,
                    "target_head_ref": target_head_ref,
                },
            },
            {
                "kind": "apply-check",
                "mode": "argv",
                "command": None,
                "argv": ["git", "apply", "--check"],  # 59e255c4:L265
                "tainted": {},
            },
        ]
    if version == "v2":
        numbers = sorted({int(pull_number), int(target_number)})
        refspecs = [
            f"+refs/pull/{n}/head:refs/remotes/origin/pr/{n}" for n in numbers
        ]
        return [
            {
                "kind": "fetch-pr",
                "mode": "argv",
                "command": None,
                "argv": ["git", "fetch", "origin", *refspecs],  # 0107ac6a:L159-170
                "tainted": {},
            },
            {
                "kind": "checkout",
                "mode": "argv",
                "command": None,
                "argv": [
                    "git",
                    "checkout",
                    "--detach",
                    f"origin/pr/{int(pull_number)}",
                ],  # 0107ac6a:L175
                "tainted": {},
            },
            {
                "kind": "merge",
                "mode": "argv",
                "command": None,
                "argv": _merge_argv(base_ref),
                "tainted": {"base_ref": base_ref},
            },
            {
                "kind": "format-patch",
                "mode": "argv",
                "command": None,
                "argv": [
                    "git",
                    "format-patch",
                    f"origin/{base_ref}..origin/pr/{int(target_number)}",
                    "--stdout",
                ],  # 0107ac6a:L204-207
                "tainted": {"base_ref": base_ref},
            },
            {
                "kind": "apply-check",
                "mode": "argv",
                "command": None,
                "argv": ["git", "apply", "--check"],  # 0107ac6a:L286
                "tainted": {},
            },
        ]
    raise ValueError(version)


def _head_fields(tainted: dict) -> dict:
    return {k: v for k, v in tainted.items() if k in ("head_ref", "target_head_ref")}


def detect(inv: dict) -> str:
    """Label one invocation.

    SHELL_METACHAR: a shell string interpolates a tainted value that
    contains a metacharacter (the CVE).
    CLEAN: a shell string, but no metacharacter in the interpolated values.
    ARGV_SAFE: argv form; a head-branch value may still appear as one slot.
    NUMERIC_REF: argv form and no head-branch value appears in argv.
    """
    tainted = inv["tainted"]
    if inv["mode"] == "shell":
        if any(has_meta(v) for v in tainted.values()):
            return "SHELL_METACHAR"
        return "CLEAN"
    argv = inv["argv"] or []
    heads = _head_fields(tainted)
    blob = "\0".join(argv)
    if any(v and v in blob for v in heads.values()):
        return "ARGV_SAFE"
    return "NUMERIC_REF"


def analyze(
    version: str,
    head_ref: str,
    base_ref: str = "main",
    target_head_ref: str | None = None,
    pull_number: int = 1,
    target_number: int = 2,
) -> dict:
    if target_head_ref is None:
        target_head_ref = head_ref
    invs = invocations(
        version, head_ref, base_ref, target_head_ref, pull_number, target_number,
    )
    labels = [detect(i) for i in invs]
    if "SHELL_METACHAR" in labels:
        outcome = "SHELL_METACHAR"
    elif version == "v2":
        # Head-branch names never reach git; merge may still carry base_ref.
        outcome = "NUMERIC_REF"
    elif version == "v1":
        outcome = "ARGV_SAFE"
    elif version == "pre":
        outcome = "CLEAN"
    else:
        raise ValueError(version)
    rule = {"pre": PRE_RULE, "v1": V1_RULE, "v2": V2_RULE}[version]
    return {
        "outcome": outcome,
        "shell": version == "pre",
        "invocations": invs,
        "labels": labels,
        "rule": rule,
        "head_ref_in_git": any(
            (head_ref and head_ref in (i["command"] or ""))
            or (head_ref and head_ref in (i["argv"] or []))
            or (target_head_ref and target_head_ref in (i["command"] or ""))
            or any(
                target_head_ref and target_head_ref in a
                for a in (i["argv"] or [])
            )
            for i in invs
        ),
    }
