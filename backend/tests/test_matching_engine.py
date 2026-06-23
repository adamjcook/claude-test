from app.matching.engine import evaluate, match_all
from app.schemas.match_result import MatchStatus


def _result_for(grants, grant_id, profile):
    grant = next(g for g in grants if g.id == grant_id)
    return evaluate(grant, profile)


def test_small_arable_farm_matches_sfi_window_1(loaded_grants, small_arable_farm_england):
    result = _result_for(loaded_grants, "sfi-2026", small_arable_farm_england)
    assert result.status == MatchStatus.MATCHED
    assert any("Window 1" in c.reason for c in result.checks)


def test_small_arable_farm_partial_on_capital_grants(loaded_grants, small_arable_farm_england):
    result = _result_for(loaded_grants, "countryside-stewardship-capital-grants", small_arable_farm_england)
    assert result.status == MatchStatus.PARTIAL
    assert result.missing_requirements


def test_large_dairy_farm_with_elm_matches_sfi_window_2(loaded_grants, large_dairy_farm_with_elm):
    result = _result_for(loaded_grants, "sfi-2026", large_dairy_farm_with_elm)
    assert result.status == MatchStatus.MATCHED
    assert any("Window 2" in c.reason for c in result.checks)


def test_large_dairy_farm_partial_on_higher_tier(loaded_grants, large_dairy_farm_with_elm):
    result = _result_for(loaded_grants, "countryside-stewardship-higher-tier", large_dairy_farm_with_elm)
    assert result.status == MatchStatus.PARTIAL


def test_scotland_farm_not_matched_on_all_grants(loaded_grants, scotland_livestock_farm):
    results = match_all(loaded_grants, scotland_livestock_farm)
    assert len(results) == 4
    assert all(r.status == MatchStatus.NOT_MATCHED for r in results)
    assert all(any("region" in c.rule_name for c in r.checks if not c.passed) for r in results)


def test_sssi_woodland_farm_matches_higher_tier(loaded_grants, farm_with_sssi_woodland):
    result = _result_for(loaded_grants, "countryside-stewardship-higher-tier", farm_with_sssi_woodland)
    assert result.status == MatchStatus.MATCHED
    assert result.missing_requirements == []


def test_sssi_woodland_farm_partial_on_fetf(loaded_grants, farm_with_sssi_woodland):
    result = _result_for(loaded_grants, "farming-equipment-technology-fund", farm_with_sssi_woodland)
    assert result.status == MatchStatus.PARTIAL


def test_match_all_sorts_matched_before_not_matched(loaded_grants, small_arable_farm_england):
    results = match_all(loaded_grants, small_arable_farm_england)
    statuses = [r.status for r in results]
    order = {MatchStatus.MATCHED: 0, MatchStatus.PARTIAL: 1, MatchStatus.NOT_MATCHED: 2}
    assert statuses == sorted(statuses, key=lambda s: order[s])


def test_missing_requirements_empty_when_matched(loaded_grants, small_arable_farm_england):
    result = _result_for(loaded_grants, "sfi-2026", small_arable_farm_england)
    assert result.status == MatchStatus.MATCHED
    assert result.missing_requirements == []


def test_missing_requirements_populated_when_not_matched(loaded_grants, scotland_livestock_farm):
    result = _result_for(loaded_grants, "sfi-2026", scotland_livestock_farm)
    assert result.status == MatchStatus.NOT_MATCHED
    assert result.missing_requirements
