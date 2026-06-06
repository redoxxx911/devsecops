# Pipeline 1 - CI Quality and Unit Tests

## Objective

This pipeline validates the application before any security or deployment stage starts. It installs backend/frontend dependencies, checks code style, and runs automated tests with coverage export.

## Stages

1. `install`: install Python and Node.js dependencies.
2. `lint`: run `flake8` for the FastAPI backend and `npm run lint` for the React frontend.
3. `test`: run `pytest` with Cobertura coverage output.

## Evidence to Capture

- GitLab pipeline graph showing the install, lint, and test jobs.
- Coverage artifact named `coverage.xml`.
- Job logs for backend and frontend linting.

## Result Summary

The current repository already includes backend dependency installation and lint/test jobs. The frontend package also exposes an `npm run lint` command, so the global pipeline includes that check as an additional quality gate.
