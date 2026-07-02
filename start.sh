#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -f .env ]; then
  echo "No .env found. Copy .env.example to .env and set CREDENTIAL_ENCRYPTION_KEY first." >&2
  exit 1
fi

docker compose up -d --build

echo
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:5000/health"
echo "Postgres migrations applied by the 'migrate' service on every start."
echo "Logs: docker compose logs -f"
