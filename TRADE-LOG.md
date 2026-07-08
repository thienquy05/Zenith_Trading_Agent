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
