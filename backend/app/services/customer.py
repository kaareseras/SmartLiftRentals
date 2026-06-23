from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def get_customers(db: Session) -> list[Customer]:
    return db.query(Customer).order_by(Customer.name.asc()).all()


def get_customer(db: Session, customer_id: int) -> Customer | None:
    return db.query(Customer).filter(Customer.id == customer_id).first()


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    data = payload.model_dump()
    if data.get("email") is not None:
        data["email"] = str(data["email"])
    customer = Customer(**data)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer_id: int, payload: CustomerUpdate) -> Customer | None:
    customer = get_customer(db, customer_id)
    if customer is None:
        return None
    data = payload.model_dump(exclude_unset=True)
    if data.get("email") is not None:
        data["email"] = str(data["email"])
    for field, value in data.items():
        setattr(customer, field, value)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> bool:
    customer = get_customer(db, customer_id)
    if customer is None:
        return False
    db.delete(customer)
    db.commit()
    return True
