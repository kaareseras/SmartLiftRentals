from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.lift_type import LiftTypeResponse


class LiftBase(BaseModel):
    uid: str
    name: str
    lift_type_id: int
    status: str = "available"
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    battery_voltage: float | None = None
    telemetry_state: str | None = "idle"
    last_seen: datetime | None = None


class LiftCreate(LiftBase):
    pass


class LiftUpdate(BaseModel):
    uid: str | None = None
    name: str | None = None
    lift_type_id: int | None = None
    status: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    battery_voltage: float | None = None
    telemetry_state: str | None = None
    last_seen: datetime | None = None


class LiftResponse(LiftBase):
    id: int
    lift_type_name: str | None = None
    model: str | None = None
    lift_type: LiftTypeResponse | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
