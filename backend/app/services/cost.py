from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.cost import Cost
from app.schemas.cost import CostCreate, CostUpdate


def get_costs(db: Session, lift_id: int | None = None) -> list[Cost]:
    query = db.query(Cost).options(joinedload(Cost.lift))
    if lift_id is not None:
        query = query.filter(Cost.lift_id == lift_id)
    return query.order_by(Cost.incurred_on.desc(), Cost.id.desc()).all()


def get_cost(db: Session, cost_id: int) -> Cost | None:
    return (
        db.query(Cost).options(joinedload(Cost.lift)).filter(Cost.id == cost_id).first()
    )


def create_cost(db: Session, payload: CostCreate) -> Cost:
    cost = Cost(**payload.model_dump())
    db.add(cost)
    db.commit()
    db.refresh(cost)
    return get_cost(db, cost.id) or cost


def update_cost(db: Session, cost_id: int, payload: CostUpdate) -> Cost | None:
    cost = get_cost(db, cost_id)
    if cost is None:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cost, field, value)
    db.add(cost)
    db.commit()
    db.refresh(cost)
    return get_cost(db, cost.id)


def delete_cost(db: Session, cost_id: int) -> bool:
    cost = get_cost(db, cost_id)
    if cost is None:
        return False
    db.delete(cost)
    db.commit()
    return True
