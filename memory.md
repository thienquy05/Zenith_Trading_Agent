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
