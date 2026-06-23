from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_admin
from app.schemas.statistics import (
    LiftStat,
    LiftStatDetail,
    MonthlyStat,
    OverviewStats,
    YearlyStat,
)
from app.services import statistics

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/overview", response_model=OverviewStats)
def get_overview(db: Session = Depends(get_db)) -> OverviewStats:
    return statistics.overview(db)


@router.get("/monthly", response_model=list[MonthlyStat])
def get_monthly(
    year: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[MonthlyStat]:
    return statistics.monthly(db, year or date.today().year)


@router.get("/yearly", response_model=list[YearlyStat])
def get_yearly(db: Session = Depends(get_db)) -> list[YearlyStat]:
    return statistics.yearly(db)


@router.get("/by-lift", response_model=list[LiftStat])
def get_by_lift(db: Session = Depends(get_db)) -> list[LiftStat]:
    return statistics.by_lift(db)


@router.get("/lifts/{lift_id}", response_model=LiftStatDetail)
def get_lift_detail(
    lift_id: int,
    year: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> LiftStatDetail:
    detail = statistics.lift_detail(db, lift_id, year or date.today().year)
    if detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lift not found")
    return detail
