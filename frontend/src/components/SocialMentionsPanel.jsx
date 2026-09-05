import { useState, useEffect } from 'react'
import { api } from '../api'

const PLATFORMS = [
  { id: 'all', label: 'All', icon: 'bi-grid' },
  { id: 'twitter', label: 'X', icon: 'bi-twitter-x' },
  { id: 'reddit', label: 'Reddit', icon: 'bi-reddit' },
  { id: 'linkedin', label: 'LinkedIn', icon: 'bi-linkedin' },
  { id: 'facebook', label: 'Facebook', icon: 'bi-facebook' },
  { id: 'instagram', label: 'Instagram', icon: 'bi-instagram' },
  { id: 'hackernews', label: 'HN', icon: 'bi-newspaper' },
]

const PLATFORM_COLORS = {
  twitter: '#000000',
  reddit: '#FF4500',
  linkedin: '#0A66C2',
  facebook: '#1877F2',
  instagram: '#E4405F',
  hackernews: '#FF6600',
}

const SOURCE_LABELS = {
  live: { text: 'Live', class: 'bg-success' },
  demo: { text: 'Illustrative', class: 'bg-warning text-dark' },
  search: { text: 'Search link', class: 'bg-secondary' },
}

const SENTIMENT_STYLES = {
  negative: 'sentiment-negative',
  positive: 'sentiment-positive',
  neutral: 'sentiment-neutral',
}

