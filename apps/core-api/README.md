# Core API

FastAPI service providing the core business logic and API endpoints for Terminal-V.

## Setup

```bash
poetry install
poetry run uvicorn core_api.main:app --reload
```

## Architecture

This service acts as the API layer between the Terminal Web UI and the Nexus Engine data processing layer.
