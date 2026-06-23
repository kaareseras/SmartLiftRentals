from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_admin
from app.schemas.contract import ContractCreate, ContractResponse, ContractUpdate
from app.services.contract import (
    create_contract,
    delete_contract,
    get_contract,
    get_contracts,
    update_contract,
)
from app.services.customer import get_customer
from app.services.lift import get_lift

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
    dependencies=[Depends(get_current_admin)],
)


def _validate_refs(db: Session, lift_id: int | None, customer_id: int | None) -> None:
    if lift_id is not None and get_lift(db, lift_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lift not found")
    if customer_id is not None and get_customer(db, customer_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer not found")


@router.get("", response_model=list[ContractResponse])
def list_contracts(
    lift_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ContractResponse]:
    return get_contracts(db, lift_id=lift_id)


@router.get("/{contract_id}", response_model=ContractResponse)
def read_contract(contract_id: int, db: Session = Depends(get_db)) -> ContractResponse:
    contract = get_contract(db, contract_id)
    if contract is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    return contract


@router.post("", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
def create_contract_endpoint(
    payload: ContractCreate, db: Session = Depends(get_db)
) -> ContractResponse:
    _validate_refs(db, payload.lift_id, payload.customer_id)
    return create_contract(db, payload)


@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract_endpoint(
    contract_id: int, payload: ContractUpdate, db: Session = Depends(get_db)
) -> ContractResponse:
    _validate_refs(db, payload.lift_id, payload.customer_id)
    contract = update_contract(db, contract_id, payload)
    if contract is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    return contract


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract_endpoint(contract_id: int, db: Session = Depends(get_db)) -> Response:
    if not delete_contract(db, contract_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
