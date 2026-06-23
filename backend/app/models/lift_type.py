from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class LiftType(Base):
    __tablename__ = "lift_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    manufacturer = Column(String(255), nullable=True)
    model = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    default_daily_rate = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )

    lifts = relationship("Lift", back_populates="lift_type")

    @property
    def lift_count(self) -> int:
        return len(self.lifts)
