# Security-Agent Memory Log

Running log of Security-Agent's reviews, findings, and reasoning. Same
convention as the root [`memory.md`](../memory.md), scoped to this
agent's work.

Convention (read before adding an entry):
- Newest entry at the top (reverse-chronological).
- One entry per *meaningful* event: a security review performed (pass or
  fail), a finding raised, a constraint or check added to `CLAUDE.md` /
  `SKILLS.md`, or a blocking finding escalated to the user.
- Not for routine/no-decision edits (typo fixes, formatting-only diffs).
- Entries are append-only — do not edit past entries except to fix
  factual errors, and mark the fix inline rather than silently rewriting
  history.
- Entry header format: `## YYYY-MM-DD — <short title>`

Entry template:

```
## YYYY-MM-DD — <short title>

**What was reviewed:**
- ...

**Findings:**
- ...

**Why (severity / reasoning):**
- ...

**Open questions / what's next:**
- ...
```

---

## 2026-07-01 — Security-Agent created

> **Correction (same day):** The "Why" below originally said Security-Agent
> was "a new Member Agent under the Engineering plugin." That's wrong —
> Security-Agent is an engineering co-worker agent that helps build this
> project, not an entity inside the org's own multi-agent architecture
> (see root `memory.md`, 2026-07-01 correction entry). Left as-is per the
> append-only convention; corrected charter now lives in `CLAUDE.md`.

**What was reviewed:**
- N/A — this is the agent's creation entry, not a code review.

**Findings:**
- N/A.

**Why (severity / reasoning):**
- Security-Agent added as a new Member Agent under the Engineering
  plugin (`swarm-trading-system-plan.md` §9.2), alongside Test-Agent.
  Charter: review code for exploitable flaws, and specifically enforce
  that credentials/sensitive data are always encrypted at rest with
  strong database-level validation and access restriction. See this
  folder's `CLAUDE.md` and `SKILLS.md` for the full charter and
  operational checklist.

**Open questions / what's next:**
- No scanning tooling or CI hook exists yet — this folder currently
  documents the agent's intended role only (repo is still planning-only
  per root `CLAUDE.md`).
- First real review will happen once there's actual code to review.

---

## 2026-07-01 — Critical finding: Next.js 15.1.3 had a known critical CVE, fixed

**What was reviewed:**
- `frontend/package.json` dependency versions, surfaced via `npm audit`
  while verifying the frontend actually builds (see Test-Agent's CI
  work, same session).

