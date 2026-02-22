## ChatGPT Wrapped

Local web app that imports a `conversations.json` export and shows summary analytics.

## Stack

- Backend: Python, FastAPI, uv, pytest
- Frontend: Svelte + Vite (JavaScript), Tailwind CSS, Chart.js
- Runtime: Docker, Docker Compose, Nginx

## Quick Start 

### Docker

```bash
docker compose up --build
```

### Without Docker

Backend:

```bash
uv sync --frozen
PYTHONPATH=backend uv run uvicorn app.main:app --app-dir backend --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Architecture 

- browser UI (Svelte) sends `multipart/form-data` with `conversations.json`
- backend route validates file name, size, and JSON shape
- parser flattens conversation mapping into message records
- stats service computes:
  - global totals
  - conversation stats
  - model usage
  - time stats (hour/day/month/year + rolling 12-month window)
- frontend renders cards + charts from one API response