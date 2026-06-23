from app.matching.rules import RULES
from app.models.farm_profile import FarmProfile
from app.models.grant import Grant
from app.schemas.match_result import MatchResult, MatchStatus, RuleCheck


def evaluate(grant: Grant, profile: FarmProfile) -> MatchResult:
    checks: list[RuleCheck] = []
    for rule in RULES:
        result = rule(grant, profile)
        if result is not None:
            checks.append(result)

    failed = [c for c in checks if not c.passed]
    if any(c.category == "hard" for c in failed):
        status = MatchStatus.NOT_MATCHED
    elif failed:
        status = MatchStatus.PARTIAL
    else:
        status = MatchStatus.MATCHED

    return MatchResult(
        grant_id=grant.id,
        grant_name=grant.name,
        status=status,
        checks=checks,
        missing_requirements=[c.reason for c in failed],
    )


_STATUS_ORDER = {MatchStatus.MATCHED: 0, MatchStatus.PARTIAL: 1, MatchStatus.NOT_MATCHED: 2}


def match_all(grants: list[Grant], profile: FarmProfile) -> list[MatchResult]:
    results = [evaluate(grant, profile) for grant in grants]
    return sorted(results, key=lambda r: _STATUS_ORDER[r.status])