**Findings:**
- **[Fixed, was blocking] `next@15.1.3` — critical severity advisory**
  (CVE-2025-66478 / GHSA-3h52-269p-cp9r, "Information exposure in Next.js
  dev server due to lack of origin verification"), plus ~20 other
  advisories affecting the `9.3.4-canary.0 - 16.3.0-canary.5` version
  range that 15.1.3 falls inside (cache poisoning, SSRF via middleware
  redirects, RCE in the React flight protocol, auth bypass in
  middleware, among others). A known-critical-CVE dependency landing in
  a "first CI/CD pipeline" commit would defeat the purpose of having
  Security-Agent review this commit at all — treated as blocking, not
  advisory, and fixed immediately rather than just logged.
  - Fix: bumped to `next@16.2.10` (current `latest` dist-tag).
  - That alone left a moderate finding: Next.js's own bundled `postcss`
    dependency (`postcss@8.4.31`, pulled in transitively by `next`
    itself, not something in our direct control) is below the patched
    `8.5.10` floor for GHSA-qx2v-qp2m-jg93 (XSS via unescaped
    `</style>` in CSS stringify output). `npm audit fix --force`'s
    suggested "fix" was downgrading `next` to `9.3.3` — reintroducing
    the critical finding above to silence a moderate one, which is
    worse, not better. Instead added an `"overrides": { "postcss":
    "^8.5.10" }` entry to `package.json`, forcing the patched version
    without touching Next's own version. Reinstalled and confirmed
    `npm audit` reports 0 vulnerabilities, and `npm run build` /
    `npm run dev` still both work (verified: production build succeeds,
    dev server serves the placeholder page correctly at
    `localhost:3000`).

**Why (severity / reasoning):**
- Critical, actively-fixable supply-chain-adjacent finding caught before
  it ever shipped — exactly the class of issue SKILLS.md §1 calls out
  ("insecure defaults... credentials in code or config committed to the
  repo" extends naturally to "known-vulnerable dependency committed to
  the repo"). No reason to defer a zero-tradeoff fix (newer Next.js,
  same API surface for a two-file placeholder app) to "later."
- The `overrides` approach was chosen over accepting the moderate
  finding or downgrading Next.js because it's the only option that
  closes the gap without reopening a worse one, and it was verified
  (not just applied) — build and dev-server both re-tested after the
  change.

**Open questions / what's next:**
- `postcss` is pinned via `overrides` to a version Next.js didn't
  officially ship with. Low risk (postcss 8.x has been API-stable across
  patch/minor versions, and Next's own build succeeded against it in
  this session), but worth dropping the override the next time `next` is
  upgraded and its own bundled `postcss` has caught up past `8.5.10`.
- No dependency-scanning step exists in CI yet (`npm audit` /
  `pip-audit` are not wired into `.github/workflows/ci.yml`) — this
  finding was only caught because a human-equivalent review pass
  happened to run `npm audit` manually. Worth adding as an explicit CI
  step so this class of finding doesn't depend on someone remembering to
  check.

---

## 2026-07-01 — First real code review: Phase 0 Postgres schema, FastAPI backend, Docker Compose

**What was reviewed:**
- `backend/app/models/*.py` (users, agents, accounts, api_credentials,
  api_usage_log SQLAlchemy models), `backend/app/security.py` (password
  hashing, credential encryption), `backend/app/config.py`,
  `backend/alembic/versions/0001_initial_schema.py`, `docker-compose.yml`,
  `backend/Dockerfile`, `frontend/Dockerfile`, `.env`/`.env.example`/
  `.gitignore`. This is the first real-code review this folder has done —
  everything before this was charter-writing against no code.

**Findings:**
1. **[Fixed] Weak typing on money/count columns.** `Account.allocated_capital`,
   `Account.current_balance`, and `ApiUsageLog.cost_usd` were declared
   `Mapped[Numeric]` (the SQLAlchemy column-type class, not a Python
   type) instead of `Mapped[Decimal]`. Not exploitable by itself, but
   wrong static typing on financial fields is exactly the kind of
   silent-footgun class of bug that later turns into a real one (e.g. an
   IDE/type-checker failing to catch a float assigned where a Decimal was
   assumed). Fixed in `account.py` and `api_usage_log.py`.
2. **[Fixed] No DB-level bounds checking on capital/token/cost columns.**
   Per SKILLS.md §5 ("writes to sensitive tables are themselves
   validated... bounds-checked... before persistence, not just filtered
   on read"): `allocated_capital`, `current_balance`, `tokens_in`,
   `tokens_out`, and `cost_usd` had no constraint preventing negative
   values, even though none of them have a legitimate negative-value case
   in this system (no margin/short-capital concept exists). Added
   `CHECK (... >= 0)` constraints at the DB level (not just app-level) in
   both the models and the Alembic migration, so a negative value can't
   land even via a raw SQL path that bypasses the ORM.
3. **[Fixed] Docker Compose published all ports on all interfaces.**
   `postgres` (5432), `redis` (6379), `backend` (5000), and `frontend`
   (3000) were all published as `"<port>:<port>"`, which binds
   `0.0.0.0` — reachable from the LAN, not just localhost, on any machine
   without a restrictive firewall. Nothing in this phase is meant to be
   reachable outside the dev machine. Rebound all four to
   `127.0.0.1:<port>:<port>`.
4. **[Fixed] Containers ran as root.** Neither `backend/Dockerfile` nor
   `frontend/Dockerfile` dropped to a non-root user before `CMD`. Added
   a non-root `appuser` (backend) and used the base image's built-in
   `node` user (frontend), with `chown` before `USER`. Defense-in-depth:
   limits blast radius if either process is ever compromised or a
   dependency is malicious.
5. **[Advisory, not fixed — logged as open] No DB-role separation.**
   SKILLS.md §5 asks for least-privilege database access: "no application
   code path that queries sensitive tables with broader permissions than
   it needs." Right now a single Postgres role (`POSTGRES_USER` from
   `.env`) both owns the schema (used by the `migrate` service for DDL)
   and runs all application queries (used by the `backend` service) — no
   separate low-privilege runtime role exists. Not fixed in this pass:
   doing it properly needs either a password-templated
   `docker-entrypoint-initdb.d` script or an out-of-band role-provisioning
   step, and there's no live sensitive data yet (schema only, zero rows,
   no auth endpoints reading/writing it). Judged non-blocking for Phase 0
   but real — should be closed before any account holds actual capital or
   any credential row is written for real.
