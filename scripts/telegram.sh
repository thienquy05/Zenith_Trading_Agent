#!/usr/bin/env bash
# Send a Telegram message to Quy. Usage: scripts/telegram.sh "message"
# Also: scripts/telegram.sh --get-updates   (to discover the chat id)
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && { set -a; source .env; set +a; }
: "${TELEGRAM_BOT_TOKEN:?not in .env or environment}"
API="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN"

if [ "${1:-}" = "--get-updates" ]; then
  curl -sS "$API/getUpdates"; echo; exit 0
fi

: "${TELEGRAM_CHAT_ID:?missing in .env (run --get-updates after messaging the bot)}"
msg=${1:?usage: telegram.sh "message"}
# Telegram hard limit 4096 chars — truncate to stay under it
msg=${msg:0:4000}
curl -sS -X POST "$API/sendMessage" \
  --data-urlencode "chat_id=$TELEGRAM_CHAT_ID" \
  --data-urlencode "text=$msg" \
  -d "parse_mode=HTML" \
  -o /dev/null -w "telegram:%{http_code}\n"
