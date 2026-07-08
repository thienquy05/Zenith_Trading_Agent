#!/usr/bin/env python3
"""C-TJL (Crypto Trend Join Long) backtest on Alpaca DAILY crypto bars.

Strategy (TRADING-STRATEGY.md §2c):
  entry  — daily bar (UTC-midnight aligned) closes above the highest high
           of the previous 55 daily bars AND above its daily SMA200,
           while the master regime gate (BTC prev daily close > BTC daily
           SMA200) is open. Entry at signal bar close.
  stop   — entry − 2.0 × ATR(14); target — entry + 3R (R = 2 × ATR).
  both hit in one bar counts as a stop (conservative); max hold 30 days
  (exit at close); 3-day cooldown per symbol after any exit; long only.

Costs: net figures subtract 0.6% of entry notional per round trip
(0.25% taker fee + 0.05% slippage, each side) expressed in R.

Why daily bars: the same breakout on 4H bars is gross-positive but net
NEGATIVE — with a 2-ATR(4H) stop (~2% of price) the 0.6% round trip is
~0.3R/trade and eats the edge (validated 2026-07-08, every 4H grid cell
lost over 12m and 48m). On daily bars the stop is ~7% of price, costs
~0.1R, and the 48-month grid is net positive across all cells.

Universe: fixed liquid-majors list (crypto has no gappers/watchlist flow;
the liquid set is stable). Override with --tickers BTC/USD,ETH/USD.

Usage: backtest_crypto.py [--tickers A,B] [--months 48] [--grid]
  --grid runs a small parameter grid (Donchian x ATR-mult x gate) to
  check robustness — neighbors of the chosen cell should not collapse.
Output: scans/backtest_crypto_<start>_<end>.json + printed stats
"""
import sys
from datetime import datetime, timedelta, timezone

from alpaca_common import SCANS, get_crypto_bars, load_env, save_json

UNIVERSE = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD",
            "DOGE/USD", "LINK/USD", "AVAX/USD", "LTC/USD"]
TF = "1Day"
DONCHIAN = 55          # breakout lookback, daily bars
ATR_LEN = 14
ATR_MULT = 2.0         # stop distance in ATRs
R_TARGET = 3.0
MAX_HOLD_BARS = 30     # days
COOLDOWN_BARS = 3      # days before re-entry
SMA_LEN = 200          # per-symbol daily trend filter
COST_PCT = 0.006       # round-trip fees+slippage as fraction of notional
REGIME_SMA_DAYS = 200  # master gate: BTC daily close > SMA200 = bull


