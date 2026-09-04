import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'
import StatusProgress from '../components/StatusProgress'
import AdBanner from '../components/AdBanner'

export default function ComplaintDetail() {
  const { id } = useParams()
  const { user, isBrand } = useAuth()
  const [complaint, setComplaint] = useState(null)
  const [comment, setComment] = useState('')
  const [resolutionForm, setResolutionForm] = useState({ resolution_type: 'Refund', description: '' })
  const [aiSuggestion, setAiSuggestion] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    api.complaint(id).then(setComplaint).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [id])

  useEffect(() => {
    if (isBrand && id) api.aiSuggestResolution(id).then(r => setAiSuggestion(r.suggestion)).catch(() => {})
  }, [isBrand, id])

  const handleMeToo = async () => {
    await api.meToo(id)
    load()
  }

  const handleComment = async (e) => {
    e.preventDefault()
    await api.addComment(id, { body: comment })
    setComment('')
    load()
  }

  const handleProposeResolution = async (e) => {
    e.preventDefault()
    await api.proposeResolution(id, resolutionForm)
    load()
  }

  const handleRespondResolution = async (resId, action, extra = {}) => {
    await api.respondResolution(id, resId, { action, ...extra })
    load()
  }

  if (loading) return <div className="container py-5 text-center"><div className="spinner-border text-primary" /></div>
  if (!complaint) return <div className="container py-5">Complaint not found</div>

  const pendingResolution = complaint.resolutions?.find(r => r.status === 'proposed')
  const isAuthor = user && complaint.author_name === user.display_name

  return (
    <div className="container py-4">
      <div className="row">
        <div className="col-lg-8">
          <div className="card-panchaayat p-4 mb-4 animate-fade-in">
            <div className="d-flex justify-content-between align-items-start mb-3">
              <div>
                <span className="badge bg-light text-muted me-2">{complaint.case_number}</span>
                <span className={`status-badge status-${complaint.status}`}>{complaint.status.replace(/_/g, ' ')}</span>
              </div>
              <div className="rating-stars">{'★'.repeat(complaint.rating)}{'☆'.repeat(5 - complaint.rating)}</div>
            </div>
            <h2 className="fw-bold mb-3">{complaint.title}</h2>
            <div className="d-flex flex-wrap gap-2 mb-3">
              {complaint.brand_name && <span className="badge bg-primary">{complaint.brand_name}</span>}
              <span className="badge bg-secondary">{complaint.category}</span>
              {complaint.city && <span className="badge badge-muted"><i className="bi bi-geo-alt" /> {complaint.area}, {complaint.city}</span>}
            </div>

            <StatusProgress status={complaint.status} />

            {complaint.ai_summary && (
              <div className="ai-bubble mb-3">
                <i className="bi bi-stars me-2" /><strong>AI Summary:</strong> {complaint.ai_summary}
                <div className="small text-muted mt-1">AI-generated summary — not a platform determination</div>
              </div>
            )}

            <div className="mb-4">
              <h6 className="fw-bold">Consumer Story</h6>
              <p>{complaint.description}</p>
              <div className="small text-muted">
                by {complaint.author_name}
                {complaint.author_verified && <i className="bi bi-patch-check-fill text-primary ms-1" />}
                · Weight score: {complaint.weight_score}
              </div>
            </div>

            {complaint.desired_resolution && (
              <div className="mb-3"><strong>Desired resolution:</strong> {complaint.desired_resolution}</div>
            )}

            <div className="d-flex gap-2 mb-4">
              <button className="btn btn-outline-primary btn-sm" onClick={handleMeToo}>
                <i className="bi bi-hand-thumbs-up me-1" />Me Too ({complaint.me_too_count})
              </button>
            </div>
          </div>

          {/* Timeline */}
          <div className="card-panchaayat p-4 mb-4">
            <h5 className="fw-bold mb-3"><i className="bi bi-clock-history me-2" />Case Timeline</h5>
            <div className="timeline">
              {complaint.timeline?.map(ev => (
                <div key={ev.id} className="timeline-item">
                  <div className={`timeline-dot ${ev.event_type === 'resolved' ? 'resolved' : ev.event_type === 'brand_response' ? 'brand' : ''}`} />
                  <div className="fw-semibold">{ev.title}</div>
                  {ev.description && <div className="small text-muted">{ev.description}</div>}
                  <div className="small text-muted">{new Date(ev.created_at).toLocaleString()} {ev.actor_name && `· ${ev.actor_name}`}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Resolution */}
          {pendingResolution && isAuthor && (
            <div className="card-panchaayat p-4 mb-4 border-primary">
              <h5 className="fw-bold text-primary mb-3">Resolution Proposed — Your Confirmation Required</h5>
              <p>{pendingResolution.description}</p>
              <p className="small text-muted">Type: {pendingResolution.resolution_type}</p>
              <div className="d-flex flex-wrap gap-2">
                <button className="btn btn-success" onClick={() => handleRespondResolution(pendingResolution.id, 'accept', { response: 'Issue resolved', resolution_rating: 4 })}>
                  Yes, Resolved
                </button>
                <button className="btn btn-warning" onClick={() => handleRespondResolution(pendingResolution.id, 'partial', { response: 'Partially resolved' })}>
                  Partially Resolved
                </button>
                <button className="btn btn-danger" onClick={() => handleRespondResolution(pendingResolution.id, 'reject', { rejection_reason: 'Resolution not sufficient' })}>
                  Reject & Reopen
                </button>
              </div>
            </div>
          )}

          {complaint.resolution_feedback && (
            <div className="card-panchaayat p-4 mb-4 bg-success bg-opacity-10">
              <h6 className="fw-bold">Post-Resolution Feedback</h6>
              <p>{complaint.resolution_feedback}</p>
              {complaint.resolution_rating && <div>Resolution rating: {'★'.repeat(complaint.resolution_rating)}</div>}
            </div>
          )}

          {/* Brand propose resolution */}
          {isBrand && !pendingResolution && complaint.status !== 'resolved' && (
            <div className="card-panchaayat p-4 mb-4">
              <h5 className="fw-bold mb-3">Propose Resolution</h5>
              {aiSuggestion && <div className="ai-bubble small mb-3"><strong>AI Suggestion:</strong> {aiSuggestion}</div>}
              <form onSubmit={handleProposeResolution}>
                <select className="form-select mb-2" value={resolutionForm.resolution_type}
                  onChange={e => setResolutionForm({ ...resolutionForm, resolution_type: e.target.value })}>
                  {['Refund', 'Replacement', 'Repair', 'Installation', 'Apology', 'Compensation', 'Other'].map(t => (
                    <option key={t}>{t}</option>
                  ))}
                </select>
                <textarea className="form-control mb-2" rows={3} placeholder="Describe the resolution..."
                  value={resolutionForm.description} onChange={e => setResolutionForm({ ...resolutionForm, description: e.target.value })} required />
                <button className="btn btn-primary" type="submit">Propose Resolution</button>
              </form>
            </div>
          )}

          {/* Discussion */}
          <div className="card-panchaayat p-4 mb-4">
            <h5 className="fw-bold mb-3">Discussion ({complaint.comments?.length || complaint.comment_count})</h5>
            {complaint.comments?.length > 0 ? complaint.comments.map(c => (
              <div key={c.id} className={`mb-3 ${c.is_official_brand_reply ? 'official-reply' : ''}`}>
                <div className="fw-semibold small">
                  {c.author_name}
                  {c.is_official_brand_reply && <span className="badge bg-primary ms-2">Official Response</span>}
                </div>
                <p className="mb-1">{c.body}</p>
                <div className="small text-muted">{new Date(c.created_at).toLocaleString()}</div>
                {c.replies?.map(r => (
                  <div key={r.id} className="ms-4 mt-2 border-start ps-3">
                    <div className="fw-semibold small">{r.author_name}</div>
                    <p className="mb-0 small">{r.body}</p>
                  </div>
                ))}
              </div>
            )) : (
              <p className="text-muted small">No comments yet. Be the first to share your experience or support the consumer.</p>
            )}
            <form onSubmit={handleComment} className="mt-3">
              <textarea className="form-control mb-2" rows={2} placeholder="Add a comment..."
                value={comment} onChange={e => setComment(e.target.value)} required />
              <button className="btn btn-primary btn-sm" type="submit">Post Comment</button>
            </form>
          </div>
        </div>

        <div className="col-lg-4">
          <AdBanner placement="sidebar" category={complaint.category} keywords={complaint.ai_topics?.join(',')} city={complaint.city} area={complaint.area} />
          <div className="card-panchaayat p-3 mt-3">
            <h6 className="fw-bold">Escalation Options</h6>
            <p className="small text-muted">Still unresolved?</p>
            <ul className="small">
              <li>National Consumer Helpline: 1800-11-4000</li>
              <li>E-Jagriti portal</li>
              <li>Brand escalation team</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
