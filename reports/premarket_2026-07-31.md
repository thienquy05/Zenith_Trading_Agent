# 🧠 AI PREMARKET REPORT - Zenith

### Friday, July 31, 2026 · Claude, rules + discretion passes

### Watchlists built by the rules: Day = Trend Join Long · Swing = gap-up + real catalyst

> Deterministic criteria (WATCHLIST_CRITERIA.md) decide who makes the list;
> the AI judges quality only. Premarket RVOL is true premarket volume when
> Alpaca data is live, full-day RVOL on the fallback path. Paper trading
> research, not financial advice.

## Summary

A genuine Big Tech earnings divergence closes out the week: Amazon
crushed estimates (EPS $5.75 vs $1.82 expected, AWS accelerating to its
fastest growth in 18 quarters) and is up ~8-12% premarket, drawing price
target raises from Barclays and JPMorgan (both to $365). Apple also
beat on revenue and EPS ($109.4B/$2.02 vs $108.65B/$1.89 estimates) but
is **down over 7% premarket** — a classic sell-the-news reaction after
~25% YTD gains, driven by a services miss, China revenue weakness, and
guidance citing supply constraints. The paper AAPL position was already
exited via trailing stop yesterday morning at $331.52 (+6.78%) — pure
mechanical trail discipline, not foresight, but it means today's drop
is not a live risk to the book. Indexes are broadly higher (SPX 7,437.63,
NDX 28,106.35) and VIX has eased sharply to 16.88 from Wednesday's 19.37
— Amazon/Microsoft strength is outweighing Meta's and now Apple's
weakness. AMZN itself shows up as an 8.27% gapper clearing every swing
check except market cap (a data-feed gap, not a real disqualifier for a
company this size) — correctly not promoted per the rules, but a clear
near-miss worth flagging. Account is exactly at the 4-position cap
(VOO/BTC/ETH/SOL) — no headroom for a new entry regardless.

## 📊 Pre-Market Gappers

**12 candidates** from the Alpaca screener path (real gap data) — the
largest batch in weeks, reflecting the post-earnings dispersion:

| Symbol | Gap % | Price | Catalyst found | Notes |
|---|---|---|---|---|
| AXTX | +64.3% | $7.64 | No | No catalyst, no data — skip |
| AXTU | +56.4% | $3.91 | No | No catalyst, no data — skip |
| PN | -16.01% | $19.68 | Weak | Generic "20 stocks moving" list mention only |
| IREX | +12.53% | $14.91 | No | No catalyst, no data |
| IRE | +11.60% | $10.49 | No | No catalyst, no data |
| NUWE | -10.49% | $4.01 | Weak | "Stock Explodes... what's driving?" — speculative pump |
| IREG | +10.49% | $8.11 | No | No catalyst, no data |
| **AMZN** | **+8.27%** | **$255.25** | **Yes** | **Real earnings beat + 2 analyst PT raises — see below** |
| SNDU | +7.23% | $17.64 | No | No catalyst, no data |
| SNXX | +6.51% | $11.13 | No | No catalyst, no data |
| SOXL | +3.83% | $119.42 | Weak | Leveraged semis ETF, sector-recovery mention, not company-specific |
| DFNS | -3.62% | $81.70 | Weak | Same "what's driving the momentum?" speculative pattern as prior days |

## ☀️ Day Trading Watchlist

Rule: `day_eligible: true` requires gap >3% (up), price >$3, market cap
>$1B, premarket RVOL >1.5x, price above prior-day high, and prior close
above the 200-day SMA (WATCHLIST_CRITERIA.md). **AMZN clears
gap/price/prior-high/SMA200 but fails on market cap** — a yfinance data
gap (mcap comes back null for every gapper this run), not a real
disqualifier for a >$2T company. SOXL also clears gap/price/prior-high/
SMA200 but is a leveraged ETF, not an equity the rule is built to
screen, and also fails mcap on the same data gap. Table empty per the
rules as written.

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📈 Notable Swing Watchlist

Rule: `swing_eligible: true` requires gap ≥8% (up), price >$3, open above
prior high and 200-day SMA, market cap ≥$800M, confirmed catalyst.
**AMZN clears every single check except market cap** (data gap only —
Amazon is unambiguously a mega-cap in reality). Per the standing rule,
never promote a ticker the packet's own flag didn't clear — table stays
empty — but this is the cleanest near-miss case since NOK (7/23) and
INTC (7/24), and worth calling out explicitly in Skips & Traps below.

