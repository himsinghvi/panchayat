import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import ComplaintCard from '../components/ComplaintCard'
import AdBanner from '../components/AdBanner'
import { StatsGrid } from '../components/StatCard'

const HOME_STATS = (stats) => [
  { icon: 'bi-chat-square-text', label: 'Experiences Shared', value: stats?.total_complaints, variant: 'primary' },
  { icon: 'bi-check2-circle', label: 'Resolution Rate', value: stats?.resolution_rate, suffix: '%', variant: 'success' },
  { icon: 'bi-building', label: 'Brands Tracked', value: stats?.total_brands, variant: 'info' },
  { icon: 'bi-hand-thumbs-up', label: 'Resolved Cases', value: stats?.resolved_complaints, variant: 'accent' },
]

export default function Home() {
  const [stats, setStats] = useState(null)
  const [trending, setTrending] = useState([])
  const [resolved, setResolved] = useState([])
  const [brands, setBrands] = useState([])
  const [searchQ, setSearchQ] = useState('')

  useEffect(() => {
    api.homeStats().then(setStats).catch(() => {})
    api.complaints('?feed=trending&limit=5').then(setTrending).catch(() => {})
    api.complaints('?feed=resolved&limit=3').then(setResolved).catch(() => {})
    api.brands().then(setBrands).catch(() => {})
  }, [])

  return (
    <>
      <section className="hero-section">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-8 mx-lg-0 animate-fade-in">
              <h1 className="hero-title mb-3">
                Had a bad experience?<br />
                <span className="text-primary">Make it visible. Get it resolved.</span>
              </h1>
              <p className="hero-subtitle mb-4">
                Share reviews, complaints & grievances. Brands respond publicly.
                Only you confirm when it's truly resolved.
              </p>
              <div className="d-flex flex-wrap gap-2 mb-4">
                <Link to="/share" className="btn btn-primary btn-lg">
                  <i className="bi bi-megaphone me-2" />Share Your Experience
                </Link>
                <Link to="/feed" className="btn btn-outline-primary btn-lg">Browse Feed</Link>
              </div>
              <form className="search-hero" onSubmit={e => { e.preventDefault(); window.location.href = `/search?q=${encodeURIComponent(searchQ)}` }}>
                <div className="input-group">
                  <input className="form-control search-input" placeholder="Search brands, products, shops, complaints..."
                    value={searchQ} onChange={e => setSearchQ(e.target.value)} />
                  <button className="btn btn-primary" type="submit"><i className="bi bi-search" /></button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </section>

      {stats && (
        <section className="metrics-strip">
          <div className="container">
            <StatsGrid items={HOME_STATS(stats)} />
          </div>
        </section>
      )}

      <section className="py-5 section-surface">
        <div className="container">
          <h2 className="text-center fw-bold mb-5">How Panchaayat Works</h2>
          <div className="row">
            {[
              { icon: 'bi-megaphone', title: 'Share', desc: 'Post your experience with evidence' },
              { icon: 'bi-people', title: 'Discuss', desc: 'Community discusses & supports' },
              { icon: 'bi-building', title: 'Brand Responds', desc: 'Verified brands reply officially' },
              { icon: 'bi-handshake', title: 'Resolve', desc: 'Brand proposes resolution' },
              { icon: 'bi-check-circle', title: 'You Confirm', desc: 'Only you close the case' },
            ].map((s, i) => (
              <div key={s.title} className={`col animate-fade-in stagger-${i + 1}`}>
                <div className="how-step">
                  <div className="how-icon"><i className={`bi ${s.icon}`} /></div>
                  <h6 className="fw-bold">{s.title}</h6>
                  <p className="small text-muted">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-5">
        <div className="container">
          <div className="row">
            <div className="col-lg-8">
              <div className="d-flex justify-content-between align-items-center mb-4">
                <h3 className="fw-bold mb-0">Trending Experiences</h3>
                <Link to="/feed" className="btn btn-sm btn-outline-primary">View All</Link>
              </div>
              {trending.map((c, i) => <ComplaintCard key={c.id} complaint={c} delay={i * 100} />)}

              {resolved.length > 0 && (
                <>
                  <h3 className="fw-bold mt-5 mb-4"><i className="bi bi-check-circle text-success me-2" />Recently Resolved</h3>
                  {resolved.map((c, i) => <ComplaintCard key={c.id} complaint={c} delay={i * 100} />)}
                </>
              )}
            </div>
            <div className="col-lg-4">
              <AdBanner placement="sidebar" />
              <div className="card-panchaayat p-3 mt-3">
                <h6 className="fw-bold mb-3">Popular Brands</h6>
                {brands.slice(0, 5).map(b => (
                  <Link key={b.id} to={`/brand/${b.slug}`} className="d-flex align-items-center mb-3 text-decoration-none link-body">
                    <img src={b.logo_url} alt="" width="32" height="32" className="rounded me-2" />
                    <div>
                      <div className="fw-semibold small">{b.name}</div>
                      <div className="text-muted" style={{ fontSize: '0.75rem' }}>{b.complaint_count} complaints · {b.resolution_rate}% resolved</div>
                    </div>
                  </Link>
                ))}
              </div>
              <div className="guest-banner mt-3">
                <i className="bi bi-info-circle me-2" />
                <strong>Tip:</strong> Login to get higher priority & faster brand response.
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
