# PROJECT-TRADING-CHALLENGE.md — overview + rules

## What this is

Quy's paper-trading challenge: **Claude runs the trading desk**, Quy
observes. Claude researches, decides, executes on an Alpaca **paper**
account, logs everything in this repo, and surfaces it all through the
Quy Dashboard artifact and Telegram. No human approval is required per
trade — the transparency requirements below are the control.

## Roles

- **Claude (the agent)**: full control of the Alpaca paper account
  within `TRADING-STRATEGY.md` rules. Does research (web search +
  sub-agents), places/manages orders, maintains all logs, updates the
  dashboard, sends Telegram notifications.
- **Quy (the owner)**: watches via dashboard + Telegram, edits
  `TRADING-STRATEGY.md` whenever he wants (Claude follows the file as
  written each run), and owns the credentials.
- **Robinhood account**: linked read-only for display on the dashboard.
  Claude never places Robinhood orders.
- **Gemini**: not wired in yet. Research is done by Claude sub-agents.
  A `GEMINI_API_KEY` slot exists in `.env.example` for later.

## Operating rules

1. Paper trading only, on `paper-api.alpaca.markets`. Live trading is
   out of scope for this challenge, full stop.
2. Every position has a stop from the moment it exists.
3. Every action is logged in `TRADE-LOG.md` / `RESEARCH-LOG.md` and
   pushed to the repo the same run — nothing happens silently.
4. Strategy compliance: Claude trades only setups allowed by
   `TRADING-STRATEGY.md` as it exists at run time. Rule violations get
   confessed in the log and the weekly review, not hidden.
5. Secrets live in `.env` only. Anyone reading this repo sees the
   trades, never the keys.

## Cadence

Four automated runs, Mon–Fri (US Central): 6:00 pre-market research,
8:30 open execution, 12:00 midday scan, 3:00 daily summary. Details in
`AGENT-INSTRUCTIONS.md`.

## Success criteria (first review after 4 weeks)

- Process: zero unlogged trades, zero positions without stops, ≤2 rule
  violations total.
- Performance: positive expectancy (avg R across closed trades > 0)
  beats raw P&L — the point is to prove the process before sizing up.
