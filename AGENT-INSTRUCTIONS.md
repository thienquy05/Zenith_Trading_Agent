# AGENT-INSTRUCTIONS.md — start here

You are the trading agent for Quy's Alpaca paper-trading challenge. This
file is the complete operating manual: daily workflows, API reference,
gotchas, and strategy quick reference. Read the section for the workflow
you were woken up to run, do it, log it, update the dashboard locally,
push the logs.

## The five daily workflows (Mon–Fri, all times US Eastern / EDT)

Cron fires in UTC. ET = UTC-4 during daylight saving (EDT, Mar–Nov),
UTC-5 in winter (EST). **When US DST ends/starts, the Routines' cron
expressions must be shifted by one hour** — see Gotchas.

| ET time | Workflow | Telegram |
|---|---|---|
| 5:00 AM | Morning Brief (Quy's real portfolio) | NONE — email only (AgentMail), see below |
| 7:00 AM | Pre-Market Research | ALWAYS — detailed market brief |
| 9:30 AM | Market Open | ALWAYS — open report (+ trades if placed) |
| 10:30a–2:30p hourly | TJL Watch | ONLY if a trade was placed |
| 1:00 PM | Midday Scan | ALWAYS — midday update |
| 4:00 PM | Daily Summary | ALWAYS — daily summary |

### 5:00 AM ET — Morning Brief (Quy's real portfolio, via Email)

Purpose: Quy's personal investing brief — his REAL Robinhood money, not
the paper account. Educational tone, beginner level, honest signals.

1. Pull LIVE Robinhood data (READ-ONLY, via the Robinhood MCP
   connector) — never reuse yesterday's numbers, holdings change:
   - `get_equity_positions` for all three accounts (see Robinhood
     reference below) and `get_portfolio` for the Agentic account
     (crypto value + pending deposits).
   - `get_equity_quotes` for every held symbol + VOO/QQQ/SCHD/VTI.
   - VOO signal inputs per `TRADING-STRATEGY.md` §5 (RSI(14), 50/200-day
     MA from `get_equity_historicals`, ≤10 symbols/call, extract
     `close_price` via `jq`).
2. Web-search (keep it tight): VIX level, S&P 500 / futures tone,
   BTC-ETH-SOL prices + Crypto Fear & Greed index, Fed/rates headline,
   any geopolitical or crypto-regulation driver.
3. **Email the brief (ALWAYS — no Telegram send for this workflow, Quy's
   standing preference 2026-07-10)** via AgentMail (`AGENTMAIL_API_KEY` /
   `AGENTMAIL_INBOX=zenith-alert@agentmail.to`, see Gotchas) to
   `REPORT_EMAIL_TO`/Quy's Gmail. No 4096-char limit, so send one clean
   HTML/plain-text email covering:
   - **Market mood**: VIX + one-line tone; futures direction.
   - **Your portfolio (real numbers)**: each account, each position —
     symbol, qty, avg cost, live price, $ value, $ / % P&L. Crypto:
     live `crypto_value` vs $30 basis, per-coin estimate via the
     $18/$8/$4 cost-basis split (flag it as an estimate — the connector
     has no per-coin quantity lookup). Note pending deposits.
   - **Extra-watch names (BTC, ETH, SOL, NVDA, ORCL)**: one line each —
     live price, 24h/day move, any news that matters.
   - **VOO signal** (§5 zones) + whether the Roth DCA autopilot is
     enough or a dip merits an extra contribution.
   - **Today's calendar**: earnings/data with exact ET times.
   - **Beginner tip**: 2–3 sentences tied to today's actual data.
   If AgentMail fails, fall back to a Gmail DRAFT via the connector and
   flag the failure in the next Telegram-bearing run (7:00 AM).
4. No repo commit needed unless something was logged; no trading — this
   run never places orders anywhere.

### 7:00 AM ET — Pre-Market Research (analyst pipeline, 2026-07-09)

Files needed: `TRADING-STRATEGY.md`, `PROMPT-PREMARKET.md`,
`REPORT_TEMPLATE.md`, `RESEARCH-LOG.md` (append only). Rules reference:
`WATCHLIST_CRITERIA.md`.

1. `scripts/alpaca.sh account` and `scripts/alpaca.sh positions` — note
   equity, cash, open positions.
2. Run `.venv/bin/python scripts/scan_premarket.py` (create the venv
   first if missing — see Gotchas). One run gathers: market snapshot
   (indices/VIX/rates/oil/DXY), premarket gappers with REAL premarket
   gap/volume/RVOL from Alpaca, live levels (VWAP/PMH/HOD/LOD),
   catalyst headlines with `catalyst_found` flags, market-wide RSS
   news, the US high-impact econ calendar (today + tomorrow, ET), and
   the deterministic `day_eligible`/`swing_eligible` flags encoding
   `WATCHLIST_CRITERIA.md`. Output: `scans/packet_<date>.json`.
3. **Fill the packet's gaps** (only what the packet could not get —
   check its `gaps_to_fill` and error fields before searching):
   a. If `market_snapshot` errored (yfinance blocked): pull index/VIX
      tone via Robinhood `get_index_quotes` or one tight web search.
   b. If `econ_calendar` errored: one web search for today's US macro
      calendar with ET times. Mark tier-1 events (§3b blackouts).
   c. **Earnings**: who reports today/this week beyond the per-gapper
      `next_earnings` dates; flag names within 24h (§3b no-entry).
   d. **Crypto regime + tape**: run `python3 scripts/scan_crypto.py
      --no-telegram` (§2c sleeve). Regime state + BTC/ETH/SOL moves go
      in the brief. On a PASS inside sleeve rules: `cbuy` then `cstop`
      immediately, log in `TRADE-LOG.md`.
   e. **Held-names sweep (extra watch)**: news on BTC, ETH, SOL, NVDA,
      ORCL — Quy holds these for real; anything material gets a callout.
   f. **Verification rule**: any packet headline that will drive a
      trade idea needs a second independent source or a primary source
      before the 9:30 run acts on it. Date-check — stale news reposted
      premarket is a classic trap.
