# Project Memory Log

Running log of the reasoning/process behind meaningful changes to this
project. Purpose: preserve context across sessions so future work (by
Claude or the user) does not have to re-derive *why* something is the way
it is. This is a plain repo file, not the Claude Code global memory
system.

Convention (read before adding an entry):
- Newest entry at the top (reverse-chronological).
- One entry per *meaningful* change: a planning doc is added/changed, a
  phase/milestone completes, an architectural decision is made, a
  plugin/connector is added, or the diagram is reconciled with the docs
  (or found to diverge from them).
- Not for routine/no-decision edits (typo fixes, formatting-only diffs).
- Entries are append-only — do not edit past entries except to fix
  factual errors, and mark the fix inline rather than silently rewriting
  history.
- Entry header format: `## YYYY-MM-DD — <short title>`

Entry template:

```
## YYYY-MM-DD — <short title>

**What changed:**
- ...

**Why:**
- ...

**Open questions / what's next:**
- ...
```

---

## 2026-07-02 — Diagram: schema cluster expanded to column-level detail

**What changed:**
- Rebuilt the "Postgres schema (general picture)" cluster in
  `Documents/system.excalidraw` (user request, same branch/PR as the
  schema itself): each of the 12 table boxes now lists its columns with
  types and markers (`PK`, `UQ`, `-> table (ondelete)` for FKs, `?` for
  nullable), monospace, laid out on a 3×4 grid with regenerated FK
  arrows (child → parent) and the revise-and-resubmit self-loop on
  `proposals`. Legend now explains the notation and the DB-enforced
  append-only ledgers. Script-verified: valid JSON, unique ids, no
  dangling `boundElements`/binding refs, no line overflowing its box.

**Why:**
- The name-only boxes stopped earning their keep once the real columns
  existed in migrations 0003/0004 — the diagram is the plan doc's visual
  counterpart and should answer "what's in this table?" at a glance.

**Open questions / what's next:**
- None — regenerate via script (kept in session scratchpad, trivially
  rewritable) if columns change in later branches.

## 2026-07-02 — Branch 1 `features/db-trading-core` built and verified: trading-domain schema + DB-role separation

**What changed:**
- Migrations 0003 + 0004 and matching ORM models — the full trading-core
  schema from roadmap §1: `proposals` (structured §3.1 object; reasoning
  TEXT NOT NULL; revise-and-resubmit via `parent_proposal_id` self-FK),
  `decisions` (append-only §7 audit ledger, bigint PK, created_at only),
  `hard_rule_params` (versioned snapshots; 0003 seeds §6.1 defaults —
  conservative end of each stated range — as version 1, `created_by`
  NULL = system seed), `system_controls` (single row, CHECK id=1, seeded)
  + `control_events` (append-only), `orders` (proposal_id NOT NULL,
  UNIQUE `idempotency_key`) + `positions` (UNIQUE account+ticker).
- `users` simplified per the 2026-07-02 single-operator decision: email /
  full_name / role (+ `user_role` enum) dropped, `username` UNIQUE NOT
  NULL added — done in 0003, with backfill both directions so the
  round-trip survives data; migrations 0001/0002 untouched.
- `api_usage_log.linked_proposal_id` got its deferred FK → proposals
  (SET NULL) + index.
- DB-role separation (closes the standing `.Security-Agent/memory.md`
  pre-Phase-1 finding): migration 0004 creates `POSTGRES_APP_USER`
  (default `trading_runtime`) with DML-only grants and **no
  UPDATE/DELETE on decisions / control_events / api_usage_log** —
  append-only is now a database property, not a convention. Runtime
  engine (`app/database.py`) connects as this role; the schema-owning
  `POSTGRES_USER` is reserved for Alembic + test fixtures.
  `alembic_version` fully revoked from the runtime role.
- Tests 19 → 40: trading-core constraint/FK-semantics tests, schema
  invariants extended (append-only tables must not carry `updated_at`),
  and `test_db_roles.py` proving the runtime role's denials *and* that
  its INSERT/SELECT grants work (so denials aren't just "no access").
- Diagram: the dashed "planned" tables in the Postgres-schema cluster
  flipped to solid; legend rewritten (all live; users username-only;
  append-only tables noted). `.env.example` + CI env gained
  `POSTGRES_APP_USER` / `POSTGRES_APP_PASSWORD`.

**Why:**
- Roadmap §1: land every table the pipeline needs first, so later
  branches add code, not schema churn; FK topology (proposals → accounts
  RESTRICT, decisions → proposals RESTRICT) makes audit history
  undeletable transitively — deleting a user whose account has proposal
  history is rejected by the DB itself.
- Role separation done *in a migration* (not a compose initdb hack —
  the approach the security review warned against) so CI and every
  environment get it identically, and the round-trip gate covers it.
- Learned: psycopg's `exec_driver_sql` rejects any `%` in SQL (reads it
  as a placeholder) — Postgres `format('%I')` can't be used inside
  migration DDL strings; validated-and-inlined identifiers instead.

