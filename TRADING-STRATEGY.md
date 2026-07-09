# TRADING-STRATEGY.md — current rulebook

> **Status: DRAFT v1 — written by Claude, awaiting Quy's edits.**
> Quy: the gap definition in §2 is my interpretation of "find the gap
> (middle of the lowest bar to the increasing bar)" — please correct it
> if I read you wrong. Everything else is standard risk discipline you
> can tighten or loosen.

## 1. Core: 3R/1R

Every trade risks **1R** to make **3R**.

- **1R (the risk unit)** = entry price − stop price, in dollars per
  share. Dollar risk per trade = **≤1% of account equity**.
- **Position size** = floor(equity × 1% ÷ (entry − stop)) shares.
- **Target = entry + 3 × (entry − stop)** — a 3:1 reward-to-risk. With
  3R targets, ~1 winner in 3 trades breaks even; anything better
  compounds.
- Enter with a **bracket order** (entry + stop + 3R target in one call)
  so no position ever exists without its stop.

## 2. Strategy 1 — the gap setup (long)

Worked on intraday bars (15Min default) or daily bars for swing entries.

1. **Find the low**: locate the lowest bar of the recent decline (the
   swing low).
2. **Find the turn**: the first clearly increasing (bullish) bar after
   it — closes above its open and above the prior bar's close.
3. **The gap zone** = the price span from the **midpoint of the lowest
   bar** ((high+low)/2 of that bar) up to the **open of the increasing
   bar**. This is the imbalance the market left behind when it turned.
