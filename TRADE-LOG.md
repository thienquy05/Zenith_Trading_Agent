# TRADE-LOG.md — all trades + daily snapshots (append-only)

Append entries at the BOTTOM. Never edit past entries; corrections get
a new dated line.

## Templates

### Trade entry
```
### YYYY-MM-DD HH:MM CT — BUY|SELL TICKER
- Qty / entry / stop / target: N @ $X.XX | stop $X.XX | target $X.XX (3R)
- Risk: $XX (X.X% of equity) | 1R = $X.XX/share
- Setup: gap-retest | other (explain)
- Thesis: one or two lines
- Order id(s): ...
```

### Exit
```
### YYYY-MM-DD HH:MM CT — EXIT TICKER
- Qty @ $X.XX | P&L: $XX (+X.XR) | reason: target | stop | thesis-break | -7% | trail
- Lesson (if any):
```

### Daily snapshot (3 PM run)
```
### YYYY-MM-DD — daily snapshot
- Equity $X | day P&L $X (X.X%) | cash $X
- Open: TICKER n@x (uP&L $x), ...
- Trades today: n | notes:
```

---

## Phase 2 — Alpaca paper account (active)

*(no trades yet — account initialized 2026-07-08)*

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
