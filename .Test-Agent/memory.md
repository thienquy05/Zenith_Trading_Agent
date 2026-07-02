# Test-Agent Memory Log

Running log of Test-Agent's reviews, test cases written, and reasoning.
Same convention as the root [`memory.md`](../memory.md), scoped to this
agent's work.

Convention (read before adding an entry):
- Newest entry at the top (reverse-chronological).
- One entry per *meaningful* event: a test-coverage review performed
  (pass or fail), a coverage gap raised, a constraint or check added to
  `CLAUDE.md` / `SKILLS.md`, or a blocking finding escalated to the user.
- Not for routine/no-decision edits (typo fixes, formatting-only diffs).
- Entries are append-only — do not edit past entries except to fix
  factual errors, and mark the fix inline rather than silently rewriting
  history.
- Entry header format: `## YYYY-MM-DD — <short title>`

Entry template:

```
## YYYY-MM-DD — <short title>

**What changed (function/module under test):**
- ...

**Test cases added/updated:**
- ...

**Result (pass/fail, coverage gaps):**
- ...

**Open questions / what's next:**
- ...
```

---

## 2026-07-01 — Test-Agent created

> **Correction (same day):** The "Why" below originally said Test-Agent
> was "a new Member Agent under the Engineering plugin." That's wrong —
> Test-Agent is an engineering co-worker agent that helps build this
> project, not an entity inside the org's own multi-agent architecture
> (see root `memory.md`, 2026-07-01 correction entry). Left as-is per the
> append-only convention; corrected charter now lives in `CLAUDE.md`.

**What changed (function/module under test):**
- N/A — this is the agent's creation entry, not a test review.

**Test cases added/updated:**
- N/A.

**Result (pass/fail, coverage gaps):**
- N/A.

**Why:**
- Test-Agent added as a new Member Agent under the Engineering plugin
  (`swarm-trading-system-plan.md` §9.2), alongside Security-Agent.
  Charter: write test cases for CI/CD whenever a new function or change
  needs verification before merge to `master`. See this folder's
  `CLAUDE.md` and `SKILLS.md` for the full charter and operational
  checklist.

**Open questions / what's next:**
- No CI pipeline exists yet — this folder currently documents the
  agent's intended role only (repo is still planning-only per root
  `CLAUDE.md`).
- First real test review will happen once there are actual
  functions/modules to cover.

---

## 2026-07-01 — First real test suite: backend/tests/, ruff lint, first CI pipeline

**What changed (function/module under test):**
- Everything added in this session's earlier Phase 0 pass: `app/security.py`
  (password hashing, credential encryption), `app/main.py` (`/health`),
  and the five SQLAlchemy models (`users`, `agents`, `accounts`,
  `api_credentials`, `api_usage_log`) plus their constraints.

**Test cases added/updated:**
- `backend/tests/test_security.py` (no DB required):
  - `hash_password`/`verify_password` roundtrip, correct password
    accepted, wrong password rejected.
  - `encrypt_secret`/`decrypt_secret` roundtrip; ciphertext doesn't
    contain the plaintext; tampered ciphertext raises on decrypt;
    `encrypt_secret` raises `RuntimeError` when
    `CREDENTIAL_ENCRYPTION_KEY` is unset — closes the exact "secret
    silently stored in plaintext" failure mode Security-Agent's charter
    calls out as a blocking-severity class of bug.
- `backend/tests/test_main.py` (no DB required): `GET /health` returns
  200 with the expected JSON shape.
