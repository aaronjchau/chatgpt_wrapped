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

Dashboard includes:

- Global summary cards
- Model usage bar chart
- Message timing charts (EST): hour, day of week, month, year
- Rolling 12-month heatmap with hover tooltips per day
- Dark mode dashboard styling

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

`time_stats` currently includes:

- `msgs_sent_by_hour` (0-23, EST)
- `msgs_sent_by_day`
- `msgs_sent_by_month`
- `msgs_sent_by_year`
- `rolling_12_months` (`start_date`, `end_date`, `daily_counts`)

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
- Frontend is intentionally minimal and library-driven (Chart.js + Tailwind).
