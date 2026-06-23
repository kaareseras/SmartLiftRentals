from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_admin
from app.schemas.cost import CostCreate, CostResponse, CostUpdate
from app.services.cost import create_cost, delete_cost, get_cost, get_costs, update_cost
from app.services.lift import get_lift

router = APIRouter(
    prefix="/costs",
    tags=["costs"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("", response_model=list[CostResponse])
def list_costs(
    lift_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[CostResponse]:
    return get_costs(db, lift_id=lift_id)


@router.get("/{cost_id}", response_model=CostResponse)
def read_cost(cost_id: int, db: Session = Depends(get_db)) -> CostResponse:
    cost = get_cost(db, cost_id)
    if cost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")
    return cost


@router.post("", response_model=CostResponse, status_code=status.HTTP_201_CREATED)
def create_cost_endpoint(payload: CostCreate, db: Session = Depends(get_db)) -> CostResponse:
    if get_lift(db, payload.lift_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lift not found")
    return create_cost(db, payload)


@router.put("/{cost_id}", response_model=CostResponse)
def update_cost_endpoint(
    cost_id: int, payload: CostUpdate, db: Session = Depends(get_db)
) -> CostResponse:
    if payload.lift_id is not None and get_lift(db, payload.lift_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lift not found")
    cost = update_cost(db, cost_id, payload)
    if cost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")
    return cost


@router.delete("/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost_endpoint(cost_id: int, db: Session = Depends(get_db)) -> Response:
    if not delete_cost(db, cost_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
