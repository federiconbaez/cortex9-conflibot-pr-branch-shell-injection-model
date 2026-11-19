# cortex9-conflibot-pr-branch-shell-injection-model

Offline, inert model of **CVE-2026-55158** (GHSA-2qvg-qr73-mqxp, CWE-78).
wktk/conflibot before **1.2.1** built `git` commands by interpolating
attacker-controlled pull-request branch names (`head.ref`) into a single
string passed to `child_process.exec` (a shell). Under the documented
`pull_request_target` workflow this runs on a runner that holds the base
repository secrets and a write-scoped token.

The v1.2.1 fix, commit `59e255c49c920fd6b67471ab9ef3bf194439a3f2`, keeps
the branch names but runs git with `execFile` / `spawn` argument arrays
(59e255c4:L152, 59e255c4:L244-247, 59e255c4:L265). The v2.0.0 fix,
commit `0107ac6a4575ea200d0b92287ea58f975be9505d`, also references pull
requests by number through `refs/pull/<n>/head` (0107ac6a:L159-170,
0107ac6a:L175, 0107ac6a:L204-207). See
[evidence/fix-in-1.2.1.md](evidence/fix-in-1.2.1.md).

Spanish: [README.es.md](README.es.md). Exercises: [PRACTICE.md](PRACTICE.md).

## The model

- `src/c9conflibot/gitcmd.py` rebuilds the checkout, merge, format-patch
  and (post) apply-check invocations for `pre`, `v1` and `v2`. **git and
  shells are never executed**.
- Outcomes: `SHELL_METACHAR` (pre: a tainted branch name with a shell
  metacharacter is interpolated into a shell string), `CLEAN` (pre, no
  metacharacter), `ARGV_SAFE` (v1: argv, branch name may still appear as
  one slot), `NUMERIC_REF` (v2: branch names never reach git).

## Differential evidence (`results/summary.csv`)

| Class | n | pre | v1 | v2 |
|---|---|---|---|---|
| pos | 6 | 6 `SHELL_METACHAR` | 6 `ARGV_SAFE` | 6 `NUMERIC_REF` |
| neg | 2 | 2 `CLEAN` | 2 `ARGV_SAFE` | 2 `NUMERIC_REF` |
| observation | 1 | 1 `SHELL_METACHAR` (`o01`, crafted `base.ref`) | 1 `ARGV_SAFE` | 1 `NUMERIC_REF` |

`o01` is a **model observation**, not a separate finding. See
[LIMITATIONS.md](LIMITATIONS.md).

## Line citations

Every line citation has the form `<tag>:L<n>` or `<tag>:L<n>-<m>`: the real
`cat -n` line(s) of the official fix diffs copied into `sources/`
(upstream license: MIT). `sources/diffs.tsv` names them:

- `59e255c4` → `CVE-2026-55158_conflibot_59e255c49c92.diff`, SHA-256 `40b385aed9e08bb59cf588fbe5b46f24bf75f3ae0da30a6bff536f74363c0088`,
  https://github.com/wktk/conflibot/commit/59e255c49c920fd6b67471ab9ef3bf194439a3f2.diff
- `0107ac6a` → `CVE-2026-55158_conflibot_0107ac6a4575.diff`, SHA-256 `7a6bf0d819212c9c8405a9bb001a6132aa880a2bf6b62169572d5ae36d296599`,
  https://github.com/wktk/conflibot/commit/0107ac6a4575ea200d0b92287ea58f975be9505d.diff

`citations.tsv` is the single table of cited ranges; for each range it
stores the SHA-256 of the cited text (lines `start`..`end` of the diff
exactly as stored, joined with `\n`, no final newline, UTF-8).

```sh
PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

## Run

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

A model is not a finding. See [LIMITATIONS.md](LIMITATIONS.md) and
[SOURCES.md](SOURCES.md). License: Apache-2.0. The copied diffs remain
under the upstream MIT license (`sources/UPSTREAM-LICENSE`).
