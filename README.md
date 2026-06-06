# DevSecOps Semester Project

This repository groups the CI/CD and DevSecOps work completed during the semester for a Zero-Trust Vault application.

The project demonstrates a full delivery chain:

- CI quality gates for a FastAPI backend and React frontend.
- GitLab CI/CD stages for linting, tests, SAST, Docker image build, container scanning, DAST, and deployment.
- Security tooling with SonarQube, Trivy, OWASP ZAP, Filebeat, Elasticsearch, Kibana, and a SecOps automation bot.
- Docker Compose deployment for the local/staging environment.
- Kubernetes manifests for a cluster deployment model.
- Automation scripts for repeatable build, scan, evidence collection, and deployment tasks.
- One global final report, including a detailed LaTeX source file in `docs/rapport_final.tex`.

The application source directories `app/`, `frontend/`, and `secops-bot/` are also included so the Docker, CI/CD, and deployment files can be executed from this folder as a standalone repository.

## Repository Structure

```text
devsecops-project/
├── Pipeline1/
├── Pipeline2/
├── Pipeline3/
├── Pipeline4/
├── Pipeline5/
├── scripts/
├── docker/
├── kubernetes/
├── screenshots/
├── docs/
│   ├── rapport_final.html
│   ├── rapport_final.md
│   ├── rapport_final.pdf
│   └── rapport_final.tex
├── app/
├── frontend/
├── secops-bot/
├── .gitlab-ci.yml
├── docker-compose.yml
└── README.md
```

## Pipeline Overview

| Folder | Pipeline | Objective |
| --- | --- | --- |
| `Pipeline1/` | CI quality and unit tests | Install dependencies, lint source code, run tests, export coverage. |
| `Pipeline2/` | SAST and code quality | Run static analysis with SonarQube and secret/dependency checks. |
| `Pipeline3/` | Docker build and container scan | Build application images and scan them with Trivy. |
| `Pipeline4/` | DAST and monitoring | Run OWASP ZAP against the deployed frontend and collect runtime logs with ELK. |
| `Pipeline5/` | Deployment and automation | Deploy with Docker Compose or Kubernetes and automate SecOps checks. |

## Quick Start

From this directory:

```bash
./scripts/build-images.sh
./scripts/security-scan.sh
docker compose up -d
```

For Kubernetes:

```bash
kubectl apply -k kubernetes/
```

## Main Deliverable

The final report is available at:

- `docs/rapport_final.tex`
- `docs/rapport_final.pdf`
- `docs/rapport_final.md`
- `docs/rapport_final.html`
- `docs/secops_bot_alarm_report.tex`

The LaTeX files are the detailed editable report sources. Compile them with `pdflatex` on a machine that has a LaTeX distribution installed.