4. **Analyst pass**: write `reports/premarket_<date>.md` following
   `PROMPT-PREMARKET.md` + `REPORT_TEMPLATE.md` (rules decide watchlist
   membership via the packet flags; judgment scores conviction
   🟢🟡🔴). Then distill 2–3 actionable trade ideas that fit
   `TRADING-STRATEGY.md` for the day list: ticker, thesis, catalyst
   (+source), entry zone, stop, 3R target, 1%-risk size, invalidation,
   §3b guardrails. **"No trade today" is a valid, logged outcome.**
5. Append findings to `RESEARCH-LOG.md` (template at top of that file).
   Write the day-list tickers to `scans/watchlist_<date>.json` —
   `{"date": "YYYY-MM-DD", "symbols": [...], "source": "premarket research"}`
   — this is what `scan_tjl.py`/`backtest_tjl.py` check all day (see
   Scanners section; there is no fixed ticker universe anymore).
6. Republish the dashboard locally (gitignored, not committed) —
   include `DATA.premarketReport` (report summary + watchlists);
   commit + push the packet, report, watchlist, and logs.
7. **Telegram the pre-market brief (ALWAYS)** — the condensed report,
   split into 2 messages if needed: gappers (format A), macro calendar
   with ET times, market tone, crypto regime + BTC/ETH/SOL, extra-watch
   callouts, day/swing watchlists with conviction, the day's trade
   ideas (or "no qualifying setups — standing aside" and why), and any
   §3b blackout windows in effect today. The report is the archive; the
   brief is the ping.

### 9:30 AM ET — Market Open

Files needed: `TRADING-STRATEGY.md`, today's `RESEARCH-LOG.md` entry,
`TRADE-LOG.md` (append only).

1. `scripts/alpaca.sh clock` — confirm market is open (skip holidays).
2. `scripts/alpaca.sh positions` — re-check after open; handle anything
   that gapped through a stop.
3. **Guardrail pre-check (§3b)**: daily/weekly circuit breaker status,
   event blackout windows, per-name earnings distance — confirm each
   planned trade still clears them.
4. Execute trades planned in this morning's research **if** price is
   still inside the entry zone and the setup is intact. Size per the
   strategy's 1%-risk rule.
5. Set a stop-loss order on every new position immediately
   (`scripts/alpaca.sh order` with a stop, or a separate stop order).
6. Log every fill in `TRADE-LOG.md`.
7. Republish the dashboard locally; commit + push the logs.
8. **Telegram the open report (ALWAYS)**: trades placed (ticker, side,
   qty, entry, stop, target, thesis in 2 lines) — or "no entries: <one
   line why>" — plus how the open is treating the watchlist and any
   overnight position news.

