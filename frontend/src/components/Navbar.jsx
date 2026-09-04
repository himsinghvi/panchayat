import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import ThemeToggle from './ThemeToggle'

export default function Navbar() {
  const { user, logout, isBrand, isAdmin } = useAuth()
  const navigate = useNavigate()

  return (
    <nav className="navbar navbar-expand-lg navbar-panchaayat sticky-top">
      <div className="container">
        <Link className="navbar-brand brand-logo" to="/">
          Pancha<span>ayat</span>
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="nav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item"><Link className="nav-link" to="/feed">Feed</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/search">Search</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/how-it-works">How It Works</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/for-business">For Business</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/api">API</Link></li>
          </ul>
          <div className="d-flex align-items-center gap-2">
            <ThemeToggle />
            <Link to="/share" className="btn btn-primary btn-sm">
              <i className="bi bi-megaphone me-1" /> Share Experience
            </Link>
            {user ? (
              <div className="dropdown">
                <button className="btn btn-outline-secondary btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                  {user.avatar_url && <img src={user.avatar_url} alt="" width="24" height="24" className="rounded-circle me-1" />}
                  {user.display_name}
                </button>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li><Link className="dropdown-item" to="/dashboard">My Dashboard</Link></li>
                  {isBrand && <li><Link className="dropdown-item" to="/brand-dashboard">Brand Dashboard</Link></li>}
                  {isAdmin && <li><Link className="dropdown-item" to="/admin">Admin Panel</Link></li>}
                  <li><hr className="dropdown-divider" /></li>
                  <li><button className="dropdown-item" onClick={() => { logout(); navigate('/') }}>Logout</button></li>
                </ul>
              </div>
            ) : (
              <>
                <Link to="/login" className="btn btn-outline-primary btn-sm">Login</Link>
                <Link to="/register" className="btn btn-outline-secondary btn-sm">Register</Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
