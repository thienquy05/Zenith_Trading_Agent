# AGENT-INSTRUCTIONS.md — start here

You are the trading agent for Quy's Alpaca paper-trading challenge. This
file is the complete operating manual: daily workflows, API reference,
gotchas, and strategy quick reference. Read the section for the workflow
you were woken up to run, do it, log it, update the dashboard, push.

## The four daily workflows (Mon–Fri, all times US Central)

Cron fires in UTC. CT = UTC-5 during daylight saving (Mar–Nov),
UTC-6 in winter. **When US DST ends/starts, the Routines' cron
expressions must be shifted by one hour** — see Gotchas.

### 6:00 AM CT — Pre-Market Research
Files needed: `TRADING-STRATEGY.md`, `RESEARCH-LOG.md` (append only).
1. `scripts/alpaca.sh account` and `scripts/alpaca.sh positions` — note
   equity, cash, open positions.
2. Web-search today's catalysts: earnings due today, economic data
   (CPI/PPI/FOMC/jobs), sector momentum, notable geopolitical events.
   Spawn an Explore/general sub-agent for the research sweep if it saves
   tokens over doing many searches inline.
3. Find 2–3 actionable trade ideas that fit `TRADING-STRATEGY.md`
   (gap setups preferred). For each: ticker, thesis, entry zone, stop,
   3R target, catalyst, risk.
4. Append findings to `RESEARCH-LOG.md` (template at top of that file).
5. Update dashboard, commit + push. **Silent on Telegram unless
   something urgent** (e.g., overnight position gapped past its stop).

### 8:30 AM CT — Market Open
Files needed: `TRADING-STRATEGY.md`, today's `RESEARCH-LOG.md` entry,
`TRADE-LOG.md` (append only).
1. `scripts/alpaca.sh clock` — confirm market is open (skip holidays).
2. `scripts/alpaca.sh positions` — re-check after open; handle anything
   that gapped through a stop.
3. Execute trades planned in this morning's research **if** price is
   still inside the entry zone and the setup is intact. Size per the
   strategy's 1%-risk rule.
4. Set a stop-loss order on every new position immediately
   (`scripts/alpaca.sh order` with a stop, or a separate stop order).
5. Log every fill in `TRADE-LOG.md`.
6. Update dashboard, commit + push. **Telegram Quy ONLY if a trade was
   placed** (ticker, side, qty, entry, stop, target, thesis in 2 lines).

### 12:00 PM CT — Midday Scan
Files needed: `TRADING-STRATEGY.md`, `TRADE-LOG.md` (append only).
1. `scripts/alpaca.sh positions` — check P&L and movement on each.
2. Adjust trailing stops upward on big winners (≥ +2R unrealized).
3. Sell anything that broke its thesis or is at/below **-7%**.
4. Quick web check for afternoon catalysts (Fed speakers, 1 PM ET
   auctions, earnings after close).
5. Log any actions in `TRADE-LOG.md`; update dashboard, commit + push.
   **Silent on Telegram unless action was taken.**

### 3:00 PM CT — Daily Summary (market close)
Files needed: `TRADE-LOG.md` (append only), `WEEKLY-REVIEW.md` (Fridays).
1. `scripts/alpaca.sh account` + `positions` + `orders` — end-of-day
   state.
2. Append the daily snapshot to `TRADE-LOG.md`: equity, day P&L ($ and
   %), open positions with unrealized P&L, trades made today, lessons.
3. On **Fridays**, also append the weekly review to `WEEKLY-REVIEW.md`.
4. Regenerate + republish the dashboard (see Dashboard procedure).
5. Commit + push.
6. **Telegram the daily summary** (always): equity, day P&L, positions
   held, trades made. Keep it under 10 lines.

## Alpaca API quick reference (paper)

All via `scripts/alpaca.sh` (loads `.env`; keys never appear on the
command line). Base: `https://paper-api.alpaca.markets/v2`, market data:
`https://data.alpaca.markets/v2`.

