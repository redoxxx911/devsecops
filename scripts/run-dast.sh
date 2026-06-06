#!/usr/bin/env sh
set -eu

TARGET_URL="${1:-http://localhost:5173}"
mkdir -p reports

docker run --rm \
  -v "$(pwd)/reports:/zap/wrk" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t "$TARGET_URL" -g gen.conf -I -r dast_report.html

echo "DAST report written to reports/dast_report.html"
