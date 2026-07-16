# 🧠 AI PREMARKET REPORT - Zenith

### Thursday, July 16, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

The quietest morning of the week: zero gappers cleared the scan's filter
and zero US high-impact econ events are on today's calendar. After two
straight days of CPI-then-PPI blackout windows, the macro calendar
finally clears. The catch we're watching: quiet doesn't mean nothing's
happening — UNH reports before the bell and NFLX after the close tonight,
neither a held name but both market-moving for sentiment. Rules and
discretion agree: there's nothing to screen because there's nothing here,
not because we're being cautious.

## 📊 Pre-Market Gappers

**None.** The scan's gap filter (>5% move, >$3 price, >50k premarket
volume via the keyless fallback path) returned zero candidates from 60
Alpaca-screener candidates today — a genuinely quiet premarket, not a
data-feed gap (the Alpaca candidate path worked fine, `gaps_to_fill`
only lists the usual yfinance-blocked items: RVOL/levels/earnings-calendar
detail, same as every run this week).

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

- **The CPI/PPI blackout run is over**: after Tuesday's CPI and
  Wednesday's PPI (both cooler than expected) and two days of Fed Chair
  Warsh testimony, today's calendar is genuinely clear — no tier-1 US
  print scheduled.
- Futures are mixed but leaning calmer: some reads show S&P futures
  +0.2% on eased inflation worries, others show -0.1% — nothing like
  this week's earlier volatility. 10Y yield has drifted down to ~4.57%
  as the softer CPI/PPI combo works through the market.
- **Earnings to watch (not held names, but market-moving)**: UnitedHealth
  Group (UNH) reports before the bell — cost trends and demand across
  healthcare services will move sentiment in that sector. Netflix (NFLX)
  reports after today's close — subscriber trends and content spend
  under the microscope, often a volatile after-hours mover.
- No gapper set to read a sector signal from today.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $64,724.27 vs daily SMA200
  $73,517.57 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-16_1112UTC.json`).
- **BTC** $64,117.94 (live), -0.9% vs today's session open ($64,714.30)
  — pulling back slightly after reclaiming $65k yesterday on the softer
  inflation data and $180M+ in spot ETF inflows ($139M into IBIT alone).
- **ETH** $1,885.08 (live), -1.6% vs today's open ($1,916.20) — also
  cooling off after a strong +2.6% move yesterday to ~$1,923.
- **SOL** $76.19 (live), -1.3% vs today's open ($77.21). Separately,
  Solana is reportedly capturing ~95% of tokenized-equity trading volume
  across blockchains (~$1.29B), a structural theme rather than a
  today-specific catalyst.
- **NVDA** $208.85 (live premarket) vs prior close $212.50, -1.7% — no
  company-specific headline found today.
- **ORCL** $134.00 (live premarket) vs prior close $132.49, +1.1% —
  continuing this week's bounce off Monday/Tuesday's slide. Note: an
  "Oracle" hack headline circulating today is about a DeFi price-oracle
  exploit on the Ostium protocol (~$18M), unrelated to Oracle Corp —
  flagging so it doesn't get confused with the ORCL position.

## 📊 Technical Signals for Today

- SPX 7,572.40 · NDX 29,502.60 · RUT 2,976.26 (Robinhood index feed,
  yesterday's regular-session close — yfinance snapshot path blocked
  again this run).
- VIX 16.10, down again from Wednesday's 16.38 — third straight session
  of cooling after last week's Iran-driven spike toward 17.5.
- 10Y yield ~4.57% per market coverage (yfinance ^TNX/^IRX blocked, no
  live print in the packet).
- No gappers today, so no gap-quality read to make.

## 💰 Economic Data, Rates & the Fed

**Light data day** — 0 US high-impact events on today's calendar
(ForexFactory live fetch). No tier-1 print, no §3b event blackout window
in effect today — the first clear morning since Monday.

### Guardrail status (Zenith standing section)

- Daily/weekly circuit breakers: not tripped. Equity $100,018.13 vs
  $100,000 baseline — up slightly, AAPL now +5.8% unrealized.
- Weekly entry cap: 0 of 5 used this week.
- No §3b blackout window today.
- No names within 24h of earnings (no gappers today to check against).
- No sector cap conflicts, no open crypto positions, no consecutive
  same-day stop-outs.

## 📅 Coming Up

- No US high-impact events surfaced for tomorrow (7/17) in this run's
  calendar pull yet — will confirm at the next run.
- NFLX reports after today's close; watch for after-hours volatility
  bleeding into tomorrow's premarket tape even though it's not a held
  name.

## 🚫 Skips & Traps

- Nothing to flag — there were no gappers to screen today.

---

## 🤖 Where rules and discretion landed

- **Agreement**: trivially in agreement — there's nothing to disagree
  about. Both passes see an empty gapper set and an empty calendar.
- **Rules vs discretion**: n/a today.
- **Sharp catches**: the read's job today is just noticing that "quiet"
  isn't the same as "nothing happening" — UNH and NFLX earnings, plus
  Solana's tokenized-equity volume share, are all real stories that
  don't touch our screens but are worth knowing about walking into the
  session.
- Nothing to trade, nothing forced. A clean, boring premarket after three
  straight days of macro-event traffic — take the breather.
