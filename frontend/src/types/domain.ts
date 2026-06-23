export type FarmType =
  | 'arable'
  | 'livestock'
  | 'dairy'
  | 'horticulture'
  | 'mixed'
  | 'upland'
  | 'forestry'
  | 'any'

export type UKRegion = 'england' | 'scotland' | 'wales' | 'northern_ireland'

export type Activity =
  | 'livestock_grazing'
  | 'arable_cropping'
  | 'horticulture'
  | 'woodland_management'
  | 'hedgerow_management'
  | 'slurry_management'
  | 'organic'
  | 'environmental_stewardship'
  | 'equipment_technology'
  | 'water_quality'

export interface FarmProfile {
  farm_type: FarmType
  size_hectares: number
  region: UKRegion
  activities: Activity[]
  has_sbi: boolean
  sbi_registered_before_2026_01_01: boolean
  has_existing_elm_agreement: boolean
  has_environmentally_significant_features: boolean
}

export interface ApplicationWindow {
  opens: string
  closes: string | null
  label: string
}

export interface Grant {
  id: string
  name: string
  administering_body: string
  scheme_type: 'revenue' | 'capital' | 'higher_tier_agreement'
  summary: string
  description: string
  funding_amount_description: string
  application_windows: ApplicationWindow[]
  application_url: string
  last_verified_date: string
}

export type MatchStatus = 'matched' | 'partial' | 'not_matched'

export interface RuleCheck {
  rule_name: string
  passed: boolean
  category: 'hard' | 'soft'
  reason: string
}

export interface MatchResult {
  grant_id: string
  grant_name: string
  status: MatchStatus
  checks: RuleCheck[]
  missing_requirements: string[]
}
