# CLAUDE.md

Rules for working in this repo. This file is durable and auto-loaded
every session — for the dated log of *why* things changed, see
[`memory.md`](memory.md).

## Status

Planning-only project (no source code, no commits yet). Everything below
is architecture/process, not implementation.

## The logging rule

Any meaningful change — a planning doc added/changed, a milestone hit, an
architectural decision, a plugin/connector added, or the diagram
(`Documents/system.excalidraw`) updated — must get an entry in
`memory.md`, following the template at the top of that file. Routine,
no-decision edits (typos, formatting) don't need an entry. `memory.md`
entries are append-only; never rewrite past entries, only add corrections
inline.

## codebase-memory-mcp usage policy

`codebase-memory-mcp` is installed globally (indexes this repo already —
9 files, mostly docs). Its `SessionStart` and `PreToolUse` hooks stay
enabled, but its query tools (`search_graph`, `trace_path`,
`get_architecture`, etc.) are token overhead with little payoff on a
docs-only repo. Don't call them proactively — only reach for them once
this repo has enough real source code that a call graph would actually
save more tokens than a few targeted Grep/Read calls. Re-run
`index_repository` after substantial code additions so the graph doesn't
go stale.

## Source of truth

- `Documents/swarm-trading-system-plan.md` — Sections 1–7 are the
  detailed Finance/Investment Banking build plan (Member Agents → Manager
  Agent → Shared Data Layer, build Phases 0–5). Sections 8–11 are the
  org-wide multi-domain plugin/connector architecture.
- `Documents/system.excalidraw` — the visual counterpart. Keep it and the
  plan doc in sync: if you add/change a plugin or connector in the doc,
  reflect it in the diagram too (and log it in `memory.md`).

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
