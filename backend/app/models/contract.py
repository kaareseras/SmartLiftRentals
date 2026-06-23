from __future__ import annotations

from datetime import date, datetime, timedelta

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


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    lift_id = Column(Integer, ForeignKey("lifts.id", ondelete="CASCADE"), nullable=False, index=True)
    customer_id = Column(
        Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_date = Column(Date, nullable=False)
    duration_days = Column(Integer, nullable=False)
    daily_rate = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, server_default=text("'active'"))
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )

    lift = relationship("Lift", back_populates="contracts")
    customer = relationship("Customer", back_populates="contracts")

    @property
    def end_date(self) -> date | None:
        if self.start_date is None or self.duration_days is None:
            return None
        return self.start_date + timedelta(days=self.duration_days)

    @property
    def total_price(self) -> float:
        if self.daily_rate is None or self.duration_days is None:
            return 0.0
        return round(self.daily_rate * self.duration_days, 2)

    @property
    def customer_name(self) -> str | None:
        return self.customer.name if self.customer else None

    @property
    def lift_name(self) -> str | None:
        return self.lift.name if self.lift else None

    @property
    def lift_uid(self) -> str | None:
        return self.lift.uid if self.lift else None
