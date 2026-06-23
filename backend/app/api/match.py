from fastapi import APIRouter

from app.data.loader import get_all_grants
from app.matching.engine import match_all
from app.models.farm_profile import FarmProfile
from app.schemas.match_result import MatchResult

router = APIRouter(prefix="/api/match", tags=["match"])


@router.post("", response_model=list[MatchResult])
def match_grants(profile: FarmProfile) -> list[MatchResult]:
    grants = get_all_grants()
    return match_all(grants, profile)
