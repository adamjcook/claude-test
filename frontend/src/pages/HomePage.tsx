import { useState } from 'react'
import { getGrants, matchProfile } from '../api/client'
import { FarmProfileForm } from '../components/FarmProfileForm'
import { ResultsList } from '../components/ResultsList'
import type { FarmProfile, Grant, MatchResult } from '../types/domain'

export function HomePage() {
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [grants, setGrants] = useState<Grant[] | null>(null)
  const [results, setResults] = useState<MatchResult[] | null>(null)

  async function handleSubmit(profile: FarmProfile) {
    setSubmitting(true)
    setError(null)
    try {
      const [grantsData, matchData] = await Promise.all([getGrants(), matchProfile(profile)])
      setGrants(grantsData)
      setResults(matchData)
    } catch {
      setError('Something went wrong while checking grants. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="home-page">
      <h1>UK Farm Grant Matcher</h1>
      <p>
        Tell us about your farm and we'll show you which UK government grants and schemes you may
        be eligible for, and why.
      </p>
      <FarmProfileForm onSubmit={handleSubmit} submitting={submitting} />
      {error && <p className="error">{error}</p>}
      {grants && results && <ResultsList grants={grants} results={results} />}
    </main>
  )
}
