#!/usr/bin/env bash
# Alpaca paper-trading curl helper. Usage: scripts/alpaca.sh <cmd> [args]
# Commands: account | positions | orders [status] | clock | quote SYM |
#   bars SYM [timeframe] [limit] | buy SYM QTY [limit] | sell SYM QTY [limit] |
#   bracket SYM QTY LIMIT STOP TARGET | stop SYM QTY STOP_PRICE |
#   cancel ORDER_ID | raw METHOD /path ['json']
# Crypto (symbols like BTC/USD; 24/7, gtc, NO bracket support):
#   cquote SYM | cbars SYM [timeframe] [limit] |
#   cbuy SYM QTY [limit] | csell SYM QTY [limit] |
#   cstop SYM QTY STOP_PRICE [limit_price]  (stop_limit sell; limit
#     defaults to 0.5% below stop — place immediately after every entry)
set -euo pipefail
cd "$(dirname "$0")/.."
# .env when present (interactive sessions); otherwise env vars from the
# Claude Code environment config (fresh cron sessions have no .env)
[ -f .env ] && { set -a; source .env; set +a; }
: "${ALPACA_API_KEY:?not in .env or environment}" "${ALPACA_SECRET_KEY:?not in .env or environment}"
BASE="${ALPACA_BASE_URL:-https://paper-api.alpaca.markets}/v2"
DATA="${ALPACA_DATA_URL:-https://data.alpaca.markets}/v2"

req() { # req METHOD URL [json-body]
  local m=$1 u=$2 b=${3:-}
  curl -sS --fail-with-body -X "$m" "$u" \
    -H "APCA-API-KEY-ID: $ALPACA_API_KEY" \
    -H "APCA-API-SECRET-KEY: $ALPACA_SECRET_KEY" \
    -H "Content-Type: application/json" \
    ${b:+-d "$b"}
  echo
}

cmd=${1:?usage: alpaca.sh <account|positions|orders|clock|quote|bars|buy|sell|bracket|stop|cancel|raw>}
case "$cmd" in
  account)   req GET "$BASE/account" ;;
  positions) req GET "$BASE/positions" ;;
  orders)    req GET "$BASE/orders?status=${2:-open}&limit=50" ;;
  clock)     req GET "$BASE/clock" ;;
  quote)     req GET "$DATA/stocks/${2:?symbol}/quotes/latest" ;;
  bars)      req GET "$DATA/stocks/${2:?symbol}/bars?timeframe=${3:-15Min}&limit=${4:-40}&adjustment=split&feed=iex" ;;
  buy|sell)
    sym=${2:?symbol} qty=${3:?qty} lim=${4:-}
    if [ -n "$lim" ]; then
      req POST "$BASE/orders" "{\"symbol\":\"$sym\",\"qty\":\"$qty\",\"side\":\"$cmd\",\"type\":\"limit\",\"limit_price\":\"$lim\",\"time_in_force\":\"day\"}"
    else
      req POST "$BASE/orders" "{\"symbol\":\"$sym\",\"qty\":\"$qty\",\"side\":\"$cmd\",\"type\":\"market\",\"time_in_force\":\"day\"}"
    fi ;;
  bracket)
    sym=${2:?symbol} qty=${3:?qty} lim=${4:?limit} stp=${5:?stop} tgt=${6:?target}
    req POST "$BASE/orders" "{\"symbol\":\"$sym\",\"qty\":\"$qty\",\"side\":\"buy\",\"type\":\"limit\",\"limit_price\":\"$lim\",\"time_in_force\":\"day\",\"order_class\":\"bracket\",\"stop_loss\":{\"stop_price\":\"$stp\"},\"take_profit\":{\"limit_price\":\"$tgt\"}}" ;;
  stop)
    sym=${2:?symbol} qty=${3:?qty} stp=${4:?stop_price}
    req POST "$BASE/orders" "{\"symbol\":\"$sym\",\"qty\":\"$qty\",\"side\":\"sell\",\"type\":\"stop\",\"stop_price\":\"$stp\",\"time_in_force\":\"gtc\"}" ;;
  cquote)    req GET "${ALPACA_DATA_URL:-https://data.alpaca.markets}/v1beta3/crypto/us/latest/quotes?symbols=${2:?symbol}" ;;
  cbars)     req GET "${ALPACA_DATA_URL:-https://data.alpaca.markets}/v1beta3/crypto/us/bars?symbols=${2:?symbol}&timeframe=${3:-4Hour}&limit=${4:-40}" ;;
  cbuy|csell)
    side=${cmd#c} sym=${2:?symbol} qty=${3:?qty} lim=${4:-}
    if [ -n "$lim" ]; then
      req POST "$BASE/orders" "{\"symbol\":\"$sym\",\"qty\":\"$qty\",\"side\":\"$side\",\"type\":\"limit\",\"limit_price\":\"$lim\",\"time_in_force\":\"gtc\"}"
    else
      req POST "$BASE/orders" "{\"symbol\":\"$sym\",\"qty\":\"$qty\",\"side\":\"$side\",\"type\":\"market\",\"time_in_force\":\"gtc\"}"
    fi ;;
  cstop)
    sym=${2:?symbol} qty=${3:?qty} stp=${4:?stop_price} lim=${5:-}
    [ -z "$lim" ] && lim=$(awk "BEGIN{printf \"%.6g\", $stp*0.995}")
    req POST "$BASE/orders" "{\"symbol\":\"$sym\",\"qty\":\"$qty\",\"side\":\"sell\",\"type\":\"stop_limit\",\"stop_price\":\"$stp\",\"limit_price\":\"$lim\",\"time_in_force\":\"gtc\"}" ;;
  cancel)    req DELETE "$BASE/orders/${2:?order_id}" ;;
  raw)       req "${2:?method}" "$BASE${3:?/path}" "${4:-}" ;;
  *) echo "unknown command: $cmd" >&2; exit 2 ;;
esac
