import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', email: '', password: '', display_name: '', city: '' })
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await register(form)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="container py-5">
      <div className="col-md-5 mx-auto">
        <div className="card-panchaayat p-4">
          <h3 className="fw-bold mb-4 text-center">Create Account</h3>
          <p className="text-muted small text-center">Registered users get higher complaint weight & faster resolution.</p>
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit}>
            {['display_name', 'username', 'email', 'password', 'city'].map(field => (
              <div className="mb-3" key={field}>
                <label className="form-label text-capitalize">{field.replace('_', ' ')}</label>
                <input className="form-control" type={field === 'password' ? 'password' : field === 'email' ? 'email' : 'text'}
                  value={form[field]} onChange={e => setForm({ ...form, [field]: e.target.value })} required={field !== 'city'} />
              </div>
            ))}
            <button className="btn btn-primary w-100">Register</button>
          </form>
          <p className="text-center mt-3 small">Already have an account? <Link to="/login">Login</Link></p>
        </div>
      </div>
    </div>
  )
}
