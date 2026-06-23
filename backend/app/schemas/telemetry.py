from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LiftTelemetry(BaseModel):
    id: int
    uid: str
    name: str
    status: str
    lift_type_name: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    battery_voltage: float | None = None
    telemetry_state: str | None = None
    last_seen: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