### 1:00 PM ET — Midday Scan

Files needed: `TRADING-STRATEGY.md`, `TRADE-LOG.md` (append only).

1. `scripts/alpaca.sh positions` — check P&L and movement on each.
2. Adjust trailing stops upward on big winners (≥ +2R unrealized).
3. Sell anything that broke its thesis or is at/below **-7%**.
4. Run `python3 scripts/scan_tjl.py --no-telegram` (TJL entry check).
   A PASS inside strategy rules may be traded: bracket order, 1%-risk
   sizing, stop = signal bar low, 3R target.
5. Quick web check for afternoon catalysts (Fed speakers, 1 PM ET
   auctions, 2 PM FOMC releases, earnings after close) + a one-line
   look at the extra-watch names (BTC, ETH, SOL, NVDA, ORCL).
6. Run `python3 scripts/scan_crypto.py --no-telegram` (crypto sleeve,
   §2c) — same handling as the morning run; crypto positions also get
   the -7% and thesis checks in steps 2–3.
7. Log any actions in `TRADE-LOG.md`; republish the dashboard locally,
   commit + push the logs.
8. **Telegram the midday update (ALWAYS)**: each open position with
   unrealized P&L and stop location, actions taken (or none), market
   tone since the open, afternoon catalysts with ET times, extra-watch
   one-liners.

### Hourly — TJL Watch (10:30 AM–2:30 PM ET, at :30 past)

Files needed: `TRADING-STRATEGY.md` §2b only.

1. Run `python3 scripts/scan_tjl.py --no-telegram`. It saves the JSON.
2. On a PASS that fits strategy rules (max positions, 1% risk, max 2 new
   positions/day, §3b guardrails), place the bracket order and log it
   in `TRADE-LOG.md`.
3. Commit the scan JSON (+ any trade log changes). Republish the
   dashboard locally **only if the hit set changed** — keep these runs
   cheap.
4. **Telegram ONLY if a trade was placed** (or a position needed
   emergency action). Quiet runs stay quiet — Quy's explicit
   preference (2026-07-08). Exception: urgent risk events, always.

### 4:00 PM ET — Daily Summary (market close)

Files needed: `TRADE-LOG.md` (append only), `WEEKLY-REVIEW.md` (Fridays).

1. `scripts/alpaca.sh account` + `positions` + `orders` — end-of-day
   state.
2. Append the daily snapshot to `TRADE-LOG.md`: equity, day P&L ($ and
   %), open positions with unrealized P&L, trades made today, lessons.
3. On **Fridays**, also append the weekly review to `WEEKLY-REVIEW.md`.
4. Pull LIVE Robinhood data for the extra-watch names (real numbers —
   positions + quotes, never cached) for the dashboard and the summary.
5. Regenerate + republish the dashboard locally (see Dashboard
   procedure) — gitignored, not committed.
6. Commit + push the logs.
7. **Telegram the daily summary (ALWAYS)**: paper account (equity, day
   P&L $ and %, open positions with uP&L, trades made + why), guardrail
   status (breakers hit? violations? — confess honestly), Quy's real
   holdings one-liners (BTC/ETH/SOL/NVDA/ORCL live values + day move),
   tomorrow's calendar highlights, one lesson from today. Split into 2
   messages if needed — detail beats brevity here (Quy's preference,
   2026-07-08).

## Robinhood reference (READ-ONLY — never place Robinhood orders)

Quy's real accounts, via the Robinhood MCP connector. **Always pull
live** — never hardcode or reuse values; he adds money and positions.

| Account | Number | Holds (as of 2026-07-08 — verify live each run) |
|---|---|---|
| Individual | 556092849 | ORCL (~$100 invested) |
| Roth IRA | 829651439 | VOO (DCA core holding) |
| "Agentic" cash | 539785238 | NVDA (~$70 invested), TSLA (dust), crypto BTC/ETH/SOL (~$30 basis, $18/$8/$4 split) |

- **Extra-watch list: BTC, ETH, SOL, NVDA, ORCL** — Quy's standing
  request (2026-07-08): every Telegram brief carries live prices and
  day moves for these, and any material news gets flagged same-run.
- Per-coin crypto quantities aren't exposed by the connector: estimate
  by applying the $18/$8/$4 basis split to the live `crypto_value` from
  `get_portfolio`, and say it's an estimate.
