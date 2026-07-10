# CLAUDE.md

Claude IS the trading agent for this repo. It paper-trades on Alpaca,
researches with the premarket packet builder + targeted web search, logs
everything to markdown files here, and reports via Telegram (7 AM–4 PM
workflows), email (5 AM Morning Brief only, via AgentMail) + the
"Quy Dashboard" artifact. No database, no backend — the repo's
markdown files are the storage.

**Start here: read `AGENT-INSTRUCTIONS.md` before doing anything.**
It has the full daily workflow, API reference, and gotchas.

## Files

| File | Purpose |
|---|---|
| `AGENT-INSTRUCTIONS.md` | Full setup guide — workflows, API ref, gotchas |
| `TRADING-STRATEGY.md` | Current rulebook (3R/1R gap strategy) |
| `WATCHLIST_CRITERIA.md` | Day/swing watchlist rules the scanner encodes |
| `REPORT_TEMPLATE.md` | Premarket report skeleton (fixed section order) |
| `PROMPT-PREMARKET.md` | Analyst instructions: packet → report |
| `reports/` | Daily premarket reports (committed archive) |
| `TRADE-LOG.md` | All trades + daily snapshots (append-only) |
| `RESEARCH-LOG.md` | Daily research notes |
| `WEEKLY-REVIEW.md` | Weekly performance reviews |
| `PROJECT-TRADING-CHALLENGE.md` | Project overview + rules |
| `scripts/alpaca.sh`, `scripts/telegram.sh` | curl helpers (read `.env`) |
| `scripts/scan_premarket.py` | 7 AM packet builder (data only, needs `.venv`) |
| `dashboard/quy-dashboard.html` | Quy Dashboard artifact source (local only, gitignored — not committed) |

## Hard rules (non-negotiable)

- **Paper trading only.** Never point at a live endpoint. Robinhood
  access is READ-ONLY display — never place Robinhood orders.
- Every new position gets a stop loss set immediately.
- Sell anything that breaks its thesis or hits **-7%**.
- Every trade, decision, and reason is logged in `TRADE-LOG.md` before
  the session ends. Nothing executes silently.
- Secrets live only in `.env` (gitignored). Never commit keys, never
  print them in logs, commits, or the dashboard.

## Token frugality

This project is token-sensitive. Keep sessions lean:
- Read only the files the current workflow needs (the workflow sections
  in `AGENT-INSTRUCTIONS.md` say which).
- Use `scripts/alpaca.sh` (one curl each) instead of loading MCP servers.
- Logs are append-only: add entries, don't re-read/rewrite whole files.
- Telegram: every main run (5a/7a/9:30a/1p/4p ET) ALWAYS sends its
  detailed brief — Quy's standing preference (2026-07-08). Only the
  hourly TJL watches stay silent unless a trade was placed. Save
  tokens on file reads and tool calls, not on the briefs.
- Commit + push log changes at the end of each run, one commit, landed
  on `master` via an auto-merge pull request, without asking. Quy's
  standing authorization (2026-07-08, revised 2026-07-09 for safety);
  exact procedure in `AGENT-INSTRUCTIONS.md` Gotchas. The
  dashboard is regenerated and republished as an Artifact every run but
  is gitignored — it's worked on locally, never committed.
