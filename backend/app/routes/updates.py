from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from app.core.dependencies import require_admin
from app.db_models import User
from app.services.updates import get_latest_updates, get_all_updates, add_update


router = APIRouter(tags=["updates"])


class UpdateIn(BaseModel):
    date: str
    indicators: List[str]
    source: str


@router.get("/updates/latest")
def latest_updates():
    return get_latest_updates()


@router.get("/updates")
def all_updates():
    return get_all_updates()


@router.post("/updates")
def create_update(
    payload: UpdateIn,
    admin: User = Depends(require_admin),
):
    add_update(payload.model_dump())
    return {"status": "ok"}