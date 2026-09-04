import { useState, useEffect } from 'react'
import { api } from '../api'
import ComplaintCard from '../components/ComplaintCard'
import AdBanner from '../components/AdBanner'

const FEEDS = [
  { key: 'recent', label: 'Recent' },
  { key: 'trending', label: 'Trending' },
  { key: 'resolved', label: 'Resolved' },
]

const CATEGORIES = ['All', 'Installation', 'Refund', 'Delivery', 'Service', 'Billing', 'Safety', 'Warranty', 'Product']

export default function Feed() {
  const [feed, setFeed] = useState('recent')
  const [category, setCategory] = useState('All')
  const [complaints, setComplaints] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const params = new URLSearchParams({ feed, limit: '30' })
    if (category !== 'All') params.set('category', category)
    api.complaints(`?${params}`).then(setComplaints).finally(() => setLoading(false))
  }, [feed, category])

  return (
    <div className="container py-4">
      <h2 className="fw-bold mb-4">Experience Feed</h2>
      <div className="d-flex flex-wrap gap-2 mb-3">
        {FEEDS.map(f => (
          <button key={f.key} className={`btn btn-sm ${feed === f.key ? 'btn-primary' : 'btn-outline-secondary'}`}
            onClick={() => setFeed(f.key)}>{f.label}</button>
        ))}
      </div>
      <div className="d-flex flex-wrap gap-2 mb-4">
        {CATEGORIES.map(c => (
          <button key={c} className={`btn btn-sm ${category === c ? 'btn-dark' : 'btn-light border'}`}
            onClick={() => setCategory(c)}>{c}</button>
        ))}
      </div>
      <div className="row">
        <div className="col-lg-8">
          {loading ? (
            <div className="text-center py-5"><div className="spinner-border text-primary" /></div>
          ) : complaints.length ? (
            complaints.map((c, i) => <ComplaintCard key={c.id} complaint={c} delay={i * 50} />)
          ) : (
            <div className="text-center py-5 text-muted">No experiences found. <a href="/share">Share yours!</a></div>
          )}
        </div>
        <div className="col-lg-4">
          <AdBanner placement="sidebar" />
        </div>
      </div>
    </div>
  )
}
