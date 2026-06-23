from pydantic import BaseModel

from app.models.grant import Activity, FarmType, UKRegion


class FarmProfile(BaseModel):
    farm_type: FarmType
    size_hectares: float
    region: UKRegion
    activities: list[Activity] = []
    has_sbi: bool
    sbi_registered_before_2026_01_01: bool = False
    has_existing_elm_agreement: bool = False
    has_environmentally_significant_features: bool = False
