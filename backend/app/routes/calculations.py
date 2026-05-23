from fastapi import APIRouter
from app.models import CalculationInput
from app.services.calculations import calculate_indicator

router = APIRouter(tags=["calculations"])


@router.post("/calculate")
def calculate(payload: CalculationInput):
    return calculate_indicator(payload.indicator, payload.data)