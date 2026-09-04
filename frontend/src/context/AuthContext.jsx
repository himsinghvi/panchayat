import { createContext, useContext, useState, useEffect } from 'react'
import { api } from '../api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      api.me().then(setUser).catch(() => localStorage.removeItem('token')).finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (username, password) => {
    const data = await api.login({ username, password })
    localStorage.setItem('token', data.access_token)
    setUser(data.user)
    return data.user
  }

  const register = async (form) => {
    const data = await api.register(form)
    localStorage.setItem('token', data.access_token)
    setUser(data.user)
    return data.user
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  const isBrand = user?.role === 'brand_rep'
  const isAdmin = user?.role === 'admin'
  const isModerator = user?.role === 'moderator'

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, isBrand, isAdmin, isModerator }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
