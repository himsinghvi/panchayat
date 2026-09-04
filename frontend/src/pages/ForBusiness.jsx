import { Link } from 'react-router-dom'
import { useDemoToast, PlanButton, SalesLink } from '../components/MarketingHelpers'

const PLANS = [
  {
    id: 'startup',
    name: 'Startup',
    tag: 'For solo founders & small teams just getting queries organised',
    price: '₹1,999',
    featured: false,
    variant: 'outline',
    features: [
      'Branded page at panchaayat.in/yourbrand',
      'Up to 150 private cases/month',
      'Case status, comments & attachments',
      'Email + SMS notifications to customers',
      '1 support seat',
    ],
  },
  {
    id: 'scaleup',
    name: 'Scale-up',
    tag: 'For growing teams with 3–15 support agents',
    price: '₹3,999',
    featured: true,
    features: [
      'Everything in Startup',
      'Unlimited cases + 2-way email-to-case sync',
      'Branded FAQ page + CSAT/NPS tracking',
      'Auto-tagging of social escalations (X, LinkedIn, FB)',
      'Up to 10 support seats + SLA rules',
    ],
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    tag: 'For companies needing full case-management ops',
    price: '₹5,999',
    featured: false,
    variant: 'dark',
    features: [
      'Everything in Scale-up',
      'Full REST API + bulk export (CSV/JSON)',
      'AI chatbot for first-line triage & FAQs',
      'White-label + custom domain, webhooks',
      'Live quality-monitoring dashboards, unlimited seats',
    ],
  },
]

const FEATURE_MATRIX = [
  { icon: 'bi-envelope', title: '2-way email-to-case sync', desc: 'Customer emails become cases automatically; agent replies sync back both ways.' },
  { icon: 'bi-diagram-3', title: 'Escalation matrix repository', desc: 'Public contact hours, HQ address, and named escalation contacts with verified social handles.' },
  { icon: 'bi-share', title: 'Social escalation auto-scraping', desc: 'Mentions and tags on X, LinkedIn and Facebook get linked to a case automatically.' },
  { icon: 'bi-shield-lock', title: 'Secure attachment & recording uploads', desc: 'Call recordings, bills and screenshots stored encrypted, visible only to customer and agents.' },
  { icon: 'bi-box-arrow-up-right', title: 'Webhooks & bulk export', desc: 'Push case events into your CRM/helpdesk in real time, or export full case history any time.' },
  { icon: 'bi-graph-up', title: 'Live quality dashboards', desc: 'SLA breaches, agent response times, CSAT/NPS trends — updated in real time (Enterprise).' },
]

const STEPS = [
  'Branded page replaces the "email us" link on their website and order-confirmation SMS.',
  'Every query gets a case ID, a status, and an owner — nothing sits unread in an inbox again.',
  'Customers can choose to keep a query private (default for SME plans) or escalate it publicly if unresolved.',
  'Support team gets a live dashboard: open queries, SLA breaches, and CSAT after every resolution.',
  'Two-way email sync means agents keep replying from Outlook/Gmail — cases stay in sync either way.',
]

