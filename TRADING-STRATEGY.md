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
  symbol. Signal lands just after 00:00 UTC (7 PM CT); execution waits
  for the 6 AM CT run — that ~11h gap is budgeted as slippage and is
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
- If equity draws down **-10% from its high-water mark**, stop opening
  new positions and Telegram Quy for a strategy review.

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

**Refresh**: recomputed every dashboard run alongside the Alpaca data (see
`AGENT-INSTRUCTIONS.md` → Dashboard procedure). Historicals calls easily
exceed tool output limits above ~5 symbols; request ≤10 symbols per call
and extract just `close_price` via `jq` rather than reading the raw
payload.

## 6. Review cadence

- Daily: snapshot + lessons in `TRADE-LOG.md` (3 PM run).
- Weekly (Fri): win rate, avg R won/lost, expectancy, rule violations,
  one change to test next week → `WEEKLY-REVIEW.md`.
- Any rule change gets recorded here with a date and a one-line reason.

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
