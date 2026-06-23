from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_admin
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer import (
    create_customer,
    delete_customer,
    get_customer,
    get_customers,
    update_customer,
)

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("", response_model=list[CustomerResponse])
def list_customers(db: Session = Depends(get_db)) -> list[CustomerResponse]:
    return get_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)) -> CustomerResponse:
    customer = get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer_endpoint(
    payload: CustomerCreate, db: Session = Depends(get_db)
) -> CustomerResponse:
    return create_customer(db, payload)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(
    customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)
) -> CustomerResponse:
    customer = update_customer(db, customer_id, payload)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_endpoint(customer_id: int, db: Session = Depends(get_db)) -> Response:
    if not delete_customer(db, customer_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
