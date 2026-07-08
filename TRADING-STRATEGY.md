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
- **Candidate flow**: the 6:00 AM premarket gappers scan
  (`scripts/scan_gappers.py`) builds the day's watchlist; TJL then gates
  which of those (plus the core AMD/NVDA/MU test universe) are entries.
- Backtest (2026-01-09 → 2026-07-08, AMD/NVDA/MU, 5-min bars): 83
  trades, 32.5% win rate, +8.04R, profit factor 1.15. Positive
  expectancy but concentrated in MU — treat as validation of the
  mechanics, not proof of edge.

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
- **No overnight leverage; no options; no crypto** in v1. Equities only,
  liquid names (>1M average daily volume), price > $5.
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

## 5. Review cadence

- Daily: snapshot + lessons in `TRADE-LOG.md` (3 PM run).
- Weekly (Fri): win rate, avg R won/lost, expectancy, rule violations,
  one change to test next week → `WEEKLY-REVIEW.md`.
- Any rule change gets recorded here with a date and a one-line reason.

## Changelog

- 2026-07-08: v1 drafted by Claude (initial 3R/1R gap rulebook).
- 2026-07-08: added Strategy 2 (Trend Join Long) + scanners/backtest
  per Quy's spec; backtest baseline recorded.
