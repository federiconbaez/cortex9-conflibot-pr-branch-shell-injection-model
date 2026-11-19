# Guía práctica (6 niveles)

Ejercicios **offline**. No se ejecuta git ni ninguna shell. Si quieres
ver conflibot real, hazlo en un repositorio de laboratorio tuyo, nunca
contra un runner ajeno.
Respuestas en `tests/test_practice.py`.

Ayuda: `PYTHONPATH=src python3 -c "from c9conflibot import gitcmd; print(gitcmd.analyze('pre','main;id')['outcome'])"`.

**Básico**

1. **Rama sana.** `main` en pre. (`CLEAN`)
2. **Punto y coma.** `main;id` en pre. (`SHELL_METACHAR` — 59e255c4:L151)

**Intermedio**

3. **El fix de v1.** Lo mismo en v1. (`ARGV_SAFE`, `head.ref` sigue en un
   slot de argv, 59e255c4:L152)
4. **v2.** Lo mismo en v2. (`NUMERIC_REF`, checkout `origin/pr/<n>`,
   0107ac6a:L175)

**Avanzado**

5. **Otra PR.** `head.ref` limpio y `target.head.ref` igual a `other;id`
   en pre. ¿Por qué sigue siendo `SHELL_METACHAR`? (59e255c4:L174-176)
6. **Observación o01.** ¿Qué campo interpola el merge, y por qué no es
   el vector que nombra el advisory?

Más allá: agrega un caso a `fixtures/cases.json` y regenera expected.tsv.
