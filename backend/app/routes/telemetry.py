from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.schemas.telemetry import LiftTelemetry
from app.services.lift import get_lifts

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.get("", response_model=list[LiftTelemetry])
def list_telemetry(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
) -> list[LiftTelemetry]:
    return get_lifts(db)
