from __future__ import annotations

import asyncio
import logging
import random
from datetime import UTC, datetime

from app.config.database import SessionLocal
from app.models.lift import Lift

logger = logging.getLogger(__name__)

STATES = ["operating", "charging", "idle"]


def _step(lift: Lift) -> None:
    """Advance one lift's fake telemetry by a small random amount."""
    state = lift.telemetry_state or "idle"
    voltage = lift.battery_voltage if lift.battery_voltage is not None else 24.0

    # Occasionally switch operating mode.
    if random.random() < 0.12:
        state = random.choice(STATES)

    if state == "charging":
        voltage += random.uniform(0.05, 0.20)
    elif state == "operating":
        voltage -= random.uniform(0.05, 0.20)
    else:
        voltage += random.uniform(-0.05, 0.05)

    voltage = max(21.5, min(26.6, voltage))

    lift.battery_voltage = round(voltage, 2)
    lift.telemetry_state = state
    lift.last_seen = datetime.now(UTC)


async def run_simulator(stop_event: asyncio.Event, interval: float = 5.0) -> None:
    """Periodically update lift telemetry until the stop event is set."""
    while not stop_event.is_set():
        try:
            db = SessionLocal()
            try:
                for lift in db.query(Lift).all():
                    _step(lift)
                db.commit()
            finally:
                db.close()
        except Exception:  # pragma: no cover - background best-effort task
            logger.warning("telemetry simulator step failed", exc_info=True)

        try:
            await asyncio.wait_for(stop_event.wait(), timeout=interval)
        except asyncio.TimeoutError:
            pass
