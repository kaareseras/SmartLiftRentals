from __future__ import annotations

from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_lifts: int
    total_lift_types: int
    total_customers: int
    total_contracts: int
    active_contracts: int
    total_revenue: float
    total_cost: float
    net_profit: float


class MonthlyStat(BaseModel):
    year: int
    month: int
    label: str
    revenue: float
    cost: float
    profit: float
    contracts: int


class YearlyStat(BaseModel):
    year: int
    revenue: float
    cost: float
    profit: float
    contracts: int


class LiftStat(BaseModel):
    lift_id: int
    uid: str
    name: str
    lift_type_name: str | None = None
    revenue: float
    cost: float
    profit: float
    contracts: int


class LiftStatDetail(LiftStat):
    monthly: list[MonthlyStat] = []
    yearly: list[YearlyStat] = []
