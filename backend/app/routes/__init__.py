from .calculations import router as calculations_router
from .forecast import router as forecast_router
from .region import router as region_router
from .updates import router as updates_router
from .auth import router as auth_router


all_routers = [
    calculations_router,
    forecast_router,
    region_router,
    updates_router,
    auth_router,
]