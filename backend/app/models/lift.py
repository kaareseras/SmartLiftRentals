from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, func, text

from app.config.database import Base


class Lift(Base):
    __tablename__ = "lifts"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, server_default=text("'available'"))
    location = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )
