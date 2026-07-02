# SKILLS.md — Security-Agent

Operational detail behind the charter in [`CLAUDE.md`](CLAUDE.md): what
Security-Agent actually looks for and how it works. Planning-only for
now — no scanner/tool is wired up yet, so this is the spec that a future
implementation (or a manual review pass) should follow.

## 1. Code-level flaw review

- Review new/changed code for common exploitable classes: injection
  (SQL, command, template), broken auth/authorization, insecure
  deserialization, path traversal, SSRF, unsafe use of `eval`/dynamic
  code execution, and OWASP Top-10-style issues generally.
- Flag missing input validation at trust boundaries (anywhere external
  input — user, market data feed, connector response — enters the
  system), consistent with this project's principle that hard-coded
  rules gate machine judgment, not the reverse.
- Flag insecure defaults: permissive CORS, disabled TLS verification,
  overly broad file/network permissions, credentials in code or config
  committed to the repo.
- Review connector integrations (Robinhood, Github, Excalidraw,
  Goodnotes, AgentMail — root `CLAUDE.md` quick reference) for
  least-privilege API scopes and safe handling of returned data.

## 2. Credential and sensitive-data handling

- Any credential, API key, token, or secret must never be stored or
  logged in plaintext — encrypted at rest, minimum. Prefer a dedicated
  secrets manager over encrypted DB columns where the architecture
  allows it; if secrets do live in the database, they must be encrypted
  there, not just access-controlled.
- Trace where secrets flow: config → memory → logs → error messages.
  Flag any of those paths that could leak a secret (e.g., an exception
  handler that dumps a full request object containing an API key).
- If/when the trading system's manual override / kill switch and audit
  log (root `CLAUDE.md`) exist in code, confirm they cannot be disabled
  or bypassed via a credential/config change alone — that would defeat
  the non-negotiable constraint silently.

## 3. Authentication & authorization (JWT / session tokens)

- **JWT validation, on every protected request, not just at login:**
  correct signature/algorithm (reject `alg: none` and algorithm
  confusion), expiry (`exp`) and not-before (`nbf`) enforced, issuer/
  audience checked where applicable. An expired or tampered token must
  fail closed.
- **Session tokens must be real and revocable** — bound to a server-side
  session (or short-lived with refresh-token rotation), so a logout,
  password change, or detected compromise actually invalidates access.
  A JWT alone with no revocation path is a finding.
- **Authorization is enforced server-side, per route/resource, by
  default-deny.** Never trust a client-side route guard, hidden nav
  item, or obscured link as the only gate — flag any route or API
  endpoint reachable by directly requesting its URL/path (e.g. typing
  `ai_trading/dashboard` in the address bar) without a valid, authorized
  session. "Not linked in the UI" is not "not accessible."
- **No backdoors.** Debug flags, admin override headers/params, internal
  test routes, or "temporary" bypasses that skip JWT/session checks are
  critical findings regardless of environment (including
  staging/local) — they tend to leak into production.
- Confirm failed auth/authz responses (401/403) fail closed and don't
  leak information that aids route/resource enumeration.
- **Rate limiting / brute-force protection**: login, password-reset, and
  token-refresh endpoints need throttling, lockout, or backoff — a
  correct auth check with no rate limit is still crackable by brute
  force.
- **CSRF, if sessions ever live in cookies**: state-changing requests
  need a CSRF token, `SameSite` cookie attribute, or equivalent. Not
  applicable to pure header-based bearer tokens (e.g.
  `Authorization: Bearer ...`) with no cookie — confirm which transport
  is actually in use before flagging or clearing this.

## 4. Audit log integrity

- Per root `CLAUDE.md`'s non-negotiable "full audit log of every
  proposal, reasoning, decision, and override": verify the log storage
  itself is append-only / write-once (e.g., DB-level `INSERT`-only
  permissions, an append-only log store, or hash-chained entries) — not
  just that logging calls exist in the code.
- Flag any code path (including admin tooling) that can update or delete
  existing audit-log rows. An editable audit log is equivalent to no
  audit log for incident reconstruction purposes.

## 5. Database validation and restriction

- Schema review: sensitive columns (credentials, PII, financial
  identifiers) must have encryption at the column or application layer,
  NOT NULL / type constraints appropriate to the data, and no default
  values that weaken security (e.g., a default admin flag).
- Access review: confirm role-based / least-privilege access to
  sensitive tables — no shared superuser credentials, no application code
  path that queries sensitive tables with broader permissions than it
  needs.
- Validate that writes to sensitive tables are themselves validated
  (type-checked, bounds-checked, sanitized) before persistence, not just
  filtered on read.
- Treat "untouchable" as the working bar: a sensitive record should
  survive a compromised application-layer credential (defense in depth),
  not rely solely on network perimeter security.

## 6. How findings are reported

- Each review produces: what was checked, what was found (if anything),
  severity (blocking vs. advisory), and a suggested fix or mitigation.
- Blocking findings (plaintext secrets, missing DB validation on
  sensitive tables, a path around the hard-rules/kill-switch gate) stop a
  merge — raise them to the user directly, don't self-approve past them.
- Every review that finds something — or confirms a clean pass on a
  security-sensitive change — gets an entry in this folder's `memory.md`,
  per the append-only convention in `CLAUDE.md`.

## 7. Working relationship with Test-Agent

- Security-relevant changes should get both a Security-Agent review and
  Test-Agent coverage (e.g., a test that actually attempts the injection
  Security-Agent flagged, to prove the fix holds). Don't treat these as
  redundant — a passing test suite is not a substitute for a security
  review, and a security review is not a substitute for regression tests.
