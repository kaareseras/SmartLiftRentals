from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_admin, get_current_user
from app.schemas.lift_type import LiftTypeCreate, LiftTypeResponse, LiftTypeUpdate
from app.services.lift_type import (
    create_lift_type,
    delete_lift_type,
    get_lift_type,
    get_lift_types,
    update_lift_type,
)

router = APIRouter(prefix="/lift-types", tags=["lift-types"])


@router.get("", response_model=list[LiftTypeResponse])
def list_lift_types(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
) -> list[LiftTypeResponse]:
    return get_lift_types(db)


@router.get("/{lift_type_id}", response_model=LiftTypeResponse)
def read_lift_type(
    lift_type_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
) -> LiftTypeResponse:
    lift_type = get_lift_type(db, lift_type_id)
    if lift_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lift type not found")
    return lift_type


@router.post(
    "",
    response_model=LiftTypeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def create_lift_type_endpoint(
    payload: LiftTypeCreate,
    db: Session = Depends(get_db),
) -> LiftTypeResponse:
    return create_lift_type(db, payload)


@router.put(
    "/{lift_type_id}",
    response_model=LiftTypeResponse,
    dependencies=[Depends(get_current_admin)],
)
def update_lift_type_endpoint(
    lift_type_id: int,
    payload: LiftTypeUpdate,
    db: Session = Depends(get_db),
) -> LiftTypeResponse:
    lift_type = update_lift_type(db, lift_type_id, payload)
    if lift_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lift type not found")
    return lift_type


@router.delete(
    "/{lift_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def delete_lift_type_endpoint(
    lift_type_id: int,
    db: Session = Depends(get_db),
) -> Response:
    lift_type = get_lift_type(db, lift_type_id)
    if lift_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lift type not found")
    if lift_type.lifts:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a lift type that is assigned to lifts",
        )
    delete_lift_type(db, lift_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
