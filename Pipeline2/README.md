# Pipeline 2 - SAST and Code Quality

## Objective

This pipeline focuses on static security and maintainability checks before Docker images are built.

## Tools

- SonarQube / SonarScanner for maintainability, bugs, vulnerabilities, and code smells.
- Dependency review through package lock files and Python requirements.
- Secret review for risky values committed in source code.

## Findings Observed in the Source Repository

- The backend contains a hardcoded JWT signing key.
- CORS is configured with `allow_origins=["*"]`.
- Demo credentials are hardcoded in the authentication endpoint.
- The frontend contains a hardcoded API base URL.
- The bot expects sensitive API tokens through environment variables, which is correct, but the `.env` file must never be committed.

## Evidence to Capture

- SonarQube project dashboard.
- List of vulnerabilities/code smells.
- Screenshot showing the quality gate result.
