import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useDemoToast } from '../components/MarketingHelpers'

const NAV = [
  { id: 'auth', label: 'Authentication' },
  { id: 'cases', label: 'Cases' },
  { id: 'comments', label: 'Comments & status' },
  { id: 'hotqueries', label: 'Hot queries' },
  { id: 'webhooks', label: 'Webhooks' },
  { id: 'export', label: 'Bulk export' },
]

const ENDPOINTS = [
  { method: 'POST', methodClass: 'post', path: '/v1/cases', desc: 'Create a new case, returns a Panchaayat ID' },
  { method: 'GET', methodClass: '', path: '/v1/cases/:id', desc: 'Fetch case detail, comments and status history' },
  { method: 'POST', methodClass: 'post', path: '/v1/cases/:id/comments', desc: 'Post a response as a verified company rep' },
  { method: 'POST', methodClass: 'post', path: '/v1/cases/:id/status', desc: 'Update status: open, in_progress, resolved' },
  { method: 'GET', methodClass: '', path: '/v1/export', desc: 'Bulk export cases as CSV or JSON (Enterprise)' },
]

const HOT_QUERIES = [
  { name: 'Register DND / stop sales calls', code: 'hotquery.dnd_register', desc: 'Used heavily against telemarketing-heavy sectors — e.g. Policybazaar, Bajaj Finance.' },
  { name: 'Check loan / credit card application status', code: 'hotquery.application_status', desc: 'Pulls status directly if the company has connected their processing system via webhook.' },
  { name: 'Check insurance claim status', code: 'hotquery.claim_status', desc: 'Surfaces claim stage and next required document, if available.' },
  { name: 'Request refund status', code: 'hotquery.refund_status', desc: 'Common for e-commerce and wallet/UPI-linked refund delays.' },
]

