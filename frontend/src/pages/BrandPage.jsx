import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'
import ComplaintCard from '../components/ComplaintCard'
import AdBanner from '../components/AdBanner'
import StatCard from '../components/StatCard'

export default function BrandPage() {
  const { slug } = useParams()
  const [brand, setBrand] = useState(null)
  const [complaints, setComplaints] = useState([])

  useEffect(() => {
    api.brandBySlug(slug).then(b => {
      setBrand(b)
      api.brandComplaints(b.id).then(setComplaints)
    }).catch(() => {})
  }, [slug])

  if (!brand) return <div className="container py-5 text-center"><div className="spinner-border text-primary" /></div>

  return (
    <div className="container py-4">
      <div className="card-panchaayat p-4 mb-4 animate-fade-in">
        <div className="row align-items-center">
          <div className="col-auto">
            <img src={brand.logo_url} alt="" width="80" height="80" className="rounded" />
          </div>
          <div className="col">
            <h2 className="fw-bold mb-1">{brand.name}</h2>
            <span className={`badge ${brand.verification_status === 'verified' ? 'bg-primary' : 'bg-secondary'}`}>
              {brand.verification_status === 'verified' ? '✓ Verified Brand' : brand.verification_status}
            </span>
            <p className="text-muted mt-2 mb-0">{brand.description}</p>
          </div>
        </div>
        <div className="brand-stats-row">
          <StatCard icon="bi-star-fill" label="Avg Rating" value={brand.average_rating} variant="warning" />
          <StatCard icon="bi-chat-square-text" label="Complaints" value={brand.complaint_count} variant="primary" />
          <StatCard icon="bi-check2-circle" label="Resolution Rate" value={brand.resolution_rate} suffix="%" variant="success" />
          <StatCard icon="bi-reply" label="Response Rate" value={brand.response_rate} suffix="%" variant="info" />
          <StatCard icon="bi-clock-history" label="Avg Response" value={brand.avg_response_hours} suffix="h" variant="accent" />
        </div>
      </div>
      <div className="row">
        <div className="col-lg-8">
          <h4 className="fw-bold mb-3">Complaints & Experiences</h4>
          {complaints.map((c, i) => <ComplaintCard key={c.id} complaint={c} delay={i * 50} />)}
          {!complaints.length && <p className="text-muted">No complaints yet.</p>}
        </div>
        <div className="col-lg-4">
          <AdBanner placement="sidebar" category={brand.category} />
        </div>
      </div>
    </div>
  )
}
