# 🧠 AI PREMARKET REPORT - Zenith

### Friday, July 17, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

Moot morning for new entries regardless of what the scan found: the
account is carrying 7 concurrent positions (Quy's manual trades from
yesterday's open pushed it well past the strategy's 4-max) so no new
agent entry is permitted today under §3, full stop. The scan found 2
gappers anyway, neither eligible. Iran/US tension has an easing tone this
morning (Trump says Iran wants to negotiate) after Wednesday's VIX spike
toward 19, but the reading is still elevated. Rules and discretion agree:
nothing to trade, and the account's own position count would veto it
even if there were.

## 📊 Pre-Market Gappers

**ATPC** — gap +9.65% to $4.66 (prev close $4.25). "Catalyst" is a
12-symbol healthcare roundup headline, not company-specific. Price is
~75% below its 200-day SMA ($18.34) — this is a severely broken
downtrend stock bouncing on no real news, not a breakout.

**STAK** — gap -4.5% to $3.40 (prev close $3.56). Real headline ("What's
Going On With STAK Shares On Thursday?") but vague, and the stock
circuit-breaker-halted up 46% back in June before fading hard since —
another one that's cooled off, not heating up. Down-gap regardless.

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **No names cleared it
today** — table empty.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst. **No
names cleared it today** — table empty. ATPC clears the gap-size bar but
fails on prior-day-high, 200-day SMA, and a real catalyst; it's a roundup
mention, not news.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Iran tension, tentatively easing**: stocks rallied Thursday after
  President Trump said Iran called to make a deal; Qatar and Pakistan
  are reportedly brokering "technical talks" to bring the US and Iran
  back to the table. VIX had spiked toward 19 on Wednesday; some
  coverage has it easing back toward the 15 range, though our live
  read this morning (18.14) is still elevated — treat the de-escalation
  as tentative, not confirmed.
- Oil is behaved for now (WTI ~$71.59/bbl, -$0.49), a tell that the
  market isn't pricing a near-term supply shock.
- **Today's data is lower-tier, not tier-1**: June housing starts,
  building permits, industrial production, and the preliminary July
  University of Michigan consumer sentiment read are all on today's
  calendar but none trigger a §3b blackout (ForexFactory's high-impact
  filter returned 0 events today). Travelers, Truist, and Fifth Third
  report earnings today — regional bank read-through, not held names.
- Yesterday's session was red on chip-sector weakness (TSM beat but
  sold off on spending concerns, dragging NVDA and the complex) — that
  weakness is still visible in this morning's NVDA premarket print.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $63,783.12 vs daily SMA200
  $73,397.04 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-17_1111UTC.json`).
  Crypto Fear & Greed reads 27 (Fear) per market coverage.
- **BTC** $63,077 (live), -1.1% vs prior close — broader crypto market
  down ~1.6% in the last 24h per market coverage, tracking dollar/yield
  sensitivity and semiconductor weakness.
- **ETH** $1,834 (live), down alongside BTC.
- **SOL** $74.79 (live), also lower; a Solana-lending-pool exploit on
  DeFiTuna (~$580K, already patched) is circulating but is a minor,
  protocol-specific story, not a SOL-wide driver.
- **NVDA** $202.10 (live premarket) vs prior close $207.40, -2.6% —
  continuing yesterday's chip-sector weakness (TSM spending-concern
  selloff), no new NVDA-specific headline found today.
- **ORCL** $122.64 (live premarket) vs prior close $124.21, -1.3% —
  continuing its pullback from earlier in the week; no new
  company-specific news found today.

## 📊 Technical Signals for Today

- SPX 7,533.77 · NDX 29,025.77 · RUT 2,974.57 (Robinhood index feed,
  yesterday's regular-session close — yfinance snapshot path blocked
  again this run — down across the board on yesterday's chip selloff).
- VIX 18.14, up from Thursday's 16.10 — the week's high read so far
  this run, consistent with the Iran-tension headline risk even as some
  coverage frames it as de-escalating.
- 10Y yield: no live print again (yfinance ^TNX/^IRX blocked).
- Only 2 gappers today, one up (roundup non-catalyst, broken trend) one
  down (real but vague catalyst) — no collective read to draw.

## 💰 Economic Data, Rates & the Fed

Light data day by our tier-1 standard — 0 US high-impact events on
today's calendar (ForexFactory live fetch). Housing starts/permits,
industrial production, and UMich consumer sentiment (prelim) are
scheduled but don't trigger a §3b blackout. No tier-1 print, no event
blackout window today.

### Guardrail status (Zenith standing section)

- **Position count: 7 open (AAPL, NVDA, ORCL, VOO, BTC, ETH, SOL) vs
  the strategy's 4-concurrent max.** Quy placed all 6 non-AAPL
  positions manually yesterday morning outside the research workflow
  (confirmed in the 7/16 09:41 AM open log). **No new agent entry is
  permitted today regardless of scan results** — the account is already
  over the position cap. This is independent of today's finding zero
  qualifying setups anyway.
- Weekly new-entry cap: 6 used this week, all Quy's manual trades (0
  agent-driven entries this week) — also already past the 5/week cap
  for the account as a whole.
- Daily/weekly circuit breakers: not tripped. Equity $100,000.16 vs
  $100,000 baseline — flat.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): none of the 7 positions are near their stops or the
  -7% hard-bail level. Worst is ORCL at -4.2% (stop at $118.97, ~3%
  cushion remaining). AAPL is the standout at +7.2%, stop already
  trailed to breakeven ($310.47).
- No names within 24h of earnings on today's gappers (`next_earnings`
  null for both — unknown, not a confirmed clear).

## 📅 Coming Up

- No US high-impact events surfaced for tomorrow (7/18, Saturday —
  markets closed) in this run's calendar pull.
- Next week: watch for the position-count situation to normalize as
  positions close out or Quy consolidates; until then this section of
  the guardrail check will keep flagging "no new agent entries" as the
  standing condition, not a one-off.

## 🚫 Skips & Traps

- **ATPC** — bouncing on a generic roundup mention, not real news, and
  still ~75% below its 200-day SMA. Classic dead-stock pop, don't chase.
- **STAK** — real but vague headline, down-gap, already faded from a
  June circuit-breaker halt. Skip.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing here is tradeable, and even a
  clean setup would be vetoed by the position-count guardrail today.
  The rules reject both gappers on trend/mcap grounds; discretion
  independently reads ATPC's catalyst as noise and STAK's as stale.
- **Rules vs discretion**: no disagreement today.
- **Sharp catches**: the read's job today is mostly account hygiene, not
  stock-picking — flagging that yesterday's manual trades changed the
  playing field (7 positions, cap breached) so today's screen result is
  almost beside the point. Worth Quy's attention: the strategy's
  guardrails assume agent-only trading: they don't auto-adjust when
  manual trades are layered in.
- Nothing to trade, nothing forced, and nothing would clear the position
  cap even if it wanted to. Stand aside; monitor the 7 open positions at
  the scheduled checkpoints today.
