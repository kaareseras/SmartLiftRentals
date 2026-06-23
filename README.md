# SmartLiftRentals

SmartLiftRentals is a barebone IoT platform for construction lift rentals. It combines a FastAPI backend, PostgreSQL/TimescaleDB storage, MQTT telemetry ingestion, Redis caching, a Vue 3 + TypeScript frontend, and Azure Bicep infrastructure templates.

## Platform Overview

- **Lift fleet management** - register, update, and retire rental lifts
- **MQTT telemetry** - receive lift health and location messages on `lifts/+/telemetry`
- **Operational API** - FastAPI CRUD endpoints for lift inventory
- **Web dashboard** - Vue 3 frontend for fleet overview
- **Azure IaC** - starter Bicep templates for backend hosting and PostgreSQL

## Repository Structure

```text
backend/   FastAPI application, SQLAlchemy models, Alembic, tests
frontend/  Vue 3 + TypeScript + Vite application
broker/    Mosquitto development broker config
infra/     Azure Bicep templates
```

## Local Development

1. Copy `backend/.env.example` to `backend/.env` and adjust secrets.
2. Start the development stack:
   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```
3. In the backend container, run migrations:
   ```bash
   cd /workspace/backend
   uv run alembic upgrade head
   ```
4. Start the backend API:
   ```bash
   cd /workspace/backend
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. The frontend dev server is available at `http://localhost:5173`.

## Default Services

- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- PostgreSQL/TimescaleDB: `localhost:5432`
- MQTT broker: `localhost:1883`
- Redis: `localhost:6379`

## Next Steps

- Add Alembic migrations for domain changes
- Expand telemetry ingestion and command flows
- Add authentication and authorization
- Add lift rental, maintenance, and billing modules
