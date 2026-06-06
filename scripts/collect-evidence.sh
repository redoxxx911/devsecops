#!/usr/bin/env sh
set -eu

mkdir -p screenshots reports

docker compose ps > reports/docker-compose-ps.txt || true
kubectl -n devsecops-project get all > reports/kubernetes-status.txt 2>/dev/null || true

cat > screenshots/README.md <<'EOT'
# Screenshot Evidence

Place final screenshots in this directory using these names:

- 01-gitlab-pipeline-overview.png
- 02-sonarqube-dashboard.png
- 03-trivy-scan-results.png
- 04-zap-dast-report.png
- 05-kibana-dashboard.png
- 06-docker-compose-services.png
- 07-kubernetes-workloads.png
- 08-secops-bot-alert.png
EOT

echo "Evidence text files written to reports/. Screenshot checklist refreshed."
