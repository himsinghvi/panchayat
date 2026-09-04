import { Link } from 'react-router-dom'
import AdBanner from './AdBanner'

export default function Footer() {
  return (
    <footer className="footer-panchaayat">
      <div className="container">
        <div className="row mb-4">
          <div className="col-md-4">
            <h5 className="brand-logo mb-2">Pancha<span>ayat</span></h5>
            <p className="text-muted small">
              Your voice matters. Share experiences, discuss publicly, and get real resolutions — verified by you.
            </p>
          </div>
          <div className="col-md-2">
            <h6 className="fw-bold small mb-2">Platform</h6>
            <div className="d-flex flex-column gap-1">
              <Link to="/feed" className="text-muted small text-decoration-none">Browse feed</Link>
              <Link to="/share" className="text-muted small text-decoration-none">Share experience</Link>
              <Link to="/how-it-works" className="text-muted small text-decoration-none">How it works</Link>
            </div>
          </div>
          <div className="col-md-2">
            <h6 className="fw-bold small mb-2">For business</h6>
            <div className="d-flex flex-column gap-1">
              <Link to="/for-business" className="text-muted small text-decoration-none">Plans & pricing</Link>
              <Link to="/api" className="text-muted small text-decoration-none">API docs</Link>
              <Link to="/brand-dashboard" className="text-muted small text-decoration-none">Brand dashboard</Link>
            </div>
          </div>
          <div className="col-md-4">
            <AdBanner placement="footer" />
          </div>
        </div>
        <div className="d-flex justify-content-between align-items-center border-top pt-3">
          <span className="text-muted small">&copy; 2026 Panchaayat. Consumer experiences are user-submitted.</span>
          <div className="d-flex gap-3">
            <Link to="/how-it-works" className="text-muted small">How It Works</Link>
            <Link to="/for-business" className="text-muted small">For Business</Link>
            <Link to="/api" className="text-muted small">API</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
