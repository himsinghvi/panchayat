const API = '/api'

function getToken() {
  return localStorage.getItem('token')
}

async function request(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  const token = getToken()
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${API}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }))
    const msg = Array.isArray(err.detail)
      ? err.detail.map(e => e.msg || JSON.stringify(e)).join(', ')
      : (typeof err.detail === 'string' ? err.detail : 'Request failed')
    throw new Error(msg)
  }
  return res.json()
}

export const api = {
  health: () => request('/health'),
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  me: () => request('/auth/me'),
  personas: () => request('/auth/personas'),
  complaints: (params = '') => request(`/complaints${params}`),
  complaint: (id) => request(`/complaints/${id}`),
  createComplaint: (data) => request('/complaints', { method: 'POST', body: JSON.stringify(data) }),
  meToo: (id) => request(`/complaints/${id}/me-too`, { method: 'POST' }),
  addComment: (id, data) => request(`/complaints/${id}/comments`, { method: 'POST', body: JSON.stringify(data) }),
  proposeResolution: (id, data) => request(`/complaints/${id}/resolutions`, { method: 'POST', body: JSON.stringify(data) }),
  respondResolution: (id, resId, data) => request(`/complaints/${id}/resolutions/${resId}/respond`, { method: 'POST', body: JSON.stringify(data) }),
  brands: () => request('/brands'),
  brand: (id) => request(`/brands/${id}`),
  brandBySlug: (slug) => request(`/brands/slug/${slug}`),
  brandComplaints: (id) => request(`/brands/${id}/complaints`),
  brandStats: () => request('/brands/dashboard/stats'),
  search: (q, filters = {}) => {
    const params = new URLSearchParams({ q })
    if (filters.category) params.set('category', filters.category)
    if (filters.status) params.set('status', filters.status)
    if (filters.city) params.set('city', filters.city)
    return request(`/search?${params}`)
  },
  aiDraft: (raw_text) => request('/ai/draft', { method: 'POST', body: JSON.stringify({ raw_text }) }),
  aiQuality: (title, description) => request(`/ai/quality-check?title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}`, { method: 'POST' }),
  aiSuggestResolution: (id) => request(`/ai/suggest-resolution?complaint_id=${id}`),
  aiSuggestAdTargeting: (title, description = '') => request('/ai/suggest-ad-targeting', {
    method: 'POST', body: JSON.stringify({ title, description }),
  }),
  ads: (params = '') => request(`/ads${params}`),
  adminAds: () => request('/admin/ads'),
  createAd: (data) => request('/admin/ads', { method: 'POST', body: JSON.stringify(data) }),
  updateAd: (id, data) => request(`/admin/ads/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteAd: (id) => request(`/admin/ads/${id}`, { method: 'DELETE' }),
  notifications: () => request('/notifications'),
  homeStats: () => request('/stats/home'),
  locations: () => request('/locations'),
}