6. **[Reviewed, no finding] Credential/password handling.**
   `users.password_hash` uses argon2 (one-way, correct for passwords).
   `api_credentials.encrypted_value` uses app-level Fernet encryption
   (reversible, correct — the app needs the plaintext back to call
   broker/LLM APIs, so hashing would be wrong here). Key comes from
   `CREDENTIAL_ENCRYPTION_KEY` env var, not hardcoded; `security.py`
   raises loudly if it's unset rather than silently no-op'ing.
   `.env` (with the real local key) is gitignored and confirmed absent
   from `git status`; `.env.example` (committed) has no real secret.
7. **[Reviewed, no finding — not applicable yet] JWT/session auth, rate
   limiting, CSRF, audit-log tamper-evidence, input-validation/injection
   review.** No auth endpoints, no audit-log table, and no user-facing
   API routes beyond `GET /health` exist yet in this phase — these
   constraints (`CLAUDE.md`) stay open until that code exists, consistent
   with every prior entry in this log.
8. **[Reviewed, no finding] CORS.** No CORS middleware is configured on
   the FastAPI app, which defaults to browsers blocking cross-origin
   requests — a safe default. Will need an explicit, non-wildcard
   allow-list once the frontend actually calls the backend cross-origin
   (`localhost:3000` -> `localhost:5000`); flagged for whoever wires that
   up next, not blocking now since no such call exists yet.

**Why (severity / reasoning):**
- Findings 1–4 were cheap, unambiguous fixes with no functional
  downside (correct typing, DB constraints matching business reality,
  localhost-only binding for a single-machine dev setup, non-root
  containers) — fixed directly rather than just reported, consistent
  with "reviews and recommends" not requiring a separate sign-off round
  for changes with no tradeoff.
- Finding 5 (role separation) was left open rather than half-implemented
  with a fragile password-templating hack in an initdb script, which
  itself risks introducing a bug into the exact area (DB credential
  handling) it's meant to protect. Deferred with a concrete trigger
  condition (before real capital/credentials exist) rather than a vague
  "later."

**Open questions / what's next:**
- Close finding 5 (DB role separation: dedicated least-privilege runtime
  role, distinct from the migration-owning role) before Phase 1 writes
  any real credential or capital row.
- Re-review once auth endpoints, the audit-log table, and the
  hard-rules/kill-switch code exist — items 7 becomes live at that point.
- Re-review CORS config the moment the frontend makes its first real
  cross-origin call to the backend.

---

## 2026-07-01 — Constraint added: JWT/session auth, no route backdoors

**What was reviewed:**
- N/A — this is a charter update, not a code review (no auth code exists
  yet).

**Findings:**
- N/A.

