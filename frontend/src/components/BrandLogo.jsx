import { Link } from 'react-router-dom'
import { useBrand } from '../context/BrandContext'

const LOGO = {
  mark: '/brand/panchaayat-mark.png',
  horizontal: '/brand/panchaayat-logo-horizontal-dark.png',
}

export default function BrandLogo({ variant = 'mark', className = '', height, to = '/' }) {
  const { isModern } = useBrand()
  const h = height ?? (variant === 'horizontal' ? 34 : 40)

  if (isModern) {
    return (
      <Link to={to} className={`brand-logo-link ${className}`} aria-label="Panchaayat home">
        <img
          src={LOGO[variant]}
          alt="Panchaayat"
          className={variant === 'horizontal' ? 'brand-logo-img' : 'brand-mark-img'}
          style={{ height: h }}
        />
      </Link>
    )
  }

  if (variant === 'horizontal') {
    return (
      <Link to={to} className={`navbar-brand brand-logo ${className}`}>
        Pancha<span>ayat</span>
      </Link>
    )
  }

  return (
    <Link to={to} className={`brand-logo brand-logo--footer ${className}`}>
      Pancha<span>ayat</span>
    </Link>
  )
}
