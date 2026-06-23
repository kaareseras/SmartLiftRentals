from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ContractBase(BaseModel):
    lift_id: int
    customer_id: int
    start_date: date
    duration_days: int = Field(gt=0)
    daily_rate: float = Field(ge=0)
    status: str = "active"
    notes: str | None = None


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    lift_id: int | None = None
    customer_id: int | None = None
    start_date: date | None = None
    duration_days: int | None = Field(default=None, gt=0)
    daily_rate: float | None = Field(default=None, ge=0)
    status: str | None = None
    notes: str | None = None


class ContractResponse(ContractBase):
    id: int
    end_date: date | None = None
    total_price: float = 0.0
    customer_name: str | None = None
    lift_name: str | None = None
    lift_uid: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
