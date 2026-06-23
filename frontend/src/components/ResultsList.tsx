import type { Grant, MatchResult, MatchStatus } from '../types/domain'
import { GrantCard } from './GrantCard'

const SECTIONS: { status: MatchStatus; title: string }[] = [
  { status: 'matched', title: 'Matched grants' },
  { status: 'partial', title: 'Partially matched grants' },
  { status: 'not_matched', title: 'Not matched' },
]

interface Props {
  grants: Grant[]
  results: MatchResult[]
}

export function ResultsList({ grants, results }: Props) {
  const grantsById = new Map(grants.map((g) => [g.id, g]))

  return (
    <div className="results-list">
      {SECTIONS.map((section) => {
        const sectionResults = results.filter((r) => r.status === section.status)
        if (sectionResults.length === 0) return null
        return (
          <section key={section.status}>
            <h2>{section.title}</h2>
            {sectionResults.map((result) => {
              const grant = grantsById.get(result.grant_id)
              if (!grant) return null
              return <GrantCard key={result.grant_id} grant={grant} result={result} />
            })}
          </section>
        )
      })}
    </div>
  )
}
