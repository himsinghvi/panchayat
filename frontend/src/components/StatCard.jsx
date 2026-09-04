export default function StatCard({ icon, label, value, suffix = '', variant = 'primary', sublabel }) {
  const display = value === undefined || value === null ? '—' : `${value}${suffix}`

  return (
    <div className={`stat-card stat-card--${variant}`}>
      <div className="stat-card-icon-wrap">
        <i className={`bi ${icon}`} />
      </div>
      <div className="stat-card-content">
        <div className="stat-card-value">{display}</div>
        <div className="stat-card-label">{label}</div>
        {sublabel && <div className="stat-card-sublabel">{sublabel}</div>}
      </div>
    </div>
  )
}

export function StatsGrid({ items, className = '' }) {
  return (
    <div className={`stats-grid ${className}`}>
      {items.map((item) => (
        <StatCard key={item.label} {...item} />
      ))}
    </div>
  )
}
