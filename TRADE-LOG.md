# TRADE-LOG.md — all trades + daily snapshots (append-only)

Append entries at the BOTTOM. Never edit past entries; corrections get
a new dated line.

## Templates

### Trade entry
```
### YYYY-MM-DD HH:MM ET — BUY|SELL TICKER
- Qty / entry / stop / target: N @ $X.XX | stop $X.XX | target $X.XX (3R)
- Risk: $XX (X.X% of equity) | 1R = $X.XX/share
- Setup: gap-retest | other (explain)
- Thesis: one or two lines
- Order id(s): ...
```

### Exit
```
### YYYY-MM-DD HH:MM ET — EXIT TICKER
- Qty @ $X.XX | P&L: $XX (+X.XR) | reason: target | stop | thesis-break | -7% | trail
- Lesson (if any):
```

### Daily snapshot (4 PM ET run)
```
### YYYY-MM-DD — daily snapshot
- Equity $X | day P&L $X (X.X%) | cash $X
- Open: TICKER n@x (uP&L $x), ...
- Trades today: n | notes:
```

---

## Phase 2 — Alpaca paper account (active)

*(no trades yet — account initialized 2026-07-08)*

### 2026-07-08 08:30 CT — market open check
- Market open confirmed (`clock`), equity $100,000 | cash $100,000 |
  open positions: none.
- No trades executed: pre-market research found no ideas meeting the
  §4 filter (gap setup + defined risk) — session was catalyst-light
  (empty gappers scan) and no watchlist entries qualified. Watching the
  memory/semi complex (MU, STX, KLAC, LRCX, TER) for a TJL breakout
  intraday; FOMC minutes at 2 PM ET is the main event risk.

### 2026-07-08 10:47 CT — BUY AAPL
- Qty / entry / stop / target: 1 @ $310.47 | stop $300.00 | target $325.00
- Risk: $10.47 (~0.01% of equity) | 1R = $10.47/share
- Setup: system test — verifying Alpaca bracket-order pipeline end-to-end (entry + stop + target fill correctly), not a TRADING-STRATEGY.md signal
- Thesis: n/a (infrastructure/performance verification trade, minimal size to limit exposure)
- Order id(s): 41f3b9cd-3267-4f71-8ad6-87aebd48048e (entry, filled), bc06d1fb-70f8-47de-bbbc-f8d1c066d3b6 (stop, held), d1cfa077-a671-495e-92c9-1f162bc269e2 (target, held)

### 2026-07-08 — account verification snapshot
- Equity $100,000 | day P&L ~$0 (0.0%) | cash $99,689.53
- Open: AAPL 1@$310.47 (uP&L -$0.06)
- Trades today: 1 | notes: account created 2026-07-07, no prior trades; this session confirmed clock/account/positions endpoints working and placed a 1-share bracket test trade to verify end-to-end order execution + stop-loss attachment. No strategy signal — pure system check.

### 2026-07-08 — daily snapshot (4:00 PM ET run)
- Equity $100,002.87 | day P&L +$2.87 (+0.00%) | cash $99,689.53
- Open: AAPL 1@$310.47, current $313.34 (uP&L +$2.87 / +0.92%)
- Trades today: 1 total (AAPL bracket test buy, already logged above; no new fills since) | notes:
  - **Guardrail confession — stop-loss gap**: AAPL's bracket order used
    day-TIF stop ($300) and target ($325) legs. Both expired/canceled
    at today's 20:00 UTC market close (confirmed via `orders all`),
    leaving the AAPL position with **no active protective stop
    overnight**. Day-TIF brackets don't carry into the next session.
    Action needed: re-attach a stop for AAPL at tomorrow's 9:30 AM
    open workflow before anything else, and prefer GTC stops (or
    re-arm daily) for any position intended to be held multi-day.
  - A stray BTC/USD limit order (0.0005 BTC @ $30,000 limit, ~$15
    notional) was created and canceled one second later at 15:24 UTC —
    never filled, no capital impact. Flagging since the crypto sleeve
    regime gate is BEAR today and should be standing down entirely;
    worth confirming this wasn't an unintended test order going
    forward.
  - **Data gap**: the Robinhood MCP connector is installed but not
    enabled in this chat session (`enabledInChat: false`), so no live
    Robinhood data (real accounts 556092849 / 829651439 / 539785238 or
    extra-watch quotes) could be pulled this run. Reported honestly
    instead of reusing stale numbers — dashboard's Robinhood section
    and the Telegram extra-watch lines are marked unavailable this
    run.
