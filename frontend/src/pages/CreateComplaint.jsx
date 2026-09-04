import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'
import AdBanner from '../components/AdBanner'

const CATEGORIES = ['Product', 'Service', 'Billing', 'Warranty', 'Safety', 'Delivery', 'Installation', 'Refund', 'Other']
const STEPS = ['What Happened', 'Details', 'AI Review', 'Preview']

export default function CreateComplaint() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [brands, setBrands] = useState([])
  const [rawText, setRawText] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [quality, setQuality] = useState(null)
  const [form, setForm] = useState({
    title: '', description: '', category: 'Other', rating: 3,
    brand_id: '', brand_name_free: '', product_name: '', city: '', area: '',
    amount: '', desired_resolution: '', is_anonymous: false,
    guest_name: '', guest_email: '',
  })

  useEffect(() => { api.brands().then(setBrands).catch(() => {}) }, [])

  const handleAIDraft = async () => {
    if (!rawText.trim()) return
    setAiLoading(true)
    try {
      const draft = await api.aiDraft(rawText)
      setForm(f => ({
        ...f,
        title: draft.title,
        description: draft.description,
        category: draft.category,
        brand_name_free: draft.brand_name || f.brand_name_free,
        product_name: draft.product_name || f.product_name,
        city: draft.city || f.city,
        area: draft.area || f.area,
        amount: draft.amount || f.amount,
        desired_resolution: draft.desired_resolution || f.desired_resolution,
      }))
      setStep(1)
    } finally {
      setAiLoading(false)
    }
  }

  const handleQualityCheck = async () => {
    setAiLoading(true)
    try {
      const qc = await api.aiQuality(form.title, form.description)
      setQuality(qc)
      setStep(2)
    } finally {
      setAiLoading(false)
    }
  }

  const handleSubmit = async () => {
    const payload = {
      ...form,
      brand_id: form.brand_id ? parseInt(form.brand_id) : null,
      amount: form.amount ? parseFloat(form.amount) : null,
      rating: parseInt(form.rating),
    }
    const result = await api.createComplaint(payload)
    navigate(`/complaint/${result.id}`)
  }

  const update = (k, v) => setForm(f => ({ ...f, [k]: v }))

  return (
    <div className="container py-4">
      <div className="row">
        <div className="col-lg-8 mx-auto">
          <h2 className="fw-bold mb-2">Share Your Experience</h2>
          <p className="text-muted mb-4">No login required — but logged-in users get higher priority & faster resolution.</p>

          {!user && (
            <div className="guest-banner mb-4">
              <i className="bi bi-exclamation-triangle me-2" />
              You're posting as a guest (lower weight). <a href="/login">Login</a> to be heard better.
            </div>
          )}

          <div className="progress-steps mb-4">
            {STEPS.map((s, i) => (
              <div key={s} className={`progress-step ${i === step ? 'active' : ''} ${i < step ? 'done' : ''}`}>
                <div className="step-circle">{i < step ? '✓' : i + 1}</div>
                <div className="step-label">{s}</div>
              </div>
            ))}
          </div>

          <div className="card-panchaayat p-4">
            {step === 0 && (
              <div className="wizard-step active">
                <h5 className="fw-bold mb-3">What happened?</h5>
                <p className="text-muted small">Describe in your own words — our AI will help structure it.</p>
                <textarea className="form-control mb-3" rows={6}
                  placeholder="e.g. Bought AC from XYZ shop. They promised installation next day. Nobody came for 4 days..."
                  value={rawText} onChange={e => setRawText(e.target.value)} />
                <div className="ai-bubble mb-3">
                  <i className="bi bi-stars me-2" />
                  <strong>AI Assistant</strong> will extract brand, category, location & structure your complaint. It never invents facts.
                </div>
                <button className="btn btn-primary" onClick={handleAIDraft} disabled={aiLoading || !rawText.trim()}>
                  {aiLoading ? <span className="spinner-border spinner-border-sm me-2" /> : <i className="bi bi-stars me-2" />}
                  Structure with AI
                </button>
                <button className="btn btn-link" onClick={() => { update('description', rawText); setStep(1) }}>Skip AI, fill manually</button>
              </div>
            )}

            {step === 1 && (
              <div className="wizard-step active">
                <h5 className="fw-bold mb-3">Complaint Details</h5>
                {!user && (
                  <div className="row mb-3">
                    <div className="col-md-6">
                      <label className="form-label">Your Name</label>
                      <input className="form-control" value={form.guest_name} onChange={e => update('guest_name', e.target.value)} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Email (private)</label>
                      <input className="form-control" type="email" value={form.guest_email} onChange={e => update('guest_email', e.target.value)} />
                    </div>
                  </div>
                )}
                <div className="mb-3">
                  <label className="form-label">Title</label>
                  <input className="form-control" value={form.title} onChange={e => update('title', e.target.value)} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Description</label>
                  <textarea className="form-control" rows={5} value={form.description} onChange={e => update('description', e.target.value)} required />
                </div>
                <div className="row mb-3">
                  <div className="col-md-6">
                    <label className="form-label">Category</label>
                    <select className="form-select" value={form.category} onChange={e => update('category', e.target.value)}>
                      {CATEGORIES.map(c => <option key={c}>{c}</option>)}
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Rating (1-5)</label>
                    <input type="range" className="form-range" min="1" max="5" value={form.rating} onChange={e => update('rating', e.target.value)} />
                    <div className="rating-stars">{'★'.repeat(form.rating)}{'☆'.repeat(5 - form.rating)}</div>
                  </div>
                </div>
                <div className="row mb-3">
                  <div className="col-md-6">
                    <label className="form-label">Brand</label>
                    <select className="form-select mb-2" value={form.brand_id} onChange={e => update('brand_id', e.target.value)}>
                      <option value="">Select or type below</option>
                      {brands.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
                    </select>
                    <input className="form-control" placeholder="Or enter brand name" value={form.brand_name_free}
                      onChange={e => update('brand_name_free', e.target.value)} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Product</label>
                    <input className="form-control" value={form.product_name} onChange={e => update('product_name', e.target.value)} />
                  </div>
                </div>
                <div className="row mb-3">
                  <div className="col-md-4">
                    <label className="form-label">City</label>
                    <input className="form-control" value={form.city} onChange={e => update('city', e.target.value)} />
                  </div>
                  <div className="col-md-4">
                    <label className="form-label">Area</label>
                    <input className="form-control" value={form.area} onChange={e => update('area', e.target.value)} />
                  </div>
                  <div className="col-md-4">
                    <label className="form-label">Amount (₹)</label>
                    <input className="form-control" type="number" value={form.amount} onChange={e => update('amount', e.target.value)} />
                  </div>
                </div>
                <div className="mb-3">
                  <label className="form-label">Desired Resolution</label>
                  <input className="form-control" value={form.desired_resolution} onChange={e => update('desired_resolution', e.target.value)} />
                </div>
                <div className="form-check mb-3">
                  <input className="form-check-input" type="checkbox" checked={form.is_anonymous}
                    onChange={e => update('is_anonymous', e.target.checked)} id="anon" />
                  <label className="form-check-label" htmlFor="anon">Post anonymously (lower trust weight)</label>
                </div>
                <div className="d-flex gap-2">
                  <button className="btn btn-outline-secondary" onClick={() => setStep(0)}>Back</button>
                  <button className="btn btn-primary" onClick={handleQualityCheck} disabled={aiLoading}>
                    {aiLoading ? 'Checking...' : 'AI Quality Check →'}
                  </button>
                </div>
              </div>
            )}

            {step === 2 && quality && (
              <div className="wizard-step active">
                <h5 className="fw-bold mb-3">AI Quality Review</h5>
                <div className="ai-bubble mb-3">
                  <i className="bi bi-shield-check me-2" />
                  AI reviewed your complaint before publishing.
                </div>
                {quality.warnings?.length > 0 && (
                  <div className="alert alert-warning">
                    <strong>Warnings:</strong>
                    <ul className="mb-0">{quality.warnings.map((w, i) => <li key={i}>{w}</li>)}</ul>
                  </div>
                )}
                {quality.suggestions?.length > 0 && (
                  <div className="alert alert-info">
                    <strong>Suggestions:</strong>
                    <ul className="mb-0">{quality.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul>
                  </div>
                )}
                {quality.pii_detected && <div className="alert alert-danger">Personal information detected — please remove before publishing.</div>}
                <div className="d-flex gap-2">
                  <button className="btn btn-outline-secondary" onClick={() => setStep(1)}>Edit</button>
                  <button className="btn btn-primary" onClick={() => setStep(3)}>Continue to Preview →</button>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="wizard-step active">
                <h5 className="fw-bold mb-3">Preview — How it will appear</h5>
                <div className="card-panchaayat p-3 mb-3 bg-light">
                  <h5>{form.title}</h5>
                  <p>{form.description}</p>
                  <div className="d-flex gap-2">
                    <span className="badge bg-secondary">{form.category}</span>
                    {form.brand_name_free && <span className="badge bg-primary">{form.brand_name_free}</span>}
                    {form.city && <span className="badge badge-muted">{form.city}</span>}
                  </div>
                  <div className="rating-stars mt-2">{'★'.repeat(form.rating)}{'☆'.repeat(5 - form.rating)}</div>
                </div>
                <p className="small text-muted">By publishing, you confirm this is your genuine experience.</p>
                <div className="d-flex gap-2">
                  <button className="btn btn-outline-secondary" onClick={() => setStep(2)}>Back</button>
                  <button className="btn btn-primary btn-lg" onClick={handleSubmit}>
                    <i className="bi bi-send me-2" />Publish Complaint
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
        <div className="col-lg-4 d-none d-lg-block">
          <AdBanner placement="inline" category={form.category} city={form.city} area={form.area} />
        </div>
      </div>
    </div>
  )
}
