"""Shared Alpaca/Telegram helpers for the scanner scripts (stdlib only).

Data feed is IEX (free tier): volumes undercount the consolidated tape
and quotes can lag SIP slightly. Fine for scanning; noted in reports.
"""
import json
import os
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
REPO = Path(__file__).resolve().parent.parent
SCANS = REPO / "scans"


def load_env():
    """Populate os.environ from .env when present (cron sessions rely on
    real environment variables instead)."""
    envfile = REPO / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    for k in ("ALPACA_API_KEY", "ALPACA_SECRET_KEY"):
        if not os.environ.get(k):
            raise SystemExit(f"{k} not set (in .env or environment)")


def get(url, params=None):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"],
        "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"],
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


DATA = "https://data.alpaca.markets"


def get_bars(symbols, timeframe, start, end=None, feed="iex"):
    """Multi-symbol bars, transparently paged. Returns {sym: [bar, ...]}
    with bar timestamps as ET datetimes in bar['t']."""
    out = {s: [] for s in symbols}
    params = {"symbols": ",".join(symbols), "timeframe": timeframe,
              "start": start.isoformat(), "limit": 10000,
              "adjustment": "split", "feed": feed}
    if end:
        params["end"] = end.isoformat()
    while True:
        resp = get(f"{DATA}/v2/stocks/bars", params)
        for sym, bars in (resp.get("bars") or {}).items():
            for b in bars:
                b["t"] = datetime.fromisoformat(
                    b["t"].replace("Z", "+00:00")).astimezone(ET)
            out.setdefault(sym, []).extend(bars)
        token = resp.get("next_page_token")
        if not token:
            return out
        params["page_token"] = token


def latest_trades(symbols):
    """{sym: price} from the latest-trades endpoint."""
    resp = get(f"{DATA}/v2/stocks/trades/latest",
               {"symbols": ",".join(symbols), "feed": "iex"})
    return {s: t["p"] for s, t in (resp.get("trades") or {}).items()}


def send_telegram(text):
    """Send via curl exactly as specced. Logs failures, never raises."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("telegram: skipped (TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID not set)")
        return
    try:
        r = subprocess.run(
            ["curl", "-s", f"https://api.telegram.org/bot{token}/sendMessage",
             "-d", f"chat_id={chat}", "--data-urlencode", f"text={text[:4000]}",
             "-d", "parse_mode=Markdown"],
            capture_output=True, text=True, timeout=30)
        ok = '"ok":true' in r.stdout
        print(f"telegram: {'sent' if ok else 'FAILED — ' + r.stdout[:200]}")
    except Exception as e:  # never fail the scan over a notification
        print(f"telegram: FAILED — {e}")


def save_json(path, obj):
    SCANS.mkdir(exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")
    print(f"saved {path.relative_to(REPO)}")