- Guardrail/breaker status: day P&L +0.003%, far inside the -2%
  day / -4% week circuit breakers — no trip. No rule violations. 1 of
  5 weekly new-entry slots used (the AAPL test buy).
- Lesson: day-TIF bracket legs silently expire at the close — treat
  "stop is on" as a per-session fact to re-verify, not a set-and-forget
  one, for any position meant to survive overnight.

### 2026-07-09 07:14 ET — stop re-armed on AAPL (risk-management action)
- Confirmed via `orders open` (empty) that AAPL's day-TIF bracket
  stop/target from 2026-07-08 had expired at the prior close, leaving
  the 1-share position with no protective stop overnight — a hard-rule
  violation ("every position gets a stop set immediately").
- Action: placed a standalone GTC stop, AAPL qty 1 @ stop $300 (same
  level as the original bracket's 1R), order id
  `7709c58e-aeda-4d01-9c5e-765d354a4af8`, status pending_new. No
  resting 3R take-profit currently (original target leg also expired
  and was not re-created — informational only, not a full re-bracket).
- Guardrail/honesty note: this is the confessed fix for yesterday's
  flagged gap, done at the 7:00 AM pre-market run rather than waiting
  for the 9:30 AM open, since the position was unprotected in the
  interim.

### 2026-07-09 09:30 ET — market open check
- Market open confirmed (`clock`). Equity $100,001.32 | cash $99,689.52
  | day P&L -$1.59 (-0.0016%) | open positions: AAPL 1@$310.47
  (current $311.89, uP&L +$1.42/+0.46%). GTC stop confirmed still
  resting (`7709c58e...`, stop $300, status `new`) — no gap-through
  event, position remains protected.
- Guardrail pre-check (§3b), all clear: daily breaker (-2%) — day P&L
  -0.0016%, no trip. Weekly breaker (-4%) — week P&L ~flat off the
  $100,000 baseline, no trip. Weekly trade cap — 1 of 5 entries used
  (AAPL test buy 7/8). Event blackout — no tier-1 macro release today
  (Initial Jobless Claims 8:30 AM already released pre-open, not
  tier-1). Earnings 24h — no held/candidate name inside the window.
  Correlation cap — n/a (single position). Tilt stop — n/a (no
  stop-outs today). Checks are moot this run: no trades were planned.
- No entries: the 7:00 AM `RESEARCH-LOG.md` run found zero qualifying
  setups (0 premarket gappers, no verified gap-with-catalyst anywhere,
  crypto sleeve regime-gated flat). Energy (XLE/XOM/CVX) and
  memory/semi (MU/LRCX/KLAC) remain TJL trend-join watches only
  (`scans/watchlist_2026-07-09.json`, feeds the hourly scanner) — no
  gap setup to execute at the open.
- Geopolitical update since 7 AM: the US launched new airstrikes on
  Iran overnight and Iran retaliated against Gulf targets — an
  escalation beyond the "ceasefire declared over" headline noted this
  morning. VIX spiked toward ~18 intraday before easing back; WTI
  pulled back ~0.9% to ~$72.9 after Wednesday's +4.4% spike. S&P/Nasdaq
  futures still opened green — tape shrugging off the headline so far,
  but flagging elevated overnight/weekend gap risk on the open AAPL
  position. Not a §3b tier-1 blackout event (no scheduled data
  release), noted for risk awareness only.
- ORCL (Robinhood extra-watch, real money) up +4.05% today
  ($140.49→$146.18) — no single confirmed catalyst found (ex-dividend
  $0.50 tomorrow 7/10, bullish Piper Sandler commentary/$225 PT
  circulating, but technicals still weak per moving averages); flagged
  as a notable move without a confirmed driver, not acted on (Claude
  never trades Robinhood).
- Dashboard republished with live Robinhood pull: Individual ORCL
  0.761815@$146.18 (uP&L +$5.78/+5.5%, RSI(14) 27.3 → STRONG BUY ZONE);
  Roth IRA VOO 0.110322@$687.61 (uP&L +$0.11, RSI 52.4, neutral-DCA,
  core — never sell); Agentic NVDA 0.358944@$201.80 (uP&L +$2.40, RSI
  51.0, neutral-DCA) + TSLA 0.002340@$395.17 (dust, uP&L -$0.08, RSI
  47.1, earnings 7/22 pm flagged — within the 14-day caution window)
  + crypto $31.36 (est. BTC ~$18.81/ETH ~$8.36/SOL ~$4.18 off the
  $18/$8/$4 basis split) + $70 pending deposit.

### 2026-07-09 14:25 ET — midday scan
- Positions: AAPL 1@$310.47, current $314.53, uP&L +$4.06/+1.31%. GTC
  stop still resting at $300 (order `7709c58e...`, status `new`) — no
  gap-through. Not near +2R (would need ~$10.47/share gain, currently
  ~$4.06) so no trailing-stop adjustment; not near -7% or thesis-break,
  no sell. No action needed on the position.
- `scan_tjl.py --no-telegram` (universe: XLE, XOM, CVX, MU, LRCX, KLAC
  from today's watchlist): 0/6 PASS — XLE/XOM/CVX fail_daily (price ≤
  prior-day high), MU/LRCX/KLAC fail_intraday (price ≤ HOD/PMH). No
  trade.
- `scan_crypto.py --no-telegram`: regime still BEAR (BTC $62,244.95 <
  daily SMA200 $74,356.29) — sleeve stands down, no entries. Crypto
  positions: none open (sleeve flat), so no -7%/thesis check applies.
- Guardrail check: moot this run (no PASS to evaluate) — daily/weekly
  breakers not tripped (equity $100,004.10, ~flat), weekly trade cap 1
  of 5 used, no earnings-24h conflicts, no tilt-stop triggers.
- Afternoon catalysts: no tier-1 macro release this afternoon — June
  FOMC minutes already released Wed 7/8, no fresh Treasury auction
  today (next 30Y auction is 7/15). Market tone: US-Iran conflict still
  the dominant driver (new US strikes + Iranian retaliation against
  Gulf targets reported this morning); PEP (held? no — market-wide)
  missed EPS by $0.01 this AM, other earnings light until after the
  bell. No held/watchlist name reports today; TSLA earnings 7/22 pm
  remains the nearest 24h-window flag (not yet inside window).
- Extra-watch one-liners (live): BTC ~$62,870 (bear regime intact, well
  under SMA200 ~$74.4k); ETH ~$1,744; SOL ~$78.23 (holding the $79
  support test per crypto press); NVDA $203.12 (-0.49% today, chip
  stocks mixed); ORCL $143.925 (+2.44% today, continuing yesterday's
  rally — ex-dividend $0.50 today, Piper Sandler $225 PT chatter still
  circulating, no single new confirmed catalyst).
- Dashboard republished (local, gitignored) with fresh Alpaca + live
  Robinhood pulls for all three accounts; RSI/MA signals reused from
  this morning's 9:30 AM computation (unchanged materially over ~5h,
  skipped re-running the historicals call for token frugality — noted
  in the dashboard as "as of 9:30 AM").

