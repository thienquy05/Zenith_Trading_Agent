# CLAUDE.md

Rules for working in this repo. This file is durable and auto-loaded
every session — for the dated log of *why* things changed, see
[`memory.md`](memory.md).

## Status

Phase 1 scaffolding underway (per `Documents/scaffold-roadmap.md`: one
feature branch per section, built in order). Landed so far: `backend/`
(FastAPI + SQLAlchemy + Alembic) with the full trading-domain schema —
Phase 0's users/agents/accounts/api_credentials/api_usage_log plus
`features/db-trading-core`'s proposals/decisions/hard_rule_params/
system_controls/control_events/orders/positions, with DB-enforced
append-only ledgers via a least-privilege runtime role — a minimal
`frontend/` (Next.js placeholder), `docker-compose.yml` (postgres + redis
+ backend + frontend + one-shot `migrate` service), and `start.sh` /
`stop.sh`. Branch 3's hard-rules engine (`backend/app/rules/` — pure
functions, one per §6.1 rule, every violation reported in one pass) is
built and verified; branch 2 (`features/auth-api`) is pushed and awaiting
its PR/merge. No live agent logic yet — roadmap branches 4+ (proposal
pipeline, control plane, …) are next. See `memory.md` for the full
rationale.

## The logging rule

Any meaningful change — a planning doc added/changed, a milestone hit, an
architectural decision, a plugin/connector added, or the diagram
(`Documents/system.excalidraw`) updated — must get an entry in
`memory.md`, following the template at the top of that file. Routine,
no-decision edits (typos, formatting) don't need an entry. `memory.md`
entries are append-only; never rewrite past entries, only add corrections
inline.

## codebase-memory-mcp usage policy

`codebase-memory-mcp` is installed globally and indexes this repo. Once a
branch carries real source (the FastAPI `backend/` and Next.js
`frontend/`), the graph covers it — not just docs — so a call graph can
pay off. Reach for its query tools (`search_graph`, `trace_path`,
`get_architecture`, etc.) when a structural question would cost more in
Grep/Read than a single graph call; still prefer Grep/Read for text,
configs, non-code files, and branches that are docs-only.

Freshness is automated: a project `SessionStart` hook
(`.claude/hooks/cbm-autoindex.sh`, wired in `.claude/settings.json`)
re-indexes in `fast` mode whenever the git tree changed since the last
index, and no-ops otherwise. Its state lives in the git-ignored
`.codebase-memory/`. You normally don't need to re-index by hand — do a
manual `index_repository` (full mode) only after a large refactor, or if
you suspect drift mid-session (the hook fires at session start, not
per-edit).

## Source of truth

- `Documents/swarm-trading-system-plan.md` — Sections 1–7 are the
  detailed Finance/Investment Banking build plan (Member Agents → Manager
  Agent → Shared Data Layer, build Phases 0–5). Sections 8–11 are the
  org-wide multi-domain plugin/connector architecture.
- `Documents/system.excalidraw` — the visual counterpart. Keep it and the
  plan doc in sync: if you add/change a plugin or connector in the doc,
  reflect it in the diagram too (and log it in `memory.md`). It also
  carries the "Postgres schema (general picture)" cluster — update it
  when tables are added/changed.
- `Documents/scaffold-roadmap.md` — the feature-branch build breakdown of
  plan §3/§5 Phases 1–2 (one `features/*` branch per section, built in
  order, each verified before the next starts). Read it before starting
  any implementation branch.

## Non-negotiable constraints (Finance/Investment Banking plugin)

From `swarm-trading-system-plan.md` Section 7 — restated here since this
file is what gets read first:
- No component ever bypasses the hard-rules layer, regardless of LLM
  confidence.
- No live trading until backtesting + paper trading both show acceptable
  behavior.
- Full audit log of every proposal, reasoning, decision, and override —
  nothing executes silently.
- Manual override / kill switch must be checked before every real order,
  not asynchronously.

## Plugin → connector quick reference

| Connector | Plugin(s) | Role |
|---|---|---|
| Robinhood | Finance / Investment Banking | Trade execution (equities + crypto) |
| Github | Engineering | Code / repo / PR / issue work |
| Excalidraw | Design | Diagramming |
| Goodnotes | Design | Note-taking |
| AgentMail | Cross-cutting (all plugins) | Notifications, reports, communication |

Full detail: `swarm-trading-system-plan.md` Sections 9–10.