| Command | Does |
|---|---|
| `scripts/alpaca.sh account` | Equity, cash, buying power, day P&L |
| `scripts/alpaca.sh positions` | All open positions w/ unrealized P&L |
| `scripts/alpaca.sh orders [status]` | Orders (default `open`) |
| `scripts/alpaca.sh clock` | Market open/closed + next open/close |
| `scripts/alpaca.sh quote SYM` | Latest quote |
| `scripts/alpaca.sh bars SYM [timeframe] [limit]` | OHLCV bars (default 15Min x 40) |
| `scripts/alpaca.sh buy SYM QTY [limit_price]` | Market (or limit) buy, day TIF |
| `scripts/alpaca.sh sell SYM QTY [limit_price]` | Market (or limit) sell |
| `scripts/alpaca.sh bracket SYM QTY LIMIT STOP TARGET` | Buy w/ attached stop-loss + take-profit (preferred entry) |
| `scripts/alpaca.sh stop SYM QTY STOP_PRICE` | Standalone stop-loss sell |
| `scripts/alpaca.sh cancel ORDER_ID` | Cancel an order |
| `scripts/alpaca.sh raw METHOD /path ['json']` | Anything else |

Prefer `bracket` for entries — one call sets entry + stop + 3R target
and satisfies the "stop on every position" rule atomically.

## Telegram

`scripts/telegram.sh "message"` sends to Quy's chat
(`TELEGRAM_CHAT_ID` in `.env`). Markdown supported (`-m MarkdownV2` is
NOT used; plain text + simple `*bold*` HTML mode — see script). Policy:
- 8:30 run: only if a trade was placed.
- 12:00 run: only if action was taken.
- 3:00 run: always (daily summary).
- Any run: urgent risk events (halt, gap through stop, API failure that
  blocks risk management).

## Dashboard procedure (Quy Dashboard artifact)

`dashboard/quy-dashboard.html` is the artifact source. Artifacts cannot
fetch live data, so every workflow run regenerates it:
1. Collect fresh JSON: Alpaca account/positions/orders, Robinhood
   portfolio + equity positions (READ-ONLY, via the Robinhood MCP
   connector), latest TRADE-LOG / RESEARCH-LOG entries.
2. Rewrite the `const DATA = {...}` block near the top of the HTML with
   the fresh data + `lastUpdated` ISO timestamp. Don't touch the rest.
3. Publish with the Artifact tool — favicon `📈`, and **always pass the
   artifact's URL** so it updates in place instead of minting a new one:
   `https://claude.ai/code/artifact/6f2a645b-ee8e-448d-a6ba-7f2185ddd5ab`

## Gotchas

- **Credentials in cron sessions**: fresh sessions have no `.env` (it's
  gitignored). The scripts fall back to plain environment variables —
  `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `TELEGRAM_BOT_TOKEN`,
  `TELEGRAM_CHAT_ID` must be set in the Claude Code environment
  configuration. If they're missing, say so in the log and skip trading
  (never guess credentials).
- **Working branch**: until this setup merges to `master`, cron sessions
  must `git fetch origin claude/alpaca-paper-trading-setup-visljt &&
  git checkout claude/alpaca-paper-trading-setup-visljt` first (a fresh
  clone starts on `master`, which may not have these files). Skip this
  once `AGENT-INSTRUCTIONS.md` exists on `master`.
- **Sessions are ephemeral.** Anything not committed + pushed is lost
  when the container is reclaimed. Every workflow ends with a push to
  the working branch.
- **Cron is UTC, schedule is CT.** Current Routines assume CDT (UTC-5).
  In early November (DST ends) shift all four cron expressions +1 hour;
  reverse in March. The Daily Summary run nearest the change should
  flag it via Telegram.
- **Market holidays**: `scripts/alpaca.sh clock` says if the market is
  open — check it before trading; research runs can proceed anyway.
- **Wash-trade rejections**: Alpaca rejects an order that would
  immediately cross your own opposite-side open order — cancel the old
  stop before selling manually.
- **Fractional + bracket don't mix**: bracket orders need whole shares.
- **`orders` defaults to open only** — pass `all` to see fills.
- **Data plan limits**: free Alpaca data is IEX-only, 15-min-delayed
  SIP quotes; fine for this strategy's timescale. Don't hammer bars —
  one call per symbol per run.
- **Telegram 4096-char limit** per message; script truncates.
- **Token frugality** (see CLAUDE.md): append to logs, don't rewrite;
  keep sub-agent research prompts tight; one commit per run.

## Strategy quick reference

Full rules in `TRADING-STRATEGY.md`. TL;DR: 3R/1R gap strategy —
find the gap zone (midpoint of the lowest bar up to the first
increasing/bullish bar), enter on retest, stop 1R below the gap low,
target +3R. Risk ≤1% of equity per trade, max 4 concurrent positions,
hard -7% bail, stops on everything, trail winners past +2R.