### 2026-07-09 — daily snapshot (4:00 PM ET run)
- Equity $100,005.42 | day P&L +$2.51 (+0.0025%) | cash $99,689.52
- Open: AAPL 1@$310.47, current $315.90 (uP&L +$5.43 / +1.75%)
- Trades today: 0 | notes:
  - No new entries executed; premarket research + TJL + midday scans yielded zero setups meeting §2 (gap-retest) + §4 (defined 1R risk) criteria. Universe: energy (XLE/XOM/CVX) and memory/semi (MU/LRCX/KLAC) stayed in TJL-watch-only mode; crypto regime remained BEAR (BTC < SMA200).
  - AAPL position held unchanged, GTC stop $300 (order `7709c58e...`) confirmed still resting end-of-day — no gap-through, position remains protected.
  - **Geopolitical tape resilience**: US-Iran military escalation overnight (new US strikes + Iranian Gulf retaliation) spiked VIX intraday but tape closed resilient (+0.003% day P&L); flagging elevated overnight gap risk on the AAPL position heading into the weekend. No §3b tier-1 blackout, just risk awareness.
  - **Robinhood extra-watch moves**: ORCL $140.49→$144.26 (+2.68%, ex-div $0.50 tomorrow 7/10, Piper PT chatter continues); NVDA $204.12→$202.76 (-0.67%); TSLA dust position noted, earnings 7/22 PM approaching (enter 14-day caution window 7/16).
- Guardrail/breaker status: day P&L +0.0025%, zero trip (breaker -2%). Week P&L ~flat off $100,000 baseline (no -4% trip). Weekly trade cap 1 of 5 new entries used. No earnings 24h, no tilt-stop triggers, no violations. All clear.
- Lesson: quiet catalyst-light tape — setups require gap + retest, not momentum. Iran escalation is real (risk noted), but tape stays resilient on core market health. Weekend gap risk elevated; tighter stop/reduced size would be prudent if entering large intraday Friday near close.
