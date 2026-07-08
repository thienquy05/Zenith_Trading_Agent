#!/usr/bin/env python3
"""Scanner B — Trend Join Long (TJL) entry criteria, right now.

PASS = daily breakout (price > previous daily high AND previous close >
SMA200) AND intraday breakout (price > premarket high AND price > today's
high-of-day so far, excluding the forming bar). Time-gated to
10:00–15:30 ET.

Telegram gating: sends only when this is the first run of the day, the
hit set changed vs the previous run today, or the scan errored. The
committed scan JSONs are the state (fresh cron containers keep nothing
else).

Usage: scan_tjl.py [--force] [--no-telegram] [TICKER ...]
Output: scans/tjl_watchlist_YYYY-MM-DD_HHMMET.json
"""
import sys
from datetime import datetime, timedelta
import json

from alpaca_common import (ET, SCANS, get_bars, latest_trades, load_env,
                           save_json, send_telegram)

DEFAULT_UNIVERSE = ["AMD", "NVDA", "MU"]


def prior_files(today_tag, current):
    return sorted(p for p in SCANS.glob(f"tjl_watchlist_{today_tag}_*.json")
                  if p != current)


def main():
    load_env()
    force = "--force" in sys.argv
    quiet = "--no-telegram" in sys.argv
    tickers = [a.upper() for a in sys.argv[1:] if not a.startswith("-")] \
        or DEFAULT_UNIVERSE

    now = datetime.now(ET)
    today = now.date()
    tag = f"{today}_{now:%H%M}ET"
    outfile = SCANS / f"tjl_watchlist_{tag}.json"

    gate_lo = now.replace(hour=10, minute=0, second=0, microsecond=0)
    gate_hi = now.replace(hour=15, minute=30, second=0, microsecond=0)
    if not (gate_lo <= now <= gate_hi) and not force:
        save_json(outfile, {"scanned_at": now.isoformat(),
                            "error": "outside 10:00-15:30 ET time gate"})
        print(f"outside time gate ({now:%H:%M} ET) — exiting cleanly")
        return

    hits, all_results, lines = [], [], []
    try:
        daily = get_bars(tickers, "1Day", now - timedelta(days=330))
        prices = latest_trades(tickers)
        intraday = get_bars(tickers, "1Min",
                            now.replace(hour=4, minute=0, second=0, microsecond=0))
        open_t = now.replace(hour=9, minute=30, second=0, microsecond=0)
        forming = now.replace(second=0, microsecond=0)

        for sym in tickers:
            done = [b for b in daily.get(sym, []) if b["t"].date() < today]
            if len(done) < 200 or sym not in prices:
                all_results.append({"symbol": sym, "result": "fail_daily"})
                lines.append(f"{sym}: fail_daily — insufficient data")
                continue
            prev_high, prev_close = done[-1]["h"], done[-1]["c"]
            sma200 = sum(b["c"] for b in done[-200:]) / 200
            px = prices[sym]

            bars = intraday.get(sym, [])
            pmh = max((b["h"] for b in bars if b["t"] < open_t), default=None)
            hod = max((b["h"] for b in bars
                       if open_t <= b["t"] < forming), default=None)

            daily_ok = px > prev_high and prev_close > sma200
            intra_ok = (pmh is not None and hod is not None
                        and px > pmh and px > hod)
            if daily_ok and intra_ok:
                result = "PASS"
                hits.append({"symbol": sym, "curr_price": round(px, 2),
                             "prev_daily_high": round(prev_high, 2),
                             "sma200": round(sma200, 2),
                             "pmh": round(pmh, 2),
                             "today_hod": round(hod, 2)})
                reason = f"px {px:.2f} > prev high {prev_high:.2f}, PMH {pmh:.2f}, HOD {hod:.2f}"
            elif not daily_ok:
                result = "fail_daily"
                reason = (f"px {px:.2f} ≤ prev high {prev_high:.2f}"
                          if px <= prev_high else
                          f"prev close {prev_close:.2f} ≤ SMA200 {sma200:.2f}")
            else:
                result = "fail_intraday"
                reason = (f"px {px:.2f} ≤ PMH {pmh:.2f}" if pmh and px <= pmh
                          else f"px {px:.2f} ≤ HOD {hod:.2f}" if hod
                          else "no intraday bars")
            all_results.append({"symbol": sym, "result": result})
            lines.append(f"{sym}: {result} — {reason}")
        error = None
    except Exception as e:
        error = str(e)

    out = {"scanned_at": now.isoformat(),
           "candidates_checked": len(tickers),
           "hits": hits, "all_results": all_results}
    if error:
        out["error"] = error
    prior = prior_files(today, outfile)  # before saving ours
    save_json(outfile, out)
    for ln in lines:
        print(ln)
    if error:
        print(f"scan error: {error}", file=sys.stderr)

    # Telegram gating
    should = error is not None or not prior
    if not should and prior:
        try:
            last = json.loads(prior[-1].read_text())
            should = ({h["symbol"] for h in last.get("hits", [])}
                      != {h["symbol"] for h in hits})
        except Exception:
            should = True
    if should and not quiet:
        if error:
            body = f"⚠️ TJL scan error: {error}"
        elif hits:
            body = "\n".join([f"🎯 *TJL Watchlist* — {now:%H:%M} ET"] + [
                f"• {h['symbol']} @ ${h['curr_price']} (PMH ${h['pmh']}, "
                f"prev\\_high ${h['prev_daily_high']}, SMA200 ${h['sma200']})"
                for h in hits])
        else:
            body = f"🎯 *TJL Watchlist* — {now:%H:%M} ET\nNo TJL hits this run."
        send_telegram(body)
    elif not should:
        print("telegram: suppressed (no change vs previous run today)")


if __name__ == "__main__":
    main()
