# 🧠 AI PREMARKET REPORT - Zenith

### Wednesday, July 22, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Yesterday's ceasefire-hope rally reversed hard overnight: Secretary of
State Rubio said Iran is "not serious" about talks, US struck Iran for an
11th straight night, and oil jumped ~4% (Brent near $94/bbl). Futures are
sliding into Alphabet and Tesla earnings tonight. Still moot for new
entries either way — the account remains at 7 concurrent positions, so no
new agent entry is permitted today. 3 gappers today, none eligible: one
is a fading pump, two are thinly-traded leveraged single-stock ETFs
riding chip-sector momentum, not real company catalysts. Rules and
discretion agree: stand aside, watch the book, and note Tesla earnings
tonight for the dust position.

## 📊 Pre-Market Gappers

**CPHI (China Pharma Holdings)** — gap -7.0% to $8.04 (prev close
$8.64). The stock soared nearly 700% Tuesday on "unusual market
activity" that the company itself says it has no knowledge of any
material development behind — a classic unexplained pump. Today's move
is the pump partially unwinding. Down-gap regardless, never in
contention.

**SNXX** — gap +4.6% to $18.67 (prev close $17.85). This is a leveraged
single-stock ETF tracking SanDisk (part of Tradr's 2X ETF lineup), not
an operating company — no 200-day SMA data exists because these products
are relatively new. The attached "catalyst" headlines are from May/April,
stale and unrelated to today. It's riding the broader chip-sector bounce,
not reacting to fresh news.

**SNDU** — gap +3.7% to $29.18 (prev close $28.14). Same story as SNXX:
another Tradr leveraged single-stock ETF (SanDisk-linked), stale
headlines, no real today-specific catalyst, no SMA200 data.

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it
today** — table empty. SNXX and SNDU clear the gap-size and
above-prior-high checks but fail on market cap and RVOL data (both
unavailable, defaults to fail) — appropriately conservative given
neither is a real operating company anyway.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No
names cleared it today** — table empty. Neither up-gapper reaches the 8%
threshold anyway.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Ceasefire hopes reversed overnight**: Rubio told reporters in Manila
  that Iran is "not serious about talks" ("if they're serious, we're
  serious"), the US struck Iran for an 11th consecutive night, and
  Brent crude jumped ~4% toward $94/bbl on renewed Strait of Hormuz
  disruption risk. Confirmed via CNN, CNBC, Al Jazeera, and The
  National. This directly reverses yesterday's relief-rally driver —
  exactly the fast-reversal risk flagged in yesterday's report.
- Yesterday's regular session was strong before this reversal: Dow
  +0.74%, S&P +0.89% to 7,509.20, Nasdaq +1.29% — chipmakers led. That
  strength is now being tested by this morning's oil spike and futures
  are sliding into the open.
- **Big Tech earnings tonight**: Alphabet and Tesla report after
  today's close, with Intel also reporting this week. TSLA is Quy's
  real (dust) Robinhood holding — worth watching the print even though
  it's a tiny position. Markets are watching whether earnings justify
  elevated AI-related valuations after last week's semiconductor
  wobble.
- Gapper set has no real fresh company-specific catalyst in it — no
  sector signal to draw.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $66,527.99 vs daily SMA200
  $72,814.00 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-22_1115UTC.json`).
- **BTC** $65,980 (live), -0.8% vs today's session open ($66,525) —
  giving back a little of yesterday's strength as the Iran-headline
  reversal weighs on risk assets broadly.
- **ETH** $1,928 (live), roughly flat vs today's open ($1,929).
- **SOL** $77.76 (live), -0.5% vs today's open ($78.15).
- **NVDA** $205.37 (live premarket) vs prior close $207.29, -0.9% —
  pulling back slightly, no company-specific headline found today.
- **ORCL** $126.98 (live premarket) vs prior close $127.05, roughly
  flat — no new company-specific news found today.

## 📊 Technical Signals for Today

- SPX 7,509.20 · NDX 29,155.18 · RUT 2,987.40 (yesterday's regular-
  session close, confirmed via Robinhood index feed — a strong session
  now being tested by this morning's oil/Iran headlines).
- VIX 17.45 (live, 7:15 AM ET), up from yesterday's close read as the
  oil spike and Iran headline risk feed back into hedging demand.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- Gapper set offers no collective read — one fading pump, two
  leveraged ETF products with no real catalyst behind today's move.

## 💰 Economic Data, Rates & the Fed

Light data day by our tier-1 standard — 0 US high-impact events on
today's calendar (ForexFactory live fetch). No tier-1 print, no §3b
event blackout window today.

### Guardrail status (Zenith standing section)

- **Position count: still 7 open (AAPL, NVDA, ORCL, VOO, BTC, ETH, SOL)
  vs the strategy's 4-concurrent max.** No new agent entry is permitted
  today regardless of scan results — fourth-plus straight trading day
  flagging this standing condition (pinned since 7/18).
- Daily/weekly circuit breakers: not tripped. Equity $100,007.01 vs
  $100,000 baseline — flat.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): all 7 positions healthy, none near their stops.
  AAPL leads at +5.3%; worst is VOO at -0.8%, all crypto legs green.
- Elevated geopolitical risk remains a standing flag, sharper today
  given the ceasefire-hope reversal — gap risk on the book (especially
  crypto, which trades through headlines any time of day) stays live.
- No names within 24h of earnings on today's gappers (`next_earnings`
  null across the board — unknown, not a confirmed clear). Note: TSLA
  (held, dust position) reports after today's close — inside its
  14-day caution window already flagged in prior runs.

## 📅 Coming Up

- No US high-impact events surfaced for tomorrow (7/23) in this run's
  calendar pull yet.
- **Alphabet and Tesla report after today's close** — watch for
  after-hours moves bleeding into tomorrow's premarket, especially for
  the TSLA dust position and broader Big Tech sentiment.
- FOMC decision July 29 (~85.6% priced for a hold per prior reads) —
  still a week out, not yet a blackout concern.

## 🚫 Skips & Traps

- **CPHI** — an unexplained 700% pump (company itself disclaims any
  known catalyst) partially unwinding today. Don't touch either
  direction.
- **SNXX / SNDU** — leveraged single-stock ETF products, not operating
  companies, riding sector momentum on stale headlines rather than
  fresh news. Not real trading candidates regardless of what the gap
  size says.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing here is tradeable, and the
  position-count cap would veto a new entry regardless. The rules
  reject all 3 gappers on data-availability/trend grounds; discretion
  independently flags that none of them have a real, fresh,
  company-specific catalyst behind today's move.
- **Rules vs discretion**: no disagreement today.
- **Sharp catches**: discretion's real job today is noting how fast the
  macro backdrop flipped — yesterday's ceasefire-hope rally is already
  reversing on a single Rubio quote and an 11th night of strikes. That
  volatility matters more for risk awareness on the existing book (and
  on TSLA earnings tonight) than anything the gapper scan turned up.
- Nothing to trade, nothing forced, and the position cap blocks new
  entries regardless. Stand aside; monitor the 7 open positions at the
  scheduled checkpoints, and watch for Alphabet/Tesla earnings reaction
  after the close.
