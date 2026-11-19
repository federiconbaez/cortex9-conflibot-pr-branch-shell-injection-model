# Limitations

- **Command construction only.** The model rebuilds the git checkout,
  merge, format-patch and (post) apply-check invocations. It does not
  simulate `pull_request_target`, tokens, secrets, conflict reporting or
  a real git repository. Git and shells are never executed.
- **v1 still passes branch names to git.** After 59e255c4:L152 and
  59e255c4:L181-185 the crafted `head.ref` is one argv slot, so it is no
  longer shell syntax, but it is still a git revision string. That is
  outside the scope of CVE-2026-55158 (CWE-78). v2 is the stricter
  follow-up (0107ac6a:L159-170).
- **o01** (a crafted `base.ref`) is a **model observation**: pre also
  interpolates `base.ref` in the merge and format-patch shell strings
  (59e255c4:L157-158, 59e255c4:L174-176). The advisory's stated vector
  is attacker-controlled `head.ref` under `pull_request_target`. This is
  not a separate finding. v2 still puts `origin/${base.ref}` in the
  merge argv (0107ac6a:L182-190), without a shell.
- **`dummy@conflibot.invalid`** is the upstream placeholder already
  present in the merge command (59e255c4:L157-158, 59e255c4:L159-167).
  It is not a real mailbox.
- The official GitHub `.diff` files fetched on 2026-11-19 use 7-character
  blob abbreviations on `index` lines. An earlier inventory copy of the
  same commits used 8-character abbreviations (SHA-256 `401a7b77…` and
  `338cb5e9…`). The TypeScript hunks and their line numbers are the same;
  this repo keeps the official files as fetched (SHA-256 in
  `sources/SHA256SUMS`).
- This is not a finding and not an exploit. The only command name in
  fixtures is the inert marker `id`.
