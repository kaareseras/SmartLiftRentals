from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import relationship

from app.config.database import Base


class Lift(Base):
    __tablename__ = "lifts"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    lift_type_id = Column(
        Integer, ForeignKey("lift_types.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status = Column(String(50), nullable=False, server_default=text("'available'"))
    location = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    battery_voltage = Column(Float, nullable=True)
    telemetry_state = Column(String(50), nullable=True, server_default=text("'idle'"))
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )

    lift_type = relationship("LiftType", back_populates="lifts")
    contracts = relationship(
        "Contract", back_populates="lift", cascade="all, delete-orphan"
    )
    costs = relationship("Cost", back_populates="lift", cascade="all, delete-orphan")

    @property
    def lift_type_name(self) -> str | None:
        return self.lift_type.name if self.lift_type else None

    @property
    def model(self) -> str | None:
        return self.lift_type.model if self.lift_type else None
