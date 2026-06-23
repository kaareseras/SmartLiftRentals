from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LiftBase(BaseModel):
    uid: str
    name: str
    model: str
    status: str = "available"
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    last_seen: datetime | None = None


class LiftCreate(LiftBase):
    pass


class LiftUpdate(BaseModel):
    uid: str | None = None
    name: str | None = None
    model: str | None = None
    status: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    last_seen: datetime | None = None


class LiftResponse(LiftBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
