import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Feed from './pages/Feed'
import ComplaintDetail from './pages/ComplaintDetail'
import CreateComplaint from './pages/CreateComplaint'
import BrandPage from './pages/BrandPage'
import SearchPage from './pages/SearchPage'
import Login from './pages/Login'
import Register from './pages/Register'
import ConsumerDashboard from './pages/ConsumerDashboard'
import BrandDashboard from './pages/BrandDashboard'
import AdminPanel from './pages/AdminPanel'
import HowItWorks from './pages/HowItWorks'
import ForBusiness from './pages/ForBusiness'
import ApiDocs from './pages/ApiDocs'

export default function App() {
  return (
    <>
      <Navbar />
      <main className="page-enter">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/feed" element={<Feed />} />
          <Route path="/complaint/:id" element={<ComplaintDetail />} />
          <Route path="/share" element={<CreateComplaint />} />
          <Route path="/brand/:slug" element={<BrandPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<ConsumerDashboard />} />
          <Route path="/brand-dashboard" element={<BrandDashboard />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/for-business" element={<ForBusiness />} />
          <Route path="/api" element={<ApiDocs />} />
        </Routes>
      </main>
      <Footer />
    </>
  )
}
