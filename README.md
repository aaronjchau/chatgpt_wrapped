# ChatGPT Wrapped (Local-Only MVP)

Local web app that analyzes ChatGPT export data from `conversations.json`.

## Quick Start (Docker)

```bash
docker compose up --build
```

Open:

- Frontend: `http://localhost:3000`
- Backend health: `http://localhost:8000/api/v1/health`

## Architecture

- Frontend: Svelte + Vite + Tailwind + Chart.js (`frontend/`)
- Backend: FastAPI API (`backend/app`)
- Orchestration: Docker Compose (`docker-compose.yml`)

## API Shape

`POST /api/v1/import/conversations`

- Content type: `multipart/form-data`
- Field: `file`
- Expected filename: `conversations.json`

Success response includes:

- `global_stats`
- `conversation_stats`
- `model_stats`
- `time_stats`
- `meta`

## Local Dev (No Docker)

Backend (from repo root):

```bash
PYTHONPATH=backend uv run uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Tests

Backend:

```bash
PYTHONPATH=backend uv run pytest backend/tests
```

Frontend:

```bash
cd frontend
npm test
```

## Notes

- Dependency lock files are committed for reproducible installs.
- This MVP is local-only and does not persist imported data.
