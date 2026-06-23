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
   The backend container automatically runs `uvicorn --reload` and the frontend
   container runs `vite`, so both services start and hot-reload on file changes.
   Database tables are created and demo data is seeded automatically on startup.
3. Open the app at `http://localhost:5174` and sign in with the seeded admin
   account (`admin@smartliftrentals.com` / `Admin123!`).

To reset the development database to a clean, freshly seeded state:

```bash
cd /workspace/backend
uv run python -m app.scripts.reset_db
```

## Default Services

- Frontend: `http://localhost:5174`
- Backend API: `http://localhost:8001` (docs at `/docs`)
- PostgreSQL/TimescaleDB: `localhost:5433`
- MQTT broker: `localhost:1884`
- Redis: `localhost:6380`

## Next Steps

- Add Alembic migrations for domain changes
- Expand telemetry ingestion and command flows
- Add authentication and authorization
- Add lift rental, maintenance, and billing modules
