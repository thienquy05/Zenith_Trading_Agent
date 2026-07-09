# RESEARCH-LOG.md — daily research notes (append-only)

Append at the BOTTOM, one entry per pre-market run.

## Template

```
## YYYY-MM-DD — pre-market
- Account: equity $X | cash $X | open positions: ...
- Macro/calendar: (CPI/PPI/FOMC/jobs/earnings due, times in ET) +
  §3b blackout windows in effect today
- Sector momentum / market tone:
- Crypto regime: BULL|BEAR (BTC vs daily SMA200) | BTC/ETH/SOL 24h
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): anything material, else "quiet"
- Ideas (2–3):
  1. TICKER — thesis | catalyst (+source) | entry zone | stop | 3R
     target | size @1% risk | invalidation | guardrails checked
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

## 2026-07-09 — pre-market
- Account: equity $100,002.04 | cash $99,689.52 | open positions: AAPL
  1@$310.47 (current $312.52, uP&L +$2.05/+0.66%). **Stop-loss gap
  found and fixed this run**: yesterday's AAPL bracket used day-TIF
  stop/target legs that expired at the 20:00 UTC close, leaving the
  position unprotected overnight (`orders open` returned `[]`). Placed
  a standalone GTC stop at $300 (same level as the original 1R) —
  order `7709c58e...`, pending_new. Lesson carried to today: any
  position meant to survive past the session needs a GTC (not day)
  stop re-armed explicitly.
- Gappers scan: 0 names (>5%/$3/50k premarket filters) — quiet
  premarket, cross-checked against general market scanners
  (TradingView/Barchart/stockanalysis.com), which show only
  illiquid/low-float names with no verifiable catalyst. No gap
  candidates today.
- Macro/calendar (today 2026-07-09, ET): Initial Jobless Claims 8:30 AM
  (~218K forecast vs 215K prior); Existing Home Sales later in the
  session; Treasury 6-Week & 13/26-Week Bill auctions + a 30-Year bond
  auction today (tail end of this week's $119B note/bond slate — 3-yr
  Tue, 10-yr Wed, 30-yr today). Fed speakers this week: Gov. Waller
  (ECB Research Network conf., Rome) and Vice Chair Bowman. **No
  tier-1 event today** — no CPI/PPI/FOMC decision/NFP this week (June
  FOMC minutes already released yesterday 7/8); no §3b event blackout
  window in effect today.
- Earnings: PepsiCo (PEP) reports pre-market today, ~6:00 AM materials
  / 8:15 AM analyst call, consensus EPS $2.21 (PepsiCo IR — primary
  source). ~13 companies report today, 7 tomorrow incl. Delta (DAL)
  pre-market Fri 7/10 (EPS est. $1.47). AAPL next earnings 7/30 (not
  within 24h — no flag). NVDA: no imminent date found. ORCL: next
  earnings ~9/14 (not within 24h). No held/candidate name is inside
  the 24h no-entry window today.
- Market tone: S&P futures +0.1–0.3%, Nasdaq-100 futures +0.5%, Dow
  flattish; VIX ~16.1–17.5 (up slightly). Yesterday (7/8): S&P -0.3%,
  Dow -1.5%, Nasdaq-100 +0.3% — mixed/narrow breadth (NYSE advancers
  led 1.3:1, Nasdaq decliners led 1.55:1). Sector leaders yesterday:
  Tech (XLK +1.7%), Energy (oil >$75/bbl on renewed Iran tension);
  laggards: Health Care, Staples, Utilities (all ~-1%). Overnight
  mover: KOSPI +3.7%/Nikkei +1.65% on SK Hynix's oversubscribed (7x)
  $28B Nasdaq IPO (ADR ticker SKHY, debuts Fri 7/10) — Samsung +4%,
  Kioxia +8%, sympathy across the memory/equipment complex. Overhang:
  Trump said the Iran ceasefire was "over" — oil and yields up on the
  headline risk.
- Crypto regime: **BEAR** (BTC prev daily close $62,244.95 < daily
  SMA200 $74,356.29) — sleeve stands down, no entries
  (`scan_crypto.py --no-telegram`, no PASS candidates even if regime
  were open). BTC ~$62.4k -1.7% 24h, ETH ~$1,733 -2.3%, SOL ~$77-81
  -5.2% (SOL the laggard) — broad ~-2% crypto-mcap risk-off tracking
  the Iran-tension move in oil/yields, no crypto-specific catalyst
  found.
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): BTC/ETH/SOL — quiet on
  name-specific news, just the broad risk-off drag above. NVDA — quiet,
  live $204.14 (prev close $204.12, flat); sector chip volatility is
  Asia-IPO-driven, nothing NVDA-specific. ORCL — quiet, live $140.55
  (prev close $140.49, flat).
- Ideas (2–3): **none met the §4 filter** — 0 premarket gappers, no
  verified >5% gap-with-catalyst anywhere on a cross-check, and the
  crypto sleeve is regime-gated flat. Not forcing a trade into a quiet,
  catalyst-light tape (PEP earnings and the Treasury auctions are the
  session's only real events, neither is a gap setup). No new entries
  planned at the open.
- Watching but not trading:
  1. Energy sector (XLE/XOM/CVX) — real, verified catalyst (oil >$75 on
     Iran-ceasefire breakdown, sector led gains yesterday) but no
     defined gap entry yet; seeding for TJL trend-join if a name
     breaks to new highs intraday.
  2. Memory/semi complex (MU, LRCX, KLAC) — Asia chip rally (SK Hynix
     IPO oversubscription, KOSPI/Nikkei up) is spilling into US names
     sympathetically; same watch as 7/8, still no gap trigger.

## 2026-07-09 — strategy research (special entry, Quy's request — not a pre-market run)
- Task: enhance TRADING-STRATEGY.md with verified expert/academic
  evidence + full performance metrics (win rate, Sharpe, Sortino, PF,
  expectancy, max DD). Quy may mirror trades with real money later, so
  the bar was: primary/peer-reviewed sources, 2-source verification,
  honest small-sample caveats.
- Verification method: SSRN blocks direct fetch → every paper's numbers
  cross-checked across ≥2 independent write-ups (QuantConnect, CXO
  Advisory, Robust Trader, Quantpedia, Concretum/authors' own site).
- Sources verified & adopted into §7 evidence table:
  1. Zarattini & Aziz 2023 (SSRN 4416622) — 5-min ORB on QQQ 2016–23:
     +675% net, Sharpe 1.12, alpha 33%. Validates TJL's momentum
     bracket/EoD-exit template.
  2. Zarattini, Barbon & Aziz 2024 (SSRN 4729284) — ORB on top-20
     "Stocks in Play": +1,600% net, Sharpe 2.81, hit ratio ~43%,
     convex payoff. → proposed §2d-R1 relative-volume TJL filter
     (backtest-gated, per Quy's decision).
  3. Lempérière et al. / Moskowitz-Ooi-Pedersen — trend following
     Sharpe ~0.4 across 67 markets / 137 yrs, positive every decade;
     TSMOM positive in all 58 futures. Validates C-TJL Donchian-55.
  4. Faber (SSRN 962461) — 200d-SMA filter cuts max DD 46%→<10%.
     Validates the BTC>SMA200 regime gate.
  5. Kaminski & Lo (J. Fin. Markets) — stops add value ONLY in
     momentum regimes. Validates our hard stops; also validates NOT
     using stops on Quy's buy-and-hold Robinhood core (§5 trims).
  6. Base-rate studies: Brazil (Chague et al.: 97% of persistent day
     traders lose) + Taiwan (Barber et al.: <1% reliably profitable).
     Adopted as §7d real-money warning.
  7. FVG/gap-retest evidence reviewed and graded WEAK (practitioner
     claims only, one falsification study against) — §2 gap setup now
     explicitly flagged; §2d-R2 quality filter proposed.
- New tooling: scripts/strategy_metrics.py (win rate, PF, expectancy +
  95% bootstrap CI, max DD, per-trade & annualized Sharpe/Sortino).
  Measured: TJL 32.5% WR / PF 1.15 / ann. Sharpe ~0.78; C-TJL 39.0% WR
  / PF 1.50 / ann. Sharpe ~0.92 / Sortino ~2.0. BOTH expectancy CIs
  include 0 — edge not statistically confirmed yet; recorded in §7b
  and in the real-money warning.
- Not adopted (rejected/deferred): immediate rule changes (Quy chose
  backtest-gated adoption); FVG zone geometry as a standalone edge.

## 2026-07-09 — §2d validation run (Quy: "validate them then merge")
- R1 (TJL intraday relative-volume ≥1.5–2× gate): backtested via new
  `backtest_tjl.py --rvol` (cum session volume at signal minute vs
  14-session same-minute avg; extra 30d bars for lookback so the trade
  window matches baseline). AMD/NVDA/MU, 6mo, 2026-01-10→07-09:
  baseline 84 trades / 33.3% WR / PF 1.20 / +11.04R;
  rvol≥1.5×: 14 trades / 7.1% WR / PF 0.24 / −9.30R;
  rvol≥2.0×: 7 trades / 14.3% WR / PF 0.50 / −3.00R.
  → FAILED the gate (expectancy must be ≥ baseline) — REJECTED.
  Read: SSRN 4729284's stock-in-play edge is a UNIVERSE-selection
  effect (our gappers scan already does this); an intraday volume gate
  on already-liquid mega-caps selects chaos, not follow-through, and
  IEX-only volume makes the ratio noisy. Kept `--rvol` for future
  re-tests on watchlist universes.
- R2 (gap catalyst+volume quality filter): no §2 backtester exists and
  zero live §2 trades to date — cannot be validated numerically today.
  Adopted as a conservative pre-filter (restriction-only, adds no
  risk); formal keep/drop after 20 logged §2 setups.
- Artifacts: scans/backtest_tjl_2026-01-10_2026-07-09.json, *_rvol1.5,
  *_rvol2. Strategy §2d + changelog updated with verdicts.
