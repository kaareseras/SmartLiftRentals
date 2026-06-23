from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LiftTypeBase(BaseModel):
    name: str
    model: str
    manufacturer: str | None = None
    description: str | None = None
    default_daily_rate: float | None = None


class LiftTypeCreate(LiftTypeBase):
    pass


class LiftTypeUpdate(BaseModel):
    name: str | None = None
    model: str | None = None
    manufacturer: str | None = None
    description: str | None = None
    default_daily_rate: float | None = None


class LiftTypeResponse(LiftTypeBase):
    id: int
    lift_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
