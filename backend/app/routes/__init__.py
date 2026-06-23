from app.routes.auth import router as auth_router
from app.routes.contracts import router as contract_router
from app.routes.costs import router as cost_router
from app.routes.customers import router as customer_router
from app.routes.health import router as health_router
from app.routes.lift_types import router as lift_type_router
from app.routes.lifts import router as lift_router
from app.routes.statistics import router as statistics_router
from app.routes.telemetry import router as telemetry_router
from app.routes.users import router as user_router

__all__ = [
    "auth_router",
    "contract_router",
    "cost_router",
    "customer_router",
    "health_router",
    "lift_router",
    "lift_type_router",
    "statistics_router",
    "telemetry_router",
    "user_router",
]
