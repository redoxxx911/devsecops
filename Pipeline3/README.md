# Pipeline 3 - Docker Build and Container Scan

## Objective

This pipeline builds Docker images for each application component and scans the generated images before they are pushed or deployed.

## Images

- `backend`: FastAPI API service.
- `frontend`: React/Vite application served by Nginx.
- `secops-bot`: Telegram/GitLab/ELK automation bot.

## Security Scan

Trivy is used to detect high and critical vulnerabilities in operating system packages and application dependencies inside each image.

## Evidence to Capture

- Docker build job logs.
- Trivy scan artifacts for backend, frontend, and bot images.
- Registry image tags if the push stage is enabled.
