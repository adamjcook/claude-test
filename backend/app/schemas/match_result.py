from enum import Enum
from typing import Literal

from pydantic import BaseModel


class MatchStatus(str, Enum):
    MATCHED = "matched"
    PARTIAL = "partial"
    NOT_MATCHED = "not_matched"


class RuleCheck(BaseModel):
    rule_name: str
    passed: bool
    category: Literal["hard", "soft"]
    reason: str


class MatchResult(BaseModel):
    grant_id: str
    grant_name: str
    status: MatchStatus
    checks: list[RuleCheck]
    missing_requirements: list[str]
