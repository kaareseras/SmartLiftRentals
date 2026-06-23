from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.config.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(func.lower(User.email) == email.lower()).first()


def get_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.created_at.asc(), User.id.asc()).all()


def create_user(db: Session, payload: UserCreate) -> User:
    user = User(
        name=payload.name,
        email=str(payload.email),
        hashed_password=hash_password(payload.password),
        is_admin=payload.is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def _ensure_user(db: Session, *, name: str, email: str, password: str, is_admin: bool) -> None:
    if get_user_by_email(db, email) is not None:
        return
    db.add(
        User(
            name=name,
            email=email,
            hashed_password=hash_password(password),
            is_admin=is_admin,
        )
    )
    db.commit()


def seed_users(db: Session) -> None:
    """Seed a default administrator (and a demo operator) for first-run access."""
    _ensure_user(
        db,
        name=settings.SEED_ADMIN_NAME,
        email=settings.SEED_ADMIN_EMAIL,
        password=settings.SEED_ADMIN_PASSWORD,
        is_admin=True,
    )
    _ensure_user(
        db,
        name="Olivia Operator",
        email="operator@smartliftrentals.com",
        password="Operator123!",
        is_admin=False,
    )