| Ticker | Catalyst (headline) | Trend context | Idea | Conv. |
|---|---|---|---|---|
| — | — | — | — | — |

## 📉 Market Trends of the Day

- **Apple beats but sells off >7% premarket**: Q3 revenue $109.4B
  (+16% YoY, beat $108.65B est.), EPS $2.02 (+29% YoY, beat $1.89 est.),
  iPhone revenue $54.25B (+22% YoY, beat estimates). The drop is driven
  by a services miss ($30.74B vs $31.22B est.), Greater China weakness
  ($18.8B vs $19.5B est.), and weak forward guidance citing "supply
  constraints." Classic sell-the-news after the stock had already
  rallied ~25% YTD into the print — Tim Cook's final call as CEO ends
  with a rough market reaction despite the headline beat.
- **Amazon smashes estimates and rallies 8-12%**: EPS $5.75 vs $1.82
  expected, revenue $200.61B vs $196.47B expected. AWS revenue $42.2B,
  +36.7% YoY — the fastest AWS growth in 18 quarters, the single
  biggest driver of the reaction. Barclays and JPMorgan both raised
  price targets to $365 this morning.
- **The pattern from this week's Big Tech prints is now clear**:
  Microsoft (Tue, Azure >$100B revenue, +16% stock) and Amazon (AWS
  acceleration, +8-12%) both rallied hard on cloud/AI-infrastructure
  strength, while Meta (-10%, weak guidance) and now Apple (-7%,
  services/China miss + cautious guidance) both fell despite Apple's
  actual beat. The market is rewarding AI-infrastructure monetization
  and punishing anything that reads as consumer-demand or margin
  softness — a real, tradeable distinction for how to read the next
  round of earnings reactions.
