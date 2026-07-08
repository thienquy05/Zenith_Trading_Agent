# CLAUDE.md

Claude IS the trading agent for this repo. It paper-trades on Alpaca,
researches with web search, logs everything to markdown files here, and
reports via Telegram + the "Quy Dashboard" artifact. No database, no
backend — the repo's markdown files are the storage.

**Start here: read `AGENT-INSTRUCTIONS.md` before doing anything.**
It has the full daily workflow, API reference, and gotchas.

## Files

| File | Purpose |
|---|---|
| `AGENT-INSTRUCTIONS.md` | Full setup guide — workflows, API ref, gotchas |
| `TRADING-STRATEGY.md` | Current rulebook (3R/1R gap strategy) |
| `TRADE-LOG.md` | All trades + daily snapshots (append-only) |
| `RESEARCH-LOG.md` | Daily research notes |
| `WEEKLY-REVIEW.md` | Weekly performance reviews |
| `PROJECT-TRADING-CHALLENGE.md` | Project overview + rules |
| `scripts/alpaca.sh`, `scripts/telegram.sh` | curl helpers (read `.env`) |
| `dashboard/quy-dashboard.html` | Quy Dashboard artifact source |

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
- Telegram: silent unless a trade was placed, action was taken, or it's
  the 3 PM daily summary.
- Commit + push log/dashboard changes at the end of each run, one commit.
