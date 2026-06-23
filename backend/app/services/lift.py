from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.lift import Lift
from app.schemas.lift import LiftCreate, LiftUpdate


def get_lifts(db: Session) -> list[Lift]:
    return (
        db.query(Lift)
        .options(joinedload(Lift.lift_type))
        .order_by(Lift.id.asc())
        .all()
    )


def get_lift(db: Session, lift_id: int) -> Lift | None:
    return (
        db.query(Lift)
        .options(joinedload(Lift.lift_type))
        .filter(Lift.id == lift_id)
        .first()
    )


def create_lift(db: Session, payload: LiftCreate) -> Lift:
    lift = Lift(**payload.model_dump())
    db.add(lift)
    db.commit()
    db.refresh(lift)
    return get_lift(db, lift.id) or lift


def update_lift(db: Session, lift_id: int, payload: LiftUpdate) -> Lift | None:
    lift = get_lift(db, lift_id)
    if lift is None:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(lift, field, value)

    db.add(lift)
    db.commit()
    db.refresh(lift)
    return lift


def delete_lift(db: Session, lift_id: int) -> bool:
    lift = get_lift(db, lift_id)
    if lift is None:
        return False

    db.delete(lift)
    db.commit()
    return True
