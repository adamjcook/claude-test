import { useState } from 'react'
import type { Grant, MatchResult } from '../types/domain'

const STATUS_LABEL: Record<MatchResult['status'], string> = {
  matched: 'Eligible',
  partial: 'Possibly eligible',
  not_matched: 'Not eligible',
}

interface Props {
  grant: Grant
  result: MatchResult
}

export function GrantCard({ grant, result }: Props) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className={`grant-card grant-card--${result.status}`}>
      <div className="grant-card__header">
        <h3>{grant.name}</h3>
        <span className={`status-badge status-badge--${result.status}`}>
          {STATUS_LABEL[result.status]}
        </span>
      </div>
      <p className="grant-card__body">{grant.administering_body}</p>
      <p>{grant.summary}</p>
      <p className="grant-card__funding">{grant.funding_amount_description}</p>
      <ul className="grant-card__windows">
        {grant.application_windows.map((w) => (
          <li key={w.label}>
            {w.label}: opens {w.opens}
            {w.closes ? `, closes ${w.closes}` : ''}
          </li>
        ))}
      </ul>

      <button type="button" onClick={() => setExpanded((v) => !v)}>
        {expanded ? 'Hide details' : 'Why this result?'}
      </button>
      {expanded && (
        <div className="grant-card__reasoning">
          <ul>
            {result.checks.map((check) => (
              <li key={check.rule_name} className={check.passed ? 'check-pass' : 'check-fail'}>
                {check.passed ? '✓' : '✗'} {check.reason}
              </li>
            ))}
          </ul>
          {result.missing_requirements.length > 0 && (
            <>
              <p>To qualify, you still need to:</p>
              <ul>
                {result.missing_requirements.map((req) => (
                  <li key={req}>{req}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}

      <a href={grant.application_url} target="_blank" rel="noreferrer">
        View on GOV.UK
      </a>
    </div>
  )
}