**Why (severity / reasoning):**
- User specified the platform will authorize users via JWT plus a
  server-side session token, and that protected routes/pages (example
  given: `ai_trading/dashboard`) must never be reachable just by
  requesting the URL directly — no backdoor access via unlinked or
  hidden routes. Added as a non-negotiable constraint in `CLAUDE.md`
  (new bullet under "Non-negotiable constraints") and as a new
  operational section in `SKILLS.md` (§3, "Authentication &
  authorization (JWT / session tokens)"), covering JWT signature/expiry
  validation, revocable session tokens, server-side default-deny
  authorization per route, and treating any debug/override bypass as a
  critical finding regardless of environment.

**Open questions / what's next:**
- No auth implementation exists yet to review against this constraint —
  applies once the platform's login/session/routing code is written.

---

## 2026-07-01 — Constraints added: rate limiting, CSRF, tamper-evident audit log

**What was reviewed:**
- N/A — charter update following up on the JWT/session constraint above,
  not a code review (no code exists yet).

**Findings:**
- N/A.

**Why (severity / reasoning):**
- Follow-up recommendation after adding the JWT/session-auth constraint:
  closing the two classic follow-on gaps (brute-forceable auth endpoints,
  CSRF on cookie-based sessions) and tying the existing audit-log
  requirement (root `CLAUDE.md`) to tamper-evidence, not just presence.
  User approved adding all three. Added to `CLAUDE.md` (three new
  "Non-negotiable constraints" bullets) and `SKILLS.md` (rate
  limiting/CSRF folded into §3 auth section; new §4 "Audit log
  integrity"; sections renumbered accordingly, §4–5 -> §5–6, old §6 ->
  §7).
- CSRF is conditioned on session tokens actually living in cookies —
  not applicable to pure header-based bearer tokens. Left as a
  check-before-flagging note in `SKILLS.md` rather than an unconditional
  rule, since the platform's actual token transport isn't decided yet.

**Open questions / what's next:**
- Confirm, once auth is designed, whether session tokens use cookies or
  headers — determines whether the CSRF constraint is live or moot.
- No implementation exists yet to review against any of these three
  constraints.

---

## 2026-07-02 — Review pass: argon2 migration hardening, ORM delete semantics, credential cleanup

**What was reviewed:**
- `backend/app/security.py` (the passlib → argon2-cffi migration from
  commit `39f7bc0`) and the ORM relationship / FK delete semantics in
  `backend/app/models/`, prompted by the first real Postgres run of the
  DB-backed test suite this session.

**Findings:**
- **Fixed:** ORM relationships ignored the DB's declared `ON DELETE`
  behavior — `session.delete(user)` crashed with `NotNullViolation`
  instead of cascading. Beyond the crash, the security-relevant risk was
  drift between ORM-level and DB-level delete semantics for
  `api_credentials`: a deleted user must reliably take their encrypted
  credential rows with them. Fixed with
  `cascade="all, delete-orphan", passive_deletes=True` on the CASCADE
  relationships, `passive_deletes="all"` where the DB is RESTRICT
  (deleting a funded agent must be rejected by the DB, not silently
  reshaped by the ORM), and a regression test proving credential rows
  are gone after user deletion.
- **Verified, now test-enforced:** `verify_password` fails closed
  (returns `False`, no exception) on empty/malformed/truncated hashes,
  and still verifies a frozen passlib-era `$argon2id$` hash
  (m=102400,t=2,p=8) — the back-compat claim in the code comment is now
  pinned by a test instead of asserted in prose.
- **New guard:** `tests/test_schema.py` asserts every FK declares an
  explicit `ondelete` (no silent Postgres NO ACTION defaults in a
  schema holding capital and credentials) and every enum column
  persists values, not names.

**Why (severity / reasoning):**
- The cascade bug was High (user deletion impossible at runtime; and if
  the NOT NULL had ever been relaxed, the same ORM behavior would have
  *orphaned* credential rows instead of deleting them). The rest is
  hardening: converting previously implicit security properties
  (fail-closed verify, credential cleanup, explicit delete semantics)
  into executable checks.

**Open questions / what's next:**
- DB-role separation (migrations vs runtime) still open — unchanged,
  still pre-Phase-1.
- JWT/session/CSRF/rate-limit constraints remain not-yet-applicable (no
  auth routes exist yet).
