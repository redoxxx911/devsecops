# Pipeline 4 - DAST and Runtime Monitoring

## Objective

This pipeline validates the deployed application from the outside and connects runtime logs to a monitoring stack.

## Tools

- OWASP ZAP baseline scan for DAST.
- Filebeat for container log collection.
- Elasticsearch for indexing logs.
- Kibana for dashboards and investigation.

## DAST Scope

The ZAP baseline scan targets the frontend URL and checks for common web security weaknesses such as missing headers, passive scan alerts, cookie flags, and exposed endpoints.

## Monitoring Scope

Filebeat reads Docker container logs and sends them to Elasticsearch. Kibana is used to search events such as failed authentication attempts, API errors, and suspicious repeated requests.

## Evidence to Capture

- ZAP HTML report artifact.
- Kibana dashboard showing ingested container logs.
- Elasticsearch query results for failed login or `401` events.