function formatWhen(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const diff = Date.now() - d.getTime()
  const hours = Math.floor(diff / 3600000)
  if (hours < 24) return `${hours || 1}h ago`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}d ago`
  return d.toLocaleDateString()
}

export default function SocialMentionsPanel({ complaintId, brandId, compact = false }) {
  const [open, setOpen] = useState(!compact)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [data, setData] = useState(null)
  const [platform, setPlatform] = useState('all')
  const [fetched, setFetched] = useState(false)
  const [apiConfig, setApiConfig] = useState([])

  useEffect(() => {
    api.socialMentionsConfig().then(setApiConfig).catch(() => {})
  }, [])

  const configuredSources = apiConfig.filter(s => s.configured)

  const isPlatformApiConnected = (platformId) => {
    if (platformId === 'all' || platformId === 'hackernews') return false
    if (apiConfig.some(s => s.platform === platformId && s.configured)) return true
    const serp = apiConfig.find(s => s.platform === 'serpapi' && s.configured)
    return Boolean(serp && ['twitter', 'linkedin', 'facebook', 'instagram'].includes(platformId))
  }

  const load = async (plat = platform) => {
    setLoading(true)
    setError('')
    try {
      const result = complaintId
        ? await api.socialMentionsForComplaint(complaintId, plat)
        : await api.socialMentionsForBrand(brandId, plat)
      setData(result)
      setFetched(true)
    } catch (e) {
      setError(e.message || 'Could not fetch social mentions')
    } finally {
      setLoading(false)
    }
  }

  const handlePlatform = (id) => {
    setPlatform(id)
    if (fetched) load(id)
  }

  const mentions = data?.mentions || []
  const filtered = platform === 'all'
    ? mentions
    : mentions.filter(m => m.platform === platform)

  return (
    <div className={`social-mentions-panel ${compact ? 'social-mentions-compact' : ''}`}>
      <div className="social-mentions-header">
        <div>
          <h6 className="fw-bold mb-0">
            <i className="bi bi-megaphone me-2" />
            Social Chatter
          </h6>
          <p className="small text-muted mb-0 mt-1">
            Related posts from X, Reddit, LinkedIn & more
          </p>
        </div>
        {compact && (
          <button type="button" className="btn btn-sm btn-outline-primary" onClick={() => setOpen(v => !v)}>
            {open ? 'Hide' : 'View'}
          </button>
        )}
      </div>

      {open && (
        <>
          {configuredSources.length > 0 && (
            <div className="social-api-status mb-2">
              {configuredSources.map(s => (
                <span key={s.platform} className="social-api-badge" title={s.method}>
                  <i className="bi bi-plug-fill" /> {s.label}
                </span>
              ))}
            </div>
          )}

          <div className="social-platform-filters">
            {PLATFORMS.map(p => (
              <button
                key={p.id}
                type="button"
                className={`social-platform-chip ${platform === p.id ? 'active' : ''} ${isPlatformApiConnected(p.id) ? 'api-connected' : ''}`}
                onClick={() => handlePlatform(p.id)}
                title={isPlatformApiConnected(p.id) ? 'API key configured' : undefined}
              >
                <i className={`bi ${p.icon}`} /> {p.label}
                {isPlatformApiConnected(p.id) && <span className="api-dot" />}
              </button>
            ))}
          </div>

          <div className="d-flex gap-2 mb-3">
            <button
              type="button"
              className="btn btn-primary btn-sm flex-grow-1"
              onClick={() => load()}
              disabled={loading}
            >
              {loading ? (
                <><span className="spinner-border spinner-border-sm me-2" />Scanning…</>
              ) : (
                <><i className="bi bi-radar me-2" />{fetched ? 'Refresh scan' : 'Scan social media'}</>
              )}
            </button>
          </div>

          {error && <div className="alert alert-danger py-2 small">{error}</div>}

          {loading && !data && (
            <div className="social-mentions-skeleton">
              {[1, 2, 3].map(i => <div key={i} className="skeleton-card" />)}
            </div>
          )}

          {data && (
            <>
              <div className="social-scan-meta small text-muted mb-3">
                <span><i className="bi bi-search me-1" />Query: <em>{data.query_used}</em></span>
                <span className="ms-2">
                  <i className="bi bi-broadcast me-1" />
                  {data.live_count} live · {mentions.length} total
                </span>
              </div>

              {filtered.length === 0 ? (
                <div className="social-empty-state">
                  <i className="bi bi-chat-square-dots" />
                  <p>No mentions found for this filter. Try &quot;All&quot; or open a platform search below.</p>
                </div>
              ) : (
                <div className="social-mentions-list">
                  {filtered.map(m => (
                    <article
                      key={m.id}
                      className="social-mention-card"
                      style={{ '--platform-color': PLATFORM_COLORS[m.platform] || 'var(--primary)' }}
                    >
                      <div className="social-mention-top">
                        <span className="social-platform-badge">
                          <i className={`bi bi-${m.platform === 'twitter' ? 'twitter-x' : m.platform === 'hackernews' ? 'newspaper' : m.platform}`} />
                          {m.platform_label}
                        </span>
                        <span className={`badge ${SOURCE_LABELS[m.source]?.class || 'bg-secondary'}`}>
                          {SOURCE_LABELS[m.source]?.text || m.source}
                        </span>
                      </div>
                      <div className="social-mention-author">
                        <strong>{m.author}</strong>
                        {m.handle && <span className="text-muted ms-1">{m.handle}</span>}
                        {m.posted_at && <span className="text-muted ms-auto">{formatWhen(m.posted_at)}</span>}
                      </div>
                      <p className="social-mention-text">{m.text}</p>
                      <div className="social-mention-footer">
                        {m.sentiment && (
                          <span className={`sentiment-pill ${SENTIMENT_STYLES[m.sentiment] || ''}`}>
                            {m.sentiment}
                          </span>
                        )}
                        {m.engagement && <span className="small text-muted">{m.engagement}</span>}
                        {m.url && (
                          <a href={m.url} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-secondary ms-auto">
                            Open <i className="bi bi-box-arrow-up-right ms-1" />
                          </a>
                        )}
                      </div>
                    </article>
                  ))}
                </div>
              )}

              {data.search_links?.length > 0 && (
                <div className="social-search-links mt-3">
                  <h6 className="small fw-bold text-muted text-uppercase mb-2">Search on platform</h6>
                  <div className="social-search-grid">
                    {data.search_links.map(link => (
                      <a
                        key={link.platform}
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="social-search-link"
                        style={{ '--platform-color': PLATFORM_COLORS[link.platform] || 'var(--primary)' }}
                      >
                        <i className={`bi bi-${link.platform === 'twitter' ? 'twitter-x' : link.platform}`} />
                        <span>{link.label}</span>
                        <small>{link.hint}</small>
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {data.notes?.length > 0 && (
                <div className="social-mentions-disclaimer mt-3">
                  <i className="bi bi-info-circle me-1" />
                  {data.notes.map((note, i) => (
                    <span key={i}>{i > 0 && ' '}{note}</span>
                  ))}
                </div>
              )}
            </>
          )}
        </>
      )}
    </div>
  )
}