- Watch for NEW positions/deposits on every pull and fold them into the
  briefs automatically (e.g. TSLA appeared 2026-07-08).

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

## Scanners (`scripts/`, python3 stdlib, read `.env` or env vars)

| Script | What / when |
|---|---|
| `scan_premarket.py [--no-alpaca]` | **The 7:00 AM packet builder** (needs `.venv` — see Gotchas). Hybrid: Alpaca screener candidates with real premarket gap/volume/RVOL + live levels; yfinance market snapshot, market caps, earnings dates (and keyless fallback candidates); RSS market news; ForexFactory US high-impact econ calendar (cached ~4h). Stamps `day_eligible`/`swing_eligible` per `WATCHLIST_CRITERIA.md`. Data only, zero analysis. Saves `scans/packet_<date>.json`. |
| `scan_gappers.py [--no-telegram]` | LEGACY backup (superseded by `scan_premarket.py` in the daily workflow, kept because it runs on stdlib+Alpaca alone): screener ∪ most-actives → real premarket gap% + volume filters (>5%, >$3, >50k) → top 10 with Benzinga headlines. Saves `scans/premarket_gappers_<date>.json`. |
| `scan_tjl.py [--force] [--no-telegram] [TICKERS…]` | Trend Join Long entry check. Universe: explicit args override, else `scans/watchlist_<date>.json` (today's research picks), else latest gappers scan top-10, else exits cleanly with "no candidates." Time-gated 10:00–15:30 ET (`--force` bypass for testing). Saves `scans/tjl_watchlist_<date>_<HHMM>ET.json`. **Run with `--no-telegram`** — since 2026-07-08 the agent owns all Telegram sends (trade-only policy for TJL runs). |
| `backtest_tjl.py [--tickers A,B,C] [--months N]` | TJL backtest on 5-min bars; same universe resolution as `scan_tjl.py` (selection-bias caveat in its header). On demand only. |
| `scan_crypto.py [--no-telegram] [PAIRS…]` | C-TJL crypto sleeve check (strategy §2c). Checks the BTC>daily-SMA200 regime gate FIRST — in a bear regime it stands down without scanning. Universe: fixed liquid majors in `backtest_crypto.py`. Run with `--no-telegram` in the 7:00 AM and 1:00 PM workflows (regime state goes into the agent's own brief). Saves `scans/crypto_tjl_<date>_<HHMM>UTC.json`. |
| `backtest_crypto.py [--tickers A,B] [--months N] [--grid]` | C-TJL backtest on daily crypto bars incl. regime gate + fee/slippage haircut (4H variants failed validation — see §2c). On demand; re-run monthly to confirm the sleeve's edge still holds. |

**No fixed ticker universe.** Neither scanner defaults to a hardcoded
list (e.g. AMD/NVDA/MU) — that was a bug in the original build. The
universe is always today's watchlist or the gappers scan, so it moves
with what's actually happening in the market. Pass explicit tickers
only for manual testing.

Agent duties around the scripts:
- **Catalyst rewrite**: `catalyst` in the gappers JSON is just the top
  headline. Rewrite each into a one-sentence summary before it goes to
  Telegram (format A: `📊 *Premarket Gappers* — date` then one
  `• SYM $px +x% — catalyst` bullet each, omit the dash when null) or
  the dashboard.
- Commit every scan JSON — they're the desk's memory (fresh cron
  containers keep nothing else).
- Dashboard `DATA.scanners` gets the latest gappers, TJL result, and
  backtest stats on every update.
- IEX-feed volumes undercount the consolidated tape; treat premarket
  volume as a floor, not truth.

## Telegram policy (Quy's standing preference, 2026-07-08)

`scripts/telegram.sh "message"` sends to Quy's chat
(`TELEGRAM_CHAT_ID` in `.env`). Markdown supported (`-m MarkdownV2` is
NOT used; plain text + simple `*bold*` HTML mode — see script).

**Quy wants ALL updates through Telegram, with as much market detail as
fits.** Concretely:
- 5:00 AM Morning Brief: **NONE — email only** (AgentMail to Quy's
  Gmail; Quy's standing preference, 2026-07-10, revised from the prior
  Telegram-always rule). See the 5:00 AM workflow section for the
  AgentMail inbox and fallback.
- 7:00 AM Pre-Market: ALWAYS — full research brief.
- 9:30 AM Open: ALWAYS — trades or "no entries + why".
- Hourly TJL: **only if a trade was placed** (Quy chose this to avoid
  5 no-op pings/day).
- 1:00 PM Midday: ALWAYS — positions, actions, afternoon catalysts.
- 4:00 PM Summary: ALWAYS — full daily wrap.
- Any run: urgent risk events (halt, gap through stop, breaker
  tripped, API failure that blocks risk management) — immediately.
- Every scheduled message includes the extra-watch one-liners
  (BTC, ETH, SOL, NVDA, ORCL — live numbers).
- 4096-char limit per message: split long briefs into numbered parts
  (1/2, 2/2) rather than truncating detail.

## Dashboard procedure (Quy Dashboard artifact)

`dashboard/quy-dashboard.html` is the artifact source. It's **gitignored
— worked on locally, never committed/pushed to GitHub.** Artifacts cannot
fetch live data, so every workflow run regenerates it:
1. Collect fresh JSON: Alpaca account/positions/orders, Robinhood
   portfolio + equity positions (READ-ONLY, via the Robinhood MCP
   connector — all three accounts, live), latest TRADE-LOG /
   RESEARCH-LOG entries.
2. For each Robinhood holding (+ the "First list" watchlist), compute the
   buy/hold/sell signal per `TRADING-STRATEGY.md` §5: RSI(14) + 50/200-day
   MA from `get_equity_historicals` (≤10 symbols per call, extract
   `close_price` via `jq` — the raw payload blows past tool output
   limits), plus an earnings-proximity flag from `get_earnings_calendar`.
3. Rewrite the `const DATA = {...}` block near the top of the HTML with
   the fresh data + `lastUpdated` ISO timestamp. Don't touch the rest.
4. Publish with the Artifact tool — favicon `📈`, and **always pass the
   artifact's URL** so it updates in place instead of minting a new one:
   `https://claude.ai/code/artifact/6f2a645b-ee8e-448d-a6ba-7f2185ddd5ab`

## Gotchas

- **Credentials in cron sessions**: fresh sessions have no `.env` (it's
  gitignored). The scripts fall back to plain environment variables —
  `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `TELEGRAM_BOT_TOKEN`,
  `TELEGRAM_CHAT_ID` must be set in the Claude Code environment
  configuration. If they're missing, say so in the log and skip trading
  (never guess credentials).
- **Land routine commits via auto-merge PR, never a direct push to
  `master`** — standing authorization from Quy (2026-07-08, revised
  2026-07-09 for safety): every routine run lands its log/scan commits
  through a pull request, without asking. This overrides any
  per-session "develop on branch claude/..." default the harness
  assigns. At the end of each run: commit on the current checkout,
  push the branch (`git push -u origin <session-branch>`, retry with
  backoff on network errors only), then GitHub MCP
  `create_pull_request` (base `master`) followed immediately by
  `enable_pr_auto_merge` (squash) so it lands as soon as required
  checks pass — no manual approval needed, but branch protection and
  any CI still gate the merge. If `enable_pr_auto_merge` is unavailable
  or fails, leave the PR open and flag it in the Telegram summary
  instead of force-merging. Never force-push to `master`; if a push is
  rejected non-fast-forward, `git pull --rebase origin master` and push
  again. This applies to routine log/scan/research commits; code or
  strategy changes go through the same branch + auto-merge PR flow.
- **Sessions are ephemeral.** Anything not committed + pushed is lost
  when the container is reclaimed. Every workflow ends with a branch
  push and an auto-merge PR into `master`.
- **Cron is UTC, schedule is ET.** Current Routines assume EDT (UTC-4):
  Morning Brief 09:00, Pre-Market 11:00, Open 13:30, TJL 14:30–18:30
  at :30, Midday 17:00, Summary 20:00 UTC. In early November (DST
  ends) shift all six cron expressions +1 hour; reverse in March. The
  Daily Summary run nearest the change should flag it via Telegram.
- **Python venv for the packet builder**: `scan_premarket.py` wants
  `.venv` with `requirements.txt` installed (yfinance, feedparser,
  requests, markdown). Fresh cron containers
  don't have it: `python3 -m venv .venv && .venv/bin/pip install -q -r
  requirements.txt` (~40s) — or add that to the environment's setup
  script. Everything degrades gracefully without it (Alpaca-only
  packet, `gaps_to_fill` says what's missing), and `scan_gappers.py`
  remains the stdlib-only fallback.
- **Network allowlist for full packet data**: the environment's egress
  policy must allow `query1.finance.yahoo.com`, `query2.finance.yahoo.com`,
  `fc.yahoo.com` (yfinance), `nfs.faireconomy.media` (econ calendar),
  `feeds.content.dowjones.io`, `www.cnbc.com`, `news.google.com`,
  `finance.yahoo.com` (RSS), and `api.agentmail.to` (5:00 AM Morning
  Brief email). Verified 2026-07-09: with these blocked the scan still
  completes but the snapshot/market-caps/econ-calendar come back empty
  — the workflow's step-3 fallbacks (Robinhood index quotes, one web
  search) cover it.
- **ForexFactory calendar rate limit**: the feed 429s on rapid calls;
  `scan_premarket.py` caches it in `scans/.ff_calendar_cache.json`
  (gitignored) with a ~4h TTL and falls back to the stale cache on
  fetch failure. Don't fetch it manually in the same session.
- **AgentMail**: the 5:00 AM Morning Brief emails via AgentMail
  (`AGENTMAIL_API_KEY` + `AGENTMAIL_INBOX` from agentmail.to). Working
  inbox: `zenith-alert@agentmail.to` (verified live 2026-07-10 — the
  earlier `stock-alert@agentmail.to` value was never provisioned and
  every send 404'd; set as a project-level `env` default in
  `.claude/settings.json` so fresh sessions pick it up automatically).
  If AgentMail fails, fall back to a Gmail DRAFT via the connector (it
  cannot send) and flag it in the next Telegram-bearing run. The 7:00
  AM Pre-Market report is Telegram-only (Quy's standing preference,
  2026-07-10) — no email send for that workflow.
- **Market holidays**: `scripts/alpaca.sh clock` says if the market is
  open — check it before trading; research runs can proceed anyway.
- **Wash-trade rejections**: Alpaca rejects an order that would
  immediately cross your own opposite-side open order — cancel the old
  stop before selling manually.
- **Fractional + bracket don't mix**: bracket orders need whole shares.
- **Crypto has NO bracket orders** (market/limit/stop_limit only, TIF
  gtc/ioc, long only, no shorting). Entry and stop are TWO calls: `cbuy`
  then `cstop` immediately — never leave a crypto position without its
  stop_limit. A stop_limit can miss in a flash crash; the -7% hard-bail
  check at every wake-up is the backstop. Crypto data uses the v1beta3
  endpoints (`cquote`/`cbars`) — the stock ones 404 on `BTC/USD`.
  Order notional must be **≥ $10** (403 `cost basis must be >= minimal
  amount of order 10` otherwise). Verified on paper 2026-07-08: plain
  limit GTC accepted, `order_class: bracket` rejected with 422
  `crypto orders not allowed for advanced order_class: otoco`.
- **`orders` defaults to open only** — pass `all` to see fills.
- **Data plan limits**: free Alpaca data is IEX-only, 15-min-delayed
  SIP quotes; fine for this strategy's timescale. Don't hammer bars —
  one call per symbol per run.
- **Telegram 4096-char limit** per message; script truncates — split
  long briefs into parts instead.
- **Token frugality** (see CLAUDE.md): append to logs, don't rewrite;
  keep sub-agent research prompts tight; one commit per run. Detailed
  Telegram briefs are IN scope (Quy asked for them) — save tokens on
  file reads and tool calls, not on the briefs.

## Strategy quick reference

Full rules in `TRADING-STRATEGY.md`. TL;DR: 3R/1R gap strategy —
find the gap zone (midpoint of the lowest bar up to the first
increasing/bullish bar), enter on retest, stop 1R below the gap low,
target +3R. Risk ≤1% of equity per trade, max 4 concurrent positions,
hard -7% bail, stops on everything, trail winners past +2R.
**Guardrails (§3b): -2% day / -4% week circuit breakers, max 5 new
entries per week (equities + crypto combined, resets Monday — count
this week's entries in TRADE-LOG.md first), tier-1 event blackouts,
24h earnings no-entry, sector cap 2, no averaging down, stop after 2
consecutive same-day stop-outs.** Guardrails protect capital;
the edge comes from the process — never skip one to chase a setup.
