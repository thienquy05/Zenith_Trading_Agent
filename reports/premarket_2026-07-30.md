# 🧠 AI PREMARKET REPORT - Zenith

### Thursday, July 30, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

FOMC held steady yesterday as expected (3.50–3.75%), but the tape stayed
rough — Meta cratered 10% on an EPS miss (despite beating on revenue)
while Microsoft rose 2% on solid cloud numbers, a real divergence in
how the market is pricing AI-spend payoff. That's the backdrop for
today's headline event: **Apple reports after today's close — Tim
Cook's final earnings call as CEO** before John Ternus takes over
September 1, with consensus at ~$108.9B revenue (+16% YoY) and ~$1.89
EPS (+20% YoY); the real story analysts are watching is gross margin
under memory-chip-driven price pressure. Also today: **GDP and Core PCE
at 8:30 AM ET**, a tier-1 pair with its own narrow blackout window this
morning. Scan found 2 real gappers (DFNS +55.7%, AMIX +17.4%) but both
are textbook speculative circuit-breaker pumps with no fundamental
catalyst — correctly filtered. Account still locked at 5 positions (1
over the 4-max cap).

## 📊 Pre-Market Gappers

**4 candidates** from the Alpaca screener path (real gap data):

| Symbol | Gap % | Price | Catalyst found | Notes |
|---|---|---|---|---|
| DFNS | +55.68% | $82.12 | Weak | Circuit-breaker halt pump, "what's driving the surge?" — no real catalyst |
| AMIX | +17.41% | $5.26 | Weak | Circuit-breaker halt pump (+116% at halt) — no fundamental driver |
| SNXX | -5.70% | $6.45 | No | No catalyst, no data |
| MUZ | +4.06% | $20.26 | No | No catalyst, no data |

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). DFNS and MUZ clear the
gap/price/prior-high checks but both fail on market cap, RVOL, and
SMA200 (DFNS's SMA200 of $325.53 vs an $82 price is a wild mismatch —
same stale/unadjusted-feed pattern seen on this thin microcap before).
Table empty.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. DFNS
and AMIX both clear gap/price/catalyst-flag, but fail market cap and
SMA200 — and neither has an actual fundamental catalyst, just
speculative momentum (both were halted on upside circuit breakers
yesterday). Table empty.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Big Tech earnings divergence**: Meta fell ~10% after close
  yesterday despite beating revenue ($60.8B vs $60.17B expected) —
  EPS missed badly ($6.18 vs $7.22 expected) and next-quarter revenue
  guidance ($62.5B) came in below the $63.15B consensus. Microsoft rose
  ~2% on the same evening, delivering on cloud growth expectations.
  Bloomberg's framing — "market growing skeptical of AI" — is the
  through-line: investors are now discriminating hard between AI capex
  that's paying off (Microsoft's cloud) and AI capex that isn't yet
  (Meta's guidance cut).
- **Apple reports today after the 4:00 PM ET close** — Tim Cook's last
  earnings call as CEO. Consensus: ~$108.9B revenue (+16% YoY), ~$1.89
  EPS (+20% YoY). The real swing factor is gross margin: Cook told the
  WSJ in June that iPhone/Mac/iPad price increases are "unavoidable"
  given the global memory-chip shortage — estimates of the necessary
  price hike range from JPMorgan's conservative ~$50 to TechInsights'
  ~$270 to hold Apple's ~47% margin. This is the single most relevant
  catalyst for the desk today (AAPL is a held position).
- Indexes are lower than Tuesday's levels (SPX 7,316 vs 7,428, NDX
  27,192 vs 27,763) — continuing yesterday's risk-off tape (Dow -1.6%,
  Nasdaq -1.1% on the day per TRADE-LOG) driven by the overnight Iran
  strikes, FOMC-day caution, and now the Meta miss weighing on
  sentiment into the open.