**Verification (gate from the roadmap):**
- ruff clean; alembic upgrade → downgrade → upgrade round-trip clean;
  40/40 pytest against live Postgres 15 (local Homebrew cluster — Docker
  daemon wasn't running; CI remains the second gate). A user-side
  `docker compose up` smoke is still wanted before merge.

**Open questions / what's next:**
- PR to master pending network (github.com unresolvable from the session
  at build time); after merge, branch 2 `features/auth-api`.
- `positions.quantity` CHECK >= 0 assumes long-only (matches §6.1
  blacklist of derivatives/leverage) — revisit if shorting is ever gated
  in.

## 2026-07-02 — Scaffold roadmap: feature-branch build plan + DB schema picture in the diagram

**What changed:**
- Added `Documents/scaffold-roadmap.md` — the approved build breakdown
  ("the bone") of plan §3/§5 Phases 1–2 into ordered feature branches,
  each with scope, design decisions + rationale, and a verification
  gate: `features/db-trading-core` (proposals / decisions /
  hard_rule_params / system_controls + control_events / orders +
  positions, users simplification, api_usage_log proposal FK, DB-role
  separation), `features/auth-api`, `features/hard-rules-engine`,
  `features/proposal-pipeline`, `features/control-plane-api`,
  `features/frontend-dashboard`, `features/market-data`,
  `features/agents-runtime`, `features/backtesting`.
- Updated `Documents/system.excalidraw` (add-only, 52 → 93 elements):
  new dashed "Postgres schema (general picture)" cluster below the
  trading-system frame — one node per table (solid = live Phase 0
  tables, dashed = planned db-trading-core tables), FK arrows, a
  revise-and-resubmit self-reference note on `proposals`, and a dashed
  arrow from the existing Postgres diamond down to the cluster (its
  `boundElements` updated accordingly). Script-verified: valid JSON,
  no dangling `boundElements`/`containerId`/binding refs.
- Added the roadmap doc to `CLAUDE.md`'s "Source of truth" section.

**Why:**
- User asked for the system scaffold (frontend/backend/docker) to be
  *designed first* — "build the bone, then work through everything" —
  with one feature branch per task, each feature verified working
  before the next starts, given the money risk. Chosen in a question
  round: roadmap document only this session (implementation starts next
  session), `features/*` branch per task (permission granted), auth
  early as feature 2 so control-plane endpoints are never built
  unauthenticated.
- User decision recorded in the roadmap: `users` gets simplified
  (drop `email`, `full_name`, `role`/`user_role`; add `username`) —
  this is a local single-operator project, so no roles: a single
  "logged-in operator" auth dependency guards all mutating endpoints.
  Change lands as a new migration in `features/db-trading-core`
  (migration 0001 is merged history, stays untouched).
- Money-safety enhancements baked into the design rather than the doc's
  literal text: append-only audit enforced by DB grants (no
  UPDATE/DELETE for the runtime role on `decisions` / `control_events`
  / `api_usage_log`), `orders.proposal_id` NOT NULL + idempotency key,
  hard rules re-checked at execution time, kill switch checked
  synchronously in the order path, agents restricted to the backend API
  (never direct DB) so the hard-rules gate can't be bypassed
  structurally (§7).

**Open questions / what's next:**
- Start `features/db-trading-core` per the roadmap (first
  implementation branch).
- §6 Q3's initial fixed-budget split across agents remains open —
  config data, not schema, so it doesn't block the scaffold.
- CrewAI-vs-plain bake-off (§11 Q5) deliberately deferred to
  `features/agents-runtime`.

---

## 2026-07-02 — Plan §6: hard-rule risk limits and Member Agent success metric, starting defaults

**What changed:**
- `swarm-trading-system-plan.md` §6 questions 2 and 5 marked resolved with
  concrete starting defaults, added as new subsections 6.1 (hard-rule
  parameters) and 6.2 (success metric / capital-reallocation model).
  Question 3 (capital allocation model) noted as partially addressed by
  6.2's probation model, but the *initial* fixed-budget split across
  agents is still open.
- **6.1 (hard-rules layer, §3.2 layer 1):** per-agent max position size
  (20–25% of that agent's own capital), portfolio-wide max position size
  (10% of total portfolio per ticker), max sector exposure (30–40%),
  daily loss circuit breaker (−3% → auto-pause all agents), weekly loss
  circuit breaker (−5% → mandatory human review), per-position stop-loss
  (−8% to −10%), trade frequency cap (≤5 trades/agent/day), a blacklist
  (leveraged/inverse ETFs, sub-$5 stocks, options/derivatives) and an
  early-phase whitelist (S&P 500 constituents only).
- **6.2 (success metric):** rolling Sortino ratio vs. SPY benchmark
  (30–90 day window) as the primary metric, max drawdown as an
  independent guardrail, a minimum sample size (~20 trades or 30 days)
  before acting, and a probation model — underperform 2 windows → capital
  cut 50%, 3 windows → paused pending human review; outperform 2+
  windows → capital increased in fixed steps, capped per-agent.
  Retirement stays a human decision, not automatic.

**Why:**
- User asked directly for the answers to §6 questions 2 and 5, wanted
  every term explained in plain language first (financial/trading
  jargon — position, ticker, circuit breaker, Sharpe/Sortino ratio,
  alpha, drawdown, slippage, etc. — this project's own stated learning
  goal, §1), then asked to commit the defaults into the plan doc as-is,
  explicitly deferring further tuning until there's real backtesting/
  paper-trading experience to tune against rather than guessing further
  now.
- These are explicitly starting defaults, not final risk limits — framed
  that way in the doc itself (6.1/6.2 headers) so they don't get
  mistaken for validated numbers later.

**Open questions / what's next:**
- Question 3's initial fixed-budget split across agents (before any
  performance history exists to base the probation model on) is still
  unresolved.
- Question 4 (rejected proposal: discarded vs. revise-and-resubmit) is
  untouched — not part of this session's scope.
- Revisit every number in 6.1/6.2 once Phase 1 backtesting produces
  real evidence — these were reasoned defaults, not fitted to data.

---

## 2026-07-02 — ORM delete-semantics fix (first real test_models.py run), security test hardening, plan §9.1/§11 reconciliation

**What changed:**
- Logged retroactively: the previous session's commit (`39f7bc0`, pushed
  to `claude/plan-code-improvements-xezruv` without a memory entry —
  logging-rule miss, corrected here) introduced `mixins.db_enum` so all
  enum columns persist member *values* ('user') instead of names
  ('USER'), matching migration 0001's Postgres types; dropped
  `api_usage_log.updated_at` (migration 0002 — append-only ledger);
  replaced unmaintained `passlib` with `argon2-cffi` in `security.py`.
