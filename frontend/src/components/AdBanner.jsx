import { useState, useEffect } from 'react'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'

export default function AdBanner({ placement = 'sidebar', category, keywords, city, area }) {
  const { user } = useAuth()
  const [ads, setAds] = useState([])

  useEffect(() => {
    const params = new URLSearchParams({ placement })
    if (category) params.set('category', category)
    if (keywords) params.set('keywords', typeof keywords === 'string' ? keywords : keywords.join(','))
    if (city) params.set('city', city)
    if (area) params.set('area', area)
    if (user?.persona_tag) params.set('persona', user.persona_tag)
    if (user?.role) params.set('role', user.role)
    api.ads(`?${params}`).then(setAds).catch(() => {})
  }, [placement, category, keywords, city, area, user])

  if (!ads.length) return null

  return (
    <div className="ad-banner">
      {ads.map(ad => (
        <div key={ad.id} className="ad-card mb-2">
          <div className="ad-label mb-1">Sponsored · Matched for you</div>
          <h6 className="mb-1 fw-semibold">{ad.title}</h6>
          {ad.description && <p className="small text-muted mb-2">{ad.description}</p>}
          {(ad.categories?.length > 0 || ad.cities?.length > 0) && (
            <div className="mb-2">
              {ad.categories?.slice(0, 2).map(c => (
                <span key={c} className="badge badge-muted me-1">{c}</span>
              ))}
              {ad.cities?.slice(0, 1).map(c => (
                <span key={c} className="badge badge-muted me-1"><i className="bi bi-geo-alt" /> {c}</span>
              ))}
            </div>
          )}
          {ad.link_url && ad.link_url !== '#' && (
            <a href={ad.link_url} className="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">
              Learn More
            </a>
          )}
        </div>
      ))}
    </div>
  )
}
