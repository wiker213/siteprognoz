from fastapi import APIRouter
from app.services.region import get_region

router = APIRouter(tags=["region"])


@router.get("/region")
def region():
    return get_region()