- **First real run of `test_models.py` against live Postgres** (apt-
  installed PG16 in the session sandbox; Docker image pulls are blocked
  by this environment's network policy). It immediately caught a real
  bug: `session.delete(user)` raised `NotNullViolation` because the ORM
  relationships didn't know about the DB's `ON DELETE` behavior and
  tried to null child FKs first. Fixed by aligning every relationship
  with migration 0001's FK semantics: `User.accounts` /
  `User.api_credentials` / `Agent.usage_logs` get
  `cascade="all, delete-orphan", passive_deletes=True` (DB CASCADE owns
  the delete), `Agent.accounts` gets `passive_deletes="all"` (DB
  RESTRICT must be the one to reject deleting a funded agent),
  `Account.usage_logs` gets `passive_deletes=True` (DB SET NULL, don't
  load the high-volume ledger).
- Security/Test-Agent hardening pass on the argon2 + enum changes: new
  tests for fail-closed `verify_password` on malformed hashes, a frozen
  passlib-era hash verifying the back-compat claim, a security cascade
  test (deleted user leaves no encrypted credential rows), and a new
  standalone `tests/test_schema.py` guarding two schema invariants
  (every enum column goes through `db_enum`; every FK declares explicit
  `ondelete`). Full suite: 19/19 passing against live Postgres, Alembic
  upgrade→downgrade→upgrade round-trip clean, ruff clean.
- Plan doc reconciled: §9.1 now states provider-vs-strategy are
  orthogonal per-agent configuration (backed by the existing
  `agents.llm_provider` / `agents.strategy` columns), resolving §11
  open question 4; added §11 question 5 noting the §4/§6
  (LangGraph-vs-CrewAI open) vs §5/diagram (CrewAI named) tension, with
  CrewAI as working default until the Phase 1 Manager is built.
- Diagram checked against §§8–10: all plugins, connectors, and
  Finance/IB internals present, no dangling element refs — no diagram
  change needed this session.

**Why:**
- User asked to continue the code-improvement branch, then narrowed the
  session to: verify the plan/tools/map/system design are sound, and
  enhance security via the co-worker test agents. The relationship fix
  wasn't optional polish — it made user deletion impossible at runtime,
  and only surfaced because the DB-backed tests finally ran for real
  (closing the standing "run test_models.py against live Postgres" open
  item).

**Open questions / what's next:**
- DB-role separation (single Postgres role for migrations + runtime)
  remains the standing pre-Phase-1 security item.
- §11 question 5: confirm or drop CrewAI when the Phase 1 Manager gets
  built.
- CI has not yet run these changes (branch push pending at time of
  writing) — the 19/19 result is from the session sandbox.

---

## 2026-07-01 — Security-Agent + Test-Agent review pass, first CI/CD pipeline

**What changed:**
- User asked to run Security-Agent's and Test-Agent's charters against
  the Phase 0 code from the previous entry, and stand up a first CI/CD
  pipeline in the same commit. Full findings/reasoning live in each
  agent's own `memory.md` (`.Security-Agent/memory.md`,
  `.Test-Agent/memory.md`) per their own logging convention — this entry
  is the root-level summary.
