#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

source venv/bin/activate

python manage.py migrate --noinput

python manage.py loaddata \
  fixtures/00_contenttypes.json \
  fixtures/01_auth_permissions.json \
  fixtures/02_bookings.json \
  fixtures/03_website.json

echo "Fixtures loaded. Content page images live under media/ — copy that folder if needed."
