# cortex9-conflibot-pr-branch-shell-injection-model

Modelo offline e inerte de **CVE-2026-55158** (GHSA-2qvg-qr73-mqxp,
CWE-78). Antes de **1.2.1**, wktk/conflibot armaba comandos `git`
interpolando el nombre de rama del pull request (`head.ref`) en una
sola cadena pasada a `child_process.exec` (una shell). En el flujo
documentado `pull_request_target` eso corre en un runner con los
secretos del repositorio base y un token con permiso de escritura.

El fix de v1.2.1, commit `59e255c49c920fd6b67471ab9ef3bf194439a3f2`,
conserva los nombres de rama pero llama a git con arreglos de
argumentos (`execFile` / `spawn`: 59e255c4:L152, 59e255c4:L244-247,
59e255c4:L265). El de v2.0.0, commit
`0107ac6a4575ea200d0b92287ea58f975be9505d`, además referencia los pull
requests por número (`refs/pull/<n>/head`, 0107ac6a:L159-170,
0107ac6a:L175, 0107ac6a:L204-207). Ver
[evidence/fix-in-1.2.1.md](evidence/fix-in-1.2.1.md).

Inglés: [README.md](README.md). Ejercicios: [PRACTICE.md](PRACTICE.md).

## Citas de líneas

Cada cita tiene la forma `<tag>:L<n>` o `<tag>:L<n>-<m>`: la línea real de
`cat -n` de los diffs oficiales del fix, copiados en `sources/` (licencia
upstream: MIT). `sources/diffs.tsv` los identifica; `citations.tsv` guarda
el SHA-256 de cada rango citado. Los diffs se comprueban siempre en CI.

## Uso

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

Un modelo no es un hallazgo. Ver [LIMITATIONS.md](LIMITATIONS.md) y
[SOURCES.md](SOURCES.md). Licencia: Apache-2.0.
