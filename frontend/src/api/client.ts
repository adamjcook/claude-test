import type { FarmProfile, Grant, MatchResult } from '../types/domain'

export async function getGrants(): Promise<Grant[]> {
  const response = await fetch('/api/grants')
  if (!response.ok) throw new Error('Failed to load grants')
  return response.json()
}

export async function matchProfile(profile: FarmProfile): Promise<MatchResult[]> {
  const response = await fetch('/api/match', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  })
  if (!response.ok) throw new Error('Failed to match farm profile')
  return response.json()
}
