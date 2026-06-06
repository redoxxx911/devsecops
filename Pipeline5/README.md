# Pipeline 5 - Deployment and SecOps Automation

## Objective

This pipeline covers deployment and operational automation. The application can be deployed locally with Docker Compose or to a Kubernetes cluster using the manifests in `kubernetes/`.

## Runtime Components

- FastAPI backend.
- React/Nginx frontend.
- Elasticsearch and Kibana.
- Filebeat log collector.
- SecOps bot connected to Telegram, GitLab, Elasticsearch, and an LLM provider through environment variables.

## Automation Bot

The SecOps bot can:

- Query recent Elasticsearch logs.
- Report suspicious `401` or error events.
- Query GitLab for failed pipelines.
- Summarize failures and incidents using an LLM provider.

## Evidence to Capture

- Running Docker Compose services.
- Kubernetes workloads in `Running` state.
- Telegram bot response for `/siem`.
- Telegram bot response for `/pipelines`.
