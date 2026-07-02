# Multi-Agent Swarm Trading System — Project Plan (v1 Draft)

**Status:** Phase 0 — Docker Compose skeleton + Postgres schema (users/agents/accounts/api_credentials/api_usage_log) in place. See `memory.md` for details.

---

## 1. Purpose & Goals

- **Learning goal:** Deeply understand multi-agent systems, swarm intelligence concepts, and how they apply (and don't apply) to financial decision-making.
- **Practical goal:** Build a real, working system that manages real capital under strict, auditable constraints — not a black box.
- **Guiding principle:** No component executes a real trade without passing through explicit, inspectable rules first. Reasoning and machine judgment inform decisions; hard-coded limits gate them.

---

## 2. Architecture Overview

This is **not** a leaderless swarm (like ant colony optimization). It's a **hierarchical multi-agent system**:

```
                    ┌─────────────────────┐
                    │   Manager Agent      │
                    │  (approval gateway)  │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                 │
     ┌────────▼──────┐ ┌───────▼──────┐ ┌────────▼──────┐
     │ Member Agent 1 │ │ Member Agent 2│ │ Member Agent N│
     │ (own capital)  │ │ (own capital) │ │ (own capital) │
     │ e.g. Momentum  │ │ e.g. Mean-Rev │ │ e.g. Sentiment│
     └────────────────┘ └───────────────┘ └───────────────┘
              │                │                 │
              └────────────────┼─────────────────┘
                               │
                    ┌──────────▼───────────┐
                    │   Shared Data Layer   │
                    │ (price/market feeds)  │
                    └───────────────────────┘
```

**Where "swarm intelligence" actually lives:** in how member agents' independent signals get aggregated and weighted over time — not in leaderless emergence. Think of it as a *supervised swarm*: many independent, diverse voices, but with a governor that enforces sanity.

---

## 3. Core Components

### 3.1 Member Agents
- Each holds its **own allocated capital** (a sub-budget, not the whole portfolio).
- Each runs a **distinct strategy/signal source** — diversity here is the actual value of having multiple agents, not a decorative feature.
- On wanting to act, a member agent must submit a **structured proposal** to the Manager:
  - Action (buy/sell/hold), ticker, size, timeframe
  - **Reasoning** (the "why")
  - Confidence score
  - Current agent capital state

### 3.2 Manager Agent
Two-layer decision process — this is the key design correction from our earlier discussion:

1. **Hard rules layer (deterministic code, not LLM judgment)**
   - Max position size (% of that agent's capital, % of total portfolio)
   - Max sector/correlation exposure across all agents combined
   - Stop-loss / max daily loss circuit breakers
   - Blacklist/whitelist of tickers
   - Trade frequency limits (anti-overtrading)
   - **A proposal that fails any hard rule is auto-rejected — no LLM involved.**

2. **Soft judgment layer (LLM reasoning, only runs after hard rules pass)**
   - Does the member's thesis hold up?
   - Does it conflict with another agent's current position?
   - Tie-breaking when multiple agents want the same capital-adjacent action
   - Can approve, reject, or **request modification** (e.g., "reduce size by 30%") rather than a flat binary

### 3.3 Manual Override
- A human-accessible control plane (dashboard or CLI) that can:
  - Pause any individual agent
  - Pause the entire system (kill switch)
  - Force-reject a pending proposal regardless of Manager approval
  - Manually adjust hard-rule parameters without redeploying code
- This must be **checked synchronously before any real order fires** — not just a monitoring layer bolted on after the fact.

### 3.4 Shared Data Layer
- Central service that fetches and caches market data so agents aren't hitting rate limits independently.
- Feeds all member agents + the Manager with a consistent view of the market at decision time.

---

## 4. Technology Stack (Recommended)

| Layer | Recommendation | Why |
|---|---|---|
| Containerization | Docker Compose | You already want this; clean service isolation per agent |
| Inter-agent messaging | Redis pub/sub (or lightweight queue) | Simple, fast, good fit for proposal/approval flow |
| Manager framework | LangGraph (or CrewAI) | Both handle stateful, branching approval workflows better than plain OpenAI Agents SDK for this specific manager/worker pattern — worth a short bake-off before committing |
| Member agent framework | Lightweight — can be simple Python services, don't need heavy agent frameworks for straightforward strategies | Keeps early agents easy to debug |
| Stocks execution | **Robinhood Agentic Trading (MCP)** | Official, beta, built-in trade preview/override — matches your manual-override requirement natively |
| Crypto execution | **Robinhood Crypto Trading API** (key-pair auth) | Official, documented, separate from the agentic product |
| Market data / backtesting | **Alpaca** (market data API + free paper trading sandbox) | Purpose-built for this, avoids relying on Robinhood for historical data |
| News/sentiment (Phase 2) | Finnhub or Alpha Vantage news endpoint | Dedicated feed, not scraped |
| Persistence | PostgreSQL (trade history, proposals, decisions, audit log) | You'll want a full audit trail for every reasoning chain |

---

## 5. Build Phases

### Tool, Framework and Language for this system
- Backend: Python
- LLMs: OpenAI (ChatGPT, GPT-4), Gemini, Claude
- Agent Orchestration: CrewAI
- Frontend: React (for dashboard/override control plane) - use Next.js for server-side rendering and API routes and /mcp UI-UX Pro Max

### Phase 0 — Foundations (current)
- Finalize this architecture doc
- CrewAI 
- Set up Docker Compose skeleton with empty services + Redis + Postgres

### Phase 1 — Technical-only agents, backtested
- Build 2–3 member agents on **technical/price data only** (e.g., momentum, mean-reversion, MA crossover)
- Build the Manager's **hard-rules layer** first (before any LLM judgment)
- Backtest the full pipeline on historical data — no live connection yet
- Goal: prove the proposal → hard-rule-check → approval/rejection loop works end-to-end

### Phase 2 — Add Manager's soft judgment layer + paper trading
- Add LLM-based reasoning evaluation to the Manager
- Connect to Alpaca's paper trading sandbox (simulated money, live market data)
- Build the manual override control plane
- Run for a meaningful stretch (weeks, not days) before touching real capital

### Phase 3 — Add signal diversity
- Add a sentiment/news agent as one more voice in the mix
- Re-backtest / re-paper-trade to see if it improves or degrades performance
- This also tests whether the Manager's weighting logic is actually doing useful work

### Phase 4 — Real capital, stocks (small scale)
- Connect Robinhood Agentic Trading via MCP
- Start with a small, explicitly bounded capital allocation
- Trade preview/override active at all times
- Extended monitoring period before scaling capital up

### Phase 5 — Real capital, crypto
- Connect Robinhood Crypto Trading API
- Same conservative capital ramp-up approach

---

## 6. Open Design Questions (to resolve before Phase 1 build starts)

1. Framework choice: LangGraph vs CrewAI vs OpenAI Agents SDK — needs a short hands-on comparison.
2. Exact hard-rule parameters: what are your actual risk limits (max % per position, max daily loss, etc.)?
3. Capital allocation model: fixed budget per agent, or dynamic reallocation based on performance over time?
4. What happens to a rejected proposal — discarded, or does the member agent get to revise and resubmit?
5. How is "success" measured for each member agent (to eventually adjust its capital or retire it)?

---

## 7. Key Constraints (Non-Negotiable)

- No component ever bypasses the hard-rules layer, regardless of LLM confidence.
- No live trading until backtesting + paper trading both show acceptable behavior.
- Full audit log of every proposal, reasoning, decision, and override — nothing executes silently.
- Manual override / kill switch must be checked before every real order, not asynchronously.

---

## 8. Multi-Domain Org Architecture

This project is broadening from a single trading-swarm build into a **multi-domain agent org**. Everything in Sections 1–7 above remains exactly as designed — it becomes the detailed build plan for one plugin (Finance / Investment Banking) within a larger structure, not a rewrite.

**What a "plugin" means here:** a domain-scoped cluster consisting of:
- Its own **Manager Agent** (an approval gateway — reusing the two-layer hard-rules + soft-judgment pattern from Section 3.2 where it applies to that domain)
- Its own **Member Agents**, suited to that domain's work
- Access to whichever **connectors** are relevant to it (see Section 10)

Not every plugin necessarily needs the full hard-rules/soft-judgment gate — that pattern exists in Finance/Investment Banking specifically because it moves real capital. Whether Engineering or Design need an equivalent deterministic gate (vs. a lighter-weight manager) is an open question (Section 11), not decided here.

A top-level **Orchestrator** sits above all plugin Managers. It routes incoming work to the right plugin and handles cross-plugin coordination (e.g., a Design task that produces a diagram which Engineering then implements). The Orchestrator does not replace any plugin's own Manager — it is one layer above them.

---

## 9. Plugin Catalog

### 9.1 Finance / Investment Banking
This is Sections 1–7 of this document, in full — no re-derivation here. The Manager Agent is the "Manager Agent - CrewAI" box in `system.excalidraw`; the Member Agents are the ChatGPT / Gemini / Claude ellipses in that diagram, each intended to run a distinct strategy per Section 3.1 (Momentum / Mean-Reversion / Sentiment-style). The mapping between provider name (in the diagram) and strategy name (in this doc) is not yet stated explicitly anywhere — flagged in `memory.md`, not resolved here.

Finance and Investment Banking are treated as **one combined plugin** for now, per current scope. Splitting them into two separate plugins later is an open question (Section 11).

### 9.2 Engineering
Scope: the org doing engineering work on itself — infrastructure, CI, code quality, repo hygiene. Not yet detailed at the Member-Agent level (no build phases defined yet, unlike Finance/IB's Phases 0–5 in Section 5). Connector: Github.

Note: `Security-Agent/` and `Test-Agent/` at the repo root are *not* Member Agents of this plugin — they're engineering-support co-worker agents (code/security review, test-case authoring) that assist with building this project, sitting outside the org's own multi-agent architecture. See their own `CLAUDE.md` files.

### 9.3 Design
Scope: diagramming, UX, notes. Connectors: Excalidraw, Goodnotes.

---

## 10. Connector → Plugin Mapping

| Connector | Plugin(s) | Role |
|---|---|---|
| Robinhood | Finance / Investment Banking | Trade execution (equities via Agentic Trading MCP, crypto via Crypto Trading API) — matches Phases 4–5 |
| Github | Engineering | Code / repo / PR / issue work |
| Excalidraw | Design | Diagramming (`system.excalidraw` itself lives here) |
| Goodnotes | Design | Note-taking / handwritten notes |
| AgentMail | Cross-cutting (all plugins) | Notifications, reports, inter-agent or human communication — not owned by any single plugin |

---

## 11. Open Design Questions (Org-Level)

1. Does every plugin need the full two-layer hard-rules + soft-judgment Manager, or is that specific to Finance/IB's real-capital risk profile?
2. Should Investment Banking split out from Finance into its own plugin later, or stay merged as it is now?
3. What does a Member Agent look like in Engineering or Design, where there's no "capital" or "trade proposal" concept the way Finance/IB has?
4. Resolve the LLM-provider-vs-strategy naming mismatch on the Finance/IB ellipses in `system.excalidraw` (ChatGPT/Gemini/Claude vs. Momentum/Mean-Reversion/Sentiment) — either annotate the diagram with the strategy each provider runs, or state the mapping explicitly in Section 9.1.
