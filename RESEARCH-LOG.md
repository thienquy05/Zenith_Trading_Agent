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

## 2026-07-09 — premarket analyst pipeline build (special entry, Quy's request — not a pre-market run)
- Reviewed the "internet prompts" pipeline spec with Quy. Adopted hybrid:
  Alpaca stays source of truth for gaps/PM volume/true premarket RVOL/levels;
  yfinance adds market cap, index snapshot, earnings dates; RSS + ForexFactory
  replace web searches for market news + econ calendar. Codex two-brain
  dropped (rules pass vs discretion pass instead). Resend dropped; full
  report goes to repo + email (AgentMail), Telegram brief unchanged.
- New: WATCHLIST_CRITERIA.md, REPORT_TEMPLATE.md, PROMPT-PREMARKET.md,
  scripts/scan_premarket.py (packet builder), scripts/send_report.py,
  reports/ archive, .venv + requirements.txt.
- **Exit-variant backtest (the internet spec's scale-out exits vs our
  bracket, same 84 signals, 2026-01-10→2026-07-09, AMD/NVDA/MU)**:
  bracket 33.3% WR / +11.04R / PF 1.20 vs scale-out 56.0% WR / +4.35R /
  PF 1.42. The claimed 54.6% WR reproduced almost exactly — and made less
  than half the money. Win rate is not profit. Brackets stay live;
  variant stays on the bench (`backtest_tjl.py --exits pmh`).
- Shakedown packet + sample report generated midday (12:44 ET): 12 gappers,
  0 eligible (market caps blocked by this sandbox's network policy), catalyst
  matcher + NAME_STOP hardening verified live (caught the AEHG/AEHR
  leveraged-ETF headline cross-match). Network allowlist needs
  yahoo/faireconomy/dowjones/cnbc/googlenews/agentmail domains — noted in
  AGENT-INSTRUCTIONS Gotchas.

## 2026-07-10 — pre-market
- Account: equity $100,004.46 | cash $99,689.52 | open positions: AAPL
  1@$310.47, current $314.94, uP&L +$4.47/+1.44%.
- Macro/calendar: 0 US high-impact events today (ForexFactory live
  fetch + web confirm — FOMC minutes already out 7/8, no CPI/jobs
  today). No §3b blackout window in effect. SK Hynix US listing debut
  and Delta earnings beat (record revenue) are the session's watched
  events but don't touch our screens.
- Sector momentum / market tone: mixed-to-flat premarket (some reads
  +0.2% SPX futures, others -0.2% with Polymarket implying only 20%
  odds of a green open). 10Y yield sticky near 4.6%, VIX calm at 15.86.
  Gappers scan returned only 2 illiquid small caps (JLHL +75.8%, VRAX
  -12.4%), neither cleared day/swing eligibility (mcap/RVOL data
  blocked by a yfinance network failure this run, packet's Alpaca path
  otherwise intact).
- Crypto regime: BEAR (BTC prior close $63,162.31 < daily SMA200
  $74,228.84) — sleeve stands down. BTC/ETH/SOL all green today: BTC
  $64,442 (+2.0%), ETH $1,799 (+2.6%), SOL $79.53 (+2.6%, still down
  ~2.1% on the week).
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): crypto three all bouncing (see
  above, chip-rally/yen-strength driven per CoinDesk, not crypto-
  specific news). NVDA $202.76 flat, ORCL $144.26 flat — quiet, no
  material headlines found on either today.
- Ideas (2-3): none. Both premarket gappers failed the day/swing
  screens (yfinance-blocked mcap + RVOL data, defaults to fail) and
  independently read as traps on discretion: JLHL's catalyst headline
  is an unanswered question with a thin float, VRAX is fading a
  dilutive $3.3M share-exercise raise the morning after a halt-up. No
  qualifying setups — standing aside on equities. Crypto sleeve flat
  (bear regime).
