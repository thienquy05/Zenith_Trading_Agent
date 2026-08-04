# 🧠 AI PREMARKET REPORT - Zenith

### Tuesday, August 4, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Indexes keep grinding to fresh highs — SPX 7,600.50, NDX 28,776.80, VIX
down to 15.62 — continuing last week's Amazon-driven rally plus the
weekend's real Iran de-escalation. ORCL (no paper position) is up
another leg this week, +5-9% Monday, extending the Google Cloud Gemini
AI partnership story with a fresh geopolitical-calm tailwind; NVDA
(also no paper position) logged a third straight up day, +3% Monday,
still consolidating near $200 against the ongoing OpenAI
financing-guarantee overhang. Scan found 2 gappers: SNAP (+7.69%) is a
real, verified earnings beat (revenue +19% YoY, margin expansion, 8th
straight quarter of positive free cash flow, shares +17% on the print)
but genuinely fails swing eligibility — the gap falls just short of the
8% threshold and the stock is still trading below its 200-day SMA, a
real technical fact, not a data-gap artifact like recent near-misses.
TEUP (+35.1%) has no catalyst at all. Account holds at 3 positions
(VOO/BTC/ETH), still under the 4-max cap with real capacity for a
qualifying entry if one appears later today.

## 📊 Pre-Market Gappers

**2 candidates** from the Alpaca screener path (real gap data):