export default function ApiDocs() {
  const { show, Toast } = useDemoToast()
  const [active, setActive] = useState('auth')

  useEffect(() => {
    const sections = NAV.map(n => document.getElementById(n.id)).filter(Boolean)
    const observer = new IntersectionObserver(
      entries => {
        const visible = entries.filter(e => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)
        if (visible[0]) setActive(visible[0].target.id)
      },
      { rootMargin: '-20% 0px -60% 0px', threshold: [0, 0.25, 0.5] }
    )
    sections.forEach(s => observer.observe(s))
    return () => observer.disconnect()
  }, [])

  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    setActive(id)
  }

  return (
    <div className="marketing-page">
      {Toast}

      <section className="api-hero">
        <div className="container">
          <span className="marketing-kicker">DEVELOPER DOCS</span>
          <h1 className="marketing-title">Build case creation, status checks and hot service requests into your own apps.</h1>
          <p className="marketing-lead">
            The Panchaayat API lets verified companies and enterprise customers create and update cases, pull analytics,
            and expose one-tap "hot query" actions like DND registration or application-status checks directly to their customers.
          </p>
          <button type="button" className="btn btn-dark btn-lg" onClick={() => show('This would generate a sandbox API key')}>
            Get a sandbox API key
          </button>
        </div>
      </section>

      <section className="api-body py-5">
        <div className="container">
          <div className="api-grid">
            <nav className="api-nav">
              {NAV.map(item => (
                <button
                  key={item.id}
                  type="button"
                  className={`api-nav-link ${active === item.id ? 'active' : ''}`}
                  onClick={() => scrollTo(item.id)}
                >
                  {item.label}
                </button>
              ))}
            </nav>

            <div className="api-content">
              <div className="api-section" id="auth">
                <h3 className="fw-bold">Authentication</h3>
                <p className="text-muted">
                  All requests use a Bearer token issued to verified company accounts. Sandbox keys are rate-limited to
                  100 requests/min; production keys scale with your plan.
                </p>
                <pre className="code-block"><code>{`curl https://api.panchaayat.in/v1/cases \\
  -H "Authorization: Bearer sk_live_••••••••" \\
  -H "Content-Type: application/json"`}</code></pre>
              </div>

              <div className="api-section" id="cases">
                <h3 className="fw-bold">Create a case</h3>
                <p className="text-muted">
                  Used by your website, app or IVR to file a case directly against your verified account — same object
                  model as cases filed on panchaayat.in.
                </p>
                <pre className="code-block"><code>{`POST /v1/cases
{
  "reference_id": "BF-LN-77213",
  "category": "insurance_claims",
  "type": "complaint",
  "title": "Cashless claim not approved",
  "description": "...",
  "anonymous": false
}`}</code></pre>
                <div className="table-responsive">
                  <table className="table endpoint-table">
                    <thead>
                      <tr><th>Method</th><th>Endpoint</th><th>Description</th></tr>
                    </thead>
                    <tbody>
                      {ENDPOINTS.map(ep => (
                        <tr key={ep.path + ep.method}>
                          <td><span className={`method-badge ${ep.methodClass}`}>{ep.method}</span></td>
                          <td><code>{ep.path}</code></td>
                          <td className="text-muted">{ep.desc}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="api-section" id="comments">
                <h3 className="fw-bold">Comments & status</h3>
                <p className="text-muted">
                  Post official brand replies and transition case status through the same workflow consumers see on the platform.
                  Status values include <code>open</code>, <code>in_progress</code>, <code>resolution_proposed</code>, and <code>resolved</code>.
                </p>
                <pre className="code-block"><code>{`POST /v1/cases/:id/comments
{
  "body": "We have initiated a refund to your original payment method.",
  "is_official": true
}

POST /v1/cases/:id/status
{ "status": "resolution_proposed" }`}</code></pre>
              </div>

              <div className="api-section" id="hotqueries">
                <h3 className="fw-bold">Hot queries — one-tap service requests</h3>
                <p className="text-muted">
                  Pre-built request types your customers can trigger without writing a full complaint — useful on your app
                  or IVR menu. Each returns a tracked Panchaayat ID.
                </p>
                {HOT_QUERIES.map(hq => (
                  <div key={hq.code} className="hotquery-card card-panchaayat p-3 mb-2">
                    <div className="d-flex justify-content-between align-items-start gap-2 flex-wrap mb-1">
                      <span className="fw-semibold">{hq.name}</span>
                      <code className="mono-chip">{hq.code}</code>
                    </div>
                    <p className="small text-muted mb-0">{hq.desc}</p>
                  </div>
                ))}
              </div>

              <div className="api-section" id="webhooks">
                <h3 className="fw-bold">Webhooks</h3>
                <p className="text-muted">
                  Enterprise accounts can subscribe to <code>case.created</code>, <code>case.status_changed</code>,
                  <code>case.comment_added</code> and <code>case.csat_submitted</code> events to sync into an internal
                  CRM or helpdesk in real time.
                </p>
                <pre className="code-block"><code>{`POST https://your-app.com/webhooks/panchaayat
{
  "event": "case.status_changed",
  "case_id": "PAN-2026-0042",
  "status": "resolved",
  "timestamp": "2026-03-04T10:30:00Z"
}`}</code></pre>
              </div>

              <div className="api-section" id="export">
                <h3 className="fw-bold">Bulk export</h3>
                <p className="text-muted">
                  Enterprise plans can export the full case history as CSV or JSON for compliance, analytics, or migration.
                </p>
                <pre className="code-block"><code>{`GET /v1/export?format=csv&from=2026-01-01&to=2026-03-01
Authorization: Bearer sk_live_••••••••`}</code></pre>
              </div>

              <div className="card-panchaayat p-4 mt-4">
                <h5 className="fw-bold mb-2">Need API access?</h5>
                <p className="text-muted small mb-3">
                  Full REST API access is included on the Enterprise plan. Sandbox keys are available for integration testing.
                </p>
                <div className="d-flex flex-wrap gap-2">
                  <Link to="/for-business" className="btn btn-primary btn-sm">View business plans</Link>
                  <button type="button" className="btn btn-outline-primary btn-sm" onClick={() => show('This would open a sales callback form')}>
                    Talk to sales
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
