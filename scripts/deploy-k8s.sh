#!/usr/bin/env sh
set -eu

kubectl apply -k kubernetes/
kubectl -n devsecops-project get pods
