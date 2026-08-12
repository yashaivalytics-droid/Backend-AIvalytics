# AiValytics API

The Python backend for AiValytics. The starter uses FastAPI and `uv` so every
developer and CI run resolves the same locked dependency set.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Quick start

```powershell
uv sync --all-groups
Copy-Item .env.example .env
uv run uvicorn aivalytics_api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the OpenAPI documentation. The health
endpoint is available at `GET /health`.

## Team workflow

- Commit `uv.lock`; do not manually edit it.
- Add or upgrade dependencies with `uv add` / `uv add --group dev`, then commit
  both `pyproject.toml` and `uv.lock` in the same pull request.
- Install exactly the lockfile in CI with `uv sync --frozen`.
- Keep application code in `src/aivalytics_api` and tests in `tests`.
- Use feature branches and require passing CI before merge.

## Checks

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

## Docker

```powershell
docker compose up --build
```
