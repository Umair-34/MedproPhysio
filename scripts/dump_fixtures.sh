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

mkdir -p fixtures

python manage.py dumpdata contenttypes --natural-foreign --indent 2 \
  -o fixtures/00_contenttypes.json
python manage.py dumpdata auth.permission --natural-foreign --indent 2 \
  -o fixtures/01_auth_permissions.json
python manage.py dumpdata bookings --natural-foreign --natural-primary --indent 2 \
  -o fixtures/02_bookings.json
python manage.py dumpdata website --natural-foreign --natural-primary --indent 2 \
  -o fixtures/03_website.json

echo "Wrote fixtures to fixtures/"