| Symbol | Gap % | Price | Catalyst found | Notes |
|---|---|---|---|---|
| TEUP | +35.14% | $3.50 | No | No catalyst, no data — thin microcap, skip |
| SNAP | +7.69% | $5.46 | Yes | Real, verified earnings beat — see below |

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). Both gappers clear
gap/price/prior-high but fail market cap, RVOL, and SMA200 — for SNAP
the SMA200 fail is real (prior close $5.07 vs SMA200 $6.15, the stock
has been in a genuine downtrend into this earnings print, not a data
artifact). Table empty.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. SNAP
clears price/prior-high/catalyst but **genuinely misses the 8% gap
threshold (7.69%)** and fails SMA200 for real (still below its 200-day
average despite today's pop) — this is a legitimate rules fail, not the
data-gap pattern seen with AMZN/NOK/INTC. TEUP has no catalyst at all.
Table empty.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **SNAP beats and pops**: Q2 revenue $1.6B (+19% YoY, beat the $1.54B
  consensus by $60M), adjusted loss $0.10/share (beat -$0.12 est.),
  gross margin expanded 7 points to 58%, adjusted EBITDA $250M (up from
  $42M a year ago), 8th consecutive quarter of positive free cash flow
  ($121M). Shares reportedly popped as much as 17.3% on the print,
  though this morning's premarket gap has settled to +7.69%. Barclays
  reiterated Overweight and raised its price target to $16. Verified
  via Investing.com/GuruFocus and Yahoo Finance — a real, multi-sourced
  beat. Genuinely not swing-eligible per the rules (misses the 8% gap
  bar, still below its 200-SMA), a fair outcome given how far SNAP has
  fallen this year, not a data-quality complaint.
- **ORCL continues its multi-day run** (no Alpaca paper position,
  stopped out 7/25): +5.02% to +9.23% Monday depending on the source's
  intraday snapshot, extending last Thursday's Google Cloud Gemini AI
  partnership news with a fresh tailwind from easing geopolitical
  tensions. Company reported a $638B backlog and raised FY capex
  guidance to up to $95B — signaling continued aggressive AI
  infrastructure investment.
- **NVDA logged its third straight up day** (no Alpaca paper position,
  stopped out 7/28): +3% Monday, reversing an early intraday loss,
  still consolidating near $200-207 against the ongoing $250B OpenAI
  financing-guarantee debt-market concern. Reports fiscal Q2 2027
  results August 26 — 3+ weeks out, not yet a near-term watch item.
- Indexes at fresh highs across the board — SPX 7,600.50, NDX
  28,776.80. VIX 15.62, down further from Monday's 16.24, continuing
  the calming trend since the weekend's Iran de-escalation.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $63,454.24 vs daily SMA200
  $70,967.40 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-08-04_1119UTC.json`).
- **BTC** ~$63,600 (live), roughly flat — no fresh company-specific
  headline.
- **ETH** ~$1,864 (live), roughly flat, continuing to consolidate.
- **SOL** no Alpaca paper position (stopped out over the weekend,
  -7.08%, logged 8/3). Not tracked for a re-entry today since the
  sleeve regime gate is bear regardless.
- **NVDA / ORCL**: covered above — both showing real, multi-day
  strength on confirmed catalysts, neither held in the paper book.

## 📊 Technical Signals for Today

- SPX 7,600.50 · NDX 28,776.80 (Robinhood index feed — yfinance
  snapshot path down again this run, connection reset on every index/
  rates/oil symbol; RUT remains unavailable through the Robinhood MCP).
- VIX 15.62 (live), down from Monday's 16.24 — continued calm, now at
  its lowest level in weeks.
- 10Y yield: no live print again (yfinance ^TNX/^IRX connection reset).
- SNAP is the one gapper with genuine quality behind it today, but its
  own technical structure (still below SMA200) is exactly why the
  rules correctly hold it back — a real beat doesn't erase a real
  downtrend in one session.

## 💰 Economic Data, Rates & the Fed

Zero US high-impact events today or tomorrow (ForexFactory live fetch,
country=USD, impact=High) — **no §3b event blackout window today.**
July Nonfarm Payrolls remains the week's major event, Friday 8/7, 8:30
AM ET.

### Guardrail status (Zenith standing section)

- **Position count: 3 open (VOO, BTC, ETH) — still under the
  strategy's 4-concurrent max.** Real capacity remains for a qualifying
  new entry today or later this week, subject to all other §3b
  guardrails (daily/weekly circuit breakers, weekly 5-entry cap, event
  blackouts). Nothing in today's scan clears the bar.
- Daily/weekly circuit breakers: not tripped. Equity $100,000.12 —
  back to the $100k baseline exactly. Weekly new-entry cap: 0/5 used.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): VOO +0.8%, BTC -0.8%, ETH -0.9% — none near their
  stops.
- No held names within 24h of earnings.

## 📅 Coming Up

- **Tuesday 8/4 (today)**: no high-impact econ events. SNAP's
  post-earnings reaction plays out through the session.
- **Friday 8/7, 8:30 AM ET**: July Nonfarm Payrolls — major tier-1
  print, own blackout window to check that morning.
- **8/26**: NVDA reports fiscal Q2 2027 results — noting for the
  forward calendar, not yet a near-term item.

## 🚫 Skips & Traps

- **TEUP (+35.14%)**: sizeable gap on zero catalyst and zero volume
  data — no story to trade, appropriately skipped.
- **SNAP (+7.69%, real earnings beat)**: the closest thing to a
  quality name today, but genuinely fails on both the gap-size
  threshold and the SMA200 trend filter — a fair rules-based skip
  given the stock's longer downtrend, not a data-quality complaint like
  recent near-misses (AMZN, NOK, INTC).

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — SNAP's beat is real, but the stock's
  own chart (below its 200-day average) argues against chasing a
  single green day, and the rules land in the same place for a
  different but compatible reason (the literal 8%/SMA200 checks).
- **Rules vs discretion**: n/a today — no data-gap-driven near-miss
  like recent days; today's skip is a genuine quality/trend judgment,
  not a system limitation.
- **Sharp catches**: continued strength in ORCL and NVDA (both real,
  multi-sourced, multi-day moves) is worth tracking even without paper
  exposure — it's informing the broader "AI infrastructure spend still
  gets rewarded" read that's carried through the last two weeks of
  earnings reactions. Nothing in today's scan changes that thesis or
  creates a new tradeable angle on it.
- Nothing to trade, nothing forced. Position cap has real headroom
  (3/4) — watch for a qualifying setup on later scans this week,
  especially into and after Friday's NFP print.
