import { useState, useEffect } from 'react'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'

const EMPTY_FORM = {
  title: '', description: '', advertiser: '', categories: '', keywords: '',
  cities: '', locations: '', personas: '', roles: '',
  placement: 'sidebar', link_url: '#', priority: 5, active: true,
}

function splitField(val) {
  return val.split(',').map(s => s.trim()).filter(Boolean)
}

function joinField(arr) {
  return (arr || []).join(', ')
}

export default function AdminPanel() {
  const { user, isAdmin, loading: authLoading } = useAuth()
  const [ads, setAds] = useState([])
  const [form, setForm] = useState({ ...EMPTY_FORM })
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiReasoning, setAiReasoning] = useState('')

  const loadAds = async () => {
    try {
      const data = await api.adminAds()
      setAds(data)
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => {
    if (!authLoading && isAdmin) loadAds()
  }, [authLoading, isAdmin])

  if (authLoading) {
    return <div className="container py-5 text-center"><div className="spinner-border text-primary" /></div>
  }

  if (!isAdmin) {
    return (
      <div className="container py-5">
        Admin access required. Login as <code>admin</code> (password: demo123)
      </div>
    )
  }

  const applyAiSuggestions = (suggestion) => {
    setForm(f => ({
      ...f,
      categories: joinField(suggestion.categories),
      keywords: joinField(suggestion.keywords),
      cities: joinField(suggestion.cities) || f.cities,
      locations: joinField(suggestion.locations) || f.locations,
      personas: joinField(suggestion.personas) || f.personas,
      roles: joinField(suggestion.roles) || f.roles,
    }))
    setAiReasoning(suggestion.reasoning || '')
  }

  const handleAiSuggest = async () => {
    if (!form.title.trim()) {
      setError('Enter ad title first for AI suggestions')
      return
    }
    setAiLoading(true)
    setError('')
    try {
      const suggestion = await api.aiSuggestAdTargeting(form.title, form.description)
      applyAiSuggestions(suggestion)
      setSuccess('AI suggested categories & keywords — review and edit before saving')
    } catch (e) {
      setError(e.message)
    } finally {
      setAiLoading(false)
    }
  }

  const payloadFromForm = () => ({
    title: form.title,
    description: form.description || null,
    advertiser: form.advertiser || null,
    link_url: form.link_url || '#',
    placement: form.placement,
    priority: parseInt(form.priority) || 0,
    active: form.active,
    categories: splitField(form.categories),
    keywords: splitField(form.keywords),
    cities: splitField(form.cities),
    locations: splitField(form.locations),
    personas: splitField(form.personas),
    roles: splitField(form.roles),
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      const payload = payloadFromForm()
      if (editingId) {
        await api.updateAd(editingId, payload)
        setSuccess('Ad updated successfully')
      } else {
        await api.createAd(payload)
        setSuccess('Ad created successfully')
      }
      setForm({ ...EMPTY_FORM })
      setEditingId(null)
      setAiReasoning('')
      await loadAds()
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const startEdit = (ad) => {
    setEditingId(ad.id)
    setAiReasoning('')
    setForm({
      title: ad.title,
      description: ad.description || '',
      advertiser: ad.advertiser || '',
      categories: joinField(ad.categories),
      keywords: joinField(ad.keywords),
      cities: joinField(ad.cities),
      locations: joinField(ad.locations),
      personas: joinField(ad.personas),
      roles: joinField(ad.roles),
      placement: ad.placement,
      link_url: ad.link_url || '#',
      priority: ad.priority,
      active: ad.active,
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const cancelEdit = () => {
    setEditingId(null)
    setForm({ ...EMPTY_FORM })
    setAiReasoning('')
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this ad?')) return
    try {
      await api.deleteAd(id)
      if (editingId === id) cancelEdit()
      await loadAds()
      setSuccess('Ad deleted')
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="container py-4">
      <h3 className="fw-bold mb-1"><i className="bi bi-gear me-2" />Admin Panel</h3>
      <p className="text-muted mb-4">Logged in as {user.display_name}</p>

      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="row">
        <div className="col-lg-5">
          <div className="card-panchaayat p-4 mb-4">
            <h5 className="fw-bold mb-3">{editingId ? 'Edit Ad' : 'Create Ad'}</h5>
            <form onSubmit={handleSubmit}>
              <div className="mb-2"><input className="form-control" placeholder="Ad Title *" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} required /></div>
              <div className="mb-2"><textarea className="form-control" placeholder="Description" rows={2} value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} /></div>
              <button type="button" className="btn btn-outline-primary btn-sm mb-3 w-100" onClick={handleAiSuggest} disabled={aiLoading}>
                {aiLoading ? <><span className="spinner-border spinner-border-sm me-2" />Analyzing...</> : <><i className="bi bi-stars me-2" />AI Suggest Categories & Keywords</>}
              </button>
              {aiReasoning && (
                <div className="ai-bubble small mb-3">
                  <i className="bi bi-stars me-1" /><strong>AI:</strong> {aiReasoning}
                  <div className="text-muted mt-1">You can edit all fields below before saving.</div>
                </div>
              )}
              <div className="mb-2"><input className="form-control" placeholder="Advertiser" value={form.advertiser} onChange={e => setForm({ ...form, advertiser: e.target.value })} /></div>
              <div className="mb-2"><input className="form-control" placeholder="Categories (Installation, Refund...)" value={form.categories} onChange={e => setForm({ ...form, categories: e.target.value })} /></div>
              <div className="mb-2"><input className="form-control" placeholder="Keywords (refund, AC, warranty...)" value={form.keywords} onChange={e => setForm({ ...form, keywords: e.target.value })} /></div>
              <div className="mb-2"><input className="form-control" placeholder="Cities (Pune, Mumbai...)" value={form.cities} onChange={e => setForm({ ...form, cities: e.target.value })} /></div>
              <div className="mb-2"><input className="form-control" placeholder="Locations/Areas (Viman Nagar...)" value={form.locations} onChange={e => setForm({ ...form, locations: e.target.value })} /></div>
              <div className="mb-2"><input className="form-control" placeholder="Personas (Frustrated Home Buyer...)" value={form.personas} onChange={e => setForm({ ...form, personas: e.target.value })} /></div>
              <div className="mb-2"><input className="form-control" placeholder="Roles (consumer, brand_rep...)" value={form.roles} onChange={e => setForm({ ...form, roles: e.target.value })} /></div>
              <div className="mb-2">
                <select className="form-select" value={form.placement} onChange={e => setForm({ ...form, placement: e.target.value })}>
                  <option value="sidebar">Sidebar</option>
                  <option value="inline">Inline</option>
                  <option value="footer">Footer</option>
                </select>
              </div>
              <div className="mb-2"><input className="form-control" placeholder="Link URL" value={form.link_url} onChange={e => setForm({ ...form, link_url: e.target.value })} /></div>
              <div className="mb-2"><input className="form-control" type="number" placeholder="Priority" value={form.priority} onChange={e => setForm({ ...form, priority: e.target.value })} /></div>
              <div className="form-check mb-3">
                <input className="form-check-input" type="checkbox" checked={form.active} onChange={e => setForm({ ...form, active: e.target.checked })} id="adActive" />
                <label className="form-check-label" htmlFor="adActive">Active</label>
              </div>
              <div className="d-flex gap-2">
                <button className="btn btn-primary flex-grow-1" disabled={loading}>
                  {loading ? 'Saving...' : editingId ? 'Update Ad' : 'Add Ad'}
                </button>
                {editingId && <button type="button" className="btn btn-outline-secondary" onClick={cancelEdit}>Cancel</button>}
              </div>
            </form>
          </div>
        </div>
        <div className="col-lg-7">
          <h5 className="fw-bold mb-3">All Ads ({ads.length})</h5>
          <p className="small text-muted">Ads are matched by category, keywords, city, location, persona & role.</p>
          {ads.length === 0 && <p className="text-muted">No ads yet. Create one using the form.</p>}
          {ads.map(ad => (
            <div key={ad.id} className={`card-panchaayat p-3 mb-2 ${editingId === ad.id ? 'border border-primary' : ''}`}>
              <div className="d-flex justify-content-between align-items-start">
                <div className="flex-grow-1">
                  <div className="mb-1">
                    <span className={`badge me-2 ${ad.active ? 'bg-success' : 'bg-secondary'}`}>{ad.active ? 'Active' : 'Inactive'}</span>
                    <span className="badge bg-secondary me-2">{ad.placement}</span>
                    <span className="badge badge-muted">P{ad.priority}</span>
                  </div>
                  <strong>{ad.title}</strong>
                  <div className="small text-muted">{ad.advertiser}</div>
                  <div className="small mt-1">{ad.description}</div>
                  <div className="mt-2 d-flex flex-wrap gap-1">
                    {ad.categories?.map(c => <span key={c} className="badge bg-primary bg-opacity-10 text-primary">{c}</span>)}
                    {ad.keywords?.slice(0, 4).map(k => <span key={k} className="badge bg-secondary bg-opacity-10 text-secondary">{k}</span>)}
                    {ad.cities?.map(c => <span key={c} className="badge bg-info bg-opacity-10 text-info"><i className="bi bi-geo-alt" /> {c}</span>)}
                    {ad.personas?.map(p => <span key={p} className="badge bg-warning bg-opacity-10">{p}</span>)}
                  </div>
                </div>
                <div className="d-flex gap-1 ms-2">
                  <button className="btn btn-sm btn-outline-primary" onClick={() => startEdit(ad)}>Edit</button>
                  <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(ad.id)}>Delete</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
