import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'
import ComplaintCard from '../components/ComplaintCard'
import { StatsGrid } from '../components/StatCard'

export default function ConsumerDashboard() {
  const { user } = useAuth()
  const [complaints, setComplaints] = useState([])
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    api.complaints('?limit=50').then(all => {
      setComplaints(all.filter(c => c.author_name === user?.display_name))
    }).catch(() => {})
    api.notifications().then(setNotifications).catch(() => {})
  }, [user])

  if (!user) return <div className="container py-5 text-center">Please <Link to="/login">login</Link></div>

  const awaiting = complaints.filter(c => ['resolution_proposed', 'consumer_reviewing'].includes(c.status))
  const open = complaints.filter(c => !['resolved', 'partially_resolved', 'closed'].includes(c.status))
  const resolved = complaints.filter(c => ['resolved', 'partially_resolved'].includes(c.status))

  const statItems = [
    { icon: 'bi-journal-text', label: 'My Experiences', value: complaints.length, variant: 'primary' },
    { icon: 'bi-hourglass-split', label: 'Open', value: open.length, variant: 'warning' },
    { icon: 'bi-bell', label: 'Need Your Action', value: awaiting.length, variant: 'accent' },
    { icon: 'bi-check2-circle', label: 'Resolved', value: resolved.length, variant: 'success' },
  ]

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center mb-4">
        <img src={user.avatar_url} alt="" width="56" className="rounded-circle me-3" />
        <div>
          <h3 className="fw-bold mb-0">{user.display_name}</h3>
          <span className="text-muted">{user.persona_tag || user.role}</span>
          {user.verified && <i className="bi bi-patch-check-fill text-primary ms-2" />}
        </div>
      </div>

      <StatsGrid items={statItems} className="mb-4" />

      {awaiting.length > 0 && (
        <>
          <h5 className="fw-bold text-primary"><i className="bi bi-exclamation-circle me-2" />Awaiting Your Confirmation</h5>
          {awaiting.map(c => <ComplaintCard key={c.id} complaint={c} />)}
        </>
      )}

      <h5 className="fw-bold mt-4">All My Complaints</h5>
      {complaints.map(c => <ComplaintCard key={c.id} complaint={c} />)}

      {notifications.length > 0 && (
        <>
          <h5 className="fw-bold mt-4">Notifications</h5>
          {notifications.map(n => (
            <div key={n.id} className="card-panchaayat p-3 mb-2">
              <div className="fw-semibold">{n.title}</div>
              <div className="small text-muted">{n.message}</div>
            </div>
          ))}
        </>
      )}
    </div>
  )
}
