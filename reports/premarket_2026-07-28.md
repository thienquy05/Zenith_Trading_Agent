# 🧠 AI PREMARKET REPORT - Zenith

### Tuesday, July 28, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Risk-off morning: a state-backed Chinese firm has reportedly begun mass
production of a domestic DUV lithography machine, and Asian/European chip
names sold off hard on the news (ASML -7%+, dragging Applied Materials,
Lam Research, KLA). US premarket semis are following — Nvidia, AMD, and
Micron all reported lower. This lands directly on the book: **NVDA's
current price ($194.85, -7.14% unrealized) is now below its resting
$195.15 stop order**, which will almost certainly fill at the open (stop
orders don't execute premarket). Scan is otherwise thin — one gapper
(DFNS, +8.7%) but it fails every size/quality check, so both watchlists
are empty again. Account remains locked at 6 positions (2 over the
4-max cap) — no new entries regardless. FOMC's two-day meeting begins
today; the actual rate decision (and its narrow blackout window) is
tomorrow, not today.

## 📊 Pre-Market Gappers

**1 candidate** from the Alpaca screener path (real gap data, not a
yfinance fallback):

| Symbol | Gap % | Price | Catalyst found | Notes |
|---|---|---|---|---|
| DFNS | +8.68% | $15.03 | Yes | 13D filing — activist stake disclosed |

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **DFNS fails 4 of 6
checks** (no market cap data, no premarket RVOL data, price $15.03 is
below its prior-day high of $15.86, and prior close $13.83 is far below
its 200-day SMA of $335.78 — a stale/likely-unadjusted SMA on a thin
microcap, but the rule reads the number as given and fails it either
way). Table empty.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. DFNS
clears the gap and catalyst checks but fails open-above-prior-high,
open-above-SMA200, and market cap. Table empty.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **China DUV lithography breakthrough is the story of the morning**: a
  state-backed Chinese firm has reportedly begun mass production of an
  immersion DUV lithography machine (modest volume — ~5 units in 2026,
  ~20 more in 2027 — but a real supply-chain milestone since advanced
  EUV tools remain export-controlled). ASML fell over 7% on the report,
  dragging Applied Materials, Lam Research, and KLA with it; US
  premarket has Nvidia off roughly 5%, AMD down over 8%, Micron down
  close to 6%. Verified across CNBC, Yahoo Finance, and Investing.com —
  a real, multi-sourced story, not a single-outlet rumor. Directly
  relevant here: it's compounding the pressure that already pushed NVDA
  to -7% (see Guardrail status below).
- VIX has ticked up to 18.99 from yesterday's 17.66 — modest risk-off,
  consistent with a sector-specific selloff rather than a broad
  macro shock.
- SPX 7,413.18 · NDX 28,039.21 · RUT 2,948.03 (Robinhood index feed,
  Monday's close basis — yfinance snapshot path is down again this run,
  connection reset on every index/rates/oil symbol).
- No fresh company-specific headlines found today for BTC, ETH, SOL, or
  ORCL beyond the semis story above.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $63,701.95 vs daily SMA200
  $71,996.77 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-28_1115UTC.json`).
- **BTC** $63,386 (live), essentially flat vs the crypto risk-off tone.
- **ETH** $1,873 (live) — held Alpaca position now roughly flat since
  entry (-0.3%), giving back some of Monday's strength.
- **SOL** $73.07 (live) — held position -4.3% unrealized, still well
  clear of its stop_limit at $70.76.
- **NVDA** $194.85 (live premarket) vs prior close $196.51, -0.8% and
  falling on the China DUV story — see Guardrail status, this is the
  headline item for today.
- **ORCL** no fresh headline found today; not held in the Alpaca book
  (stopped out 7/24).

## 📊 Technical Signals for Today

- SPX 7,413.18 · NDX 28,039.21 · RUT 2,948.03 (Robinhood index feed).
- VIX 18.99 (live), up from 17.66 — mild risk-off tied to the semis
  selloff, not a broad macro move.
- 10Y yield: no live print again (yfinance ^TNX/^IRX connection reset).
- Only one gapper today (DFNS) and it fails the watchlist rules outright
  on data quality (SMA200 mismatch, missing mcap/RVOL) — no gap-quality
  read worth making.

## 💰 Economic Data, Rates & the Fed

Zero US high-impact events today (ForexFactory live fetch) — **no §3b
event blackout window today.** The FOMC's two-day meeting begins today,
but the actual decision, statement, and press conference are all
**tomorrow, Wednesday 7/29**: Federal Funds Rate 2:00 PM ET, FOMC
Statement 2:00 PM ET, FOMC Press Conference 2:30 PM ET. That means
tomorrow's blackout window is narrow — roughly 1:30–2:15 PM ET (30 min
before the 2:00 PM release to 15 min after) — not a multi-day window.
(Correcting an overstated "FOMC blackout 7/18–7/30" note that appeared
in an earlier log entry — the rule per TRADING-STRATEGY.md §3b is 30
minutes before to 15 minutes after the specific tier-1 release only.)

### Guardrail status (Zenith standing section)

- **Position count: 6 open (AAPL, NVDA, VOO, BTC, ETH, SOL) vs the
  strategy's 4-concurrent max.** Still 2 over the cap — no new agent
  entry permitted today regardless of scan results, though the scan
  produced nothing qualifying anyway.
- **NVDA is at/through its stop and will very likely execute at the
  open.** Current price $194.85, unrealized -7.14% (past the hard -7%
  bail threshold), resting stop order (id `327083b0`) at $195.15,
  status still "new" — Alpaca stop orders don't trigger during the
  premarket session, only regular hours (9:30 AM–4:00 PM ET). Barring a
  recovery above $195.15 in the next ~20 minutes, this should fill
  shortly after the open and will be logged in TRADE-LOG.md by the
  9:30 AM workflow. The China DUV/semis selloff this morning is added
  pressure, not the original cause — NVDA was already at -6.7% on
  Monday's OpenAI financing-news selloff.
- Daily/weekly circuit breakers: not tripped. Equity $99,989.64 vs
  $100,000 baseline — flat.
- Other 5 positions healthy: AAPL +9.1%, BTC -1.3%, ETH -0.3%, SOL
  -4.3%, VOO -1.9% — none near their stops.
- No names within 24h of earnings today (no gappers qualify to check
  against). AAPL reports Thursday 7/30 after close — 2 days out, not
  yet inside the no-entry window for that existing position.

## 📅 Coming Up

- **Tuesday 7/28 (today)**: FOMC two-day meeting begins, no
  announcement. NVDA stop likely fills at the open.
- **Wednesday 7/29, 2:00 PM ET**: FOMC rate decision, statement, and
  2:30 PM press conference — tier-1, narrow ~1:30–2:15 PM ET blackout
  window.
- **Thursday 7/30, after close**: AAPL (held) and Amazon report
  earnings, alongside Meta and Microsoft earlier in the week — one of
  the year's largest earnings days.

## 🚫 Skips & Traps

- **DFNS (+8.68%, activist 13D filing)**: real catalyst, but fails 4 of
  6 day-eligibility checks and 3 of 6 swing checks — no market cap or
  premarket RVOL data, price below its own prior-day high, and a
  200-day SMA ($335.78) wildly out of line with the current price
  ($15.03), most likely a stale/unadjusted feed for this thinly-traded
  microcap. Correctly skipped either way: the rules read the numbers as
  given, and even setting the SMA figure aside, "price below prior-day
  high" alone is disqualifying for both lists.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — DFNS is a legitimate news mover but
  clearly not a quality setup (thin, no size confirmation, already
  below its own prior high), so the rules-based skip and my own read
  land in the same place.
- **Rules vs discretion**: n/a for the scan today — nothing to promote,
  nothing to argue for promoting.
- **Sharp catches**: the real story today isn't the empty scan, it's
  that a live, multi-sourced geopolitical/supply-chain headline (China
  DUV lithography) is adding fresh pressure to a position (NVDA) that
  was already sitting on the stop line from an unrelated Monday
  headline (OpenAI financing). Two independent bad-news days back to
  back pushed it through -7% — worth noting for the pattern, not as a
  reason to second-guess the stop (the stop-loss rule doesn't
  distinguish cause, and shouldn't).
- Nothing to trade, nothing forced. Stand aside on new entries (still
  over the position cap and nothing qualifies anyway); watch for the
  NVDA stop fill at the open and the tomorrow's FOMC decision.
