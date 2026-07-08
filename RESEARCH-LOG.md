# RESEARCH-LOG.md — daily research notes (append-only)

Append at the BOTTOM, one entry per pre-market run.

## Template

```
## YYYY-MM-DD — pre-market
- Account: equity $X | cash $X | open positions: ...
- Macro/calendar: (CPI/PPI/FOMC/jobs/earnings due, times in CT)
- Sector momentum / market tone:
- Ideas (2–3):
  1. TICKER — thesis | catalyst | entry zone | stop | 3R target | risk notes
- Watching but not trading: ... (why not)
```

---

## 2026-07-08 — pre-market
- Account: equity $100,000 | cash $100,000 | open positions: none
- Macro/calendar: FOMC meeting minutes released today (2:00 PM ET /
  1:00 PM CT) — main catalyst risk for the session, especially
  rate-sensitive names. Levi Strauss (LEVI) reports earnings today;
  PepsiCo (PEP) tomorrow, Delta (DAL) Friday. Light data week otherwise
  (holiday-shortened, post-July 4th).
- Sector momentum / market tone: gappers scan came back empty (0 names
  >5% gap, >$3, >50k premarket vol) — quiet premarket. Ongoing
  memory-chip narrative: Micron's CEO reiterated an AI-driven memory
  shortage could last beyond 2028, and SK Hynix/Direxion 2x leveraged
  ETF filings are circulating — driving chatter in SOXS/SOXL and the
  memory/equipment complex (MU, STX, KLAC, LRCX, TER all showed up as
  premarket gainers per general market scans, though below our gap
  threshold).
- Ideas (2–3): none met the §4 filter (needs a concrete gap setup with
  defined risk) — no trades planned at the open. Not forcing a trade
  into a catalyst-light morning.
- Watching but not trading:
  1. Memory/semi complex (MU, STX, KLAC, LRCX, TER) — real catalyst
     (AI memory shortage narrative) but no gap entry today; watchlist
     seeded for TJL (Strategy 2) trend-join checks in case one breaks
     to new highs intraday.
  2. FOMC minutes at 2 PM ET — could move the whole tape; no new
     entries planned into the release, re-assess at the noon scan.

## 2026-07-08 — crypto strategy build & validation (on-demand session)
- Task: build a crypto-specific strategy and validate it on paper first.
- Built §2c "C-TJL" (Crypto Trend Join Long): daily-bar Donchian-55
  breakout + per-symbol daily SMA200 filter + master regime gate
  (BTC prev daily close > BTC daily SMA200), stop = 2×ATR(14) (1R),
  target +3R, max hold 30d, 3d cooldown, fixed liquid-majors universe
  (BTC, ETH, SOL, XRP, DOGE, LINK, AVAX, LTC /USD).
- Validation (all with 0.6%/round-trip cost haircut):
  - 4H breakout: REJECTED — all 18 grid cells net negative over 12m AND
    48m (gross edge exists; Alpaca costs ≈0.3R/trade eat it).
  - 4H mean-reversion dip-buy: REJECTED — all 8 variants negative.
  - Daily-bar C-TJL, 48 months: PASSED — 77 trades, 39% win, +23.34R
    net, PF 1.50, max DD 8.45R; every neighboring parameter cell also
    positive (PF 1.07–1.51); edge spread across 5/8 pairs.
    Record: scans/backtest_crypto_2022-07-29_2026-07-08.json
- Market context: crypto majors −31% to −64% over 12m — deep bear.
  Regime gate is BEAR today (BTC $63.3k < SMA200 $74.5k), so the sleeve
  is live but flat; scan_crypto.py now runs in the 6 AM + 12 PM
  workflows and stands down until BTC reclaims its daily SMA200.
- Order mechanics verified on paper: crypto limit GTC accepted +
  cancelled cleanly; bracket rejected (422 otoco) as documented; $10
  min notional discovered (403) and noted in gotchas. No position taken
  (none should be — bear regime).
- Sizing: 0.25% equity risk/trade during the live paper gate (≥15
  trades or 8 open-gate weeks, expectancy ≥0R), then 0.5%. Caps: 2
  concurrent crypto positions, 20% sleeve notional, 10% per position.
