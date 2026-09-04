const STEPS = [
  { key: 'published', label: 'Shared' },
  { key: 'awaiting_response', label: 'Awaiting' },
  { key: 'business_responded', label: 'Responded' },
  { key: 'resolution_proposed', label: 'Proposed' },
  { key: 'resolved', label: 'Resolved' },
]

const STATUS_ORDER = {
  published: 0, awaiting_response: 1, business_responded: 2,
  resolution_proposed: 3, consumer_reviewing: 3,
  resolved: 4, partially_resolved: 4, reopened: 2, not_resolved: 3,
}

export default function StatusProgress({ status }) {
  const current = STATUS_ORDER[status] ?? 1

  return (
    <div className="progress-steps">
      {STEPS.map((step, i) => (
        <div key={step.key} className={`progress-step ${i < current ? 'done' : ''} ${i === current ? 'active' : ''}`}>
          <div className="step-circle">{i < current ? '✓' : i + 1}</div>
          <div className="step-label">{step.label}</div>
        </div>
      ))}
    </div>
  )
}
