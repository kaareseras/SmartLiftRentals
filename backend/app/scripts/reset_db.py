"""One-off development helper: drop and recreate all tables, then seed.

Usage (from the backend container):
    uv run python -m app.scripts.reset_db

This DESTROYS all data in the configured database and is intended for local
development only, where the schema is managed by create_all rather than
Alembic migrations.
"""
from __future__ import annotations

from app.config.database import Base, SessionLocal, engine
from app.models import *  # noqa: F401,F403  (register all tables on Base.metadata)
from app.services.seed import seed_all


def main() -> None:
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Seeding data...")
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()
    print("Done.")


if __name__ == "__main__":
    main()
