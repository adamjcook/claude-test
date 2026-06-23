import { useState } from 'react'
import type { Activity, FarmProfile, FarmType, UKRegion } from '../types/domain'

const FARM_TYPES: { value: FarmType; label: string }[] = [
  { value: 'arable', label: 'Arable' },
  { value: 'livestock', label: 'Livestock' },
  { value: 'dairy', label: 'Dairy' },
  { value: 'horticulture', label: 'Horticulture' },
  { value: 'mixed', label: 'Mixed' },
  { value: 'upland', label: 'Upland' },
  { value: 'forestry', label: 'Forestry' },
]

const REGIONS: { value: UKRegion; label: string }[] = [
  { value: 'england', label: 'England' },
  { value: 'scotland', label: 'Scotland' },
  { value: 'wales', label: 'Wales' },
  { value: 'northern_ireland', label: 'Northern Ireland' },
]

const ACTIVITIES: { value: Activity; label: string }[] = [
  { value: 'livestock_grazing', label: 'Livestock grazing' },
  { value: 'arable_cropping', label: 'Arable cropping' },
  { value: 'horticulture', label: 'Horticulture' },
  { value: 'woodland_management', label: 'Woodland management' },
  { value: 'hedgerow_management', label: 'Hedgerow management' },
  { value: 'slurry_management', label: 'Slurry management' },
  { value: 'organic', label: 'Organic farming' },
  { value: 'environmental_stewardship', label: 'Environmental stewardship' },
  { value: 'equipment_technology', label: 'Equipment / technology upgrades' },
  { value: 'water_quality', label: 'Water quality improvements' },
]

interface Props {
  onSubmit: (profile: FarmProfile) => void
  submitting: boolean
}

export function FarmProfileForm({ onSubmit, submitting }: Props) {
  const [farmType, setFarmType] = useState<FarmType>('arable')
  const [sizeHectares, setSizeHectares] = useState(10)
  const [region, setRegion] = useState<UKRegion>('england')
  const [activities, setActivities] = useState<Activity[]>([])
  const [hasSbi, setHasSbi] = useState(false)
  const [sbiBefore2026, setSbiBefore2026] = useState(false)
  const [hasElmAgreement, setHasElmAgreement] = useState(false)
  const [hasEnvFeatures, setHasEnvFeatures] = useState(false)

  function toggleActivity(activity: Activity) {
    setActivities((prev) =>
      prev.includes(activity) ? prev.filter((a) => a !== activity) : [...prev, activity],
    )
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    onSubmit({
      farm_type: farmType,
      size_hectares: sizeHectares,
      region,
      activities,
      has_sbi: hasSbi,
      sbi_registered_before_2026_01_01: hasSbi && sbiBefore2026,
      has_existing_elm_agreement: hasElmAgreement,
      has_environmentally_significant_features: hasEnvFeatures,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="farm-profile-form">
      <label>
        Farm type
        <select value={farmType} onChange={(e) => setFarmType(e.target.value as FarmType)}>
          {FARM_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </label>

      <label>
        Farm size (hectares)
        <input
          type="number"
          min={0}
          step="0.1"
          value={sizeHectares}
          onChange={(e) => setSizeHectares(Number(e.target.value))}
        />
      </label>

      <label>
        Region
        <select value={region} onChange={(e) => setRegion(e.target.value as UKRegion)}>
          {REGIONS.map((r) => (
            <option key={r.value} value={r.value}>
              {r.label}
            </option>
          ))}
        </select>
      </label>
      {region !== 'england' && (
        <p className="hint">Most schemes below are England-only (Defra/RPA). Devolved nation schemes are not yet covered.</p>
      )}

      <fieldset>
        <legend>Activities (select all that apply)</legend>
        {ACTIVITIES.map((a) => (
          <label key={a.value} className="checkbox-label">
            <input
              type="checkbox"
              checked={activities.includes(a.value)}
              onChange={() => toggleActivity(a.value)}
            />
            {a.label}
          </label>
        ))}
      </fieldset>

      <fieldset>
        <legend>Registration & agreements</legend>
        <label className="checkbox-label">
          <input type="checkbox" checked={hasSbi} onChange={(e) => setHasSbi(e.target.checked)} />
          Registered with the Rural Payments Agency (has an SBI)
        </label>
        {hasSbi && (
          <label className="checkbox-label indent">
            <input
              type="checkbox"
              checked={sbiBefore2026}
              onChange={(e) => setSbiBefore2026(e.target.checked)}
            />
            Registered before 1 January 2026
          </label>
        )}
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={hasElmAgreement}
            onChange={(e) => setHasElmAgreement(e.target.checked)}
          />
          Has an existing ELM revenue agreement (SFI, Countryside Stewardship, HLS)
        </label>
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={hasEnvFeatures}
            onChange={(e) => setHasEnvFeatures(e.target.checked)}
          />
          Has environmentally significant features (SSSI, woodland, historic/archaeological features, common land)
        </label>
      </fieldset>

      <button type="submit" disabled={submitting}>
        {submitting ? 'Checking grants...' : 'Find my grants'}
      </button>
    </form>
  )
}