- Indexes broadly higher: SPX 7,437.63 (up from Wednesday's 7,316.15),
  NDX 28,106.35 (up from 27,192.31) — Amazon/Microsoft strength
  outweighing Meta and Apple's drags at the index level.
- VIX 16.88 (live), down sharply from Wednesday's 19.37 — real
  risk-on tone into the weekend despite the mixed earnings reactions.

### Crypto regime + extra watch (Zenith standing section)

- **Regime: BEAR.** BTC prior close $64,728.66 vs daily SMA200
  $71,600.27 — sleeve stands down, no C-TJL entries today
  (`scan_crypto.py --no-telegram`, `scans/crypto_tjl_2026-07-31_1110UTC.json`).
- **BTC** ~$64,700 (live), holding up modestly — no fresh
  company-specific headline.
- **ETH** ~$1,890 (live), pulling back slightly overnight but still the
  relative outperformer on the week versus BTC.
- **SOL** ~$74 (live), roughly flat, still the laggard of the three.
- **NVDA** no Alpaca paper position (stopped out 7/28). One headline
  today worth flagging for awareness: "NVIDIA Stock Is Still Up, But
  $250 Billion AI Risk Has Spooked The Debt Market" — continued market
  chatter about the OpenAI financing-guarantee structure's credit-risk
  implications, the same story that first hit NVDA on 7/27. No new
  facts beyond what's already been tracked this week.
- **ORCL** no fresh headline today beyond yesterday's real Google Cloud
  Gemini AI partnership news (+7.1% on 7/30). No Alpaca paper position
  (stopped out 7/25).

## 📊 Technical Signals for Today

- SPX 7,437.63 · NDX 28,106.35 (Robinhood index feed, Thursday's close
  basis — yfinance snapshot path down again this run, connection reset
  on every index/rates/oil symbol; RUT quotes unavailable through the
  Robinhood MCP today, a tool-level restriction not a data outage).
- VIX 16.88 (live), down from Wednesday's 19.37 — genuine calming into
  the weekend.
- 10Y yield: no live print again (yfinance ^TNX/^IRX connection reset).
- AMZN's gap is the one real quality signal in today's batch — a
  confirmed, multi-sourced earnings beat with same-morning analyst
  target raises, clean price-above-prior-high and price-above-SMA200
  structure. Everything else in the batch is either a
  speculative/circuit-breaker pattern (DFNS, NUWE) or a no-catalyst
  gapper.

## 💰 Economic Data, Rates & the Fed

Zero US high-impact events today or tomorrow (ForexFactory live fetch,
country=USD, impact=High) — **no §3b event blackout window today.**
Yesterday's Fed speakers (Bullard, Logan, Barkin, Bostic) passed without
market disruption per the last midday log. A quiet close to a loaded
week (FOMC hold Wednesday, four Mag-7 earnings prints Tue-Thu).

### Guardrail status (Zenith standing section)

- **Position count: 4 open (VOO, BTC, ETH, SOL) — exactly at the
  strategy's 4-concurrent max**, no longer over it. AAPL's trailing
  stop filled at yesterday's open ($331.52, +6.78% realized, ~+2.0R) —
  a winning exit, not a stop-loss, and it happened to land the day
  before AAPL's post-earnings drop, pure trail-discipline timing, not
  foresight. No headroom for a new entry today even though nothing in
  the scan would qualify anyway (AMZN blocked only by the market-cap
  data gap, per the never-promote-unflagged rule).
- Daily/weekly circuit breakers: not tripped. Equity $99,988.52 vs
  $100,000 baseline — flat. Week P&L (from Monday 7/27 baseline
  $100,004.42): roughly -$16, well inside the -4% weekly breaker.
- **Position health check** (informational, full management happens at
  9:30/1:00/4:00): VOO -1.0%, BTC -0.4%, ETH +0.2%, SOL -3.1% — none
  near their stops.
- No held names within 24h of earnings.

## 📅 Coming Up

- **Friday 7/31 (today)**: no high-impact econ events. AAPL's and
  AMZN's post-earnings reactions play out through the session — worth
  watching how the divergence (AI-infra reward vs consumer-margin
  punish) holds up intraday.
- **Weekend**: no scheduled catalysts currently known; standard watch
  for any Iran/Middle East developments given this week's pattern of
  overnight surprises.
- **Monday 8/3**: new trading week begins — no specific catalysts
  identified yet in this run.

## 🚫 Skips & Traps

- **AMZN (+8.27%, real earnings beat + Barclays/JPMorgan PT raises to
  $365)**: the cleanest near-miss of the week. Clears every swing check
  except market cap, which is a yfinance data-gap artifact, not a real
  signal about Amazon's size. Correctly not promoted — the rules read
  the number as given, and the standing policy is never to override a
  data gap with judgment, however obvious the real answer is. Filed
  here as a near-miss for the record, same treatment as NOK (7/23) and
  INTC (7/24).
- **NUWE (-10.49%, "Nuwellis Stock Explodes... what's driving?")** and
  **DFNS (-3.62%, "T3 Defense Stock Continues Surge... what's driving?")**:
  same speculative-pump pattern flagged on both names in recent days —
  headlines that ask their own question are a tell. Correctly skipped.
- **PN (-16.01%)**: sizeable gap down, but its only "catalyst" is a
  generic 20-stock premarket-movers list mention — no real
  company-specific driver. Correctly skipped.

---

## 🤖 Where rules and discretion landed

- **Agreement**: near-full agreement — the only debatable case is AMZN,
  and even there the rules-vs-discretion gap isn't really a
  disagreement, it's a known data-quality limitation (yfinance mcap
  gaps have blocked several otherwise-clean setups this month: NOK,
  INTC, now AMZN).
- **Rules vs discretion**: AMZN would be an obvious swing-watchlist
  inclusion on judgment alone — real beat, real analyst confirmation,
  clean technical structure — but stays off per the never-promote rule.
  Consistent with how NOK and INTC were handled; flagging the recurring
  pattern again as a case for eventually hardening the market-cap data
  source (a static reference table for known mega/large-caps would
  fix this specific failure mode without loosening the rule for
  legitimate microcap uncertainty).
- **Sharp catches**: the real story of the week closes today — a market
  that is actively discriminating between AI-infrastructure monetization
  (Microsoft, Amazon: rewarded) and consumer-demand/margin softness
  (Meta, Apple: punished, even on a beat for Apple). Worth carrying this
  framework into how the next earnings prints get read.
- Nothing to trade, nothing forced. Stand aside on new entries (exactly
  at the position cap); AMZN filed as a near-miss, not traded; watch
  how AAPL's and AMZN's post-earnings moves settle through the session.