- Watching but not trading: JLHL, VRAX (both — see Skips & Traps in
  today's report for full reasoning).

## 2026-07-13 — pre-market
- Account: equity $100,005.71 | cash $99,689.52 | open positions: AAPL
  1@$310.47, current $316.19, uP&L +$5.72/+1.84%.
- Macro/calendar: 0 US high-impact events today, no §3b blackout window
  in effect today. Tomorrow (Tue 7/14) has CPI (core + headline, m/m +
  y/y) at 8:30 AM ET and Fed Chairman Warsh testifying at 10:00 AM ET —
  both tier-1, flagged for tomorrow's blackout window. Big bank earnings
  (C, GS, WFC, JPM, BAC) start Tuesday too.
- Sector momentum / market tone: dominant driver is a fresh US-Iran
  escalation over the weekend — CENTCOM's fifth round of strikes since
  the ceasefire broke down (140 targets, first use of one-way attack sea
  drones), Iran retaliated against Gulf bases (confirmed via CNN/Al
  Jazeera/CBS + the CENTCOM release). Chip stocks leading the selloff
  premarket: SK Hynix -8%, Micron -5.2%, Sandisk -6.3%, NVDA dragged
  ~-1.2%. Futures reads conflicting (some -0.3/-0.9% on geopolitics,
  others +0.4% on cooling global inflation) — tape is genuinely
  unsettled. Gappers scan found only 1 name (SUNE, -7.3%), gapping down
  on a non-specific 12-stock roundup headline, never eligible (gap
  direction alone disqualifies a down-gap from both day/swing lists).
  yfinance market-snapshot path blocked again this run (Robinhood index
  feed used instead, values are Friday 7/10's close, not live futures).
- Crypto regime: BEAR (BTC prior close $63,745.49 < daily SMA200
  $73,868.96) — sleeve stands down. BTC/ETH/SOL all red today: BTC
  $63,049 (-1.1% vs today's open), ETH $1,783 (-1.2%), SOL $76.50
  (-0.4%, still stuck under $80) — weekend risk-off tone / Asian-session
  leverage flush per CoinDesk.
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): NVDA $208.44 premarket (-1.2%),
  caught in the chip-sector selloff, no NVDA-specific headline found.
  ORCL $140.45 (roughly flat), quiet.
- Ideas (2-3): none. The one gapper (SUNE) failed the screens
  mechanically (down-gap) and independently reads as a non-catalyst
  (generic roundup headline, no real explanation for the move). No
  qualifying setups — standing aside on equities. Crypto sleeve flat
  (bear regime, and broader crypto tape red today anyway).
- Watching but not trading: SUNE (see Skips & Traps in today's report).
  Also watching the chip-sector selloff and the Iran situation for
  gap-risk on the open AAPL position, and tomorrow's CPI/Fed-testimony
  blackout window.

## 2026-07-14 — pre-market
- Account: equity $100,004.41 | cash $99,689.52 | open positions: AAPL
  1@$310.47, current $314.89, uP&L +$4.42/+1.42%.
- Macro/calendar: HEAVY data day, 5 tier-1 US events today — Core/
  headline CPI m/m+y/y at 8:30 AM ET (core y/y forecast 2.8% vs 2.9%
  prior, still well above the Fed's 2% target) and Fed Chair Warsh's
  congressional debut testimony at 10:00 AM ET. §3b blackout window IN
  EFFECT today around 8:30-10:00 AM ET. Separately, the US begins
  enforcing a Strait of Hormuz blockade (20% cargo fee) this afternoon —
  an escalation beyond the scheduled calendar, energy-shock/inflation
  risk. Big bank earnings (C/GS/WFC/JPM/BAC) also rolling out this week.
- Sector momentum / market tone: Monday saw a broad selloff on the
  Hormuz blockade announcement (chips hit hardest); today's futures
  described as mixed/steadier ahead of CPI+Warsh. SPX 7,515.34 / NDX
  29,264.10 / RUT 2,953.17 (Robinhood index feed, yfinance snapshot
  blocked again). VIX 17.49, climbing for a third straight session
  (15.86 Fri -> 16.30 Mon -> 17.49 today). Gappers: VEEE +19.4% (real
  merger/spinoff catalyst, verified via company IR release, but already
  faded from a 600%+ intraday spike and still below prior-day high +
  200-day SMA — trap despite real news), AGEN -3.4% (roundup headline,
  no real driver, down-gap). Neither cleared day/swing eligibility.
- Crypto regime: BEAR (BTC prior close $62,274.38 < daily SMA200
  $73,744.48) — sleeve stands down. BTC/ETH/SOL modestly green today
  after yesterday's slide: BTC $62,691 (+0.7% vs today's open), ETH
  $1,796 (+1.3%), SOL $75.46 (+0.8%).
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): NVDA $205.10 premarket (+0.8%),
  small bounce, no specific news. ORCL $128.80 premarket (-2.1%),
  continuing a sharp slide — beat Q4/FY26 earnings (cloud rev +47%) but
  fell ~6% Monday and is near a 14-month low on margin-compression /
  capex ($16.5B/qtr) / debt concerns plus a 21,000-job restructuring
  (verified via FX Leaders, TradingKey). Individual Robinhood account
  (556092849) shows no ORCL position / $0 equity for the SECOND
  consecutive check (first flagged yesterday's midday run) — likely
  Quy sold manually, confirmed pattern now not a one-off glitch.
- Ideas (2-3): none. Both gappers failed the screens (trend/mcap/RVOL);
  VEEE has a real, verified catalyst but the pop already faded 97% and
  the stock is still under its 200-day SMA — a trap, not a setup. Today
  is also inside a live §3b blackout window (CPI + Fed testimony), so
  even a borderline name would get held back until after 10 AM. No
  qualifying setups — standing aside on equities. Crypto sleeve flat
  (bear regime).
- Watching but not trading: VEEE, AGEN (see Skips & Traps in today's
  report). Reassess after CPI + Warsh testimony clear at 10 AM ET, and
  watch for Hormuz-blockade-driven volatility this afternoon.

## 2026-07-15 — pre-market
- Account: equity $100,006.32 | cash $99,689.52 | open positions: AAPL
  1@$310.47, current $316.80, uP&L +$6.33/+2.04%.
- Macro/calendar: LIVE data day again — Core/headline PPI m/m at 8:30 AM
  ET (headline forecast 0.0% vs 1.1% prior, core 0.3% vs 0.4% prior),
  Fed Chair Warsh's SECOND day of testimony (Senate Banking, after
  House Financial Services yesterday) at 10:00 AM ET. §3b blackout
  window IN EFFECT today ~8:30-10:00 AM ET, same pattern as yesterday.
  Yesterday's cool CPI (3.5% YoY vs ~3.8% exp) drove a relief rally
  (S&P +0.37%, Nasdaq +1%) but Warsh called it "not mission
  accomplished" (hawkish) — today could be two-sided again.
- Sector momentum / market tone: SPX 7,543.59 / NDX 29,586.29 / RUT
  2,964.76 (yesterday's close, up on the CPI relief rally; yfinance
  snapshot blocked again). VIX 16.38, down from 17.49 yesterday.
  Gappers: 8 total, 7 down / 1 up. SOXS (-90.1%) and TZA (-90.0%) are
  leveraged-ETF reverse-split data artifacts, not real moves (confirmed
  via prev_close vs sma200 being wildly inconsistent, e.g. SOXS $43 vs
  sma200 $417.68). CRMT -11.7% (real post-earnings selloff), BMGL +8.8%
  (real catalyst - Nasdaq compliance regained - but only 162 shares/day
  avg volume, untradeable), VEEE -7.7% (continuing to fade its Monday
  merger spike), NXTC -5.5% (real rebrand catalyst), LCID -3.0% (real
  catalyst - weighing strategic options rumor), BMNU -4.5% (no
  catalyst). None cleared day/swing eligibility - all down-gaps except
  BMGL, which fails mcap+sma200+liquidity.
- Crypto regime: BEAR (BTC prior close $64,993.47 < daily SMA200
  $73,633.01) — sleeve stands down. BTC/ETH/SOL flat-to-slightly-down
  today after a
  strong prior 24h: BTC $64,717 (-0.5% vs today's open), ETH $1,880.6
  (-0.6%), SOL $77.51 (-0.4%) — Ethereum ETF inflows (~$58M) and a
  Morgan Stanley ETH/SOL ETF filing (Coinbase as custodian) cited as
  tailwinds in broader coverage.
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): NVDA $211.68 premarket, roughly
  flat, no specific news. ORCL $129.11 premarket (+0.9%), small bounce
  after Mon/Tue's slide, no new company-specific news.
- Ideas (2-3): none. All 8 gappers failed the screens (down-gap
  direction, or mcap/sma200/liquidity for the one up-gap). Two of the
  down-gaps aren't even real moves (leveraged-ETF split artifacts).
  Today is also inside a live §3b blackout window (PPI + Fed testimony)
  — standing aside on equities regardless. Crypto sleeve flat (bear
  regime).
- Watching but not trading: none of today's gappers warrant a watch —
  see Skips & Traps in today's report. Reassess after PPI + Warsh's
  second testimony clear at 10 AM ET.

## 2026-07-16 — pre-market
- Account: equity $100,018.13 | cash $99,689.52 | open positions: AAPL
  1@$310.47, current $328.61, uP&L +$18.14/+5.84%.
- Macro/calendar: 0 US high-impact events today (ForexFactory live
  fetch) — the CPI(Tue)/PPI(Wed) blackout run is over, first clear
  morning since Monday. No §3b blackout window in effect today. UNH
  reports before the bell, NFLX after today's close (neither held, but
  market-moving for sentiment).
- Sector momentum / market tone: genuinely quiet premarket — packet's
  gap filter returned ZERO gappers from 60 Alpaca-screener candidates
  (not a data-feed issue, the Alpaca candidate path worked fine).
  Futures mixed but calmer (some +0.2% on eased inflation, some -0.1%).
  10Y yield drifted to ~4.57% on this week's cooler CPI/PPI combo. SPX
  7,572.40 / NDX 29,502.60 / RUT 2,976.26 (yesterday close, yfinance
  snapshot blocked again). VIX 16.10, third straight session cooling
  off the Iran-driven spike from last week.
- Crypto regime: BEAR (BTC prior close $64,724.27 < daily SMA200
  $73,517.57) — sleeve stands down. BTC/ETH/SOL all pulling back
  slightly today after a strong prior session: BTC $64,117.94 (-0.9% vs
  today's open), ETH $1,885.08 (-1.6%), SOL $76.19 (-1.3%) — yesterday
  saw BTC reclaim $65k on softer inflation data + $180M+ spot ETF
  inflows ($139M into IBIT).
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): NVDA $208.85 premarket (-1.7%),
  no specific news. ORCL $134.00 premarket (+1.1%), continuing this
  week's bounce. Note: an "Oracle" hack headline circulating today is
  about a DeFi price-oracle exploit on Ostium (~$18M), unrelated to
  Oracle Corp — flagged to avoid confusion.
- Ideas (2-3): none. Zero gappers to screen, zero econ events, nothing
  to force. Cleanest "no qualifying setups" of the week — the absence of
  candidates is the whole story today, not a screen filtering anything
  out. Crypto sleeve flat (bear regime).
- Watching but not trading: nothing flagged today. Watch for NFLX
  after-hours volatility bleeding into tomorrow's premarket tape.

## 2026-07-17 — pre-market
- Account: equity $100,000.16 | cash $98,584.47 | open positions: 7
  total — AAPL 1@$310.47 (now $332.92, +$22.45/+7.23%, stop trailed to
  breakeven $310.47), NVDA 1@$209.84 (now $202.05, -$7.79/-3.71%, stop
  $195.15), ORCL 1@$127.93 (now $122.55, -$5.38/-4.21%, stop $118.97),
  VOO 1@$692.29 (now $684.73, -$7.56/-1.09%, stop $643.83), BTC
  0.000699945@$64,132.85 (now ~$63,100, -1.6%, stop_limit
  59643.60/59345.40), ETH 0.010610407@$1,880.36 (now ~$1,836.60, -2.3%,
  stop_limit 1748.70/1739.96), SOL 0.130862025@$76.086 (now ~$74.63,
  -1.9%, stop_limit 70.76/70.4062). NVDA/ORCL/VOO/BTC/ETH/SOL were all
  placed by Quy manually yesterday (7/16 open), not agent-driven —
  confirmed via 7/16 09:41 AM open log.
- **Guardrail flag (standing, not one-off)**: position count is 7 open
  vs the strategy's 4-concurrent max, and this week's new-entry count
  (6, all Quy's manual trades) already exceeds the 5/week cap. **No new
  agent entry is permitted today regardless of scan results** until the
  position count normalizes. None of the 7 positions are near their
  stops or -7% today (worst is ORCL at -4.2%, ~3% cushion above stop).
- Macro/calendar: 0 US high-impact events today (ForexFactory live
  fetch) — housing starts, building permits, industrial production,
  and prelim UMich consumer sentiment are scheduled but don't trigger
  a §3b blackout. No blackout window in effect today. Travelers,
  Truist, Fifth Third report earnings (not held names).
- Sector momentum / market tone: Iran/US tension has a tentatively
  easing tone (Trump says Iran wants to negotiate, Qatar/Pakistan
  brokering talks) after Wednesday's VIX spike toward 19; oil behaved
  (WTI ~$71.59). Our live VIX read this morning is 18.14 (up from
  16.10 Thursday) — still elevated, de-escalation unconfirmed. SPX
  7,533.77 / NDX 29,025.77 / RUT 2,974.57 (yesterday close, down on
  chip-sector weakness — yfinance snapshot blocked again). Gappers:
  ATPC +9.65% (roundup non-catalyst, ~75% below 200-day SMA — dead-
  stock bounce), STAK -4.5% (vague real headline, down-gap, already
  faded from a June halt). Neither cleared day/swing eligibility.
- Crypto regime: BEAR (BTC prior close $63,783.12 < daily SMA200
  $73,397.04) — sleeve stands down. Broader crypto down ~1.6% 24h,
  Fear & Greed at 27. BTC $63,077 (live, -1.1%), ETH $1,834, SOL
  $74.79 — all lower, tracking dollar/yield sensitivity and
  semiconductor weakness. DeFiTuna Solana-lending exploit (~$580K,
  patched) circulating but minor/protocol-specific, not SOL-wide.
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): NVDA $202.10 premarket (-2.6%),
  continuing yesterday's chip-sector weakness (TSM spending-concern
  selloff), no new NVDA-specific news. ORCL $122.64 premarket (-1.3%),
  continuing its pullback, no new company-specific news.
