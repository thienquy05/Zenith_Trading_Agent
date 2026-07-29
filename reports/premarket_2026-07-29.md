# 🧠 AI PREMARKET REPORT - Zenith

### Wednesday, July 29, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

FOMC decision day, and geopolitical risk is back on the table right
before it: Iran fired ballistic missiles at US forces in the Middle East
last evening (5:45 PM ET, 7/28) — all intercepted by US air defenses —
and the US/Saudi Arabia responded with joint strikes on Iran-aligned
targets in Iraq. This ends the two-night de-escalation from the
weekend. Oil jumped on it (WTI +4.6% to ~$82.66, Brent to ~$88+). The
Fed decision itself lands at 2:00 PM ET: a hold at 3.50–3.75% is the
consensus (~62% pre-announcement odds), but Chair Warsh has been
openly hawkish ("prices are too high"), and there's a real if minority
chance (~19%) of a surprise hike. That combination — geopolitical shock
plus a hawkish Fed with limited forward guidance — makes today's
2:00–2:30 PM ET window the one to actively avoid new risk, not casually
watch. Scan produced 5 gappers, none clearing either watchlist — all
thin microcaps with no real catalyst weight. Account still locked at 5
positions (1 over the 4-max cap). Semis continue to bleed (SK Hynix
guided down again overnight) on top of yesterday's China DUV story.

## 📊 Pre-Market Gappers

**5 candidates** from the Alpaca screener path (real gap data):

