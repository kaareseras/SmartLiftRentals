from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate


def get_contracts(db: Session, lift_id: int | None = None) -> list[Contract]:
    query = db.query(Contract).options(
        joinedload(Contract.lift), joinedload(Contract.customer)
    )
    if lift_id is not None:
        query = query.filter(Contract.lift_id == lift_id)
    return query.order_by(Contract.start_date.desc(), Contract.id.desc()).all()


def get_contract(db: Session, contract_id: int) -> Contract | None:
    return (
        db.query(Contract)
        .options(joinedload(Contract.lift), joinedload(Contract.customer))
        .filter(Contract.id == contract_id)
        .first()
    )


def create_contract(db: Session, payload: ContractCreate) -> Contract:
    contract = Contract(**payload.model_dump())
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return get_contract(db, contract.id) or contract


def update_contract(db: Session, contract_id: int, payload: ContractUpdate) -> Contract | None:
    contract = get_contract(db, contract_id)
    if contract is None:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(contract, field, value)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return get_contract(db, contract.id)


def delete_contract(db: Session, contract_id: int) -> bool:
    contract = get_contract(db, contract_id)
    if contract is None:
        return False
    db.delete(contract)
    db.commit()
    return True
