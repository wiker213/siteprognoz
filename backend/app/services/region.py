import json
from pathlib import Path
from app.models import RegionInfo

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "region.json"


def get_region() -> RegionInfo:
    if not DATA_PATH.exists():
        # если файла нет — вернём дефолт
        return RegionInfo(
            name="(не задано)",
            area_km2=0,
            population=0,
            vrp=None,
            industries=[],
            description=None,
        )

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return RegionInfo(**raw)