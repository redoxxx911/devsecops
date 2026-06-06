#!/usr/bin/env sh
set -eu

mkdir -p reports

trivy image --severity HIGH,CRITICAL --format table --output reports/trivy-backend.txt zero-trust-vault/backend:semester || true
trivy image --severity HIGH,CRITICAL --format table --output reports/trivy-frontend.txt zero-trust-vault/frontend:semester || true
trivy image --severity HIGH,CRITICAL --format table --output reports/trivy-secops-bot.txt zero-trust-vault/secops-bot:semester || true

echo "Container scan reports written to reports/"
