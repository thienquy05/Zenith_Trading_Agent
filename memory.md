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
