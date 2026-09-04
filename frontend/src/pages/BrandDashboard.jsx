import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'
import ComplaintCard from '../components/ComplaintCard'
import { StatsGrid } from '../components/StatCard'

export default function BrandDashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [complaints, setComplaints] = useState([])

  useEffect(() => {
    api.brandStats().then(setStats).catch(() => {})
    api.complaints('?limit=50').then(setComplaints).catch(() => {})
  }, [])

  if (!user) return <div className="container py-5">Please <Link to="/login">login</Link> as brand rep</div>

  const openComplaints = complaints.filter(c => !['resolved', 'closed'].includes(c.status))

  const statItems = stats ? [
    { icon: 'bi-inbox', label: 'Total Complaints', value: stats.total_complaints, variant: 'primary' },
    { icon: 'bi-envelope-open', label: 'Open', value: stats.open_complaints, variant: 'warning' },
    { icon: 'bi-check2-circle', label: 'Resolved', value: stats.resolved_complaints, variant: 'success' },
    { icon: 'bi-graph-up-arrow', label: 'Resolution Rate', value: stats.resolution_rate, suffix: '%', variant: 'info' },
    { icon: 'bi-clock-history', label: 'Avg Response', value: stats.avg_response_hours, suffix: 'h', variant: 'accent' },
  ] : []

  return (
    <div className="container py-4">
      <h3 className="fw-bold mb-4"><i className="bi bi-building me-2" />Brand Dashboard</h3>
      {stats && <StatsGrid items={statItems} className="stats-grid--5 mb-4" />}

      {stats?.trending_categories?.length > 0 && (
        <div className="card-panchaayat p-3 mb-4">
          <h6 className="fw-bold">Trending Issue Categories</h6>
          {stats.trending_categories.map(c => (
            <div key={c.category} className="d-flex justify-content-between mb-1">
              <span>{c.category}</span>
              <span className="badge bg-primary">{c.count}</span>
            </div>
          ))}
        </div>
      )}

      <h5 className="fw-bold">Complaint Inbox</h5>
      {openComplaints.map(c => <ComplaintCard key={c.id} complaint={c} />)}
    </div>
  )
}
