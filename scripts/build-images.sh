#!/usr/bin/env sh
set -eu

docker build -f docker/backend.Dockerfile -t zero-trust-vault/backend:semester ./app
docker build -f docker/frontend.Dockerfile -t zero-trust-vault/frontend:semester ./frontend
docker build -f docker/secops-bot.Dockerfile -t zero-trust-vault/secops-bot:semester ./secops-bot

echo "Images built:"
docker images "zero-trust-vault/*:semester"
