from app.data.loader import get_all_grants, get_grant_by_id


def test_loads_four_grants():
    grants = get_all_grants()
    assert len(grants) == 4


def test_all_grants_have_unique_ids():
    grants = get_all_grants()
    ids = [g.id for g in grants]
    assert len(ids) == len(set(ids))


def test_get_grant_by_id_found():
    grant = get_grant_by_id("sfi-2026")
    assert grant is not None
    assert grant.name == "Sustainable Farming Incentive 2026 (SFI26)"


def test_get_grant_by_id_not_found():
    assert get_grant_by_id("does-not-exist") is None