- Ideas (2-3): none. Both gappers failed the screens on trend/mcap
  grounds, and even a clean setup would be vetoed today by the
  position-count guardrail (7 open vs 4-max). No qualifying setups —
  standing aside on equities. Crypto sleeve flat (bear regime).
- Watching but not trading: ATPC, STAK (see Skips & Traps in today's
  report). Bigger picture: watch for the 7-position count to normalize
  before the agent can take any new entry, even a great one.

## 2026-07-20 — pre-market
- Account: equity $100,009.10 | cash $98,584.47 | open positions: 7
  total, unchanged over the weekend and all healthy — AAPL +7.2%
  (stop at breakeven $310.47), NVDA -2.2%, ORCL -1.6%, VOO -0.9%, BTC
  +0.3%, ETH -0.3%, SOL +0.2% (crypto stop_limits unchanged). None near
  their stops.
- **Guardrail flag (standing, unchanged from Friday)**: position count
  still 7 open vs the strategy's 4-concurrent max. **No new agent entry
  is permitted today regardless of scan results.** New week means the
  weekly entry-cap counter resets, but the position-count cap remains
  the binding constraint.
- Macro/calendar: 0 US high-impact events today (ForexFactory live
  fetch) — no §3b blackout window in effect today.
- Sector momentum / market tone: **Iran war escalated sharply over the
  weekend** — 2 US service members killed + 1 missing after an Iranian
  strike on a Jordan base (war's US death toll now 17 over ~5 months),
  another KIA from a downed-drone detonation in Iraq, Iran struck
  Jordan and Kuwait (incl. an oil-sector site), US carried out a 9th
  consecutive night of strikes + reimposed a naval blockade of Iranian
  ports. Iran reports 50+ killed, 500+ injured from US strikes.
  Confirmed via CNN/WaPo/Fox/NPR/Al Jazeera. Gasoline back above
  $4/gallon. Market reaction mixed: some futures reads higher (Trump
  framing Iran as "very badly damaged," read as dominance/de-escalation
  by some traders), others down ~1%. 10Y yield eased to ~4.5% on softer
  inflation + safe-haven demand. Pending home sales -5.4% June.
  SPX 7,457.69 / NDX 28,592.66 / RUT 2,962.22 (Friday close, down from
  Thursday — yfinance snapshot blocked again). VIX 18.19, flat vs
  Friday's 18.14, still the week's high read. Gappers: BIYA +18.5%
  (catalyst headline is actually about a different stock in a 20-symbol
  roundup, not BIYA-specific; ~88% below its 200-day SMA) — not
  eligible, broken-trend bounce.
- Crypto regime: BEAR (BTC prior close $64,680.69 < daily SMA200
  $73,048.92) — sleeve stands down. BTC pushed below $64k over the
  weekend on Iran-risk-off flow; SOL testing $74-75 support (macro-
  driven, not SOL-specific — Circle issued $500M USDC on Solana,
  ~$900M RWA inflows over 30 days, fundamentals still constructive).
- Extra-watch (BTC/ETH/SOL/NVDA/ORCL): NVDA $205.20 premarket (+1.2%),
  small bounce, no specific news. ORCL $125.84 premarket (-0.5%),
  roughly flat, no new company-specific news.
- Ideas (2-3): none. BIYA failed the screens on trend/mcap grounds and
  its catalyst is a mismatch anyway. Even a clean setup would be vetoed
  today by the position-count guardrail (7 open vs 4-max, unchanged
  from Friday). No qualifying setups — standing aside on equities.
  Crypto sleeve flat (bear regime).
- Watching but not trading: BIYA (see Skips & Traps in today's report).
  Bigger picture: watching the Iran war for further escalation —
  dominant risk driver right now, more than anything on the scan.
