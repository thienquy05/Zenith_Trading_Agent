#!/usr/bin/env python3
"""Scanner A — premarket gappers (Alpaca).

Universe = screener top gainers ∪ most-actives. For each candidate the
gap is computed from real premarket trades: last 1-min premarket price
vs previous daily close. Filters: gap > 5%, price > $3, premarket
volume > 50,000 (IEX feed — undercounts consolidated volume). Top 10 by
gap kept. Headlines come from Alpaca's news API (Benzinga content);
`catalyst` defaults to the top headline — the agent rewrites it into a
one-sentence summary before it reaches Telegram/the dashboard.

Usage: scan_gappers.py [--no-telegram]
Output: scans/premarket_gappers_YYYY-MM-DD.json
"""
import sys
from datetime import datetime, timedelta

from alpaca_common import (DATA, ET, SCANS, get, get_bars, load_env,
                           save_json, send_telegram)

GAP_MIN, PRICE_MIN, PMVOL_MIN, TOP_N, CAND_CAP = 5.0, 3.0, 50_000, 10, 60


def candidates():
    syms, seen = [], set()
    for url, key in ((f"{DATA}/v1beta1/screener/stocks/movers?top=50", "gainers"),
                     (f"{DATA}/v1beta1/screener/stocks/most-actives?by=volume&top=50",
                      "most_actives")):
        try:
            for row in get(url).get(key, []):
                s = row["symbol"]
                if s not in seen and s.isalpha():  # skip warrants/units etc.
                    seen.add(s)
                    syms.append(s)
        except Exception as e:
            print(f"screener {key} failed: {e}", file=sys.stderr)
    return syms[:CAND_CAP]


def main():
    load_env()
    now = datetime.now(ET)
    today = now.date()
    syms = candidates()
    if not syms:
        raise SystemExit("no candidates from screener endpoints")

    # previous daily closes (last completed session before today)
    daily = get_bars(syms, "1Day", now - timedelta(days=10))
    prev_close = {}
    for s, bars in daily.items():
        done = [b for b in bars if b["t"].date() < today]
        if done:
            prev_close[s] = done[-1]["c"]

    # premarket 1-min bars: 04:00 ET → 09:30 ET (or now)
    pm_start = now.replace(hour=4, minute=0, second=0, microsecond=0)
    pm_end = min(now, now.replace(hour=9, minute=30, second=0, microsecond=0))
    if now < pm_start:
        raise SystemExit("before 04:00 ET — no premarket data yet")
    pm = get_bars(list(prev_close), "1Min", pm_start, pm_end)

    rows = []
    for s, bars in pm.items():
        bars = [b for b in bars if pm_start <= b["t"] < pm_end]
        if not bars:
            continue
        px = bars[-1]["c"]
        vol = sum(b["v"] for b in bars)
        gap = (px / prev_close[s] - 1) * 100
        if gap > GAP_MIN and px > PRICE_MIN and vol > PMVOL_MIN:
            rows.append({"symbol": s, "price": round(px, 2),
                         "gap_pct": round(gap, 2), "premarket_volume": int(vol)})
    rows.sort(key=lambda r: -r["gap_pct"])
    rows = rows[:TOP_N]

    # news per survivor; per-ticker failure ⇒ catalyst null, never abort
    headlines = {r["symbol"]: [] for r in rows}
    if rows:
        try:
            news = get(f"{DATA}/v1beta1/news",
                       {"symbols": ",".join(headlines), "limit": 50})
            for item in news.get("news", []):
                for s in item.get("symbols", []):
                    if s in headlines and len(headlines[s]) < 2:
                        headlines[s].append(item["headline"])
        except Exception as e:
            print(f"news lookup failed: {e}", file=sys.stderr)

    gappers = [{"rank": i + 1, **r,
                "catalyst": headlines[r["symbol"]][0] if headlines[r["symbol"]] else None,
                "headlines": headlines[r["symbol"]]}
               for i, r in enumerate(rows)]
    out = {"scanned_at": now.isoformat(), "gappers": gappers}
    save_json(SCANS / f"premarket_gappers_{today}.json", out)

    if "--no-telegram" not in sys.argv:
        lines = [f"📊 *Premarket Gappers* — {today}"]
        for g in gappers:
            b = f"• {g['symbol']} ${g['price']} +{g['gap_pct']}%"
            if g["catalyst"]:
                b += f" — {g['catalyst']}"
            lines.append(b)
        if not gappers:
            lines.append("No qualifying gappers this morning.")
        send_telegram("\n".join(lines))

    top3 = ", ".join(f"{g['symbol']} ({g['gap_pct']}%)"
                     + (f" — {g['catalyst']}" if g["catalyst"] else "")
                     for g in gappers[:3])
    print(f"Premarket Gappers: {len(gappers)} names." +
          (f" Top: {top3}" if top3 else ""))


if __name__ == "__main__":
    main()