4. **Entry**: wait for price to pull back and retest the gap zone;
   enter inside the zone (limit order at the zone's upper half).
5. **Stop (1R)**: just below the low of the lowest bar. If that makes
   1R > 1% of equity at minimum size, skip the trade.
6. **Target (3R)**: entry + 3 × (entry − stop). Set as the take-profit
   leg of the bracket.
7. **Invalidation**: a close below the lowest bar's low before entry
   fills = setup dead, cancel the order.

Shorts are the mirror image (allowed only if the account supports it;
skip shorts in v1).

## 2b. Strategy 2 — Trend Join Long (TJL)

Join an already-trending name when it breaks to new highs on every
timeframe at once. Implemented by `scripts/scan_tjl.py` (live check) and
`scripts/backtest_tjl.py` (historical test).

- **Daily condition**: price > previous daily high AND previous close >
  SMA200 (only join uptrends at breakout).
- **Intraday condition**: price > premarket high AND price > today's
  high-of-day so far.
- **Time gate**: entries only 10:00–15:30 ET (skip the open's chop,
  nothing new near the close).
- **Exits (3R/1R, same as Strategy 1)**: stop = signal bar low (1R),
  target = +3R, force-flat 15:55 ET, one trade per ticker per day.
- **Candidate flow — no fixed universe**: the 6:00 AM premarket run picks
  2–3 actionable ideas and writes their tickers to
  `scans/watchlist_<date>.json`; `scan_tjl.py` and `backtest_tjl.py` both
  resolve their universe from that file first, falling back to the
  latest gappers scan top-10 if no watchlist exists yet, then failing
  cleanly (no trade-worthy candidates) rather than defaulting to any
  hardcoded tickers.
- Backtest baseline (2026-01-09 → 2026-07-08, AMD/NVDA/MU as a fixed
  test set, 5-min bars, run before the dynamic-universe change): 83
  trades, 32.5% win rate, +8.04R, profit factor 1.15. Positive
  expectancy but concentrated in MU — treat as validation of the
  mechanics, not proof of edge. Re-run periodically against the
  dynamic watchlist to see if the edge holds on live candidates.

## 2c. Strategy 3 — Crypto Trend Join Long (C-TJL), regime-gated

The crypto sleeve. Implemented by `scripts/scan_crypto.py` (live check,
runs in the 6 AM and 12 PM workflows) and `scripts/backtest_crypto.py`.
Alpaca paper crypto: 24/7, long-only, fractional, **no bracket orders**.

- **Master regime gate (the rule that matters most)**: no new crypto
  entries unless **BTC's previous daily close > its daily SMA200**. In a
  bear regime the sleeve is FLAT — cash is the position. Validation
  showed every long-only entry style (breakout and mean-reversion alike)
  loses in a bear tape; the gate kept the sleeve out of the entire
  2025–26 down year at a cost of ~4R over the 48-month test.
- **Universe**: fixed liquid majors — BTC, ETH, SOL, XRP, DOGE, LINK,
  AVAX, LTC (all /USD). Fixed is deliberate: crypto has no daily
  gappers/catalyst flow and the liquid set is stable. Review monthly.
- **Entry (DAILY bars, UTC-midnight aligned)**: most recent completed
  daily bar closes above the highest high of the previous 55 daily bars
  AND above its own daily SMA200. Enter at market at the next wake-up.
  Daily, not 4H, is a validation result, not a style choice: the same
  breakout on 4H bars is gross-positive but **net negative** — with a
  2-ATR(4H) stop (~2% of price) Alpaca's ~0.6% round trip costs ~0.3R
  per trade and eats the edge. On daily bars the stop is ~7% of price
  and costs shrink to ~0.1R.
- **Stop (1R)**: entry − 2.0 × ATR(14, daily) — signal-bar lows are too
  tight on crypto bars; ATR is the natural stop unit. Placed as a
  **stop_limit GTC immediately after the entry fill** (two calls — no
  brackets in crypto). Limit leg 0.5% below the stop.
- **Target (3R)**: entry + 6 × ATR. A resting GTC limit sell is NOT
  placed — the stop_limit already consumes the position qty (wash-trade
  rule); the agent takes the 3R exit at a wake-up, or trails per §3.
  Max hold 30 days, then exit at market.
- **Cooldown**: 3 days per symbol after any exit; one position per
  symbol. Signal lands just after 00:00 UTC (8 PM EDT); execution waits
  for the 7 AM ET run — that ~11h gap is budgeted as slippage and is
  exactly what the live paper gate below measures.
- **Sizing — validation phase**: risk **0.25% of equity** per trade
  (half the sleeve's normal 0.5%, which is half the equities 1%) until
  the paper gate below is passed. Max **2 concurrent crypto positions**,
  sleeve notional cap **20% of equity**, single position cap 10%.
- **Costs are real**: ~0.25% taker fee + slippage per side. The backtest
  charges 0.6%/round trip; with a 1.5-ATR stop that's roughly 0.1–0.3R
  per trade — thin setups aren't worth taking.

### Validation status (paper gate)

- **Backtest baseline (2022-07-29 → 2026-07-08, 48 months, daily bars,
  0.6%/round-trip costs)**: 77 trades, 39.0% win rate, **+23.34R net**,
  PF 1.50, avg win +2.33R / avg loss −0.99R, max drawdown 8.45R
  (≈2% of equity at 0.25% risk). Positive in 5 of 8 pairs (ETH +8.4R,
  XRP +7.8R, LINK +5.3R, LTC +4.7R, BTC +1.9R; SOL/DOGE/AVAX small
  negatives) — not concentrated in one name. Robustness: every
  neighboring grid cell (Donchian 20/55 × ATR 1.5/2.0/2.5) is also net
  positive, PF 1.07–1.51. Full record:
  `scans/backtest_crypto_2022-07-29_2026-07-08.json`.
- **What failed validation and was rejected**: the identical breakout on
  4H bars (all 18 grid cells negative over both 12m and 48m — costs eat
  the gross edge) and 4H mean-reversion dip-buying (all 8 variants
  negative). Long-only crypto without the regime gate also loses in the
  current bear tape. These are recorded so we don't re-test them fresh.
- **Live paper gate before full 0.5% sizing**: ≥15 sleeve trades OR 8
  weeks elapsed with the gate open, net expectancy ≥ 0R and no risk-rule
  violations. Until then: 0.25% risk. Bear-regime weeks don't count —
  flat is correct behavior, not missing data. As of 2026-07-08 the
  regime is BEAR (BTC ~$63.3k vs SMA200 ~$74.5k): the sleeve is live but
  correctly flat, waiting for the gate to open.
- Re-run `backtest_crypto.py` monthly (and at every regime flip) and
  record the result in `WEEKLY-REVIEW.md`.

## 2d. Rule upgrades from the §7 research (validation results)

Added 2026-07-09 from the expert-source research in §7; validated the
same day per Quy's backtest-gated-adoption decision — evidence from
papers is a reason to test, not a reason to trade. Outcome: **R1
rejected by backtest, R2 adopted as a conservative pre-filter** pending
its live-sample review.

- **R1 — TJL "stock in play" filter: TESTED 2026-07-09 → REJECTED.**
  Proposal was: TJL entries require relative volume ≥ 1.5–2× the
  14-session same-minute average (source: SSRN 4729284, §7). The gate
  was run (`backtest_tjl.py --rvol`, AMD/NVDA/MU, 6mo, same window as
  baseline) and the filter FAILED it badly: baseline 84 trades / PF 1.20
  / +11.0R vs rvol≥1.5× 14 trades / PF 0.24 / −9.3R and rvol≥2× 7
  trades / PF 0.50 / −3.0R. Interpretation: the paper's in-play edge is
  about *universe selection* (scanning the whole market each morning
  for elevated-volume news names — which our gappers-scan→watchlist
  flow already does), not an intraday volume gate on names that are
  already liquid; on mega-caps, mid-session volume spikes mark chaos,
  not follow-through. IEX-only volume (undercounted, per Gotchas) also
  makes the ratio noisy. Verdict: **not adopted** — the in-play concept
  stays implemented at the universe level, where it already lives. The
  `--rvol` flag stays in `backtest_tjl.py` for future re-tests on
  watchlist-style universes. Full records:
  `scans/backtest_tjl_2026-01-10_2026-07-09*.json`.
- **R2 — gap setup quality filter: still pending (needs live samples).**
  A §2 gap setup is tradeable only on a **catalyst-confirmed,
  high-relative-volume gap** (≥3× relative volume or a named news
  catalyst); no-news, low-volume gaps are skipped. Source:
  gap-continuation research (§7) — follow-through concentrates in
  catalyst+volume gaps; quiet gaps tend to fade. **Gate**: log every §2
  setup taken/skipped with its volume+catalyst state for 20+ setups,
  then compare. Cannot be backtested today — there is no §2 gap-setup
  backtester and zero live §2 trades yet (checked 2026-07-09). Since
  R2 only *restricts* entries (never adds risk) and §4 already demands
  a catalyst, it is applied as a **conservative pre-filter effective
  immediately**, with the formal keep/drop decision after 20 logged
  setups.
- **Honesty note on §2 itself**: the gap-zone/retest entry is the
  component with the *weakest* external evidence (§7 grades it weak —
  practitioner claims only, no peer-reviewed support). Until we have our
  own §2 trade sample, the §4 catalyst filter and the 3R/1R bracket are
  what carry that strategy, not the zone geometry.

## 3. Risk & portfolio rules

- Max **1% of equity risked per trade**; max **4 concurrent positions**;
  max **25% of equity in any single position** (notional).
- Hard exit at **-7%** from entry regardless of thesis — no averaging
  down, ever.
- Exit immediately if the **thesis breaks** (the catalyst reversed, the
  gap zone failed on a closing basis), even if -7% hasn't hit.
- **Trailing stops on winners**: at +2R unrealized, raise stop to
  breakeven; past +2.5R, trail below each new higher low (or use a 3%
  trailing stop) while keeping the 3R take-profit.
- **No overnight leverage; no options.** Equities: liquid names (>1M
  average daily volume), price > $5. Crypto only via the §2c sleeve and
  its own caps (0.25–0.5% risk, 2 positions, 20% notional, regime gate) —
  no discretionary crypto trades outside the sleeve.
- No new entries in the last 30 minutes of the session.
- Max **2 new positions per day** — quality over activity.
- Max **5 new positions per week** (Mon–Fri, equities + crypto sleeve
  combined; exits don't count). Once the 5th entry of the week is on,
  the desk only manages — count entries in `TRADE-LOG.md` before every
  new trade. (Quy's rule, 2026-07-08.)
- If equity draws down **-10% from its high-water mark**, stop opening
  new positions and Telegram Quy for a strategy review.

## 3b. Guardrails (added 2026-07-08 — non-negotiable, checked before EVERY entry)

These exist because most beginner losses come from a handful of known
failure modes, not from bad stock picks. Guardrails don't create profit
directly — they keep the account alive long enough for the 3R/1R edge
to compound, which is where the profit actually comes from. Every
guardrail check (pass or fail) that blocks a trade gets one line in
`TRADE-LOG.md` so Quy can learn the pattern.

1. **Daily circuit breaker**: if day P&L hits **-2% of equity**, no new
   entries for the rest of the day (managing/exiting open positions is
   still required). Telegram immediately. *Failure mode it stops:
   revenge trading a bad tape.*
2. **Weekly circuit breaker**: if the week is down **-4%**, no new
   entries until Monday; Friday's review must name what went wrong.
3. **Weekly trade cap**: max **5 new entries per week** across equities
   and the crypto sleeve (see §3). The count resets Monday; check
   `TRADE-LOG.md` for this week's entries before every new position.
4. **Tilt stop**: after **2 consecutive stop-outs in the same day**,
   done entering for the day even if the daily breaker hasn't tripped.
   *Two stops in a row usually means the read on the tape is wrong.*
5. **Event blackout**: no new entries from **30 minutes before to 15
   minutes after** a tier-1 macro release (FOMC statement/minutes, CPI,
   PPI, NFP, GDP). The 7 AM research run lists today's blackout
   windows. *Spreads blow out and stops get run through news candles.*
6. **Earnings no-entry**: no new position in a name reporting earnings
   within the next **24 hours** — a coin-flip gap is gambling, not a
   setup. (Holding through earnings an existing winner is allowed only
   past +2R with the stop at breakeven or better.)
7. **Correlation cap**: max **2 open positions in the same sector or
   theme** (e.g. two AI-memory names = at the cap). Four positions in
   one theme is one position at 4× size.
8. **Spread check**: skip the trade if the bid-ask spread is more than
   **10% of 1R** — the edge leaks out through the spread on entry+exit.
9. **No averaging down. Ever.** (Restating §3 because it's the single
   most account-destroying habit.)
10. **Data-blind = flat**: if the Alpaca API (or price data) fails such
   that positions can't be checked, take no new entries and Telegram
   the failure immediately.
11. **Honesty rule**: any violated guardrail is confessed in
    `TRADE-LOG.md` and the weekly review the same day. Hidden mistakes
    can't be learned from.

## 4. Trade selection filter (from research)

A candidate needs ALL of:
1. A concrete catalyst today/this week (earnings, data, sector move).
2. A valid gap setup per §2 (or a clearly-defined equivalent entry with
   a natural stop level — flag any non-gap entry in the log).
3. Reward:risk ≥ 3:1 to a realistic target.
4. Liquidity filter above.

## 5. Robinhood advisory signals (read-only, informational only)

Quy's real Robinhood accounts are **never traded by Claude** (hard rule,
`CLAUDE.md`). This section only governs how the dashboard's buy/hold/sell
badges are computed for display — Quy places every Robinhood order
himself.

**Inputs** (Robinhood MCP connector, refreshed each dashboard run):
- RSI(14) on daily closes (Wilder smoothing) over ~200 trading days.
- Price vs 50-day and 200-day simple moving average.
- Next earnings date (`get_earnings_calendar`) for held/watchlist names.

**Zone thresholds** (RSI is primary; MA position adds context):
- RSI < 30 → 🟢 **STRONG BUY ZONE** (oversold).
- RSI 30–40 → 🟢 **FAVOURABLE ENTRY** ("ADD ZONE" if already held).
- RSI 40–60 → 🟡 **NEUTRAL — DCA** (no edge either way; steady/DCA only).
- RSI 60–70 → 🟡 **HOLD — pause new buys** (getting extended).
- RSI > 70 → 🔴 **TRIM ZONE** (overbought; consider trimming 10–25%).
- Extra flag regardless of RSI: price **>15% above its 200-day MA** →
  note "extended" (e.g. a name up huge off a rally — RSI can look neutral
  while the trend is stretched).
- Earnings within 14 days → caution note: size down or wait for the print.

**Selling discipline** (adapted from the -7% Alpaca rule for buy-and-hold
real accounts, which carry no stop-loss orders):
- Never sell 100% at once — trim in tranches (10–25% into strength).
- Rebalance the crypto sleeve back toward its target split; don't predict.
- Don't panic-sell on red days — Extreme Fear has historically rewarded
  patient DCA buyers, not sellers.
- VOO in the Roth is the multi-decade core holding — it is never flagged
  for the Trim Zone; only "neutral/DCA" or a genuine >70 RSI extended
  reading changes its badge, and even then the note says "trim never
  sell the core."
- These are informational signals only — Quy acts on them manually.

**Extra-watch list (Quy's standing request, 2026-07-08)**: **BTC, ETH,
SOL, NVDA, ORCL** — the names Quy actually holds real money in. Rules:
- Every scheduled Telegram brief carries live prices, day moves, and
  position values for these five.
- All position values come from the Robinhood connector LIVE at run
  time — never hardcoded, never reused from a previous run ("get a
  real/current number always").
- Material news on any of them (earnings, guidance, regulatory action,
  sector shock, crypto regime flip) is flagged in the same run's
  Telegram message, not held for the next scheduled brief.
- New Robinhood positions or deposits discovered on a pull are folded
  into the watch automatically and noted once in the next brief.

**Refresh**: recomputed every dashboard run alongside the Alpaca data (see
`AGENT-INSTRUCTIONS.md` → Dashboard procedure). Historicals calls easily
exceed tool output limits above ~5 symbols; request ≤10 symbols per call
and extract just `close_price` via `jq` rather than reading the raw
payload.

## 6. Review cadence

- Daily: snapshot + lessons in `TRADE-LOG.md` (4 PM ET run).
- Weekly (Fri): win rate, avg R won/lost, expectancy, rule violations,
  one change to test next week → `WEEKLY-REVIEW.md`.
- Any rule change gets recorded here with a date and a one-line reason.

## 7. Evidence base & measured performance (added 2026-07-09)

Why each rule earns its place, what the published evidence says, and
what OUR OWN backtests actually measure. Verification method: SSRN
blocks direct fetching, so every paper's numbers were cross-checked
across at least two independent write-ups (QuantConnect, CXO Advisory,
Robust Trader, Quantpedia, the authors' own Concretum site) before being
cited here — same two-source rule we apply to trade catalysts.

### 7a. Metric definitions (plain language)

- **Win rate**: % of trades that close positive. Low win rate is FINE if
  winners are big — our whole design is ~35–40% win rate × 3R winners.
- **Expectancy**: average R earned per trade. +0.30R means a typical
  trade nets +0.30× the dollars risked. Positive expectancy is the edge;
  everything else is decoration.
- **Profit factor (PF)**: gross wins ÷ gross losses. >1 profitable,
  ~1.5 solid for a retail system, >2 suspicious (usually overfit).
- **Sharpe ratio**: return per unit of volatility. Rule of thumb: <0.5
  weak, ~1 good, ~2 excellent, >3 almost never real out-of-sample. We
  compute it per-trade on R-multiples and annualize by √(trades/year).
- **Sortino ratio**: Sharpe but only penalizing downside volatility —
  kinder to strategies with big winners (like 3R/1R), which Sharpe
  unfairly punishes for upside variance.
- **Max drawdown (DD)**: worst peak-to-trough equity drop. In R units
  here; multiply by risk-per-trade for the % hit (8.9R × 0.25% ≈ 2.2%).
- **95% bootstrap CI on expectancy**: resample our own trades 10,000×;
  if the interval includes 0, the sample can't statistically rule out
  "no edge." Run `python3 scripts/strategy_metrics.py <backtest.json>`
  to reproduce every number below.

### 7b. Our measured numbers (as of 2026-07-09)

| Metric | TJL (equities, 5-min, 6mo) | C-TJL (crypto, daily, 48mo) |
|---|---|---|
| Trades | 83 (~179/yr) | 77 (~28/yr) |
| Win rate | 32.5% | 39.0% |
| Avg win / avg loss | +2.34R / −0.99R | +2.33R / −0.99R |
| Profit factor | 1.15 | 1.50 |
| Expectancy | +0.097R/trade (+8.04R net) | +0.303R/trade (+23.34R net) |
| Expectancy 95% CI | **[−0.25R, +0.47R] — includes 0** | **[−0.07R, +0.70R] — includes 0** |
| Max drawdown | 10.1R | 8.9R |
| Sharpe (annualized est.) | 0.78 | 0.92 |
| Sortino (annualized est.) | 1.59 | 2.03 |

**Read the CI row first.** Both sleeves are net positive with healthy
Sortinos, but neither sample statistically excludes zero edge yet.
That is exactly why sizing is small (0.25–1% risk) and why the §2c
paper gate exists. The gap setup (§2) has NO backtest sample yet —
zero measured statistics, evidence grade weak.

### 7c. Evidence per component (source → verified stat → why we picked it)

| Our rule | Expert source | Verified stat | Why it's in the book | Grade |
|---|---|---|---|---|
| Momentum breakout entries w/ bracket stops, EoD exit (TJL, §2b) | Zarattini & Aziz 2023, *Can Day Trading Really Be Profitable?* (SSRN 4416622) | 5-min ORB on QQQ 2016–23: +675% net (TQQQ +1,484%), Sharpe 1.12, alpha 33% | Peer-circulated proof that rule-based intraday momentum with hard stops beat buy-and-hold net of costs — the template TJL follows | Strong |
| Catalyst + relative-volume selection (§4, §2d-R1) | Zarattini, Barbon & Aziz 2024, *A Profitable Day Trading Strategy for the US Equity Market* (SSRN 4729284) | ORB on top-20 "Stocks in Play": +1,600% net 2016–23, Sharpe 2.81, alpha 36%, hit ratio ~43% w/ convex payoff | The single biggest documented edge-multiplier: same entry, but only in high-relative-volume news names. Our gappers scan ≈ their stock-in-play screen | Strong |
| Low win rate × 3R design (§1) | Same two papers + trend-following literature | Profitable at 35–43% win rates because avg win ≫ avg loss | Frees us from needing to predict; we need 1-in-3, not most, to be right. Matches our measured 32.5%/39% × +2.3R | Strong |
| Donchian-55 breakout (C-TJL, §2c) | Lempérière et al. *Two Centuries of Trend Following*; Moskowitz, Ooi & Pedersen 2012 *Time Series Momentum* (J. Fin. Econ.) | Trend following: Sharpe ~0.4 avg across 67 markets 1880–2016, positive every decade; TSMOM positive in all 58 futures tested | Century-scale, every-asset-class evidence that breakout/trend entries have a real, persistent edge — the strongest-documented anomaly we use | Strong |
| BTC > SMA200 regime gate (§2c) | Faber, *A Quantitative Approach to Tactical Asset Allocation* (SSRN 962461) | 10-mo (~200d) SMA filter: equity-like returns, max DD cut from 46% to <10%, net of costs | Cheapest known drawdown protection; our own 48-mo backtest agrees (gate cost ~4R, avoided the entire 2025–26 bear) | Strong |
| Hard stops on every position (§1, §3) | Kaminski & Lo, *When Do Stop-Loss Rules Stop Losses?* (J. Fin. Markets 2014) | Stops ADD value in momentum regimes (+50–100bp/mo during stop-outs); they SUBTRACT value in mean-reversion/random-walk regimes | Our strategies are momentum-type — precisely the regime where the academic result says stops help. (Corollary: don't bolt stops onto DCA/value holdings like VOO — §5 correctly uses trims, not stops) | Strong |
| Gap-zone retest entry (§2) | Practitioner only (edgeful YM-futures stats, ICT/FVG community; a 2026 MNQ falsification study found gap-fill fades fail at every tested entry) | Claimed 60%+ win rates WITH confluence; no peer-reviewed support; counter-evidence exists | Kept because it gives a natural stop (structure low) and pairs with §4 catalysts — but flagged: weakest link, backtest-gated (§2d) | **Weak** |
| 1% risk cap, circuit breakers, guardrails (§3, §3b) | Brazil day-trader study (Chague et al., FGV: 97% of 300+-day day traders lose; 0.4% beat minimum wage); Taiwan 15-yr study (Barber et al.: <1% reliably profitable net of fees) | The base rate for discretionary day trading is catastrophic | The guardrails ARE the response to the base rate: the papers show blow-ups come from oversizing, revenge trading and no stops — the exact failure modes §3b bans | Strong |

### 7d. Real-money warning (Quy — read before mirroring any trade)

Quy has said he may mirror these trades with real money if the record
earns trust. Conditions before that's reasonable, stated plainly:

1. **The statistical bar isn't met yet.** Both sleeves' expectancy CIs
   include zero (§7b). Mirroring now = betting on a promising but
   unproven sample. Wait for the §2c paper gate (and a TJL equivalent:
   ≥100 trades with CI > 0) before real dollars.
2. **Paper fills are optimistic.** Alpaca paper assumes perfect fills at
   quoted prices — no slippage, no partial fills, no borrow costs, no
   queue position. Real results on identical signals WILL be worse;
   budget ~0.1–0.3R/trade of degradation (that alone would currently
   put TJL near zero).
3. **The base rate is the enemy.** 97% of persistent day traders lost
   money in the Brazil study; <1% were reliably profitable in Taiwan.
   Assume we are not special until ≥100 live trades say otherwise.
4. **If mirroring ever starts**: half the paper size for the first
   month, only sleeves that passed their gates, never a trade that's
   already moved past its entry zone, and every §3b guardrail applies
   doubly. Never mirror the §2 gap setup until it has its own measured
   sample.
5. **Nothing here is financial advice.** It's a monitored experiment
   with a written rulebook — that's its only claim.

### 7e. Keeping this honest

- Re-run `scripts/strategy_metrics.py` on every new backtest and after
  every ~20 live paper trades; update §7b (this table is versioned, not
  append-only — but log the change here and in the changelog).
- A rule whose evidence grade is *weak* for two more review cycles with
  no supporting sample gets retired or demoted to paper-only.
- Sources are cited so Quy can verify independently: SSRN 4416622,
  SSRN 4729284, SSRN 962461, Kaminski & Lo (J. Financial Markets),
  Moskowitz/Ooi/Pedersen (J. Financial Economics 2012), Chague et al.
  (FGV Brazil), Barber/Lee/Liu/Odean (Taiwan).

## Changelog

- 2026-07-08: v1 drafted by Claude (initial 3R/1R gap rulebook).
- 2026-07-08: added Strategy 2 (Trend Join Long) + scanners/backtest
  per Quy's spec; backtest baseline recorded.
- 2026-07-08: removed the fixed AMD/NVDA/MU universe from `scan_tjl.py`
  and `backtest_tjl.py` — both now resolve tickers from the day's
  research watchlist, then the gappers scan, per Quy's feedback that a
  hardcoded list isn't a flexible/realistic practice.
- 2026-07-08: added §5, Robinhood advisory signals (RSI/MA/earnings-based
  buy/hold/sell badges for the read-only Robinhood dashboard section),
  ported from Quy's cowork portfolio dashboard concept.
- 2026-07-08: added §2c, the crypto sleeve (C-TJL). Validation journey:
  4H breakout and 4H mean-reversion both failed (net negative after
  costs, all parameter cells, 12m and 48m windows); daily-bar Donchian-55
  breakout with BTC>SMA200 regime gate passed (+23.34R net / PF 1.5 over
  48 months). Sleeve live at 0.25% risk pending the paper gate; regime
  currently BEAR so the sleeve is flat. Order mechanics verified on
  paper (crypto = no brackets, stop_limit placed as second call).
- 2026-07-08: added §3b guardrails (daily/weekly circuit breakers, tilt
  stop, event blackout, 24h earnings no-entry, correlation cap, spread
  check) and the §5 extra-watch list (BTC/ETH/SOL/NVDA/ORCL, live
  Robinhood numbers only) per Quy's request. All schedule references
  relabeled from Central to Eastern time (same instants — the Routines
  were already ET-aligned); Telegram policy changed to
  every-main-run-reports, TJL hourly trade-only.
- 2026-07-08: added the weekly trade cap — max 5 new entries per week,
  equities + crypto sleeve combined, reset Monday (§3 + §3b.3) — per
  Quy's request.
- 2026-07-09: added §7 (evidence base & measured performance — expert
  sources verified via 2-source rule, metric definitions, measured
  Sharpe/Sortino/PF/win-rate tables from `scripts/strategy_metrics.py`,
  per-rule evidence grades, real-money warning) and §2d (backtest-gated
  rule upgrades R1 relative-volume TJL filter + R2 gap quality filter),
  per Quy's request to enhance the strategy with verified expert
  research. New script `scripts/strategy_metrics.py`. Rule changes are
  pending validation, not live (Quy's choice: backtest-gated adoption).
- 2026-07-09 (later): §2d gates run per Quy's "validate then merge".
  R1 (intraday relative-volume gate on TJL) REJECTED — failed its
  backtest decisively (PF 1.20/+11.0R baseline → PF 0.24/−9.3R at
  rvol≥1.5×; the in-play edge belongs at universe selection, where the
  gappers scan already applies it). R2 (gap quality filter) adopted as
  a conservative pre-filter — restriction-only, keep/drop after 20
  logged §2 setups. `backtest_tjl.py` gained a reusable `--rvol` flag.
