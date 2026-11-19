# Sources

Line citations: see "Line citations" below. Official diffs are copied
under `sources/` (MIT; see `sources/README.md`).

| Source | URL | Used for | SHA-256 |
|---|---|---|---|
| Commit 59e255c49c920fd6b67471ab9ef3bf194439a3f2 (v1.2.1) as `CVE-2026-55158_conflibot_59e255c49c92.diff` | https://github.com/wktk/conflibot/commit/59e255c49c920fd6b67471ab9ef3bf194439a3f2 | pre 59e255c4:L151, 59e255c4:L174-176, 59e255c4:L237; v1 59e255c4:L152, 59e255c4:L181-185, 59e255c4:L244-247, 59e255c4:L265 | 40b385aed9e08bb59cf588fbe5b46f24bf75f3ae0da30a6bff536f74363c0088 |
| Commit 0107ac6a4575ea200d0b92287ea58f975be9505d (v2.0.0) as `CVE-2026-55158_conflibot_0107ac6a4575.diff` | https://github.com/wktk/conflibot/commit/0107ac6a4575ea200d0b92287ea58f975be9505d | v2 0107ac6a:L159-170, 0107ac6a:L175, 0107ac6a:L204-207 | 7a6bf0d819212c9c8405a9bb001a6132aa880a2bf6b62169572d5ae36d296599 |
| GHSA-2qvg-qr73-mqxp | https://github.com/advisories/GHSA-2qvg-qr73-mqxp | affected <1.2.1, patched 1.2.1 (and 2.0.0 in the body), CWE-78 | fetched 2026-11-19 via `https://api.github.com/advisories/GHSA-2qvg-qr73-mqxp` |
| Vendor advisory | https://github.com/wktk/conflibot/security/advisories/GHSA-2qvg-qr73-mqxp | same | same advisory family |
| cve.org (PUBLISHED) | https://www.cve.org/CVERecord?id=CVE-2026-55158 | PUBLISHED; CWE-78; <1.2.1; both fix commits | fetched 2026-11-19 via `https://cveawg.mitre.org/api/cve/CVE-2026-55158` |
| NVD (Deferred) | https://nvd.nist.gov/vuln/detail/CVE-2026-55158 | CVE exists; Deferred; CWE-78; same references | fetched 2026-11-19 via `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-55158` |

No instruction directed at this agent was found in those pages or in the
diffs; text about "exfiltration" and command injection is ordinary
advisory language and was treated as data.

## Line citations

Every line citation has the form `<tag>:L<n>` or `<tag>:L<n>-<m>`: the real
`cat -n` line(s) of the official fix diffs copied into `sources/`.
`sources/diffs.tsv` names them. `citations.tsv` is the single table of
cited ranges and stores the SHA-256 of each range (lines `start`..`end`
of the diff exactly as stored, joined with `\n`, no final newline, UTF-8).

```sh
PYTHONPATH=src python3 -m unittest -v tests.test_citations
# optional: confirm a freshly downloaded official copy is byte-identical
C9_DIFF=/tmp/59e255c.diff:/tmp/0107ac6.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

An earlier inventory copy of the same commits (SHA-256 `401a7b77fd878c4641e490f999cf5ebc179a545659b55e6bbe3e777db925fee9` and
`338cb5e945c418f575af8772a0a0863db8ce521931560d0d7670323f3631848b`)
differs only in 8- vs 7-character blob abbreviations on `index` lines.
