import { Link } from 'react-router-dom'

const STATUS_LABELS = {
  awaiting_response: 'Awaiting Brand',
  business_responded: 'Brand Responded',
  resolution_proposed: 'Resolution Proposed',
  resolved: 'Resolved',
  partially_resolved: 'Partially Resolved',
  reopened: 'Reopened',
  published: 'Open',
}

export default function ComplaintCard({ complaint, delay = 0, showMatchReasons = false }) {
  const statusLabel = STATUS_LABELS[complaint.status] || complaint.status?.replace(/_/g, ' ')
  const discussions = complaint.recent_comments || []

  return (
    <Link to={`/complaint/${complaint.id}`} className="complaint-card card-panchaayat p-3 mb-3 animate-fade-in" style={{ animationDelay: `${delay}ms` }}>
      <div className="d-flex justify-content-between align-items-start mb-2">
        <div>
          {complaint.brand_name && (
            <span className="badge badge-muted me-2">{complaint.brand_name}</span>
          )}
          <span className={`status-badge status-${complaint.status}`}>{statusLabel}</span>
        </div>
        <div className="rating-stars small">
          {'★'.repeat(complaint.rating)}{'☆'.repeat(5 - complaint.rating)}
        </div>
      </div>
      <h5 className="fw-semibold mb-2">{complaint.title}</h5>
      <p className="text-muted small mb-2">{complaint.description}</p>
      {complaint.ai_summary && (
        <div className="ai-bubble small mb-2">
          <i className="bi bi-stars ai-icon me-1" />
          <strong>AI Summary:</strong> {complaint.ai_summary}
        </div>
      )}
      {showMatchReasons && complaint.match_reasons?.length > 0 && (
        <div className="small text-primary mb-2">
          <i className="bi bi-search me-1" />Matched: {complaint.match_reasons.join(', ')}
        </div>
      )}
      {discussions.length > 0 && (
        <div className="mb-2 p-2 rounded discussion-preview">
          <div className="small fw-semibold mb-1"><i className="bi bi-chat-dots me-1" />Discussion</div>
          {discussions.slice(0, 2).map((c, i) => (
            <div key={i} className={`small mb-1 ${c.is_official_brand_reply ? 'official-reply p-2' : ''}`}>
              <span className="fw-semibold">{c.author_name}</span>
              {c.is_official_brand_reply && <span className="badge bg-primary ms-1" style={{ fontSize: '0.65rem' }}>Official</span>}
              <div className="text-muted">{c.body}</div>
            </div>
          ))}
          {complaint.comment_count > 2 && (
            <div className="small text-primary">+{complaint.comment_count - 2} more comments</div>
          )}
        </div>
      )}
      <div className="d-flex flex-wrap gap-3 text-muted small">
        {complaint.city && <span><i className="bi bi-geo-alt me-1" />{complaint.area ? `${complaint.area}, ` : ''}{complaint.city}</span>}
        <span><i className="bi bi-tag me-1" />{complaint.category}</span>
        <span><i className="bi bi-hand-thumbs-up me-1" />{complaint.me_too_count} me too</span>
        {complaint.comment_count > 0 && !discussions.length && (
          <span><i className="bi bi-chat me-1" />{complaint.comment_count} comments</span>
        )}
        {complaint.has_brand_response && <span className="text-primary"><i className="bi bi-check-circle me-1" />Brand responded</span>}
      </div>
      <div className="mt-2 d-flex justify-content-between align-items-center">
        <span className="small text-muted">by {complaint.author_name}</span>
        <span className="badge bg-light text-muted">{complaint.case_number}</span>
      </div>
    </Link>
  )
}
