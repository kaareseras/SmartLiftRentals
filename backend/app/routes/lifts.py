from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.lift import LiftCreate, LiftResponse, LiftUpdate
from app.services.lift import create_lift, delete_lift, get_lift, get_lifts, update_lift

router = APIRouter(prefix="/lifts", tags=["lifts"])


@router.get("", response_model=list[LiftResponse])
def list_lifts(db: Session = Depends(get_db)) -> list[LiftResponse]:
    return get_lifts(db)


@router.get("/{lift_id}", response_model=LiftResponse)
def read_lift(lift_id: int, db: Session = Depends(get_db)) -> LiftResponse:
    lift = get_lift(db, lift_id)
    if lift is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lift not found")
    return lift


@router.post("", response_model=LiftResponse, status_code=status.HTTP_201_CREATED)
def create_lift_endpoint(payload: LiftCreate, db: Session = Depends(get_db)) -> LiftResponse:
    return create_lift(db, payload)


@router.put("/{lift_id}", response_model=LiftResponse)
def update_lift_endpoint(
    lift_id: int,
    payload: LiftUpdate,
    db: Session = Depends(get_db),
) -> LiftResponse:
    lift = update_lift(db, lift_id, payload)
    if lift is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lift not found")
    return lift


@router.delete("/{lift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lift_endpoint(lift_id: int, db: Session = Depends(get_db)) -> Response:
    deleted = delete_lift(db, lift_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lift not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
