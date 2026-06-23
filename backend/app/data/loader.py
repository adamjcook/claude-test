import json
from functools import lru_cache
from pathlib import Path

from app.models.grant import Grant

SEED_FILE = Path(__file__).parent / "grants_seed.json"


@lru_cache
def _load_grants() -> list[Grant]:
    raw = json.loads(SEED_FILE.read_text())
    return [Grant.model_validate(entry) for entry in raw]


def get_all_grants() -> list[Grant]:
    return _load_grants()


def get_grant_by_id(grant_id: str) -> Grant | None:
    return next((g for g in _load_grants() if g.id == grant_id), None)