- VIX 19.37, up from Tuesday's 18.26 and roughly in line with
  yesterday's ~19.8 close — elevated but not panicked.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $63,901.24 vs daily SMA200
  $71,730.99 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-30_1109UTC.json`).
- **BTC** ~$64,000 (live), holding roughly flat — no fresh
  company-specific headline.
- **ETH** ~$1,917 (live), continuing to outperform BTC on the
  previously-noted Morgan Stanley low-cost ETH/SOL ETP rollout — a
  structural tailwind, not a today-specific move.
- **SOL** ~$74 (live), roughly flat, tracking the broader crypto chop.
- **NVDA** no Alpaca paper position (stopped out 7/28). No fresh
  company-specific headline; broader semis sentiment still soft after
  this week's China DUV-lithography and SK Hynix-miss overhang, now
  compounded by the AI-capex skepticism from Meta's miss.
- **ORCL** ~$119 (live premarket, +1.1%) — no material fresh headline;
  ongoing credit-risk/CDS-spread concerns from heavy AI infrastructure
  spend remain the dominant background story, offset by a record $638B
  backlog and continuing contract wins (Ontario healthcare rollout
  noted this week). No Alpaca paper position (stopped out 7/25).

## 📊 Technical Signals for Today

- SPX 7,316.15 · NDX 27,192.31 · RUT 2,906.31 (Robinhood index feed,
  Wednesday's close basis — yfinance snapshot path down again this run,
  connection reset on every index/rates/oil symbol).
- VIX 19.37 (live), up from Tuesday's 18.26, roughly matching
  yesterday's elevated close.
- 10Y yield: no live print again (yfinance ^TNX/^IRX connection reset);
  TRADE-LOG's Wednesday midday note had it around 4.61% on the Iran-news
  spike.
- Both real gappers today (DFNS, AMIX) are post-circuit-breaker
  momentum pumps, not clean gap-and-go setups — no gap-quality read
  worth making beyond "these are traps, not opportunities."

## 💰 Economic Data, Rates & the Fed

**Advance GDP q/q** (forecast 2.1%, prior 2.0%) and **Core PCE Price
Index m/m** (forecast 0.2%, prior 0.3%) both release at **8:30 AM ET**
today (ForexFactory live fetch, country=USD, impact=High) — both
tier-1. **§3b event blackout window in effect ~8:00–8:45 AM ET** (30
min before the release to 15 min after) — no new entries in that
window regardless of setup quality. No high-impact events found for
tomorrow (7/31). FOMC held rates steady yesterday at 3.50–3.75% as
consensus expected; no fresh Fed commentary scheduled today.

### Guardrail status (Zenith standing section)

- **Position count: 5 open (AAPL, VOO, BTC, ETH, SOL) vs the strategy's
  4-concurrent max.** Still 1 over the cap — no new agent entry
  permitted today regardless of scan results (moot anyway, nothing
  qualifies).
- Daily/weekly circuit breakers: not tripped. Equity $99,983.25 vs
  $100,000 baseline — flat. Week P&L (from Monday 7/27 baseline
  $100,004.42): roughly -$21, well inside the -4% weekly breaker.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): AAPL +8.4% unrealized, stop trailed to $331.61
  (locks in ~+2.03R). VOO -2.6%, BTC +0.6%, ETH +2.0%, SOL -2.8% — none
  near their stops.
- **AAPL earnings tonight is a real event-risk consideration** even
  though it's an existing position, not a new entry: a large post-earnings
  gap (either direction) could move price well outside the current
  $331.61 trailing stop's normal behavior. Nothing to do about it
  proactively under the current rules (the stop stands as-is; §3b's 24h
  no-entry window applies to new entries, not to managing an existing
  position), but flagging it for tomorrow morning's and tomorrow
  afternoon's position checks.
- No names besides AAPL are within 24h of earnings.

## 📅 Coming Up

- **Thursday 7/30 (today), 8:30 AM ET**: Advance GDP q/q + Core PCE —
  narrow blackout ~8:00–8:45 AM ET.
- **Thursday 7/30, after close**: **AAPL (held) reports — Tim Cook's
  final earnings call as CEO.** Amazon also reports tonight.
- **Friday 7/31**: no high-impact US events found yet; AAPL's
  post-earnings reaction will be the main story at the open.

## 🚫 Skips & Traps

- **DFNS (+55.68%, "T3 Defense Stock Soars")**: halted on an upside
  circuit breaker yesterday, up as much as 61% intraday — the
  headline itself asks "what's driving the surge?", a tell that this
  is speculative momentum, not a real catalyst. Correctly skipped: no
  market cap data, SMA200 wildly mismatched with price, no confirmed
  fundamental driver.
- **AMIX (+17.41%, "Autonomix Medical... Up 116.73%")**: same pattern —
  halted on an upside circuit breaker, no confirmed fundamental
  catalyst behind the medtech micro-cap pump. Correctly skipped.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — both real gappers today are
  circuit-breaker momentum pumps with no fundamental story, exactly
  what the rules are built to filter out regardless of how large the
  percentage move looks.
- **Rules vs discretion**: n/a today — nothing borderline.
- **Sharp catches**: the scan is quiet, but today's actual decision
  point is entirely off the scanner — Apple's earnings after the close
  (Tim Cook's last as CEO, gross-margin/price-increase story front and
  center) is a real event-risk factor for the held AAPL position, and
  this morning's GDP/PCE prints carry their own blackout window before
  that. The Meta/Microsoft earnings divergence overnight is also worth
  carrying forward as context for how the market will read Apple's
  numbers tonight.
- Nothing to trade, nothing forced. Stand aside on new entries (still
  over the position cap, and nothing qualifies anyway); respect this
  morning's GDP/PCE blackout window; watch AAPL's post-earnings
  reaction starting tomorrow.
