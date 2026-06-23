from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class CostBase(BaseModel):
    lift_id: int
    category: str = "other"
    description: str | None = None
    amount: float = Field(ge=0)
    incurred_on: date


class CostCreate(CostBase):
    pass


class CostUpdate(BaseModel):
    lift_id: int | None = None
    category: str | None = None
    description: str | None = None
    amount: float | None = Field(default=None, ge=0)
    incurred_on: date | None = None


class CostResponse(CostBase):
    id: int
    lift_name: str | None = None
    lift_uid: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
