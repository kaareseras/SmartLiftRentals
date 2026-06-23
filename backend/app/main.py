from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.config.database import Base, SessionLocal, engine
from app.config.mqtt import start_mqtt, stop_mqtt
from app.routes import (
    auth_router,
    contract_router,
    cost_router,
    customer_router,
    health_router,
    lift_router,
    lift_type_router,
    statistics_router,
    telemetry_router,
    user_router,
)
from app.services.seed import seed_all
from app.services.telemetry_sim import run_simulator


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()
    start_mqtt()

    stop_event = asyncio.Event()
    sim_task = asyncio.create_task(run_simulator(stop_event))
    try:
        yield
    finally:
        stop_event.set()
        sim_task.cancel()
        with suppress(asyncio.CancelledError):
            await sim_task
        stop_mqtt()


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(lift_type_router)
app.include_router(lift_router)
app.include_router(customer_router)
app.include_router(contract_router)
app.include_router(cost_router)
app.include_router(statistics_router)
app.include_router(telemetry_router)
