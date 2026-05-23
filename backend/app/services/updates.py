import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "updates.json"

def _load_updates():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_updates(updates):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(updates, f, ensure_ascii=False, indent=2)

def get_all_updates():
    return _load_updates()

def get_latest_updates():
    updates = _load_updates()
    return updates[0] if updates else None

def add_update(update_obj: dict):
    updates = _load_updates()
    # добавляем в начало
    updates.insert(0, update_obj)
    _save_updates(updates)