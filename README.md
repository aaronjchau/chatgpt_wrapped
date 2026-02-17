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

- Frontend: React + TypeScript app, built with Vite and served by Nginx (`frontend/`)
- Backend: FastAPI API (`backend/app`)
- Orchestration: Docker Compose (`docker-compose.yml`)

## API Shape

`POST /api/v1/upload/conversations`

- Content type: `multipart/form-data`
- Field: `file`
- Expected filename: `conversations.json`

Success response includes:

- `global_stats`
- `conversation_stats`
- `model_stats`
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
- Deeper personal architecture notes live in `README_PRIVATE.md` (gitignored).
