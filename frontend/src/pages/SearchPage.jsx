import { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { api } from '../api'
import ComplaintCard from '../components/ComplaintCard'

const CATEGORIES = ['', 'Installation', 'Refund', 'Delivery', 'Service', 'Billing', 'Safety', 'Warranty', 'Product']
const STATUSES = ['', 'awaiting_response', 'business_responded', 'resolution_proposed', 'resolved', 'reopened']

const SEARCH_EXAMPLES = [
  'delayed AC installation in Pune',
  'refund not received',
  'Samsung warranty issue',
  'overcharged at electronics store',
]

export default function SearchPage() {
  const [params] = useSearchParams()
  const [query, setQuery] = useState(params.get('q') || '')
  const [filters, setFilters] = useState({ category: '', status: '', city: '' })
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const search = async (q, f = filters) => {
    if (!q.trim()) return
    setLoading(true)
    try {
      const r = await api.search(q, f)
      setResults(r)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const q = params.get('q')
    if (q) { setQuery(q); search(q) }
  }, [params])

  const handleSearch = (e) => {
    e.preventDefault()
    search(query)
    window.history.pushState({}, '', `/search?q=${encodeURIComponent(query)}`)
  }

  return (
    <div className="container py-4">
      <h2 className="fw-bold mb-2">Smart Search</h2>
      <p className="text-muted mb-4">Search by natural language — not just exact keywords. Try describing your issue.</p>

      <form className="mb-3" onSubmit={handleSearch}>
        <div className="input-group input-group-lg">
          <input className="form-control" placeholder="e.g. delayed installation in Pune, refund pending 3 weeks..."
            value={query} onChange={e => setQuery(e.target.value)} />
          <button className="btn btn-primary" type="submit"><i className="bi bi-search me-1" />Search</button>
        </div>
      </form>

      <div className="d-flex flex-wrap gap-2 mb-3">
        {SEARCH_EXAMPLES.map(ex => (
          <button key={ex} type="button" className="btn btn-sm btn-light border"
            onClick={() => { setQuery(ex); search(ex) }}>{ex}</button>
        ))}
      </div>

      <div className="row g-2 mb-4">
        <div className="col-md-4">
          <select className="form-select" value={filters.category}
            onChange={e => { const f = { ...filters, category: e.target.value }; setFilters(f); if (query) search(query, f) }}>
            <option value="">All Categories</option>
            {CATEGORIES.filter(Boolean).map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div className="col-md-4">
          <select className="form-select" value={filters.status}
            onChange={e => { const f = { ...filters, status: e.target.value }; setFilters(f); if (query) search(query, f) }}>
            <option value="">All Statuses</option>
            {STATUSES.filter(Boolean).map(s => <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>)}
          </select>
        </div>
        <div className="col-md-4">
          <input className="form-control" placeholder="Filter by city" value={filters.city}
            onChange={e => setFilters({ ...filters, city: e.target.value })}
            onBlur={() => query && search(query, filters)} />
        </div>
      </div>

      {loading && <div className="text-center py-5"><div className="spinner-border text-primary" /></div>}

      {results && !loading && (
        <>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <p className="text-muted mb-0">{results.total} results for "{results.query}"</p>
            {results.expanded_terms?.length > 0 && (
              <div className="small text-muted">
                Also matching: {results.expanded_terms.slice(0, 6).join(', ')}
              </div>
            )}
          </div>

          {results.brands?.length > 0 && (
            <>
              <h5 className="fw-bold">Brands</h5>
              <div className="row mb-4">
                {results.brands.map(b => (
                  <div key={b.id} className="col-md-4 mb-3">
                    <Link to={`/brand/${b.slug}`} className="card-panchaayat p-3 text-decoration-none link-body d-block h-100">
                      <div className="d-flex align-items-center">
                        <img src={b.logo_url} alt="" width="40" className="rounded me-2" />
                        <div>
                          <div className="fw-bold">{b.name}</div>
                          <div className="small text-muted">{b.complaint_count} complaints</div>
                          {b.match_reasons?.length > 0 && (
                            <div className="small text-primary">Matched: {b.match_reasons.join(', ')}</div>
                          )}
                        </div>
                      </div>
                    </Link>
                  </div>
                ))}
              </div>
            </>
          )}

          <h5 className="fw-bold">Complaints & Experiences</h5>
          {results.complaints?.length ? (
            results.complaints.map((c, i) => (
              <ComplaintCard key={c.id} complaint={c} delay={i * 50} showMatchReasons />
            ))
          ) : (
            <p className="text-muted">No complaints found. Try different words or remove filters.</p>
          )}
        </>
      )}
    </div>
  )
}
