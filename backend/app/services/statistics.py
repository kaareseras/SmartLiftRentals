from __future__ import annotations

import calendar
from collections import defaultdict

from sqlalchemy.orm import Session, joinedload

from app.models.contract import Contract
from app.models.cost import Cost
from app.models.customer import Customer
from app.models.lift import Lift
from app.models.lift_type import LiftType
from app.schemas.statistics import (
    LiftStat,
    LiftStatDetail,
    MonthlyStat,
    OverviewStats,
    YearlyStat,
)

# Revenue is recognised at the contract start date; costs at the incurred date.


def _round(value: float) -> float:
    return round(value, 2)


def overview(db: Session) -> OverviewStats:
    contracts = db.query(Contract).all()
    costs = db.query(Cost).all()

    total_revenue = sum(c.total_price for c in contracts)
    total_cost = sum(c.amount for c in costs)
    active = sum(1 for c in contracts if (c.status or "").lower() == "active")

    return OverviewStats(
        total_lifts=db.query(Lift).count(),
        total_lift_types=db.query(LiftType).count(),
        total_customers=db.query(Customer).count(),
        total_contracts=len(contracts),
        active_contracts=active,
        total_revenue=_round(total_revenue),
        total_cost=_round(total_cost),
        net_profit=_round(total_revenue - total_cost),
    )


def monthly(db: Session, year: int) -> list[MonthlyStat]:
    contracts = db.query(Contract).filter(Contract.start_date.isnot(None)).all()
    costs = db.query(Cost).filter(Cost.incurred_on.isnot(None)).all()

    revenue = defaultdict(float)
    contract_counts = defaultdict(int)
    for c in contracts:
        if c.start_date.year == year:
            revenue[c.start_date.month] += c.total_price
            contract_counts[c.start_date.month] += 1

    cost_by_month = defaultdict(float)
    for cost in costs:
        if cost.incurred_on.year == year:
            cost_by_month[cost.incurred_on.month] += cost.amount

    rows: list[MonthlyStat] = []
    for month in range(1, 13):
        rev = revenue.get(month, 0.0)
        cost_total = cost_by_month.get(month, 0.0)
        rows.append(
            MonthlyStat(
                year=year,
                month=month,
                label=calendar.month_abbr[month],
                revenue=_round(rev),
                cost=_round(cost_total),
                profit=_round(rev - cost_total),
                contracts=contract_counts.get(month, 0),
            )
        )
    return rows


def yearly(db: Session) -> list[YearlyStat]:
    contracts = db.query(Contract).filter(Contract.start_date.isnot(None)).all()
    costs = db.query(Cost).filter(Cost.incurred_on.isnot(None)).all()

    revenue = defaultdict(float)
    contract_counts = defaultdict(int)
    for c in contracts:
        revenue[c.start_date.year] += c.total_price
        contract_counts[c.start_date.year] += 1

    cost_by_year = defaultdict(float)
    for cost in costs:
        cost_by_year[cost.incurred_on.year] += cost.amount

    years = sorted(set(revenue) | set(cost_by_year))
    rows: list[YearlyStat] = []
    for year in years:
        rev = revenue.get(year, 0.0)
        cost_total = cost_by_year.get(year, 0.0)
        rows.append(
            YearlyStat(
                year=year,
                revenue=_round(rev),
                cost=_round(cost_total),
                profit=_round(rev - cost_total),
                contracts=contract_counts.get(year, 0),
            )
        )
    return rows


def by_lift(db: Session) -> list[LiftStat]:
    lifts = db.query(Lift).options(joinedload(Lift.lift_type)).all()
    contracts = db.query(Contract).all()
    costs = db.query(Cost).all()

    revenue = defaultdict(float)
    contract_counts = defaultdict(int)
    for c in contracts:
        revenue[c.lift_id] += c.total_price
        contract_counts[c.lift_id] += 1

    cost_by_lift = defaultdict(float)
    for cost in costs:
        cost_by_lift[cost.lift_id] += cost.amount

    rows: list[LiftStat] = []
    for lift in lifts:
        rev = revenue.get(lift.id, 0.0)
        cost_total = cost_by_lift.get(lift.id, 0.0)
        rows.append(
            LiftStat(
                lift_id=lift.id,
                uid=lift.uid,
                name=lift.name,
                lift_type_name=lift.lift_type_name,
                revenue=_round(rev),
                cost=_round(cost_total),
                profit=_round(rev - cost_total),
                contracts=contract_counts.get(lift.id, 0),
            )
        )
    rows.sort(key=lambda r: r.profit, reverse=True)
    return rows


def lift_detail(db: Session, lift_id: int, year: int) -> LiftStatDetail | None:
    lift = (
        db.query(Lift)
        .options(joinedload(Lift.lift_type))
        .filter(Lift.id == lift_id)
        .first()
    )
    if lift is None:
        return None

    contracts = db.query(Contract).filter(Contract.lift_id == lift_id).all()
    costs = db.query(Cost).filter(Cost.lift_id == lift_id).all()

    total_revenue = sum(c.total_price for c in contracts)
    total_cost = sum(c.amount for c in costs)

    # Monthly breakdown for the requested year
    revenue_m = defaultdict(float)
    counts_m = defaultdict(int)
    for c in contracts:
        if c.start_date and c.start_date.year == year:
            revenue_m[c.start_date.month] += c.total_price
            counts_m[c.start_date.month] += 1
    cost_m = defaultdict(float)
    for cost in costs:
        if cost.incurred_on and cost.incurred_on.year == year:
            cost_m[cost.incurred_on.month] += cost.amount

    monthly_rows = [
        MonthlyStat(
            year=year,
            month=month,
            label=calendar.month_abbr[month],
            revenue=_round(revenue_m.get(month, 0.0)),
            cost=_round(cost_m.get(month, 0.0)),
            profit=_round(revenue_m.get(month, 0.0) - cost_m.get(month, 0.0)),
            contracts=counts_m.get(month, 0),
        )
        for month in range(1, 13)
    ]

    # Yearly breakdown across all years
    revenue_y = defaultdict(float)
    counts_y = defaultdict(int)
    for c in contracts:
        if c.start_date:
            revenue_y[c.start_date.year] += c.total_price
            counts_y[c.start_date.year] += 1
    cost_y = defaultdict(float)
    for cost in costs:
        if cost.incurred_on:
            cost_y[cost.incurred_on.year] += cost.amount
    years = sorted(set(revenue_y) | set(cost_y))
    yearly_rows = [
        YearlyStat(
            year=y,
            revenue=_round(revenue_y.get(y, 0.0)),
            cost=_round(cost_y.get(y, 0.0)),
            profit=_round(revenue_y.get(y, 0.0) - cost_y.get(y, 0.0)),
            contracts=counts_y.get(y, 0),
        )
        for y in years
    ]

    return LiftStatDetail(
        lift_id=lift.id,
        uid=lift.uid,
        name=lift.name,
        lift_type_name=lift.lift_type_name,
        revenue=_round(total_revenue),
        cost=_round(total_cost),
        profit=_round(total_revenue - total_cost),
        contracts=len(contracts),
        monthly=monthly_rows,
        yearly=yearly_rows,
    )
