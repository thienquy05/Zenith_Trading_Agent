# 🧠 AI PREMARKET REPORT - Zenith

### Tuesday, July 21, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Risk sentiment is bouncing this morning on ceasefire hopes out of the
Iran war, even though nothing is actually resolved — futures are up,
chip stocks are recovering, and crypto is at a two-week high. Still moot
for new entries: the account remains at 7 concurrent positions, so no
new agent entry is permitted today regardless of the scan. All 4
gappers today are down-gaps, mechanically excluded, and none had a real
company-specific catalyst worth chasing on a bounce anyway. Rules and
discretion agree: stand aside, let the position count clear before
thinking about new setups.

## 📊 Pre-Market Gappers

**SNDQ** — "gap" -90.2% to $3.91 (prev close $40.00). No catalyst found,
no 200-day SMA data available. A move this size on a stock with
227k/day average volume is almost certainly either a reverse-split
artifact or a halt-resume after a severe move — not a tradeable premarket
gap either way. Flagged as unverified, treat with caution.

**ZYBT (Zhengye Biotechnology)** — gap -38.4% to $3.79 (prev close
$6.15). Real story: the stock spiked +780.8% intraday yesterday, got
circuit-breaker halted, and has now resumed trade fading hard. Classic
pump-and-dump aftermath — yesterday's move was the news, today is just
gravity.

**ADVB (Advanced Biomed)** — gap -19.6% to $7.27 (prev close $9.04).
Headline says "surging... here's why it's trending" but the stock is
actually down sharply today — reads like Monday's pop giving back
today. Still above its 200-day SMA ($6.26), unlike the other three
gappers.

**GMM** — gap -4.1% to $3.38 (prev close $3.52). Generic 12-stock
roundup mention, no real driver.

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it
today** — table empty. All 4 gappers are down, which alone disqualifies
them from a long-only gap-up strategy.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No
names cleared it today** — table empty, same reason (all down-gaps).

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Ceasefire hopes, not a resolution**: mediators (Qatar, Egypt,
  Pakistan, Oman) presented the US and Iran with a 10-day ceasefire
  proposal that would reopen the Strait of Hormuz and give both sides
  room to salvage the collapsing memorandum of understanding. Neither
  side has accepted it — both are reportedly trying to improve their
  leverage with further strikes first, and the US has moved dozens of
  fighter jets and refueling aircraft into the region, preparing for a
  possible major escalation even while exploring the truce. The US has
  now struck Iran for 10 consecutive nights. Confirmed via Axios, CNBC,
  and Jerusalem Post. Separately, Houthis are now threatening Saudi
  shipping — a widening, not narrowing, of the regional risk. Treat
  today's rally as hope-driven, not confirmation the conflict is over.
- **Market reaction is a relief bounce**: Nasdaq-100 futures +1.3% on a
  semiconductor recovery ahead of this week's Big Tech earnings, S&P
  futures +0.5%, Dow +0.3%. Oil eased on the ceasefire headlines after
  Monday's rally. Chip names (the group that led last week's selloff)
  are leading today's bounce.
- Earnings season is in focus this week: Alphabet, Intel, and Tesla all
  report — TSLA is one of Quy's real (dust) holdings, worth watching
  even though it's not a trade candidate here.
- Gapper set is entirely negative with no clean catalyst worth
  following — no sector signal to draw.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $65,206.45 vs daily SMA200
  $72,931.17 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-21_1109UTC.json`).
- **BTC** at a two-week high near $65,500 per market coverage, helped
  by the Asian semiconductor rebound spilling into risk assets broadly,
  plus five straight days of spot BTC ETF inflows totaling $600M+ — the
  strongest institutional buying stretch since mid-July.
- **ETH** ~$1,922, +3% on the day and +8% over the last week per market
  coverage — the stronger of the two majors this move.
- **SOL** ~$78, +2% on the day.
- **NVDA** $205.25 (live premarket) vs prior close $203.28, +1.0% —
  participating in the chip-sector recovery bounce.
- **ORCL** $122.49 (live premarket) vs prior close $121.38, +0.9% —
  also bouncing modestly, no new company-specific news found today.

## 📊 Technical Signals for Today

- SPX 7,443.28 · NDX 28,604.23 · RUT 2,942.43 (Robinhood index feed,
  yesterday's regular-session close — yfinance snapshot path blocked
  again this run).
- VIX 17.74, down slightly from Monday's 18.19 — easing a touch on the
  ceasefire-hope bounce, but still elevated relative to two weeks ago.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- All 4 gappers negative, no gap-quality read to make from this set.

## 💰 Economic Data, Rates & the Fed

Light data day by our tier-1 standard — 0 US high-impact events on
today's calendar (ForexFactory live fetch). No tier-1 print, no §3b
event blackout window today. Fed officials are reportedly entering the
pre-FOMC blackout period ahead of the July 29 decision (~85.6% priced
for a hold per yesterday's midday read).

### Guardrail status (Zenith standing section)

- **Position count: still 7 open (AAPL, NVDA, ORCL, VOO, BTC, ETH, SOL)
  vs the strategy's 4-concurrent max.** No new agent entry is permitted
  today regardless of scan results — third straight day flagging this
  standing condition.
- Daily/weekly circuit breakers: not tripped. Equity $99,999.08 vs
  $100,000 baseline — flat.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): all 7 positions healthy, none near their stops.
  AAPL leads at +4.6% (stop at breakeven); BTC/ETH/SOL all green on
  the crypto bounce; worst is ORCL at -4.2%, well clear of its $118.97
  stop.
- Elevated geopolitical risk remains a standing flag — today's relief
  rally is sentiment-driven, not a resolved conflict, so gap risk on
  the book (especially crypto, which trades through the weekend/news)
  stays elevated until there's an actual ceasefire agreement.
- No names within 24h of earnings on today's gappers (`next_earnings`
  null across the board — unknown, not a confirmed clear).

## 📅 Coming Up

- No US high-impact events surfaced for tomorrow (7/22) in this run's
  calendar pull yet — will confirm at the next run.
- **TSLA earnings this week** (Quy's real dust position) — watch for
  the print alongside Alphabet and Intel this week.
- Watch for either a confirmed Iran ceasefire (risk-on continuation) or
  a breakdown back into active strikes (risk-off reversal) — today's
  bounce could go either way fast.

## 🚫 Skips & Traps

- **SNDQ** — unverified -90% move, likely a data artifact or halt-
  resume after a severe decline; not tradeable information either way.
- **ZYBT** — real story, but it's yesterday's pump fading today, not a
  fresh catalyst. Don't buy the "resume trade" dip.
- **ADVB** — headline reads bullish but the price action says
  otherwise; Monday's pop giving back today.
- **GMM** — generic roundup mention, no real driver.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing here is tradeable, and the
  position-count cap would veto a new entry regardless. The rules
  reject all 4 gappers on gap direction alone; discretion independently
  reads each one as either an artifact or a fade, not an opportunity.
- **Rules vs discretion**: no disagreement today.
- **Sharp catches**: discretion's job today is separating "market is
  bouncing on hope" from "the underlying risk is resolved" — it isn't.
  Both sides are reportedly using this diplomatic window to improve
  their military position before deciding on the ceasefire, which means
  today's relief rally could reverse fast on either a breakdown in
  talks or a fresh escalation headline.
- Nothing to trade, nothing forced, and the position cap blocks new
  entries regardless. Stand aside; monitor the 7 open positions at the
  scheduled checkpoints and watch the Iran ceasefire headlines closely
  given the gap-risk this creates on the book.
