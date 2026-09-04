import { createContext, useContext, useEffect, useState } from 'react'

const BrandContext = createContext(null)

export function BrandProvider({ children }) {
  const [brand, setBrand] = useState(() => {
    if (typeof window === 'undefined') return 'modern'
    return localStorage.getItem('panchaayat-brand') || 'modern'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-brand', brand)
    localStorage.setItem('panchaayat-brand', brand)
  }, [brand])

  const switchToClassic = () => setBrand('classic')
  const switchToModern = () => setBrand('modern')
  const toggleBrand = () => setBrand(b => (b === 'modern' ? 'classic' : 'modern'))

  return (
    <BrandContext.Provider value={{
      brand,
      setBrand,
      toggleBrand,
      switchToClassic,
      switchToModern,
      isModern: brand === 'modern',
      isClassic: brand === 'classic',
    }}>
      {children}
    </BrandContext.Provider>
  )
}

export const useBrand = () => useContext(BrandContext)