- **Security-Agent review** of `backend/` and `docker-compose.yml`:
  fixed weak `Mapped[Numeric]` typing on money columns (now
  `Mapped[Decimal]`), added DB-level `CHECK` constraints (non-negative
  capital/tokens/cost), rebound all Docker Compose published ports to
  `127.0.0.1` instead of `0.0.0.0`, added non-root users to both
  Dockerfiles. Left DB-role separation (single Postgres role for both
  migrations and app runtime) as an open, non-blocking finding — real,
  but no live sensitive data exists yet to make it urgent.
- **Critical finding, fixed:** `frontend/package.json` pinned
  `next@15.1.3`, which has a known critical CVE (CVE-2025-66478) plus
  ~20 other advisories. Bumped to `next@16.2.10` and added a
  `postcss` version override to close a secondary moderate finding
  without downgrading Next.js. Verified: `npm audit` clean, build and
  dev server both still work.
- **Dependency audit, fixed:** `pip-audit` found 11 known
  vulnerabilities in the original `backend/requirements.txt` pins, most
  notably `cryptography==44.0.0` — the exact package backing
  `security.py`'s credential encryption. Bumped every pin to current
  stable releases; re-verified `pip-audit` clean and all previously
  passing checks (model imports, migration SQL generation, ruff, tests)
  still pass against the new versions.
- **Test-Agent**: added `backend/tests/` (`test_security.py`,
  `test_main.py` — both run standalone, no DB, 6/6 passing locally;
  `test_models.py` — needs live Postgres, written but unverified locally
  since Docker Desktop's daemon wasn't running this session, will get
  its first real run in CI). Added `ruff` lint (found and fixed 10
  pre-existing `F821` findings from SQLAlchemy 2.0's string-based
  forward-reference relationships not being visible to static analysis —
  fixed with `TYPE_CHECKING`-guarded imports, the standard pattern).
- **First CI/CD pipeline**: `.github/workflows/ci.yml` — backend job
  (ruff, pip-audit, Alembic upgrade/downgrade/upgrade round-trip against
  a Postgres service container, pytest) and frontend job (npm audit,
  npm run build), triggered on push/PR to `master`.
- Added `backend/requirements-dev.txt`, `backend/pytest.ini`,
  `backend/ruff.toml`.

**Why:**
- User wants every real code change checked by both co-worker agents
  before it's treated as done, and wanted the first CI pipeline bundled
  into the same commit as the Phase 0 code itself rather than as a
  follow-up.
- Fixed rather than just reported everything with a clear-cut, no-tradeoff
  fix (typing bugs, DB constraints, port binding, non-root containers,
  both dependency CVEs) — consistent with Security-Agent's and
  Test-Agent's charters, which both frame "reviews and recommends" as not
  requiring a separate sign-off round when there's no real tradeoff to
  weigh. Left the one finding with a real tradeoff (DB role separation)
  open and explicitly flagged rather than shipping a rushed partial fix.
- Unrelated to this session's work but discovered mid-session: this
  repo's local `master` branch now has a merged PR and is the branch
  actually being worked from (origin's default branch pointer still
  shows `docs/initial_documents`) — CI triggers on `master` to match
  where work is actually happening.

**Open questions / what's next:**
- Run `test_models.py` for real against a live Postgres (local Docker or
  the next CI run) — reasoning through the logic is not the same as
  verifying it.
- Close the DB-role-separation finding (Security-Agent memory.md) before
  Phase 1 writes any real credential or capital row.
