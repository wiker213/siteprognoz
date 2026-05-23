from fastapi import APIRouter
from app.models import ForecastInput
from app.services.forecast import run_forecast

router = APIRouter(tags=["forecast"])


@router.post("/forecast")
def forecast(payload: ForecastInput):
    result = run_forecast(payload.method, payload.values, payload.horizon)
    return {"forecast": result}