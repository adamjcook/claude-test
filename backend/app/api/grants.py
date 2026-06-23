from fastapi import APIRouter, HTTPException

from app.data.loader import get_all_grants, get_grant_by_id
from app.models.grant import Grant

router = APIRouter(prefix="/api/grants", tags=["grants"])


@router.get("", response_model=list[Grant])
def list_grants() -> list[Grant]:
    return get_all_grants()


@router.get("/{grant_id}", response_model=Grant)
def get_grant(grant_id: str) -> Grant:
    grant = get_grant_by_id(grant_id)
    if grant is None:
        raise HTTPException(status_code=404, detail=f"Grant '{grant_id}' not found")
    return grant