def arg(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def atr_series(bars, n):
    """Wilder ATR; index-aligned with bars (None until warm)."""
    out = [None] * len(bars)
    trs = []
    for i, b in enumerate(bars):
        tr = (b["h"] - b["l"] if i == 0 else
              max(b["h"] - b["l"], abs(b["h"] - bars[i-1]["c"]),
                  abs(b["l"] - bars[i-1]["c"])))
        trs.append(tr)
        if i == n - 1:
            out[i] = sum(trs) / n
        elif i >= n:
            out[i] = (out[i-1] * (n - 1) + tr) / n
    return out


def btc_regime(start, end):
    """{date: True/False} — bull when BTC's PREVIOUS daily close > SMA200.
    The desk's master switch: no new crypto entries in a bear regime."""
    daily = get_crypto_bars(["BTC/USD"], "1Day",
                            start - timedelta(days=310), end=end)["BTC/USD"]
    daily.sort(key=lambda b: b["t"])
    regime = {}
    for i in range(REGIME_SMA_DAYS, len(daily)):
        sma = sum(b["c"] for b in daily[i - REGIME_SMA_DAYS:i]) / REGIME_SMA_DAYS
        regime[daily[i]["t"].date()] = daily[i - 1]["c"] > sma
    return regime


def backtest(sym, bars, donchian=DONCHIAN, atr_mult=ATR_MULT,
             use_sma=True, regime=None):
    atr = atr_series(bars, ATR_LEN)
    closes = [b["c"] for b in bars]
    trades, pos, cooldown_until = [], None, -1
    sma_sum = sum(closes[:SMA_LEN])
    for i in range(SMA_LEN, len(bars)):
        b = bars[i]
        sma = sma_sum / SMA_LEN
        sma_sum += closes[i] - closes[i - SMA_LEN]
        if pos:
            exit_px = why = None
            if b["l"] <= pos["stop"]:                 # stop first: conservative
                exit_px, why = pos["stop"], "stop"
            elif b["h"] >= pos["target"]:
                exit_px, why = pos["target"], "target"
            elif i - pos["i"] >= MAX_HOLD_BARS:
                exit_px, why = b["c"], "time"
            if exit_px is not None:
                gross_r = (exit_px - pos["entry"]) / pos["r"]
                cost_r = COST_PCT * pos["entry"] / pos["r"]
                trades.append({
                    "symbol": sym, "entry_time": pos["t"].isoformat(),
                    "exit_time": b["t"].isoformat(),
                    "entry": round(pos["entry"], 6),
                    "exit": round(exit_px, 6), "reason": why,
                    "gross_r": round(gross_r, 2),
                    "net_r": round(gross_r - cost_r, 2)})
                pos, cooldown_until = None, i + COOLDOWN_BARS
            continue
        if i <= cooldown_until or atr[i] is None:
            continue
        if regime is not None and not regime.get(b["t"].date(), False):
            continue                                  # bear regime: stay flat
        hh = max(x["h"] for x in bars[i - donchian:i])
        if b["c"] > hh and (not use_sma or b["c"] > sma):
            risk = atr_mult * atr[i]
            pos = {"entry": b["c"], "stop": b["c"] - risk, "r": risk,
                   "target": b["c"] + R_TARGET * risk, "t": b["t"], "i": i}
    return trades  # an open position at data end is simply not counted


def stats_for(trades, key="net_r"):
    if not trades:
        return {"trades": 0}
    wins = [t for t in trades if t[key] > 0]
    losses = [t for t in trades if t[key] <= 0]
    gw = sum(t[key] for t in wins)
    gl = -sum(t[key] for t in losses)
    return {"trades": len(trades),
            "win_rate_pct": round(100 * len(wins) / len(trades), 1),
            "total_r": round(sum(t[key] for t in trades), 2),
            "profit_factor": round(gw / gl, 2) if gl else None,
            "avg_win_r": round(gw / len(wins), 2) if wins else None,
            "avg_loss_r": round(-gl / len(losses), 2) if losses else None}


def main():
    load_env()
    override = arg("--tickers")
    syms = ([t.strip().upper() for t in override.split(",")] if override
            else UNIVERSE)
    months = int(arg("--months", 48))
    now = datetime.now(timezone.utc)
    bt_start = now - timedelta(days=months * 30)
    start = bt_start - timedelta(days=310)  # daily SMA200 warmup

    data = get_crypto_bars(syms, TF, start, end=now)
    data = {s: [b for b in bars if b["t"].date() < now.date()]  # drop the
            for s, bars in data.items()}          # incomplete "today" bar
    for s in syms:
        print(f"{s}: {len(data.get(s, []))} bars")
    regime = btc_regime(bt_start, now)
    bull_days = sum(regime.values())
    print(f"regime: bull on {bull_days}/{len(regime)} days in window")

    if "--grid" in sys.argv:
        print(f"\ngrid (net R | trades | PF), {bt_start.date()} → {now.date()}")
        for gate in (regime, None):
            for don in (20, 55):
                for mult in (1.5, 2.0, 2.5):
                    tr = [t for s in syms
                          for t in backtest(s, data.get(s, []), don, mult,
                                            regime=gate)]
                    st = stats_for(tr)
                    print(f"  gate={'Y' if gate else 'N'} don={don:2d} "
                          f"atr={mult:.1f} → {st.get('total_r', 0):>8} R | "
                          f"{st['trades']:3d} tr | PF {st.get('profit_factor')}")
        return

    all_trades = [t for s in syms
                  for t in backtest(s, data.get(s, []), regime=regime)]
    all_trades.sort(key=lambda t: t["exit_time"])
    peak = eq = 0.0
    max_dd = 0.0
    for t in all_trades:                      # equity curve in R, by exit
        eq += t["net_r"]
        peak = max(peak, eq)
        max_dd = max(max_dd, peak - eq)
    all_trades.sort(key=lambda t: t["entry_time"])
    stats = {
        "max_drawdown_r": round(max_dd, 2),
        "net": stats_for(all_trades, "net_r"),
        "gross": stats_for(all_trades, "gross_r"),
        "per_symbol": {s: {"trades": sum(t["symbol"] == s for t in all_trades),
                           "net_r": round(sum(t["net_r"] for t in all_trades
                                              if t["symbol"] == s), 2)}
                       for s in syms},
    }
    out = {"scanned_at": now.isoformat(),
           "params": {"tickers": syms, "months": months, "timeframe": TF,
                      "donchian": DONCHIAN, "atr_len": ATR_LEN,
                      "atr_mult": ATR_MULT, "r_target": R_TARGET,
                      "sma_filter": SMA_LEN, "max_hold_bars": MAX_HOLD_BARS,
                      "cooldown_bars": COOLDOWN_BARS,
                      "regime_gate": f"BTC daily close > SMA{REGIME_SMA_DAYS}",
                      "regime_bull_days": f"{bull_days}/{len(regime)}",
                      "round_trip_cost_pct": COST_PCT * 100},
           "stats": stats, "trades": all_trades}
    save_json(SCANS / f"backtest_crypto_{bt_start.date()}_{now.date()}.json",
              out)

    n, g = stats["net"], stats["gross"]
    print(f"\nC-TJL backtest {bt_start.date()} → {now.date()}")
    print(f"net:   {n['trades']} trades | win {n.get('win_rate_pct')}% | "
          f"{n.get('total_r')}R | PF {n.get('profit_factor')} | "
          f"avg win {n.get('avg_win_r')}R / loss {n.get('avg_loss_r')}R")
    print(f"gross: {g.get('total_r')}R | PF {g.get('profit_factor')} "
          f"(costs = {COST_PCT*100:.1f}%/round trip) | "
          f"max DD {stats['max_drawdown_r']}R")
    for s, row in stats["per_symbol"].items():
        print(f"  {s}: {row['trades']} trades, {row['net_r']}R")


if __name__ == "__main__":
    main()