- `backend/tests/test_models.py` (needs a live Postgres —
  `backend/tests/conftest.py`'s `engine`/`db_session` fixtures):
  user defaults (role, is_active) and email-uniqueness constraint;
  account defaults (status, current_balance) and the new
  non-negative-capital CHECK constraint from a negative-value insert;
  `ON DELETE CASCADE` (deleting a user removes their accounts) and
  `ON DELETE RESTRICT` (deleting an agent with open accounts fails);
  `api_credentials.encrypted_value` never contains the plaintext secret;
  `api_usage_log`'s non-negative-token CHECK constraint.
- Added `backend/requirements-dev.txt` (pytest, httpx, ruff),
  `backend/pytest.ini`, `backend/ruff.toml`.
- Ran `ruff check` over `app/`, `tests/`, `alembic/` as part of setting up
  the lint step for CI — found and fixed 10 findings, all pre-existing in
  the code from the earlier Phase 0 pass: SQLAlchemy 2.0 `Mapped["X"]`
  forward-reference relationship annotations were flagged `F821`
  undefined-name across all five model files, because the referenced
  classes were never imported anywhere ruff's static analysis could see
  (they resolve at runtime via SQLAlchemy's mapper registry). Fixed by
  adding `if TYPE_CHECKING: from app.models.x import X` guarded imports
  in each file — the standard fix, satisfies both ruff and any future
  type-checker without a runtime circular-import. Also removed one
  genuinely unused `import uuid` in `user.py`. Re-ran `ruff check`: clean.
- Added a first CI pipeline: `.github/workflows/ci.yml` — see that file
  for the concrete jobs; short version: backend job runs ruff, runs
  `alembic upgrade head` + `alembic downgrade base` + `alembic upgrade
  head` again against a Postgres service container (proves the migration
  round-trips cleanly, not just that it applies once), then `pytest`
  (all three test files, including `test_models.py` which only gets a
  real DB to run against in CI); frontend job runs `npm run build`.

**Result (pass/fail, coverage gaps):**
- `test_security.py` and `test_main.py`: ran locally, 6/6 passed (no DB
  needed for either).
- `test_models.py`: **written but not run locally** — Docker Desktop's
  daemon wasn't running in this session, so there was no live Postgres to
  point it at. Reasoned through the logic carefully (transaction/rollback
  fixture semantics, CASCADE/RESTRICT ON DELETE behavior, CHECK
  constraint violations raising `IntegrityError`) but this is not a
  substitute for actually running it. It will get its first real run the
  first time `.github/workflows/ci.yml` executes (Postgres service
  container) or the next time someone runs `pytest` locally with Docker
  up. Flagging explicitly rather than claiming coverage that hasn't been
  proven — don't want a false "tests pass" signal in this log.
- `ruff check app tests alembic`: passing, verified locally.
- While verifying the frontend actually builds (`npm install` /
  `npm run build`), found `npm audit` reported a critical Next.js CVE
  (`next@15.1.3`) plus a moderate transitive `postcss` finding — see
  Security-Agent's memory.md for the full writeup; fixed by bumping to
  `next@16.2.10` + a `postcss` version override, re-verified `npm audit`
  clean and both `npm run build` and `npm run dev` still work.
- Running `pip-audit -r requirements.txt` as part of wiring up the CI
  dependency-audit step found 11 known vulnerabilities across 2 packages
  in the originally-pinned versions: `cryptography==44.0.0` (the package
  backing `security.py`'s Fernet credential encryption — a
  security-sensitive dependency finding this deserved to be caught) and
  a stale transitive `starlette==0.41.3` pulled in by the original
  `fastapi==0.115.6` pin. Fixed by bumping every pin in
  `backend/requirements.txt` to current stable releases (`fastapi
  0.139.0`, `uvicorn 0.49.0`, `sqlalchemy 2.0.51`, `alembic 1.18.5`,
  `psycopg[binary] 3.3.4`, `pydantic-settings 2.14.2`, `cryptography
  48.0.1`; `starlette` isn't pinned directly and now resolves to a
  current version transitively via the newer `fastapi`). Re-verified in
  a clean venv: `pip-audit` reports zero vulnerabilities, models still
  import, `alembic upgrade head --sql` still generates correct SQL,
  `ruff check` still clean, and all 6 no-DB tests still pass.
- Added `pip-audit` (backend) to `requirements-dev.txt` and both
  `pip-audit -r requirements.txt` and `npm audit --audit-level=moderate`
  as explicit CI steps in `.github/workflows/ci.yml`, so this class of
  finding is caught automatically on every PR going forward instead of
  depending on someone remembering to run it by hand.
- Coverage gaps (not closed in this pass, consistent with what
  Security-Agent's own review flagged as not-yet-applicable): no auth
  endpoints exist yet, so no JWT/session test suite; no audit-log table
  yet, so no tamper-evidence tests; no trading/broker code yet, so no
  paper-trading-only test constraint to enforce yet.

**Open questions / what's next:**
- Run `test_models.py` for real (via CI or local Docker) and fix
  anything that doesn't hold up under an actual Postgres — the reasoning
  above is not verification.
- Add the auth test suite (expired/tampered JWT rejected, revoked
  session loses access, direct-URL route access denied) the moment
  auth/session code lands — this is a blocking constraint per
  `CLAUDE.md`, not optional.
- CI workflow triggers on push/PR to `master` only — the earlier
  branch-target ambiguity this session (local `master` vs.
  `origin/HEAD` pointing at `docs/initial_documents`) was resolved
  externally to `master` during this session; workflow reflects that.
- `starlette`'s `TestClient` now emits a `StarletteDeprecationWarning`
  recommending an `httpx2` package instead of `httpx` for test clients —
  no such stable package exists to pin yet as of this session; tests
  still pass today, just noting the deprecation so it isn't a surprise
  later when `httpx` support is actually dropped.

---

## 2026-07-01 — Constraints added: auth test suite, paper-trading-only tests

**What changed (function/module under test):**
- N/A — charter update, not a test review (no code exists yet).

**Test cases added/updated:**
- N/A.

**Result (pass/fail, coverage gaps):**
- N/A.

**Why:**
- Follow-up to Security-Agent's new JWT/session-auth constraint
  (`Security-Agent/CLAUDE.md`): added a matching non-negotiable
  constraint requiring an explicit auth test suite (expired/tampered JWT
  rejected, revoked session loses access, direct-URL route access denied
  without a valid session) for any auth-touching change, so the
  constraint is test-enforced, not just review-enforced.
- Also added a paper-trading-only rule for any test touching real order
  placement/broker connectors/trade execution, making root `CLAUDE.md`'s
  "no live trading until backtesting + paper trading both show
  acceptable behavior" constraint concrete at the test-authoring level.
  User approved both. Added to `CLAUDE.md` (two new "Non-negotiable
  constraints" bullets) and `SKILLS.md` §3 (two new bullets in
  "Coordination on cross-cutting concerns").

**Open questions / what's next:**
- No auth code or trading/broker code exists yet to write these tests
  against — applies once that code exists.

---

## 2026-07-02 — First live-Postgres run of test_models.py; 5 tests added, 1 real bug caught

**What changed (function/module under test):**
- `backend/app/security.py` (argon2-cffi migration) and
  `backend/app/models/` relationship delete semantics.

**Test cases added/updated:**
- `test_security.py`: `test_verify_password_returns_false_on_malformed_hash`
  (empty / garbage / truncated hash all fail closed),
  `test_verify_password_accepts_passlib_era_hash` (frozen
  `$argon2id$` hash with passlib 1.7.4 cost parameters).
- `test_models.py`: `test_deleting_user_cascades_to_their_api_credentials`
  (credential rows gone after user delete); existing cascade test now
  expires the session identity map after flush — with `passive_deletes`
  the DB removes rows behind the ORM's back, so `Session.get` must
  re-query instead of trusting the cache.
- New `test_schema.py` (standalone, no DB): all enum columns persist
  values not names (guards the `db_enum` regression class), all FKs
  declare explicit `ondelete`.

**Result (pass/fail, coverage gaps):**
- The standing open item "run test_models.py against a real Postgres"
  is closed: apt-installed Postgres 16 in the session sandbox (Docker
  pulls blocked by network policy). First run immediately failed —
  `test_deleting_user_cascades_to_their_accounts` surfaced a real bug
  (ORM nulled child FKs on user delete instead of letting the DB
  CASCADE). After the model fix: 19/19 passing, Alembic
  upgrade→downgrade→upgrade round-trip clean, ruff clean.
- Coverage gap: CI hasn't run these yet at time of writing; the
  frontend suite is still build-only (no component tests).

**Open questions / what's next:**
- Auth test suite constraint still pending actual auth code.
- Consider a constraint test for `accounts` UniqueConstraint
  (user_id, agent_id, account_name) next time models are touched.
