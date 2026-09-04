export default function HowItWorks() {
  const steps = [
    { num: 1, title: 'Share Your Experience', desc: 'Post a review, complaint, or grievance. Tag the brand, location, and product. Add evidence like invoices or photos. No login required — but registered users get higher priority.', icon: 'bi-megaphone' },
    { num: 2, title: 'AI Assists You', desc: 'Our AI helps structure your complaint, checks quality, detects personal info, and suggests improvements — without changing your facts.', icon: 'bi-stars' },
    { num: 3, title: 'Community Discusses', desc: 'Others can comment, share similar experiences with "Me Too", and add helpful information. Everything is transparent.', icon: 'bi-people' },
    { num: 4, title: 'Brand Responds', desc: 'Verified brand representatives reply officially. Their responses are clearly marked and visible to everyone.', icon: 'bi-building' },
    { num: 5, title: 'Resolution Proposed', desc: 'Brands propose concrete resolutions — refund, replacement, repair, apology, etc. Full history is preserved.', icon: 'bi-handshake' },
    { num: 6, title: 'You Confirm', desc: 'Only YOU can mark a complaint as resolved. Reject insufficient resolutions and reopen cases. Leave updated feedback after resolution.', icon: 'bi-check-circle' },
  ]

  return (
    <div className="container py-5">
      <h2 className="fw-bold text-center mb-2">How Panchaayat Works</h2>
      <p className="text-center text-muted mb-5">A transparent consumer experience & resolution network</p>

      <div className="row">
        {steps.map((s, i) => (
          <div key={s.num} className={`col-md-6 mb-4 animate-fade-in stagger-${(i % 4) + 1}`}>
            <div className="card-panchaayat p-4 h-100">
              <div className="d-flex align-items-start">
                <div className="how-icon me-3 flex-shrink-0"><i className={`bi ${s.icon}`} /></div>
                <div>
                  <h5 className="fw-bold">Step {s.num}: {s.title}</h5>
                  <p className="text-muted mb-0">{s.desc}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card-panchaayat p-4 mt-4 bg-light">
        <h5 className="fw-bold mb-3">Guest vs Registered Users</h5>
        <div className="row">
          <div className="col-md-6">
            <h6>Guest (No Login)</h6>
            <ul className="small text-muted">
              <li>Can share experiences immediately</li>
              <li>Lower weight score (0.4x)</li>
              <li>Less visibility in trending</li>
              <li>Slower brand response priority</li>
            </ul>
          </div>
          <div className="col-md-6">
            <h6>Registered & Verified</h6>
            <ul className="small text-muted">
              <li>Higher weight score (1.0x - 1.5x)</li>
              <li>Priority in brand inbox</li>
              <li>Track complaint timeline</li>
              <li>Confirm resolutions & get notifications</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="card-panchaayat p-4 mt-4">
        <h5 className="fw-bold mb-3">Our Trust Principles</h5>
        <ul>
          <li>Brands cannot unilaterally mark complaints as resolved</li>
          <li>Complete resolution history is permanently visible</li>
          <li>Businesses cannot pay to remove legitimate complaints</li>
          <li>AI assists but never judges guilt</li>
          <li>User allegations are presented as experiences, not platform assertions</li>
        </ul>
      </div>
    </div>
  )
}
