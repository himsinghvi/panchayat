import { useState, useCallback } from 'react'

export function useDemoToast() {
  const [message, setMessage] = useState(null)

  const show = useCallback((text) => {
    setMessage(text)
    window.setTimeout(() => setMessage(null), 4000)
  }, [])

  const Toast = message ? (
    <div className="page-toast" role="status">
      <i className="bi bi-info-circle me-2" />
      {message}
    </div>
  ) : null

  return { show, Toast }
}

export function PlanButton({ plan, variant = 'outline', featured, onSelect }) {
  const labels = { startup: 'Startup', scaleup: 'Scale-up', enterprise: 'Enterprise' }
  const cls = featured ? 'btn btn-primary w-100' : variant === 'dark' ? 'btn btn-dark w-100' : 'btn btn-outline-primary w-100'
  return (
    <button type="button" className={cls} onClick={() => onSelect(labels[plan] || plan)}>
      Choose {labels[plan] || plan}
    </button>
  )
}

export function SalesLink({ children, onTalk }) {
  return (
    <button type="button" className="btn btn-primary" onClick={onTalk}>
      {children}
    </button>
  )
}