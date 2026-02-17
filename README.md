# ChatGPT Wrapped (Local-Only MVP)

Simple web app for analyzing `conversations.json` from your own ChatGPT export.

This MVP is intentionally straightforward so it is easy to read, modify, and learn from.

## Privacy Model

- Local-only by default.
- Backend and frontend run on `localhost`.
- Uploads are processed in memory and not persisted to a database.
- No hosted upload flow is included in this MVP.

## Architecture

- Backend: FastAPI (`backend/app`)
- Frontend: React + TypeScript + Vite (`frontend`)
- Startup: Docker Compose (`docker-compose.yml`)

## Quick Start (Docker)

```bash
docker compose up --build
```

Then open:

- Frontend: `http://localhost:3000`
- Backend health: `http://localhost:8000/api/v1/health`

## Devcontainer + uv Workflow

From repo root:

```bash
uv sync
```

## API

### `POST /api/v1/upload/conversations`

- Content type: `multipart/form-data`
- Field: `file`
- Filename expected in MVP: `conversations.json`

Successful response includes:

- `global_stats`
- `conversation_stats`
- `model_stats`
- `meta`

## Local Dev (Without Docker)

Backend (from repo root):

```bash
PYTHONPATH=backend uv run uvicorn app.main:app --reload
```

Frontend (from `frontend/`):

```bash
npm install
npm run dev
```

## Tests

Backend tests:

```bash
PYTHONPATH=backend uv run pytest backend/tests
```

Frontend tests:

```bash
cd frontend
npm install
npm run test
```

## Suggested Git Workflow

1. Create feature branch.
2. Make small commits by concern (backend route, validation, frontend UI, Docker, tests/docs).
3. Open one PR with those commits when ready.
