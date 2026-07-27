# 🧠 AI PREMARKET REPORT - Zenith

### Monday, July 27, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Real de-escalation this time, not just hope: the US and Iran paused
strikes over the weekend for a second consecutive night, and oil is
tumbling on it (Brent -4.4%, WTI -4.9%). Futures are strongly positive
into a loaded week — FOMC decision Wednesday (Fed Chair Warsh presiding)
and four Magnificent Seven earnings, including AAPL Thursday (Tim Cook's
final call as CEO). Zero gappers today, genuinely quiet premarket. Still
moot for new entries: the account is down to 6 positions after Friday's
ORCL stop-out, but that's still 2 over the 4-max cap. Rules and
discretion agree: stand aside, watch the book, note the loaded week
ahead.

## 📊 Pre-Market Gappers

**None.** The scan's gap filter returned zero candidates from 59
Alpaca-screener candidates today — genuinely quiet, not a data-feed gap
(the Alpaca candidate path worked fine; `gaps_to_fill` only lists the
usual yfinance-blocked items).

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it
today** — table empty, no gappers to screen.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No
names cleared it today** — table empty, no gappers to screen.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Real Iran de-escalation**: the US suspended strikes against Iran for
  a second straight night over the weekend, raising real hope that
  ceasefire negotiations restart after two weeks of active conflict.
  This is a materially different situation than last Monday's failed
  ceasefire-hope rally (which reversed within 24 hours on a Rubio
  comment) — two consecutive quiet nights is a stronger signal than a
  diplomatic proposal alone. Still worth treating as fragile given how
  fast this exact situation flipped last week.
- **Oil is tumbling**: Brent crude -4.4% to $87.64/bbl, WTI -4.9% to
  $84.91/bbl — a sharp reversal from last week's spike toward
  $94–100/bbl, consistent with the strikes pause easing Strait of
  Hormuz supply concerns.
- Futures are strongly positive: Dow and S&P futures both +0.8%,
  Nasdaq-100 futures +1.6%. Polymarket implies 88% odds of a green S&P
  open. VIX has eased to 17.66 this morning from Friday's 18.84.
- **A loaded week ahead**: FOMC rate decision Wednesday, presided by Fed
  Chair Kevin Warsh. Four Magnificent Seven names report this week —
  Meta, Microsoft, Amazon, and **Apple (AAPL, held here) on Thursday
  after close** — notably, Tim Cook's final earnings call as CEO. Not
  an immediate concern (3 days out, not inside the 24h no-entry window
  for new entries and this is an existing position, not a new one), but
  worth watching for volatility building into Thursday.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $65,334.77 vs daily SMA200
  $72,133.39 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-27_1123UTC.json`).
- **BTC** $65,166 (live), -0.3% vs today's session open ($65,339).
- **ETH** $1,962 (live), +0.5% vs today's open ($1,952) — continuing a
  strong stretch (the held Alpaca ETH position is now +4.5% since
  entry, its best showing yet).
- **SOL** $76.70 (live), roughly flat vs today's open ($76.66).
- **NVDA** $208.15 (live premarket) vs prior close $206.84, +0.6% —
  no company-specific headline found today.
- **ORCL** $117.88 (live premarket) vs prior close $114.99, +2.5% —
  continuing to bounce on Friday's $6.99B, 10-year DoD contract win
  (on-prem software across military branches/intel agencies) — a real,
  verified catalyst still working through the stock. Note: the Alpaca
  paper position in ORCL was stopped out Friday morning at -7.02%
  ($118.95) before this contract news broke; the Robinhood real
  position is still held.

## 📊 Technical Signals for Today

- SPX 7,411.98 · NDX 28,128.34 · RUT 2,930.00 (Friday's regular-session
  close per the Robinhood index feed — yfinance snapshot path blocked
  again this run).
- VIX 17.66 (live), down from Friday's 18.84 — cooling with the
  Iran-strikes pause and the oil selloff.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- No gappers today, so no gap-quality read to make.

## 💰 Economic Data, Rates & the Fed

Light data day — 0 US high-impact events on today's calendar
(ForexFactory live fetch). No tier-1 print, no §3b event blackout window
today. **FOMC rate decision Wednesday 7/29, 2:00 PM ET** (Fed Chair
Warsh presiding) — two days out, will trigger a blackout window as it
approaches; watch for that at Tuesday and Wednesday's runs.

### Guardrail status (Zenith standing section)

- **Position count: 6 open (AAPL, NVDA, VOO, BTC, ETH, SOL) vs the
  strategy's 4-concurrent max.** ORCL's Friday stop-out at -7.02% freed
  one slot (was 7), but the account is still 2 over the cap. No new
  agent entry is permitted today regardless of scan results.
- Daily/weekly circuit breakers: not tripped. Equity $100,008.07 vs
  $100,000 baseline — flat.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): all 6 positions healthy, none near their stops.
  AAPL leads at +7.6%; BTC and ETH both green on the weekend crypto
  strength.
- The stop-loss infrastructure did exactly what it's designed to do
  Friday — ORCL hit -7% and exited cleanly, no gap-through, no
  emergency action needed.
- No names within 24h of earnings today (no gappers to check against).
  AAPL's Thursday earnings noted above as a forward-looking watch item,
  not a current-day flag.

## 📅 Coming Up

- **Tuesday 7/28**: FOMC meeting begins (2-day meeting).
- **Wednesday 7/29, 2:00 PM ET**: FOMC rate decision — tier-1, will
  trigger a §3b blackout window.
- **Thursday 7/30, after close**: AAPL (held) and Amazon report
  earnings — one of the largest earnings days of the year, alongside
  Meta and Microsoft earlier in the week.

## 🚫 Skips & Traps

- Nothing to flag — there were no gappers to screen today.

---

## 🤖 Where rules and discretion landed

- **Agreement**: trivially in agreement — there's nothing to disagree
  about with an empty gapper set.
- **Rules vs discretion**: n/a today.
- **Sharp catches**: the read's job today is context-setting for a
  loaded week, not stock-picking — genuine (if fragile) Iran
  de-escalation, oil tumbling, and a Wednesday FOMC decision sandwiched
  between four Mag-7 earnings prints including Quy's own AAPL position
  Thursday. None of that touches today's empty scan, but all of it
  matters for how the next few days play out.
- Nothing to trade, nothing forced. Stand aside; monitor the 6 open
  positions at the scheduled checkpoints, and start tracking the
  approaching FOMC blackout window and AAPL's earnings date.
