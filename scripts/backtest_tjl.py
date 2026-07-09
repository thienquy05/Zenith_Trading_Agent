#!/usr/bin/env python3
"""TJL strategy backtest on Alpaca historical 5-min bars (incl. premarket).

Universe (no fixed ticker list): today's research watchlist
(scans/watchlist_<date>.json) if present, else the top-10 symbols from the
latest scans/premarket_gappers_*.json; --tickers A,B,C overrides both.
NOTE: backtesting *today's* candidates over a past window carries selection
bias — it answers "how does TJL behave on names like these," not "could
I have picked them then."

Rules (mirror scan_tjl.py + the 3R/1R rulebook):
  entry  — close of the first 5-min bar in 10:00–15:30 ET where
           close > prev daily high, prev close > SMA200,
           close > premarket high, close > HOD before the bar
  stop   — signal bar low (1R); target — entry + 3R
  both hit in one bar counts as a stop (conservative); flat 15:55 ET;
  one trade per ticker per day.

Optional --rvol X (strategy §2d-R1, backtest-gated): only take signals
where cumulative session volume at the signal bar is ≥ X× the average
cumulative volume at that same minute over the prior 14 sessions (the
"stock in play" measure from SSRN 4729284). Off by default.

Usage: backtest_tjl.py [--tickers AMD,NVDA,MU] [--months 6] [--rvol 1.5]
Output: scans/backtest_tjl_<start>_<end>[_rvolX].json + printed stats table
"""
import bisect
import sys
from collections import defaultdict
from datetime import datetime, timedelta

from alpaca_common import ET, SCANS, get_bars, load_env, resolve_universe, save_json

LOOKBACK_MONTHS = 6
TF = "5Min"
R_TARGET = 3.0
RVOL_LOOKBACK = 14   # sessions of volume history behind the rvol ratio
RVOL_MIN_DAYS = 5    # min prior sessions before the ratio is trusted


