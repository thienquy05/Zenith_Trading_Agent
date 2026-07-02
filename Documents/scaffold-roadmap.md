# System Scaffold Roadmap — Feature-Branch Build Plan

**Status:** Approved design, implementation not started. This document is
the build breakdown ("the bone") of `swarm-trading-system-plan.md` §3/§5
Phases 1–2 for the Finance / Investment Banking plugin. Section references
(§) below point at that plan doc.

**How to use this document:** one feature branch per section, built in
order. A feature is *done* only when its verification gate passes and the
result is logged in `memory.md`; only then does the next branch start.
Each branch gets its own PR into `master`.

**Workflow rules (agreed 2026-07-02):**
- One `features/<name>` branch per task, PR per branch — matching the
  existing `features/cicd` / `features/codebase-memory_mcp` pattern.
- Verification gate for every branch: Alembic upgrade→downgrade→upgrade
  round-trip (when schema changes) + pytest against live Postgres + ruff
  + CI green + a real smoke run of the new surface. Sandbox note: Docker
  image pulls are blocked in the Claude session environment, so live-DB
  verification there uses apt-installed Postgres + uvicorn, with CI as
  the second gate; a full `docker compose up` check remains a user-side
  step.
- Docker evolves per feature — no big-bang compose rewrite. Compose
  already has healthchecks, localhost-bound ports, and non-root images;
  each feature adds/adjusts only its own services.

**Architecture rule (structural, not disciplinary):** agents interact
with state *only* through the backend API — never the database directly.
This makes "no component bypasses the hard-rules layer" (§7) a property
of the wiring, not a convention someone can forget.

---

## 0. Baseline — Phase 0 (already built and verified)

For orientation; nothing to do here.

- Tables: `users`, `agents`, `accounts`, `api_credentials`,
  `api_usage_log` (Alembic migrations 0001–0002).
- Backend: FastAPI with `/health` only; argon2 password hashing + Fernet
  credential encryption in `backend/app/security.py`; 19 passing tests.
- Frontend: Next.js placeholder page (port 3000).
- Docker: postgres / redis / one-shot migrate / backend (5000) /
  frontend (3000). CI: ruff, pip-audit, migration round-trip, pytest,
  npm audit + build.

---

## 1. `features/db-trading-core` — trading-domain schema

**Goal:** every table the trading pipeline needs, so later branches only
add code, not schema churn. This is the foundation everything else FKs
into.

### New tables and why they look this way

**`proposals`** — the structured proposal object of §3.1.

| Column | Type / constraint | Why |
|---|---|---|
| `id` | UUID PK | consistent with existing tables |
| `account_id` | FK → accounts, `RESTRICT` | a proposal comes from a *funded account*, which already binds agent + user + capital; no denormalized `agent_id` column, so agent/account facts can never drift apart |
| `action` | enum `buy / sell / hold` | §3.1 |
| `ticker` | varchar, NOT NULL | §3.1 |
| `quantity` | Numeric, > 0 CHECK | Decimal for money-adjacent math, never float |
| `timeframe` | varchar | §3.1 |
| `reasoning` | TEXT **NOT NULL** | the "why" is mandatory (§3.1) — an unexplained proposal is invalid by schema |
| `confidence` | Numeric, CHECK 0–1 | §3.1 |
| `capital_snapshot` | JSONB | agent capital state at submission (§3.1), frozen for audit |
| `status` | enum, lifecycle below | single source of truth for where a proposal is |
| `parent_proposal_id` | self-FK, nullable | revise-and-resubmit (§6 Q4) creates a **new row** pointing at the rejected one — past rows are never mutated (audit integrity) |

Status lifecycle:
`submitted → rejected_hard_rules | pending_manager → approved |
rejected_manager | modification_requested → executing → executed |
failed | cancelled | expired`.

