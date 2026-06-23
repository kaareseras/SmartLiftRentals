from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.lift_type import LiftType
from app.schemas.lift_type import LiftTypeCreate, LiftTypeUpdate


def get_lift_types(db: Session) -> list[LiftType]:
    return db.query(LiftType).order_by(LiftType.name.asc()).all()


def get_lift_type(db: Session, lift_type_id: int) -> LiftType | None:
    return db.query(LiftType).filter(LiftType.id == lift_type_id).first()


def create_lift_type(db: Session, payload: LiftTypeCreate) -> LiftType:
    lift_type = LiftType(**payload.model_dump())
    db.add(lift_type)
    db.commit()
    db.refresh(lift_type)
    return lift_type


def update_lift_type(db: Session, lift_type_id: int, payload: LiftTypeUpdate) -> LiftType | None:
    lift_type = get_lift_type(db, lift_type_id)
    if lift_type is None:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(lift_type, field, value)
    db.add(lift_type)
    db.commit()
    db.refresh(lift_type)
    return lift_type


def delete_lift_type(db: Session, lift_type_id: int) -> bool:
    lift_type = get_lift_type(db, lift_type_id)
    if lift_type is None:
        return False
    db.delete(lift_type)
    db.commit()
    return True