export default function ForBusiness() {
  const { show, Toast } = useDemoToast()

  const handlePlan = (plan) => show(`This would start ${plan} plan checkout`)
  const handleTrial = () => show('This would open a signup flow for business accounts')
  const handleSales = () => show('This would open a call-back request form for Custom / Call Centre plan')

  return (
    <div className="marketing-page">
      {Toast}

      <section className="biz-hero">
        <div className="container">
          <span className="marketing-kicker">FOR SMES & MSMEs WITHOUT A HELPDESK</span>
          <h1 className="marketing-title">Turn your inbox into a real case management system.</h1>
          <p className="marketing-lead">
            Most small and mid-size businesses run customer support entirely through a shared email inbox — queries get lost,
            nothing is tracked, and nobody has visibility into what's open. Panchaayat gives you a branded, hotlinked page
            where customers file private cases directly, with the same case management your largest competitors use.
          </p>
          <div className="d-flex flex-wrap gap-2">
            <button type="button" className="btn btn-dark btn-lg" onClick={handleTrial}>Start free 14-day trial</button>
            <a className="btn btn-outline-primary btn-lg" href="#plans">See plans & pricing</a>
          </div>
        </div>
      </section>

      <section className="biz-scenario py-5">
        <div className="container">
          <div className="row g-4 align-items-start">
            <div className="col-lg-6">
              <h2 className="fw-bold mb-3">A typical scenario</h2>
              <p>
                <strong>Chaitanya Furnishings</strong> is a 40-person D2C furniture brand in Bengaluru. Customer queries about
                delayed deliveries, damaged items and refunds all land in{' '}
                <code className="mono-chip">support@chaitanyafurnishings.in</code> — a single shared inbox with no ownership,
                no SLA, and no way to see which of last month's 300 emails are still unresolved.
              </p>
              <p>
                They sign up for the <strong>Scale-up plan</strong>, get a branded page at{' '}
                <code className="mono-chip">panchaayat.in/chaitanyafurnishings</code>, and connect it to their existing support
                email. Every incoming email automatically becomes a tracked case; every reply goes back out as email, SMS or
                WhatsApp — without the customer needing a new tool.
              </p>
              <p className="mb-0">
                Within a month they can see, for the first time, that refund requests take 9 days on average to close — and fix it.
              </p>
            </div>
            <div className="col-lg-6">
              <div className="card-panchaayat p-4">
                <h5 className="fw-bold mb-3">What changes for Chaitanya Furnishings</h5>
                {STEPS.map((text, i) => (
                  <div key={i} className="stepline d-flex gap-3 mb-3">
                    <div className="stepline-dot">{i + 1}</div>
                    <p className="small mb-0">{text}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="biz-plans py-5 section-surface" id="plans">
        <div className="container">
          <h2 className="fw-bold text-center mb-2">Simple plans for SMEs and MSMEs</h2>
          <p className="text-center text-muted mb-5">No helpdesk software to install. Go live on a branded page in under a day.</p>
          <div className="plan-grid">
            {PLANS.map(plan => (
              <div key={plan.id} className={`plan-card card-panchaayat p-4 ${plan.featured ? 'plan-card--featured' : ''}`}>
                {plan.featured && <span className="plan-badge">Most popular</span>}
                <div className="plan-name fw-bold">{plan.name}</div>
                <div className="plan-tag small text-muted mb-3">{plan.tag}</div>
                <div className="plan-price">{plan.price}<span>/month</span></div>
                <div className="plan-billing small text-muted mb-3">Billed monthly · cancel anytime</div>
                <ul className="plan-feats list-unstyled mb-4">
                  {plan.features.map(f => (
                    <li key={f}><i className="bi bi-check2 text-success me-2" />{f}</li>
                  ))}
                </ul>
                <PlanButton plan={plan.id} featured={plan.featured} variant={plan.variant} onSelect={handlePlan} />
              </div>
            ))}
          </div>

          <div className="enterprise-cta card-panchaayat p-4 mt-5">
            <div className="row align-items-center g-3">
              <div className="col-lg-8">
                <h3 className="fw-bold">Need a call centre too? Custom plan.</h3>
                <p className="text-muted mb-3">
                  For large corporates: fully outsourced inbound voice support, dedicated case managers, custom SLAs,
                  and everything on the Enterprise plan — priced against your call volume and headcount.
                </p>
                <div className="d-flex flex-wrap gap-2">
                  {['Outsourced inbound voice / call centre', 'Dedicated success manager', 'Custom SLA & compliance review', 'On-prem / VPC deployment option'].map(f => (
                    <span key={f} className="badge badge-muted">{f}</span>
                  ))}
                </div>
              </div>
              <div className="col-lg-4 text-lg-end">
                <SalesLink onTalk={handleSales}>Talk to sales →</SalesLink>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="biz-guarantee py-5">
        <div className="container text-center">
          <div className="guarantee-icon mb-3"><i className="bi bi-shield-check" /></div>
          <h3 className="fw-bold">30-day money-back guarantee</h3>
          <p className="text-muted mx-auto" style={{ maxWidth: '52ch' }}>
            If your team isn't resolving queries faster within 30 days of going live, we refund the plan in full —
            no lock-in contracts, cancel any time from your billing settings.
          </p>
        </div>
      </section>

      <section className="biz-features py-5 section-surface">
        <div className="container">
          <h2 className="fw-bold mb-4">Every plan includes, or can add</h2>
          <div className="row g-3">
            {FEATURE_MATRIX.map(f => (
              <div key={f.title} className="col-md-6 col-lg-4">
                <div className="fm-item card-panchaayat p-3 h-100">
                  <div className="fm-icon mb-2"><i className={`bi ${f.icon}`} /></div>
                  <h6 className="fw-bold">{f.title}</h6>
                  <p className="small text-muted mb-0">{f.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-5">
        <div className="container text-center">
          <h4 className="fw-bold mb-3">Already have a brand account?</h4>
          <div className="d-flex justify-content-center gap-2 flex-wrap">
            <Link to="/brand-dashboard" className="btn btn-primary">Go to Brand Dashboard</Link>
            <Link to="/api" className="btn btn-outline-primary">View API docs</Link>
          </div>
        </div>
      </section>
    </div>
  )
}