**`decisions`** — the append-only audit ledger required by §7 ("full
audit log of every proposal, reasoning, decision, and override").

- BigInteger PK (high-volume, same pattern as `api_usage_log`).
- `proposal_id` FK; `stage` enum (`hard_rules / manager_llm /
  human_override / execution`); `outcome` enum.
- `details` JSONB — structured rule violations (rule key, limit,
  observed value) or LLM reasoning text, machine-queryable.
- `decided_by_user_id` nullable FK → users (human overrides only).
- `hard_rule_params_id` FK — the *exact* limits in force at decision
  time (see next table).
- `created_at` only, **no `updated_at`** — decisions are never edited,
  same append-only pattern already established for `api_usage_log`.

**`hard_rule_params`** — versioned parameter-set snapshots.

- `params` JSONB (the §6.1 numbers), `created_by` FK users, `reason`
  TEXT, `activated_at`.
- A change = a **new row**; nothing is updated in place. `decisions`
  FKs the exact version used, so the audit trail can always answer
  "what limits were live when this was approved?".
- Satisfies §3.3 "manually adjust hard-rule parameters without
  redeploying code". A seed migration inserts the §6.1 starting
  defaults as version 1.

**`system_controls` + `control_events`** — the kill switch (§3.3).

- `system_controls`: single-row table holding current global halt state
  (fast synchronous read in the order path).
- `control_events`: append-only record of every flip — who, what
  (halt / resume / pause-agent / force-reject), when, why.
- Per-agent pause reuses the existing `accounts.status`
  (`active / paused / killed`) — no duplicate mechanism.

**`orders` + `positions`** — execution records (paper first).

- `orders.proposal_id` FK **NOT NULL** — nothing executes without a
  proposal chain (§7: "nothing executes silently").
- `broker` enum (`paper / alpaca / robinhood`), `broker_order_id`,
  side/qty/fill fields, status enum.
- `idempotency_key` UNIQUE — money-safety enhancement: a retried
  submission can never place a duplicate order.
- `positions`: current holdings per account+ticker (qty, avg cost),
  maintained transactionally with fills — hard rules need fast position
  lookups without replaying the order history.

### Changes to existing tables

- **`users` simplified (decision 2026-07-02):** this is a local
  single-operator project — drop `email`, `full_name`, `role` (and the
  `user_role` enum); add `username` VARCHAR UNIQUE NOT NULL as the login
  identifier. Kept: `password_hash`, `is_active`, `last_login_at`,
  timestamps. Done as a **new migration** (merged migration 0001 stays
  untouched — history is append-only). Related contents fixed in the
  same branch: `app/models/user.py`, tests referencing email/role,
  schema-invariant tests.
- **`api_usage_log.linked_proposal_id`** finally gets its FK →
  `proposals.id` (`SET NULL`) — the deferred Phase 0 item.

### Security item closed in this branch

Separate Postgres roles (the standing pre-Phase-1 finding in
`.Security-Agent/memory.md`): a `migrate` role owns DDL; the runtime
`app` role gets DML only, with **no UPDATE/DELETE grant on `decisions`,
`control_events`, `api_usage_log`** — append-only enforced by the
database itself, not by convention.

**Verify:** Alembic round-trip; model tests vs live Postgres (including
FK delete semantics, as in the existing `test_models.py`); extend
`tests/test_schema.py` invariants (every enum via `db_enum`, every FK
explicit `ondelete`) to the new tables; a test proving the app role
cannot UPDATE a decision row; ruff; CI green.

---

## 2. `features/auth-api` — authentication before any control surface

**Goal:** the login gate exists before any endpoint that can touch money
or risk limits is built — no retrofit on the exact endpoints that guard
capital.

- `POST /auth/login` (username + password) → short-lived JWT.
- **No open registration** — single-operator money system: the operator
  user is seeded by a CLI command (reads env/prompt), not an endpoint.
- **No roles** (matches the simplified `users` table): one auth
  dependency — "logged-in operator" — guards every mutating endpoint
  built afterward.
- Login rate limiting (Redis counter); CORS pinned to the frontend
  origin (closes the deferred CORS review in `memory.md`);
  `users.last_login_at` maintained.

**Verify:** auth flow tests — wrong password, expired token, missing
token, rate-limit trip; ruff; CI.

---

## 3. `features/hard-rules-engine` — the deterministic money gate

**Goal:** §3.2 layer 1 as a pure, exhaustively-tested Python module.
Built **before any agent code exists** — the gate precedes the things it
gates.

- `backend/app/rules/` — **pure functions**: input = proposal +
  portfolio state + params snapshot; output = structured violations
  list. No DB, no network, no LLM inside rule functions (the caller
  fetches state) — maximally testable, trivially auditable.
- One function per §6.1 rule: per-agent position cap, portfolio-wide
  cap, sector exposure, daily/weekly loss circuit breakers, per-position
  stop-loss, trade frequency, blacklist, whitelist.
- The engine returns pass/fail plus **every** violation (not just the
  first) — the audit trail and the agent both learn everything wrong
  with a proposal in one pass.
- Any failure ⇒ auto-reject, no LLM involved (§3.2, §7).

**Verify:** full rule test matrix including boundary values (exactly at
the limit, one cent over); ruff; CI.

---

## 4. `features/proposal-pipeline` — proposal → hard rules → decision

**Goal:** the §5 Phase 1 loop working end to end: submit → gate →
recorded decision, all inside the backend API.

- `POST /proposals` (authenticated) → service runs the hard-rules engine
  **synchronously in one DB transaction, with row locks on the affected
  account rows** — portfolio-wide limits can't be raced by two
  simultaneous proposals.
- Writes the `decisions` row, sets proposal status, publishes a Redis
  pub/sub event (§4 messaging choice).
- Manager soft-judgment (§3.2 layer 2) is **stubbed as an interface**:
  passing hard rules parks the proposal at `pending_manager`; a manual
  operator approve/reject endpoint stands in until the LLM layer lands
  (Phase 2). GET endpoints expose the proposal feed + full decision
  chain.

**Verify:** end-to-end tests submitting proposals that pass/fail each
rule class — assert status, decision rows, and the Redis event; live
smoke via uvicorn + curl.

---

## 5. `features/control-plane-api` — kill switch & overrides

**Goal:** §3.3 as API surface, with the synchronous-check property §7
demands.

- Operator endpoints (login-gated): global halt / resume, pause/resume
  an agent account, force-reject a pending proposal, post a new
  `hard_rule_params` version, read the audit trails.
- `assert_trading_allowed()` helper that the (future) execution path
  must call **synchronously before every order** — the kill switch
  lives *in* the order path, not in a monitor beside it.
- Enhancement: hard rules are **re-checked at execution time**, not just
  at proposal time — the market moves between approval and execution.

**Verify:** tests proving a halted system rejects everything regardless
of proposal status; force-reject wins over a prior manager approval.

---

## 6. `features/frontend-dashboard` — control plane UI

**Goal:** the human-accessible control plane of §3.3, on the §5 stack
(Next.js, port 3000).

- Login page (JWT); overview (agents / accounts / capital); proposal
  feed with the full decision chain; kill-switch control (with a
  confirmation step); hard-rule params editor (creates a new version,
  never edits); audit log viewer.
- Plain React + fetch, minimal dependencies.

**Verify:** `npm run build`; `npm audit` clean; manual smoke against a
running backend.

---

## 7. `features/market-data` — shared data layer

**Goal:** §3.4 — one consistent market view, agents never hit providers
independently.

- Starts as a backend module `app/marketdata/`: provider interface,
  **Alpaca first** (§4: market data + backtesting from Alpaca, not
  Robinhood), Redis cache with TTL, consistent-snapshot API.
- Deliberate deferral: splitting it into its own compose service waits
  until agents run as separate containers — no premature service
  boundary.

**Verify:** cached-vs-fresh fetch tests using recorded fixtures — no
live API key needed in CI.

---

## 8. `features/agents-runtime` — member agents + manager wiring

**Goal:** §5 Phase 1's agents, as thin skeletons that exercise the whole
pipeline.

- `agents/` package: `MemberAgent` base (observe → propose loop); first
  technical-only strategy stub (momentum); Manager agent skeleton wiring
  the hard-rules engine.
- **CrewAI-vs-plain bake-off is decided here** (§11 Q5 stays open until
  this branch).
- Compose gains agent service(s). Agents call the backend API only —
  see the architecture rule at the top of this doc.

**Verify:** an agent submits a real proposal through the full pipeline
against synthetic data, and the decision chain shows up in the dashboard.

---

## 9. `features/backtesting` — Phase 1 exit criterion

**Goal:** §5 Phase 1's proof: the proposal → hard-rule-check →
approval/rejection loop works end to end on historical data **before
anything live** (§7: no live trading until backtesting + paper trading
both look acceptable).

- Harness replaying historical bars through the pipeline with paper
  execution; produces the per-agent metrics §6.2 needs (rolling Sortino
  vs SPY, max drawdown).

**Verify:** a full backtest run completes with a coherent audit trail —
every executed paper order traces back to an approved proposal and a
recorded decision chain.

---

## Out of scope for the scaffold (later phases)

- Manager LLM soft-judgment implementation (§3.2 layer 2) — Phase 2,
  slots into the interface stubbed in branch 4.
- Alpaca paper-trading connection — Phase 2.
- Sentiment/news agent (§5 Phase 3), Robinhood live execution
  (§5 Phases 4–5), and the org-level Orchestrator (§8) — all explicitly
  after the bone above is verified.
