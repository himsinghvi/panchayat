import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [personas, setPersonas] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => { api.personas().then(setPersonas).catch(() => {}) }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const user = await login(form.username, form.password)
      if (user.role === 'brand_rep') navigate('/brand-dashboard')
      else if (user.role === 'admin') navigate('/admin')
      else navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const quickLogin = async (username) => {
    setLoading(true)
    try {
      const user = await login(username, 'demo123')
      if (user.role === 'brand_rep') navigate('/brand-dashboard')
      else if (user.role === 'admin') navigate('/admin')
      else navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container py-5">
      <div className="row">
        <div className="col-md-5 mx-auto">
          <div className="card-panchaayat p-4 animate-fade-in">
            <h3 className="fw-bold mb-4 text-center">Welcome Back</h3>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Username</label>
                <input className="form-control" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Password</label>
                <input className="form-control" type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
              </div>
              <button className="btn btn-primary w-100" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>
            <p className="text-center mt-3 small">No account? <Link to="/register">Register</Link></p>
          </div>
        </div>
        <div className="col-md-6">
          <h4 className="fw-bold mb-3">Try Demo Personas</h4>
          <p className="text-muted small mb-3">Click any persona to login instantly (password: demo123)</p>
          <div className="row g-3">
            {personas.map(p => (
              <div key={p.id} className="col-md-6">
                <div className="persona-card" onClick={() => quickLogin(p.username)}>
                  <img src={p.avatar_url} alt="" className="persona-avatar" />
                  <h6 className="fw-bold mb-1">{p.display_name}</h6>
                  <span className="badge badge-muted mb-2">{p.persona_tag}</span>
                  <p className="small text-muted mb-1">{p.bio?.slice(0, 80)}...</p>
                  <div className="small">
                    <span className="badge bg-primary">{p.role}</span>
                    {p.verified && <i className="bi bi-patch-check-fill text-primary ms-1" />}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