| Symbol | Gap % | Price | Catalyst found | Notes |
|---|---|---|---|---|
| BEZ | -17.36% | $21.00 | No | No catalyst, no data — thin, skip |
| BIYA | +9.33% | $7.03 | Weak | "Stocks moving" list mention only, not a real catalyst |
| INLF | -5.16% | $4.96 | Weak | Same — generic "stocks moving" list mention |
| EGG | +4.35% | $4.08 | Weak | Micro-catalyst (indie film investment), not tradeable weight |
| SNXX | +4.07% | $8.32 | No | No catalyst, no data |

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **None of the 5 gappers
clear it** — all missing market cap/RVOL data, and none trade above
their own prior-day high except BIYA (which still fails on cap, RVOL,
and SMA200). Table empty.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. Only
BIYA clears the gap/price/prior-high/catalyst-flag checks, but fails on
market cap and SMA200 — and its "catalyst" is a generic sector-movers
list mention, not a real driver. Table empty.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Iran fired on US forces overnight** — a real reversal of the
  weekend's de-escalation. IRGC ballistic missiles targeted US bases in
  the Middle East at 5:45 PM ET last night; all intercepted (5 over
  Jordan per Jordan's news agency). The US and Saudi Arabia responded
  with joint precision strikes on Iran-aligned "terrorist logistics and
  weapons sites" across eastern Iraq. Verified via CNN, Bloomberg, and
  Al Jazeera — multi-sourced, not a single-outlet report. Region is
  "on edge again after days of relative calm."
- **Oil surged on the news**: WTI +4.6% to ~$82.66/bbl, Brent to
  $88+/bbl — a sharp reversal of Monday's -4 to -5% de-escalation drop.
- **FOMC decision today, 2:00 PM ET**: consensus is a hold at
  3.50–3.75% (~62% pre-announcement odds per prediction markets), but
  Fed Chair Warsh has been hawkish in recent remarks ("prices are too
  high," "no tolerance for persistently elevated inflation"), and
  there's a real minority probability (~19%) the Fed surprises with a
  25bp hike. Warsh has also signaled less forward guidance than usual,
  so the post-meeting drift could be choppier than a typical hold.
- **Semis still bleeding**: SK Hynix fell again overnight on an
  earnings miss, extending the pressure that started with Monday's
  OpenAI-financing selloff and Tuesday's China DUV-lithography story.
  Multi-day negative momentum in the group, not a one-day event.
- Futures response to the Iran news was muted rather than a risk-off
  rout: S&P and Nasdaq-100 futures both modestly positive, Dow futures
  slightly negative — markets seem to be discounting the strikes as
  contained (intercepted, no reported casualties/damage) while saving
  their real reaction for the 2:00 PM Fed decision.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $63,846.55 vs daily SMA200
  $71,863.37 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-29_1110UTC.json`).
- **BTC** ~$63,900 (live), stabilizing after a rough week (-3.8% over 7
  days) — traders had been de-risking ahead of the Fed meeting; the
  Iran news adds a fresh reason for caution into the decision.
- **ETH** ~$1,964 (live), +4.4% on the day — continuing to outperform
  BTC; Morgan Stanley is reportedly rolling out low-cost ETH/SOL ETPs,
  a structural demand tailwind, not a today-specific catalyst.
- **SOL** ~$76.42 (live), +1.9% — captured 95% of tokenized-equity
  trading volume last week per one report, a notable but not
  immediately trade-relevant data point.
- **NVDA** closed Tuesday $197.01 (+0.3%) — the Alpaca paper position
  was already stopped out yesterday at the open (see Guardrail status).
  No new NVDA-specific headline beyond the ongoing OpenAI
  circular-financing concerns and sector-wide semis weakness. Microsoft
  reports earnings today after close — relevant as a read on Big Tech
  AI-capex spending, indirectly relevant to Nvidia's demand picture.
- **ORCL** ~$120 (live) — no new headline; still digesting last week's
  DoD/Navy contract wins against the Wisconsin data-center collateral
  overhang. Next earnings not until ~September 8. No Alpaca paper
  position (stopped out 7/25).

## 📊 Technical Signals for Today

- SPX 7,428.78 · NDX 27,763.13 · RUT 2,953.80 (Robinhood index feed,
  Tuesday's close basis — yfinance snapshot path down again this run,
  connection reset on every index/rates/oil symbol).
- VIX 18.26 (live), down slightly from yesterday's 18.99 — easing
  modestly even with the Iran news, consistent with futures reading it
  as contained rather than an escalation.
- 10Y yield: no live print again (yfinance ^TNX/^IRX connection reset).
- 5 gappers today but none carry real size or catalyst weight — no
  gap-quality read worth making; this is a data-quality/microcap batch,
  not a missed-opportunity batch.

## 💰 Economic Data, Rates & the Fed

**Today is the FOMC decision.** Federal Funds Rate announcement 2:00 PM
ET (forecast: hold at 3.75%, unchanged from previous), FOMC Statement
2:00 PM ET, FOMC Press Conference 2:30 PM ET (ForexFactory live fetch,
country=USD, impact=High). **§3b event blackout window in effect
today, roughly 1:30 PM–2:45 PM ET** (30 min before the 2:00 PM release
through 15 min after the later of the statement/press-conference
window) — no new entries during that stretch regardless of setup
quality. Tomorrow (7/30) brings Advance GDP q/q (forecast 2.1%, prior
2.0%) and Core PCE Price Index m/m (forecast 0.2%, prior 0.3%) at 8:30
AM ET — also tier-1, will need its own blackout check tomorrow morning.

### Guardrail status (Zenith standing section)

- **Position count: 5 open (AAPL, VOO, BTC, ETH, SOL) vs the strategy's
  4-concurrent max.** NVDA's gap-through stop fill yesterday at the
  open (-7.64%, filled at $193.81 vs $195.15 stop — normal slippage
  from a gap below the trigger, not a guardrail violation) freed one
  slot from 6 to 5. Still 1 over the cap — no new agent entry permitted
  today regardless of scan results (moot anyway, nothing qualifies).
- Daily/weekly circuit breakers: not tripped. Equity $99,996.23 vs
  $100,000 baseline — flat. Week P&L (from Monday 7/27 baseline
  $100,004.42): roughly -$8, well inside the -4% weekly breaker.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): all 5 positions healthy. AAPL leads at +10.0%
  unrealized, and its stop was already trailed to $329.10 yesterday
  after crossing the +2.5R further-trail gate (locks in ~+1.78R
  minimum). VOO -1.4%, BTC +0.5%, ETH +1.7%, SOL -2.7% — none near
  their stops.
- No names within 24h of earnings today among current holdings. AAPL
  (held) reports tomorrow, Thursday 7/30 after close — inside the 24h
  no-entry window as of tonight, though this doesn't affect an existing
  position, only would block a hypothetical new AAPL entry.

## 📅 Coming Up

- **Wednesday 7/29 (today)**: FOMC rate decision 2:00 PM ET, press
  conference 2:30 PM ET — narrow blackout ~1:30–2:45 PM ET. Microsoft
  earnings after close.
- **Thursday 7/30, 8:30 AM ET**: Advance GDP q/q and Core PCE Price
  Index m/m — both tier-1, own blackout window to check that morning.
- **Thursday 7/30, after close**: AAPL (held) and Amazon report
  earnings, alongside this week's Meta/Microsoft — one of the year's
  largest earnings days.

## 🚫 Skips & Traps

- **BIYA (+9.33%, "12 Industrials Stocks Moving" list mention)**: the
  only gapper that clears gap/price/prior-high on the swing side, but
  its "catalyst" is a generic sector-movers roundup headline, not an
  actual company-specific driver — exactly the kind of weak-catalyst
  trap the rules correctly filter out even before the mcap/SMA200 data
  gaps would have blocked it anyway.
- **BEZ (-17.36%)**: a real, sizeable gap down, but on zero catalyst
  and zero volume data — no story to trade, appropriately skipped.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing in today's gapper batch has
  real catalyst weight or size, so the rules-based empty watchlist and
  my own read match exactly.
- **Rules vs discretion**: n/a today — no borderline case worth
  arguing over.
- **Sharp catches**: the scan is genuinely quiet, but the macro
  backdrop is not — Iran's overnight strike on US forces (intercepted,
  multi-sourced) reverses the weekend's de-escalation right as the Fed
  delivers its decision at 2:00 PM with a hawkish chair and reduced
  forward guidance. That combination is the actual risk event today,
  not anything in the scanner. The blackout window (~1:30–2:45 PM ET)
  matters regardless of setup quality.
- Nothing to trade, nothing forced. Stand aside on new entries (still
  over the position cap, and nothing qualifies anyway); respect the
  FOMC blackout window this afternoon; watch AAPL's trailed stop and
  tomorrow's GDP/PCE prints plus AAPL's own earnings after tomorrow's
  close.
