from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Cost(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, index=True)
    lift_id = Column(Integer, ForeignKey("lifts.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(50), nullable=False, server_default=text("'other'"))
    description = Column(String(500), nullable=True)
    amount = Column(Float, nullable=False)
    incurred_on = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )

    lift = relationship("Lift", back_populates="costs")

    @property
    def lift_name(self) -> str | None:
        return self.lift.name if self.lift else None

    @property
    def lift_uid(self) -> str | None:
        return self.lift.uid if self.lift else None
