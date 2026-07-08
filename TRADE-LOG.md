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

### 2026-07-08 08:30 CT — market open check
- Market open confirmed (`clock`), equity $100,000 | cash $100,000 |
  open positions: none.
- No trades executed: pre-market research found no ideas meeting the
  §4 filter (gap setup + defined risk) — session was catalyst-light
  (empty gappers scan) and no watchlist entries qualified. Watching the
  memory/semi complex (MU, STX, KLAC, LRCX, TER) for a TJL breakout
  intraday; FOMC minutes at 2 PM ET is the main event risk.
