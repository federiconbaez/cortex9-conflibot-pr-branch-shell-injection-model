# Are the fixes in conflibot 1.2.1 and 2.0.0?

Answer: **yes**, according to the primary sources checked on 2026-11-19
(America/Buenos_Aires).

| Source | Result |
|---|---|
| [GHSA-2qvg-qr73-mqxp](https://github.com/advisories/GHSA-2qvg-qr73-mqxp) (and the vendor advisory) | affected `< 1.2.1`, patched `1.2.1`; body also names `2.0.0`. CWE-78 |
| [cve.org CVE-2026-55158](https://www.cve.org/CVERecord?id=CVE-2026-55158) | PUBLISHED; CWE-78; conflibot `< 1.2.1`; references both fix commits and both release tags |
| [NVD CVE-2026-55158](https://nvd.nist.gov/vuln/detail/CVE-2026-55158) | Deferred; same description and references; CWE-78 |
| Commit `59e255c49c920fd6b67471ab9ef3bf194439a3f2` | named as the v1.2.1 fix; package.json in the diff bumps `1.2.0` → `1.2.1` |
| Commit `0107ac6a4575ea200d0b92287ea58f975be9505d` | named as the v2.0.0 fix |
| Releases | https://github.com/wktk/conflibot/releases/tag/v1.2.1 and https://github.com/wktk/conflibot/releases/tag/v2.0.0 |

No git compare API was called for this note.
