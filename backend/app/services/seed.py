from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy.orm import Session

from app.models.contract import Contract
from app.models.cost import Cost
from app.models.customer import Customer
from app.models.lift import Lift
from app.models.lift_type import LiftType
from app.services.user import seed_users


def seed_all(db: Session) -> None:
    seed_users(db)
    seed_demo_data(db)


def seed_demo_data(db: Session) -> None:
    """Populate reference and demo data for a fresh database (idempotent)."""
    if db.query(LiftType).count() > 0:
        return

    tower = LiftType(
        name="Tower Crane",
        manufacturer="Potain",
        model="MDT 219",
        description="Topless tower crane for high-rise construction.",
        default_daily_rate=850.0,
    )
    mast = LiftType(
        name="Mast Climber",
        manufacturer="Alimak",
        model="MC 450",
        description="Mast climbing work platform for facade work.",
        default_daily_rate=420.0,
    )
    hoist = LiftType(
        name="Material Hoist",
        manufacturer="GEDA",
        model="1500 Z/ZP",
        description="Transport platform for materials and personnel.",
        default_daily_rate=300.0,
    )
    scissor = LiftType(
        name="Scissor Lift",
        manufacturer="Genie",
        model="GS-4047",
        description="Electric scissor lift for indoor access work.",
        default_daily_rate=180.0,
    )
    db.add_all([tower, mast, hoist, scissor])
    db.flush()

    now = datetime.now(UTC)
    lifts = [
        Lift(uid="LFT-0481", name="Tower Crane North", lift_type_id=tower.id, status="rented",
             location="Copenhagen", latitude=55.6761, longitude=12.5683,
             battery_voltage=23.8, telemetry_state="operating", last_seen=now),
        Lift(uid="LFT-0192", name="Material Hoist B12", lift_type_id=hoist.id, status="rented",
             location="Aarhus", latitude=56.1629, longitude=10.2039,
             battery_voltage=25.4, telemetry_state="charging", last_seen=now),
        Lift(uid="LFT-0337", name="Mast Climber 4", lift_type_id=mast.id, status="maintenance",
             location="Odense", latitude=55.4038, longitude=10.4024,
             battery_voltage=24.1, telemetry_state="idle", last_seen=now),
        Lift(uid="LFT-0508", name="Material Hoist 9", lift_type_id=hoist.id, status="available",
             location="Aalborg", latitude=57.0488, longitude=9.9217,
             battery_voltage=23.5, telemetry_state="operating", last_seen=now),
        Lift(uid="LFT-0623", name="Scissor Lift 12", lift_type_id=scissor.id, status="available",
             location="Esbjerg", latitude=55.4765, longitude=8.4594,
             battery_voltage=25.8, telemetry_state="charging", last_seen=now),
        Lift(uid="LFT-0701", name="Tower Crane South", lift_type_id=tower.id, status="available",
             location="Kolding", latitude=55.4904, longitude=9.4722,
             battery_voltage=24.0, telemetry_state="operating", last_seen=now),
    ]
    db.add_all(lifts)
    db.flush()

    skyline = Customer(
        name="Skyline Construction Ltd",
        email="contact@skyline.example",
        phone="+45 70 11 22 33",
        company="Skyline Construction Ltd",
        address="Havnegade 12, 1058 Copenhagen",
    )
    meridian = Customer(
        name="Meridian Builders",
        email="hello@meridian.example",
        phone="+45 70 44 55 66",
        company="Meridian Builders A/S",
        address="Industrivej 4, 8000 Aarhus",
    )
    apex = Customer(
        name="Apex Infrastructure",
        email="projects@apex.example",
        phone="+45 70 77 88 99",
        company="Apex Infrastructure ApS",
        address="Stationsvej 9, 5000 Odense",
    )
    db.add_all([skyline, meridian, apex])
    db.flush()

    contracts = [
        Contract(lift_id=lifts[2].id, customer_id=skyline.id, start_date=date(2025, 11, 10),
                 duration_days=30, daily_rate=420.0, status="completed"),
        Contract(lift_id=lifts[1].id, customer_id=meridian.id, start_date=date(2025, 12, 1),
                 duration_days=40, daily_rate=300.0, status="completed"),
        Contract(lift_id=lifts[0].id, customer_id=skyline.id, start_date=date(2026, 1, 15),
                 duration_days=60, daily_rate=850.0, status="active"),
        Contract(lift_id=lifts[1].id, customer_id=meridian.id, start_date=date(2026, 2, 1),
                 duration_days=45, daily_rate=300.0, status="active"),
        Contract(lift_id=lifts[4].id, customer_id=apex.id, start_date=date(2026, 3, 5),
                 duration_days=20, daily_rate=180.0, status="completed"),
        Contract(lift_id=lifts[0].id, customer_id=apex.id, start_date=date(2026, 5, 1),
                 duration_days=90, daily_rate=850.0, status="active"),
    ]
    db.add_all(contracts)

    costs = [
        Cost(lift_id=lifts[2].id, category="repair", description="Drive motor replacement",
             amount=3400.0, incurred_on=date(2025, 11, 15)),
        Cost(lift_id=lifts[1].id, category="insurance", description="Annual insurance premium",
             amount=600.0, incurred_on=date(2025, 12, 5)),
        Cost(lift_id=lifts[0].id, category="maintenance", description="Scheduled inspection",
             amount=1200.0, incurred_on=date(2026, 1, 20)),
        Cost(lift_id=lifts[4].id, category="maintenance", description="Battery service",
             amount=250.0, incurred_on=date(2026, 3, 10)),
        Cost(lift_id=lifts[0].id, category="transport", description="Site relocation",
             amount=800.0, incurred_on=date(2026, 5, 2)),
        Cost(lift_id=lifts[3].id, category="maintenance", description="Cable inspection",
             amount=450.0, incurred_on=date(2026, 6, 2)),
    ]
    db.add_all(costs)

    db.commit()