- Re-review CORS the moment the frontend makes a real cross-origin call
  to the backend; add the JWT/session/CSRF/audit-log-tamper-evidence
  checks the moment that code exists — all explicitly deferred as
  not-yet-applicable, not resolved.

---

## 2026-07-01 — Phase 0: Postgres schema, FastAPI backend, Next.js frontend skeleton, Docker Compose

**What changed:**
- Added `backend/` — first real source code in the repo:
  - FastAPI app (`app/main.py`, `/health` endpoint), SQLAlchemy 2.0 models
    (`app/models/`), Pydantic-settings config (`app/config.py`), password
    hashing + Fernet credential encryption (`app/security.py`).
  - Five tables via Alembic migration `0001_initial_schema.py`: `users`
    (login credentials, `role` enum for admin/kill-switch access),
    `agents` (reusable name/type/strategy/llm_provider/llm_model/task
    definitions — decoupled from capital so one agent definition can back
    multiple funded accounts), `accounts` (per-agent capital allocation:
    `allocated_capital`, `current_balance`, `status` enum incl. `killed`
    for the manual-override kill switch), `api_credentials` (broker/LLM
    secrets, `encrypted_value` as Fernet ciphertext — never plaintext),
    `api_usage_log` (per-call token/cost ledger keyed to agent + optional
    account, bigint PK since high-volume, `linked_proposal_id` column
    present but unconstrained — no FK yet since the proposals table
    doesn't exist until Phase 1).
  - Verified: models import cleanly, `alembic upgrade head --sql`
    generates correct offline SQL (postgresql+psycopg driver). Could not
    verify against a live Postgres — Docker Desktop's daemon wasn't
    running in this session.
- Added `frontend/` — minimal Next.js 15 app-router skeleton (placeholder
  home page only) so docker-compose has something real to build on port
  3000; no dashboard/control-plane UI yet.
- Added `docker-compose.yml` at repo root: `postgres` (16-alpine, healthcheck),
  `redis` (7-alpine, per Phase 0 plan even though nothing consumes it
  yet), `migrate` (one-shot `alembic upgrade head`, backend `depends_on`
  it with `service_completed_successfully`), `backend` (port 5000),
  `frontend` (port 3000). Verified with `docker compose config` (daemon
  wasn't running, so no live `up` test).
- Added `start.sh` / `stop.sh` (docker compose up -d --build / down),
  `.env` (real local Fernet key generated, gitignored) and `.env.example`
  (committed, no secrets) at repo root.
- Extended `.gitignore`: `__pycache__/`, `.venv/`, `node_modules/`,
  `.next/`, `postgres_data/`.
- Updated `swarm-trading-system-plan.md`'s status line and `CLAUDE.md`'s
  "Status" section to reflect that this is no longer a planning-only repo.

**Why:**
- User asked to start Phase 0 for real: a Postgres schema for
  users/accounts (funds, capital, agent name/model/tasks, API) plus a
  docker-compose wiring frontend (3000) + backend (5000) + migrations,
  and start/stop scripts.
- Confirmed via question round before building (since this is the first
  code in a greenfield repo — wrong defaults here are expensive to
  unwind): FastAPI (not Flask) as the actual framework; Alembic for
  migrations; Redis included now per the Phase 0 plan text even though
  today's ask only mentioned Postgres; schema split into 4 separate
  tables (not one wide Account table) plus a 5th `api_usage_log` table
  for per-agent LLM token/cost tracking, which the user flagged as a
  near-term need while answering.
- `agents` kept separate from `accounts` (not folded together) so the
  same agent definition (e.g. "Momentum-Claude") can be reused across
  multiple funded accounts rather than being 1:1 with a capital
  allocation — matches plan §3.1's "each member agent holds its own
  allocated capital" without forcing a 1:1 identity between "agent" and
  "capital pool."
- `api_credentials.encrypted_value` is Fernet-encrypted (reversible, app
  needs the plaintext to call broker/LLM APIs) rather than hashed —
  different requirement from `users.password_hash` (one-way, argon2),
  which is often conflated but isn't the same problem. Matches
  Security-Agent's "credentials encrypted at rest" charter constraint.

**Open questions / what's next:**
- Live-DB verification of the migration (`docker compose up` end-to-end,
  confirm tables actually create/drop cleanly) still needs to happen next
  session once Docker Desktop's daemon is running.
- No auth endpoints (login/register/JWT) exist yet — schema only, no API
  surface for `users`/`accounts` beyond `/health`.
- `api_usage_log.linked_proposal_id` has no FK constraint yet — revisit
  once the Phase 1 proposals table exists (plan §5, §3.1).
- Frontend is a placeholder page only — no dashboard, no manual-override
  control plane UI yet (plan §3.3).
- `CREDENTIAL_ENCRYPTION_KEY` in the committed-nowhere `.env` is a
  locally-generated dev-only key; production/staging must each get their
  own, never reused across environments.

---
## 2026-07-01 — codebase-memory graph auto-re-index hook

**What changed:**
- Re-indexed the codebase-memory-mcp graph now that real source exists:
  84 nodes / 83 edges (docs era) → 284 nodes / 534 edges (`backend/` +
  `frontend/`).
- Added a project `SessionStart` hook `.claude/hooks/cbm-autoindex.sh`
  (wired in a new tracked `.claude/settings.json`) that re-indexes in
  `fast` mode only when the git tree changed since the last index.
  Change signature = `HEAD` + `git diff HEAD` + untracked file list,
  cached in `.codebase-memory/.autoindex-sig`. No-ops otherwise; any
  failure exits 0 so it never blocks a session.
- `.gitignore` rewritten so the hook can be shared: `\.claude` (ignored
  the whole dir) → `.claude/*` with `!.claude/settings.json` and
  `!.claude/hooks/`, keeping `.claude/settings.local.json` local. Added
  `.codebase-memory/`.
- Updated CLAUDE.md's "codebase-memory-mcp usage policy" to match (graph
  now covers code; freshness automated instead of a manual re-index).

**Why:**
- The old policy relied on a human remembering to re-run
  `index_repository` after code lands — which is exactly how a graph goes
  stale. Substantial code had landed, so the graph was already out of
  date and the query tools had become worth using. A guarded hook keeps
  it fresh automatically, with no per-edit cost and no blocking risk.
- Sharing the hook via the repo (loosening the blanket `.claude` ignore)
  means anyone who clones gets the same freshness behavior.

**Open questions / what's next:**
- Hook fires at session boundaries, not per file edit, so a long session
  that edits code won't refresh mid-session. Add a debounced
  `Stop`/`PostToolUse` trigger later if that becomes a pain.
- A brand-new `.claude/settings.json` isn't picked up by the settings
  watcher until `/hooks` is opened once or Claude Code restarts.

## 2026-07-01 — codebase-memory-mcp installed and indexed, usage scoped down

**What changed:**
- Installed `codebase-memory-mcp` (github.com/DeusData/codebase-memory-mcp)
  globally — active across all Claude Code projects on this machine, not
  just this repo. Adds a `SessionStart` hook (injects a tool-preference
  reminder every session) and a `PreToolUse` hook on Grep/Glob (silently
  augments results with graph context).
- Ran `index_repository` on this repo: 9 files, 84 nodes, 83 edges
  indexed (mostly the planning docs — no real source code yet).
- Added a usage policy to `CLAUDE.md`: hooks stay enabled, but Claude
  should not proactively call the query tools (`search_graph`,
  `trace_path`, `get_architecture`, etc.) until this repo has enough real
  code that a graph query beats a few targeted Grep/Read calls on token
  cost.
- Swapped the installed binary for the UI-enabled release variant
  (`codebase-memory-mcp-ui-windows-amd64.zip`, checksum-verified against
  the published `checksums.txt`) at the same path
  (`%LOCALAPPDATA%\Programs\codebase-memory-mcp\codebase-memory-mcp.exe`),
  so both the MCP server and `serve --ui=true --port=9749` work from one
  binary. The pre-swap standard binary is kept as
  `codebase-memory-mcp.exe.standard-bak` in the same directory.

**Why:**
- User asked to save token usage. The hooks are small fixed/per-call
  overhead regardless of use; the query tools only pay for themselves
  once there's an actual call graph worth traversing, which this
  docs-only repo doesn't have yet.
- User wants the graph UI available for future use. It can't be kept
  running as a background daemon from inside Claude Code's sandboxed
  tool calls — the binary appears to tie its lifecycle to its parent
  process (consistent with its primary role as an MCP stdio subprocess),
  so it exits as soon as any single sandboxed shell call ends. User
  should launch it themselves in a normal terminal when wanted:
  `codebase-memory-mcp serve --ui=true --port=9749`, then browse to
  `http://127.0.0.1:9749`.

**Open questions / what's next:**
- Re-run `index_repository` once real source code exists, and revisit
  whether proactive tool use is worth it at that point.

---

## 2026-07-01 — Multi-domain org: plugins, connectors, memory/rules files

**What changed:**
- Added this file (`memory.md`) at repo root.
- Added `CLAUDE.md` at repo root (durable rules, auto-loaded every session).
- Appended Sections 8–11 to `Documents/swarm-trading-system-plan.md`:
  Multi-Domain Org Architecture, Plugin Catalog, Connector → Plugin
  Mapping, and Open Design Questions (Org-Level). Sections 1–7 (the
  original trading-swarm plan) were left byte-for-byte unchanged.
- Directly edited `Documents/system.excalidraw` to add: a top-level
  "Orchestrator" box with arrows down to each plugin's Manager; a new
  Engineering plugin cluster (dashed frame, "Manager Agent - Engineering"
  box, "Github" connector node); a new Design plugin cluster (dashed
  frame, "Manager Agent - Design" box, "Excalidraw" and "Goodnotes"
  connector nodes); a cross-cutting "AgentMail" node connected to the
  Orchestrator with a dashed arrow; and a small "Finance / Investment
  Banking (plugin)" label inside the existing (untouched) trading-system
  frame. All original elements in that file are unchanged — only new
  elements were added around them, plus one necessary metadata update
  (added the new arrow's id to the existing Finance/IB Manager box's
  `boundElements` array, since Excalidraw expects bound shapes to list
  the arrows attached to them).

**Why:**
- No process log existed before this — decisions and their reasoning had
  no durable home, risking loss of context between sessions.
- The project is broadening from a single trading-agent-swarm plan into
  a multi-domain agent org with four plugin categories: Finance and
  Investment Banking (combined into one plugin, = the existing trading
  plan as-is), Engineering (the org doing engineering work on itself —
  infra/repo/CI), and Design (diagramming/UX/notes). Confirmed directly
  with the user — this is a genuine scope expansion, not just a relabeling
  of the existing trading system.
- Connector-to-plugin mapping (Robinhood → Finance/IB, Github →
  Engineering, Excalidraw + Goodnotes → Design, AgentMail → cross-cutting)
  follows the natural domain fit and reuses connectors already live in
  the current environment rather than inventing new integrations.
- Initial direction was a separate new architecture doc plus
  gap-reporting only (no diagram edits); the user redirected to fold the
  architecture directly into `swarm-trading-system-plan.md` and to
  directly update `system.excalidraw` itself, so the doc and the diagram
  both reflect the org's real shape rather than describing it secondhand.

**Diagram verification findings (system.excalidraw vs. plan, before this
session's edits):**
- The diagram depicted *only* the Finance/Investment-Banking plugin's
  internals: "Manager Agent - CrewAI" with arrows down to three ellipses
  (ChatGPT, Gemini, Claude), each arrowing down to a "Shared data layer"
  box containing "Robinhood / Market data" text plus Postgres/Redis
  diamonds.
- Naming mismatch (pre-existing, still unresolved): the diagram names
  the three delegate agents by LLM provider (ChatGPT/Gemini/Claude);
  `swarm-trading-system-plan.md` Section 3.1 names member agents by
  strategy (Momentum/Mean-Reversion/Sentiment). Not necessarily a
  contradiction — each provider-named agent could run a distinct
  strategy internally — but the mapping is never stated explicitly
  anywhere. Flagged in the new Section 11, not resolved.
- The diagram had no Engineering/Design representation and no connector
  nodes prior to this session — expected, since it predated the
  plugin/connector concept. This session's edits addressed that gap
  directly (see "What changed" above) rather than just reporting it.

**Open questions / what's next:**
- Resolve the LLM-provider-vs-strategy naming mismatch on the Finance/IB
  ellipses (see Section 11 in `swarm-trading-system-plan.md`).
- Engineering and Design plugins are only scoped at a high level so far;
  neither has build phases or Member-Agent detail the way Finance/IB
  does (Phases 0–5).
- Decide whether every plugin needs the full two-layer hard-rules +
  soft-judgment Manager, or whether that's specific to Finance/IB's
  real-capital risk profile (Section 11).
- Decide whether Investment Banking should split out from Finance into
  its own plugin later.

---

## 2026-07-01 — Engineering plugin gets its first two Member Agents: Security-Agent, Test-Agent

> **Correction (same day, see next entry):** This entry's premise was
> wrong — Security-Agent and Test-Agent are engineering co-worker agents,
> not Member Agents of the Engineering plugin. The plan-doc and diagram
> changes described below were reverted. Left as-is (not rewritten) per
> the append-only convention; see the 2026-07-01 correction entry below
> for what actually stands.

**What changed:**
- Added `Security-Agent/` and `Test-Agent/` folders at repo root, each
  with its own `CLAUDE.md` (durable charter/constraints), `SKILLS.md`
  (operational checklist), and `memory.md` (per-agent decision log,
  same append-only convention as this file), mirroring the root-level
  documentation pattern.
- Updated `swarm-trading-system-plan.md` §9.2 (Engineering) to name both
  as Member Agents reporting to the Manager Agent - Engineering, closing
  part of the "no Member-Agent detail" gap noted in the previous entry.
- Updated `Documents/system.excalidraw`: added two ellipse nodes
  ("Security-Agent", "Test-Agent") inside the existing Engineering
  plugin frame, each with an arrow from `engManagerRect1` (Manager Agent
  - Engineering), alongside the existing Github connector node. Added
  the two new arrow ids to `engManagerRect1`'s `boundElements`. No
  existing elements were altered beyond that.

**Why:**
- User wants two additional Engineering-plugin agents: one for security
  review (exploitable flaws/bugs; hard requirement that
  credentials/sensitive data are always encrypted at rest and that the
  database layer has strong validation/access restriction), and one for
  test-case generation gating CI/CD before any merge to `master`.
- Charters were written to explicitly not have merge/deploy authority —
  both report findings/results to the Manager Agent - Engineering (or a
  human), matching the Member Agent → Manager approval-gateway pattern
  already established for Finance/IB (Section 3) rather than inventing a
  new authority model.
- Confirmed with the user (full-sync option) to also update the plan doc
  and diagram in the same pass, per this repo's own logging rule
  (`CLAUDE.md`): adding Member Agents to a plugin is a meaningful,
  loggable change, and the diagram must stay in sync with the doc.

**Open questions / what's next:**
- Two empty, untracked folders named `Security/` and `Test/` already
  existed alongside the ones the user asked for (`Security-Agent/`,
  `Test-Agent/`) — left untouched since they're empty; unclear if they
  were an earlier naming attempt that should be removed later.
- No actual review/testing tooling exists yet (repo is still
  planning-only) — these folders currently document charter and skills
  only, per each agent's own `CLAUDE.md`.
- Engineering plugin still has no build phases (Phases 0–5 equivalent)
  the way Finance/IB does — carried over from the previous entry's open
  question, still unresolved.

---

## 2026-07-01 — Correction: Security-Agent/Test-Agent are not part of the org's multi-agent architecture

**What changed:**
- Reverted `swarm-trading-system-plan.md` §9.2 back to its original text
  (no build phases, no Member-Agent detail), plus one new sentence
  clarifying that `Security-Agent/` and `Test-Agent/` are not Member
  Agents of this plugin.
- Reverted `Documents/system.excalidraw` to its original 52-element state
  — removed the `securityEllipse1`/`securityText1`/`testEllipse1`/
  `testText1`/`securityArrow1`/`testArrow1` elements and the dangling
  `boundElements` references to them on `engManagerRect1`. Verified via
  script: element count matches the pre-change baseline and no dangling
  `boundElements` references remain anywhere in the file.
- Rewrote `Security-Agent/CLAUDE.md` and `Test-Agent/CLAUDE.md` to drop
  all "Member Agent of the Engineering plugin" / "reports to the Manager
  Agent - Engineering" language, replacing it with: these are engineering
  co-worker agents that help build this project, outside the org's own
  multi-agent hierarchy and not depicted in the diagram. Blocking
  findings now escalate to the user directly, not to a Manager Agent.
- Updated `Security-Agent/SKILLS.md` and `Test-Agent/SKILLS.md` similarly
  (removed "escalate to the Manager Agent - Engineering" and "rest of the
  org" framing; kept the substantive review/test checklists, since those
  are still valid regardless of the agents' org placement).
- Left each agent's own `memory.md` creation entry uncorrected inline in
  this pass (still says "Member Agent of the Engineering plugin") — flagged
  in "Open questions" below to fix in each agent's own log.

**Why:**
- User clarified directly: "These agents are not multiple agents that I
  mentioned in the project. Treat them as co-worker that helps me solve
  the problem and issue about the coding product. not related with core
  multiple agents for this project." The previous entry's framing (Member
  Agent → Manager Agent approval-gateway pattern, diagram placement) was
  a misread of that intent — these agents assist with engineering work on
  the repo itself, they are not entities inside the trading-swarm /
  multi-domain-org architecture this project's docs describe.

**Open questions / what's next:**
- `Security-Agent/memory.md` and `Test-Agent/memory.md` still describe
  themselves as "a Member Agent under the Engineering plugin" in their
  2026-07-01 creation entries — should get a same-day correction entry in
  each file, same pattern as this one, next time those folders are
  touched.
- The two empty, untracked `Security/` / `Test/` folders noted in the
  previous entry are still unaddressed.
