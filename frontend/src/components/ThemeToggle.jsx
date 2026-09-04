import { useTheme } from '../context/ThemeContext'

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      type="button"
      className="btn btn-theme-toggle"
      onClick={toggleTheme}
      title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
      aria-label="Toggle theme"
    >
      <i className={`bi ${theme === 'light' ? 'bi-moon-stars' : 'bi-sun'}`} />
    </button>
  )
}
