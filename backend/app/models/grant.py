from datetime import date
from enum import Enum

from pydantic import BaseModel


class SchemeType(str, Enum):
    REVENUE = "revenue"
    CAPITAL = "capital"
    HIGHER_TIER_AGREEMENT = "higher_tier_agreement"


class FarmType(str, Enum):
    ARABLE = "arable"
    LIVESTOCK = "livestock"
    DAIRY = "dairy"
    HORTICULTURE = "horticulture"
    MIXED = "mixed"
    UPLAND = "upland"
    FORESTRY = "forestry"
    ANY = "any"


class UKRegion(str, Enum):
    ENGLAND = "england"
    SCOTLAND = "scotland"
    WALES = "wales"
    NORTHERN_IRELAND = "northern_ireland"


class Activity(str, Enum):
    LIVESTOCK_GRAZING = "livestock_grazing"
    ARABLE_CROPPING = "arable_cropping"
    HORTICULTURE = "horticulture"
    WOODLAND_MANAGEMENT = "woodland_management"
    HEDGEROW_MANAGEMENT = "hedgerow_management"
    SLURRY_MANAGEMENT = "slurry_management"
    ORGANIC = "organic"
    ENVIRONMENTAL_STEWARDSHIP = "environmental_stewardship"
    EQUIPMENT_TECHNOLOGY = "equipment_technology"
    WATER_QUALITY = "water_quality"


class EligibilityCriteria(BaseModel):
    min_land_size_ha: float | None = None
    max_land_size_ha: float | None = None
    eligible_farm_types: list[FarmType] = []
    eligible_regions: list[UKRegion] = []
    required_activities: list[Activity] = []
    requires_sbi: bool = False
    requires_no_existing_elm_agreement: bool = False
    requires_environmentally_significant_site: bool = False
    excluded_farm_types: list[FarmType] = []


class ApplicationWindow(BaseModel):
    opens: date
    closes: date | None = None
    label: str


class Grant(BaseModel):
    id: str
    name: str
    administering_body: str
    scheme_type: SchemeType
    summary: str
    description: str
    funding_amount_description: str
    eligibility: EligibilityCriteria
    application_windows: list[ApplicationWindow]
    application_url: str
    last_verified_date: date
    special_rule: str | None = None
