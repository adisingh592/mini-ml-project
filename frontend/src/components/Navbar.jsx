import { NavLink, Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { User, LogIn, LogOut, Shield } from 'lucide-react'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/upload', label: 'Upload Report' },
  { to: '/tracker', label: 'Health Tracker' },
  { to: '/biomarkers', label: 'Biomarker Guide' },
  { to: '/predict', label: 'Disease Predictor' },
  { to: '/guidance', label: 'Diet & Lifestyle' },
]

export default function Navbar() {
  const { user, isAuthenticated, logout } = useApp()

  return (
    <header className="fixed top-0 left-0 right-0 h-20 z-50 bg-white/95 backdrop-blur-md border-b border-[rgba(23,30,25,0.08)] text-[#171e19]">
      <div className="max-w-[1240px] mx-auto px-5 h-full flex items-center justify-between gap-4">
        {/* Logo & Subtitle */}
        <Link to="/" className="flex flex-col group">
          <div className="font-disp text-2xl sm:text-3xl uppercase tracking-normal flex items-baseline">
            ArogyaDrishti<span className="text-[#ffe17c] text-3xl sm:text-4xl leading-none">.</span>
          </div>
          <span className="text-[9px] uppercase tracking-wider font-semibold text-gray-500 -mt-1 group-hover:text-[#171e19] transition-colors hidden sm:block">
            6-Disease Early AI Screening
          </span>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center gap-6 text-sm font-medium">
          {navLinks.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `py-2 border-b-2 transition-colors ${
                  isActive
                    ? 'border-[#ffe17c] text-[#171e19] font-bold'
                    : 'border-transparent text-[#171e19]/70 hover:text-[#171e19]'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Actions & Account Status */}
        <div className="flex items-center gap-3">
          {isAuthenticated && user ? (
            <div className="flex items-center gap-2">
              <Link 
                to="/tracker"
                title={`Logged in as ${user.name} (${user.email})`}
                className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gray-200 bg-gray-50 hover:bg-gray-100 transition text-xs font-semibold text-gray-800"
              >
                <div className="w-6 h-6 rounded-full bg-[#171e19] text-[#ffe17c] flex items-center justify-center font-bold text-xs">
                  {user.name ? user.name[0].toUpperCase() : 'U'}
                </div>
                <span className="max-w-[100px] truncate hidden sm:inline">{user.name.split(' ')[0]}</span>
              </Link>
              <button
                onClick={logout}
                title="Sign Out"
                className="p-2 text-gray-500 hover:text-red-600 rounded-full hover:bg-gray-100 transition"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link 
              to="/login"
              className="text-xs font-bold px-3.5 py-2 border border-gray-300 hover:border-[#171e19] rounded-full flex items-center gap-1.5 transition text-[#171e19]"
            >
              <LogIn className="w-3.5 h-3.5" />
              <span>Sign In</span>
            </Link>
          )}

          <Link to="/upload" className="btn-pill whitespace-nowrap text-xs sm:text-sm">
            Upload Lab Report
          </Link>
        </div>
      </div>
    </header>
  )
}