def arg(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def universe():
    override = arg("--tickers")
    cli = [t.strip().upper() for t in override.split(",")] if override else None
    syms, source = resolve_universe(cli)
    if not syms:
        sys.exit(f"no universe available ({source}) — run scan_gappers.py "
                 f"first, write a watchlist, or pass --tickers A,B,C")
    print(f"universe: {', '.join(syms)} ({source})")
    return syms


def backtest(sym, bars5, daily, trade_from=None, rvol=None):
    """Return list of trade dicts for one symbol. Days before trade_from
    supply volume history for the rvol filter but never trade."""
    # prior-day aggregates keyed by date
    done = sorted(daily, key=lambda b: b["t"])
    daily_meta = {}
    for i in range(200, len(done)):
        d = done[i]["t"].date()
        prev = done[i - 1]
        sma = sum(b["c"] for b in done[i - 200:i]) / 200
        daily_meta[d] = (prev["h"], prev["c"], sma)

    by_day = defaultdict(list)
    for b in bars5:
        by_day[b["t"].date()].append(b)

    # per-day cumulative volume profile: day -> (minute list, cumvol list)
    profiles = {}
    for day, bars in by_day.items():
        mins, cum, tot = [], [], 0
        for b in sorted(bars, key=lambda b: b["t"]):
            tot += b.get("v", 0)
            mins.append(b["t"].hour * 60 + b["t"].minute)
            cum.append(tot)
        profiles[day] = (mins, cum)
    session_days = sorted(profiles)

    def cum_at(day, minute):
        mins, cum = profiles[day]
        i = bisect.bisect_right(mins, minute) - 1
        return cum[i] if i >= 0 else 0

    def in_play(day, minute):
        """cum volume now vs same-minute average of prior sessions."""
        prior = session_days[max(0, bisect.bisect_left(session_days, day)
                                 - RVOL_LOOKBACK):
                             bisect.bisect_left(session_days, day)]
        if len(prior) < RVOL_MIN_DAYS:
            return False
        base = sum(cum_at(d, minute) for d in prior) / len(prior)
        return base > 0 and cum_at(day, minute) / base >= rvol

    trades = []
    for day, bars in sorted(by_day.items()):
        if day not in daily_meta or (trade_from and day < trade_from):
            continue
        prev_high, prev_close, sma200 = daily_meta[day]
        if prev_close <= sma200:
            continue
        bars.sort(key=lambda b: b["t"])
        pmh = max((b["h"] for b in bars if b["t"].hour * 60 + b["t"].minute < 570),
                  default=None)
        if pmh is None:
            continue
        hod, pos = None, None
        for i, b in enumerate(bars):
            mins = b["t"].hour * 60 + b["t"].minute
            if mins < 570:            # before 09:30
                continue
            if pos is None and 600 <= mins <= 930:   # 10:00–15:30 gate
                if (b["c"] > prev_high and b["c"] > pmh
                        and hod is not None and b["c"] > hod
                        and (rvol is None or in_play(day, mins))):
                    entry, stop = b["c"], b["l"]
                    if entry > stop:  # need positive R
                        pos = {"entry": entry, "stop": stop,
                               "r": entry - stop,
                               "target": entry + R_TARGET * (entry - stop),
                               "etime": b["t"]}
            elif pos:
                if b["l"] <= pos["stop"]:            # stop first (conservative)
                    exit_px, why = pos["stop"], "stop"
                elif b["h"] >= pos["target"]:
                    exit_px, why = pos["target"], "target"
                elif mins >= 955:                    # 15:55 flat
                    exit_px, why = b["c"], "eod"
                else:
                    hod = max(hod or 0, b["h"])
                    continue
                trades.append({
                    "symbol": sym, "date": str(day),
                    "entry": round(pos["entry"], 2),
                    "exit": round(exit_px, 2), "reason": why,
                    "r_multiple": round((exit_px - pos["entry"]) / pos["r"], 2)})
                pos = None
                break                                # one trade/ticker/day
            hod = max(hod or 0, b["h"])
        if pos:                                      # day ended mid-trade
            trades.append({"symbol": sym, "date": str(day),
                           "entry": round(pos["entry"], 2),
                           "exit": round(bars[-1]["c"], 2), "reason": "eod",
                           "r_multiple": round(
                               (bars[-1]["c"] - pos["entry"]) / pos["r"], 2)})
    return trades


def main():
    load_env()
    months = int(arg("--months", LOOKBACK_MONTHS))
    rvol = arg("--rvol")
    rvol = float(rvol) if rvol else None
    syms = universe()
    now = datetime.now(ET)
    start = now - timedelta(days=months * 30 + 320)
    bt_start = now - timedelta(days=months * 30)
    # extra 30 days of 5-min bars so the rvol filter has full volume
    # history from day one; days before bt_start never trade
    bars5_start = bt_start - timedelta(days=30)

    all_trades = []
    for sym in syms:                                 # sequential: rate limits
        try:
            daily = [b for b in get_bars([sym], "1Day", start)[sym]
                     if b["t"].date() < now.date()]
            bars5 = [b for b in get_bars([sym], TF, bars5_start)[sym]]
            all_trades += backtest(sym, bars5, daily, bt_start.date(), rvol)
            print(f"{sym}: fetched {len(bars5)} bars, "
                  f"{sum(t['symbol'] == sym for t in all_trades)} trades")
        except Exception as e:
            print(f"{sym}: SKIPPED — {e}", file=sys.stderr)

    wins = [t for t in all_trades if t["r_multiple"] > 0]
    losses = [t for t in all_trades if t["r_multiple"] <= 0]
    gross_w = sum(t["r_multiple"] for t in wins)
    gross_l = -sum(t["r_multiple"] for t in losses)
    stats = {
        "total_trades": len(all_trades),
        "win_rate_pct": round(100 * len(wins) / len(all_trades), 1) if all_trades else None,
        "total_r": round(sum(t["r_multiple"] for t in all_trades), 2),
        "profit_factor": round(gross_w / gross_l, 2) if gross_l else None,
        "avg_win_r": round(gross_w / len(wins), 2) if wins else None,
        "avg_loss_r": round(-gross_l / len(losses), 2) if losses else None,
        "per_ticker": {s: {"trades": sum(t["symbol"] == s for t in all_trades),
                           "total_r": round(sum(t["r_multiple"]
                                                for t in all_trades
                                                if t["symbol"] == s), 2)}
                       for s in syms},
    }
    out = {"scanned_at": now.isoformat(),
           "params": {"tickers": syms, "months": months, "timeframe": TF,
                      "rvol_filter": rvol,
                      "rules": "entry TJL 10:00-15:30 ET; stop=signal bar low; "
                               "target=+3R; flat 15:55; 1 trade/ticker/day"
                               + (f"; rvol>={rvol}x vs {RVOL_LOOKBACK}-session "
                                  f"same-minute avg" if rvol else ""),
                      "selection_bias_note": "universe picked from today's "
                      "gappers; past-window results describe behavior, not "
                      "an achievable historical portfolio"},
           "stats": stats, "trades": all_trades}
    suffix = f"_rvol{rvol:g}" if rvol else ""
    save_json(SCANS / f"backtest_tjl_{bt_start.date()}_{now.date()}{suffix}.json",
              out)

    print(f"\nTJL backtest {bt_start.date()} → {now.date()} on {', '.join(syms)}"
          + (f" [rvol ≥ {rvol:g}x]" if rvol else ""))
    print(f"trades {stats['total_trades']} | win rate {stats['win_rate_pct']}% | "
          f"total {stats['total_r']}R | PF {stats['profit_factor']} | "
          f"avg win {stats['avg_win_r']}R / avg loss {stats['avg_loss_r']}R")
    for s, row in stats["per_ticker"].items():
        print(f"  {s}: {row['trades']} trades, {row['total_r']}R")


if __name__ == "__main__":
    main()
