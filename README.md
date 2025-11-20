# Task Management Platform

Backend FastAPI + PostgreSQL with React SPA frontend, aligned to the CI/CD practice brief.

## Quickstart
- Clone the repo and create the required env vars from `backend/.env.example` (set `DATABASE_URL`).
- Spin everything up with Docker: `docker-compose up --build`.
- Backend only: `cd backend && python -m venv .venv && .venv\\Scripts\\activate && pip install -r requirements.txt && uvicorn app.main:app --reload`.
- Frontend only: `cd frontend && npm install && npm run dev -- --host --port 5173` (set `VITE_API_BASE_URL=http://localhost:8000` if backend differs).

## Backend
- FastAPI app exposes CRUD for projects and tasks (10 endpoints: list/create/read/update/delete for both resources) with validation and error handling.
- Database: SQLAlchemy models targeting PostgreSQL; change `DATABASE_URL` to point at your Postgres instance.
- Testing: `pytest -m unit` for in-memory unit tests, `pytest -m integration` uses Testcontainers + Postgres, `pytest -m benchmark` for pytest-benchmark, `pytest -m e2e` hits a running API via `E2E_BASE_URL`.

## Frontend
- Vite + React + TypeScript SPA with Redux Toolkit state for projects/tasks.
- Components: Header, ProjectForm, ProjectList, TaskForm, TaskList, Metrics.
- Build: `npm run build`; preview `npm run preview -- --host`.

## CI/CD
- GitHub Actions workflow `.github/workflows/ci.yml` runs backend pytest (with coverage) and frontend build on push/PR.
- Dockerfiles for backend and frontend plus `docker-compose.yml` for local orchestration.

## Notes
- Integration and benchmark suites require Docker available for Testcontainers.
- E2E suite is opt-in; set `E2E_BASE_URL` to a running backend (or full stack) before running `pytest -m e2e`.
- Coverage report can be produced with `cd backend && pytest --cov=app`.

## Notes
link of evidence: https://drive.google.com/drive/folders/114djirLtMEwL9uY6N6yGzXKMkBhzDPdf?usp=drive_link
