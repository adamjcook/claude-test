import pytest

from app.data.loader import get_all_grants
from app.models.farm_profile import FarmProfile
from app.models.grant import Activity, FarmType, UKRegion


@pytest.fixture
def loaded_grants():
    return get_all_grants()


@pytest.fixture
def small_arable_farm_england() -> FarmProfile:
    return FarmProfile(
        farm_type=FarmType.ARABLE,
        size_hectares=10,
        region=UKRegion.ENGLAND,
        activities=[Activity.ARABLE_CROPPING],
        has_sbi=True,
        sbi_registered_before_2026_01_01=True,
        has_existing_elm_agreement=False,
        has_environmentally_significant_features=False,
    )


@pytest.fixture
def large_dairy_farm_with_elm() -> FarmProfile:
    return FarmProfile(
        farm_type=FarmType.DAIRY,
        size_hectares=200,
        region=UKRegion.ENGLAND,
        activities=[],
        has_sbi=True,
        sbi_registered_before_2026_01_01=True,
        has_existing_elm_agreement=True,
        has_environmentally_significant_features=False,
    )


@pytest.fixture
def scotland_livestock_farm() -> FarmProfile:
    return FarmProfile(
        farm_type=FarmType.LIVESTOCK,
        size_hectares=80,
        region=UKRegion.SCOTLAND,
        activities=[Activity.LIVESTOCK_GRAZING],
        has_sbi=False,
        has_existing_elm_agreement=False,
        has_environmentally_significant_features=False,
    )


@pytest.fixture
def farm_with_sssi_woodland() -> FarmProfile:
    return FarmProfile(
        farm_type=FarmType.MIXED,
        size_hectares=60,
        region=UKRegion.ENGLAND,
        activities=[Activity.WOODLAND_MANAGEMENT],
        has_sbi=True,
        has_existing_elm_agreement=False,
        has_environmentally_significant_features=True,
    )
