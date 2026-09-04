import { useBrand } from '../context/BrandContext'

export default function BrandToggle() {
  const { isModern, switchToClassic, switchToModern } = useBrand()

  return (
    <button
      type="button"
      className="btn btn-brand-toggle"
      onClick={isModern ? switchToClassic : switchToModern}
      title={isModern ? 'Switch to classic theme' : 'Switch to modern brand theme'}
    >
      <i className={`bi ${isModern ? 'bi-palette' : 'bi-stars'} me-1`} />
      {isModern ? 'Switch to Classic' : 'Modern Theme'}
    </button>
  )
}
