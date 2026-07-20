# 🧠 AI PREMARKET REPORT - Zenith

### Monday, July 20, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

The Iran conflict escalated hard over the weekend — this is no longer a
headline-risk story, it's a real shooting war with US casualties. Still
moot for new entries either way: the account remains at 7 concurrent
positions (Quy's manual trades from last Wednesday), so no new agent
entry is permitted today regardless of the scan. One gapper showed up
(BIYA), not eligible — another broken-trend name bouncing on a mismatched
roundup headline. Rules and discretion agree: stand aside, watch the
existing book.

## 📊 Pre-Market Gappers

**BIYA** — gap +18.5% to $4.93 (prev close $4.16). The attached headline
is actually about a different stock (Eva Live) inside a 20-symbol
roundup article — not a BIYA-specific catalyst. Price is above its
prior-day high but ~88% below its 200-day SMA ($39.75) — a severely
broken stock, not a breakout. `catalyst_found: true` on the packet's
keyword match only; there's no real BIYA news here.

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
names cleared it today** — table empty. BIYA clears the gap-size and
prior-high checks but fails on 200-day SMA (badly) and has no real
catalyst behind it, just a roundup mismatch.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Iran war has escalated sharply**: this weekend brought 2 US service
  members killed and 1 missing after an Iranian strike on a Jordan base
  (bringing the war's US death toll to 17 over ~5 months), plus another
  KIA from a downed-drone detonation in Iraq. Iran struck Jordan and
  Kuwait (both US-allied), including an oil-sector site in Kuwait. The
  US carried out its ninth consecutive night of strikes on Iran and has
  reimposed a naval blockade of Iranian ports; Iran reports 50+ killed,
  500+ injured from US strikes. Confirmed via CNN, Washington Post,
  Fox News, NPR, and Al Jazeera — this is a real, escalating conflict,
  not just headline noise.
- **Market reaction is oddly mixed**: some futures reads are higher on
  Trump framing Iran as "very, very badly damaged" (read as a
  de-escalation-through-dominance narrative by some traders), others
  show S&P futures down ~1%. Gasoline is back above $4/gallon on oil
  supply concerns. 10Y yield eased to ~4.5% on softer inflation data
  and safe-haven demand. Pending home sales fell 5.4% in June, mortgage
  rates ~6.55% — housing stocks under pressure.
- No sector signal to draw from a single low-float gapper.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $64,680.69 vs daily SMA200
  $73,048.92 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-20_1110UTC.json`).
- **BTC** pushed below $64k over the weekend on the Iran-escalation
  risk-off move per market coverage; live Alpaca spot in line with that
  read. Four mining pools now control over 70% of BTC hashrate — a
  centralization concern circulating separately from the price action.
- **ETH** — sensitive to BTC direction and the same risk-off flow;
  broader crypto tape started the week under pressure from higher oil,
  rising yields, and cautious tech sentiment.
- **SOL** — testing a $74-75 support zone as of Fri/Sat per market
  coverage, attributed to broad macro pressure rather than
  Solana-specific issues; fundamentals still constructive (Circle
  issued $500M in USDC on Solana, ~$900M in RWA inflows over 30 days).
- **NVDA** $205.20 (live premarket) vs prior close $202.81, +1.2% —
  a small bounce, no company-specific headline found today.
- **ORCL** $125.84 (live premarket) vs prior close $126.41, -0.5% —
  roughly flat, no new company-specific news today.

## 📊 Technical Signals for Today

- SPX 7,457.69 · NDX 28,592.66 · RUT 2,962.22 (Robinhood index feed,
  Friday's regular-session close — yfinance snapshot path blocked
  again this run — down across the board from Thursday's levels as
  last week's chip-sector selloff continued into Friday).
- VIX 18.19, essentially unchanged from Friday's 18.14 — still the
  week's highest read, holding elevated rather than resolving either
  direction as the Iran situation continues to develop.
- 10Y yield ~4.5% per market coverage (yfinance ^TNX/^IRX blocked, no
  live print in the packet).
- Single gapper today with no real catalyst behind it — no collective
  gap-quality read to make.

## 💰 Economic Data, Rates & the Fed

Light data day by our tier-1 standard — 0 US high-impact events on
today's calendar (ForexFactory live fetch). No tier-1 print, no §3b
event blackout window today.

### Guardrail status (Zenith standing section)

- **Position count: still 7 open (AAPL, NVDA, ORCL, VOO, BTC, ETH, SOL)
  vs the strategy's 4-concurrent max.** No new agent entry is permitted
  today regardless of scan results — same standing condition flagged
  Friday, unchanged over the weekend.
- Weekly new-entry cap: resets today (new week) — 0 agent-driven entries
  so far this week. The position-count cap is the binding constraint,
  not the weekly count.
- Daily/weekly circuit breakers: not tripped. Equity $100,009.10 vs
  $100,000 baseline — flat.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): all 7 positions came through the weekend healthy,
  none near their stops or -7%. AAPL leads at +7.2% (stop at breakeven
  $310.47); worst is ORCL at -1.6%, well clear of its $118.97 stop.
- Elevated geopolitical risk (active Iran war, US casualties, oil/gas
  price pressure) is a risk-awareness flag for the whole book,
  especially the crypto sleeve and any gap-risk on the open positions
  — not a scheduled-event blackout, but worth extra attention today.
- No names within 24h of earnings on today's one gapper (`next_earnings`
  null — unknown, not a confirmed clear).

## 📅 Coming Up

- No US high-impact events surfaced for tomorrow (7/21) in this run's
  calendar pull yet — will confirm at the next run.
- Watch the Iran situation for further escalation or any de-escalation
  signal; it's the dominant risk driver right now, more than anything
  on the scan.

## 🚫 Skips & Traps

- **BIYA** — bouncing on a mismatched roundup headline (the real story
  is about a different stock), while sitting ~88% below its 200-day
  SMA. Classic broken-stock pop, don't chase it.

---

## 🤖 Where rules and discretion landed

- **Agreement**: full agreement — nothing here is tradeable, and the
  position-count cap would veto a new entry even if something had
  cleared the screen. The rules reject BIYA on trend/mcap grounds;
  discretion independently catches that its catalyst headline isn't
  even about BIYA.
- **Rules vs discretion**: no disagreement today.
- **Sharp catches**: the read's real job this morning is geopolitical
  risk awareness, not stock-picking — the Iran war has moved from
  "tension" to "active conflict with US casualties" over the weekend,
  and that context matters more for position sizing and gap-risk than
  anything the gapper scan surfaced.
- Nothing to trade, nothing forced, and the position cap blocks new
  entries regardless. Stand aside; monitor the 7 open positions at the
  scheduled checkpoints today, with extra attention to weekend-gap-risk
  given the escalating conflict.
