#!/usr/bin/env python3
"""C-TJL live signal check (TRADING-STRATEGY.md §2c). Crypto trades 24/7 —
no time gate; runs whenever a workflow wakes up.

Order of checks:
  1. REGIME GATE — BTC previous daily close vs its daily SMA200. Bear
     regime ⇒ the whole sleeve stands down (no signal checks, no entries;
     existing stops keep working). This gate is what the 48-month backtest
     validated; the sleeve has NO edge with the gate off.
  2. Per symbol: most recent COMPLETED 4H bar closes above the highest
     high of the 20 bars before it AND above its 4H SMA200.
On a PASS it prints suggested entry/stop/target/qty. THE AGENT places the
orders (entry, then stop-limit immediately — Alpaca crypto has NO bracket
orders) per the sleeve's risk rules; this script only signals.

Telegram gating mirrors scan_tjl.py: first run of the day, changed hit
set, or error. State = latest saved scans/crypto_tjl_*.json.

Usage: scan_crypto.py [--no-telegram] [TICKERS…]   (e.g. BTC/USD)
Saves: scans/crypto_tjl_<date>_<HHMM>UTC.json
"""
import json
import sys
from datetime import datetime, timedelta, timezone

from alpaca_common import SCANS, get, get_crypto_bars, load_env, save_json, \
    send_telegram
from backtest_crypto import ATR_LEN, ATR_MULT, DONCHIAN, R_TARGET, \
    REGIME_SMA_DAYS, SMA_LEN, UNIVERSE, atr_series

RISK_PCT = 0.0025      # validation phase: 0.25% equity risk per trade
                       # (graduates to 0.5% per §2c after the gate)


def regime_now(now):
    """(is_bull, prev_close, sma200) from BTC daily bars."""
    daily = get_crypto_bars(["BTC/USD"], "1Day",
                            now - timedelta(days=320), end=now)["BTC/USD"]
    done = [b for b in daily if b["t"].date() < now.date()]
    sma = sum(b["c"] for b in done[-REGIME_SMA_DAYS:]) / REGIME_SMA_DAYS
    return done[-1]["c"] > sma, done[-1]["c"], round(sma, 2)


def check(sym, bars):
    """bars: completed 4H bars, oldest first. Returns result dict."""
    if len(bars) < SMA_LEN + 1:
        return {"symbol": sym, "pass": False, "why": "insufficient bars"}
    sig = bars[-1]                      # most recent completed bar
    hh = max(b["h"] for b in bars[-1 - DONCHIAN:-1])
    sma = sum(b["c"] for b in bars[-SMA_LEN:]) / SMA_LEN
    atr = atr_series(bars, ATR_LEN)[-1]
    ok_break = sig["c"] > hh
    ok_trend = sig["c"] > sma
    res = {"symbol": sym, "pass": bool(ok_break and ok_trend),
           "bar_close_utc": sig["t"].isoformat(), "close": sig["c"],
           "donchian_high": round(hh, 6), "sma200_4h": round(sma, 6),
           "breakout": ok_break, "trend_ok": ok_trend}
    if res["pass"]:
        risk = ATR_MULT * atr
        res.update({"entry": round(sig["c"], 6),
                    "stop": round(sig["c"] - risk, 6),
                    "target": round(sig["c"] + R_TARGET * risk, 6),
                    "risk_per_unit": round(risk, 6)})
    return res


def main():
    load_env()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    syms = [a.upper() for a in args] or UNIVERSE
    now = datetime.now(timezone.utc)

    bull, btc_close, btc_sma = regime_now(now)
    regime = {"bull": bull, "btc_prev_close": btc_close,
              "btc_daily_sma200": btc_sma}
    if not bull:
        out = {"scanned_at": now.isoformat(), "universe": syms,
               "regime": regime, "results": [],
               "note": "bear regime — sleeve flat, no signal checks run"}
        save_json(SCANS / f"crypto_tjl_{now.date()}_"
                          f"{now.strftime('%H%M')}UTC.json", out)
        print(f"REGIME: BEAR (BTC {btc_close} < SMA200 {btc_sma}) — "
              f"sleeve stands down, no entries.")
        return

    start = now - timedelta(days=40)
    data = get_crypto_bars(syms, "4Hour", start, end=now)

    results = []
    for s in syms:
        bars = [b for b in data.get(s, [])
                if b["t"] + timedelta(hours=4) <= now]   # completed only
        results.append(check(s, bars))
    hits = [r for r in results if r["pass"]]

    if hits:   # suggested qty at validation-phase risk
        try:
            eq = float(get("https://paper-api.alpaca.markets/v2/account")["equity"])
            for h in hits:
                h["suggested_qty"] = round(eq * RISK_PCT / h["risk_per_unit"], 6)
        except Exception as e:
            print(f"account fetch failed ({e}) — no qty suggestion")

    prev_files = sorted(SCANS.glob("crypto_tjl_*.json"))
    prev = json.loads(prev_files[-1].read_text()) if prev_files else {}
    prev_hits = {h["symbol"] for h in prev.get("results", []) if h.get("pass")}
    first_today = not any(f.name.startswith(f"crypto_tjl_{now.date()}")
                          for f in prev_files)

    out = {"scanned_at": now.isoformat(), "universe": syms,
           "regime": regime,
           "params": {"donchian": DONCHIAN, "atr_mult": ATR_MULT,
                      "r_target": R_TARGET, "sma": SMA_LEN,
                      "risk_pct": RISK_PCT * 100},
           "results": results}
    save_json(SCANS / f"crypto_tjl_{now.date()}_"
                      f"{now.strftime('%H%M')}UTC.json", out)

    for r in results:
        mark = "PASS" if r["pass"] else "----"
        print(f"{mark} {r['symbol']}: close {r.get('close')} "
              f"| don20H {r.get('donchian_high')} | sma {r.get('sma200_4h')}")

    hit_syms = {h["symbol"] for h in hits}
    if "--no-telegram" not in sys.argv and (first_today
                                            or hit_syms != prev_hits):
        if hits:
            lines = [f"₿ *C-TJL crypto signals* — {now.strftime('%Y-%m-%d %H:%M')} UTC"]
            lines += [f"• {h['symbol']} entry {h['entry']} stop {h['stop']} "
                      f"target {h['target']} qty≈{h.get('suggested_qty', '?')}"
                      for h in hits]
            send_telegram("\n".join(lines))
        elif prev_hits:
            send_telegram(f"₿ C-TJL: previous signals "
                          f"({', '.join(sorted(prev_hits))}) no longer pass.")


if __name__ == "__main__":
    main()
