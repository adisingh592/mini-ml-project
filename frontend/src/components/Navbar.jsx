import { NavLink, Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { User, LogIn, LogOut, Shield } from 'lucide-react'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/upload', label: 'Upload' },
  { to: '/tracker', label: 'Health Tracker' },
  { to: '/biomarkers', label: 'Biomarker Guide' },
  { to: '/predict', label: 'Interactive Lab' },
  { to: '/guidance', label: 'Guidance' },
]

export default function Navbar() {
  const { user, isAuthenticated, logout } = useApp()

  return (
    <header className="fixed top-0 left-0 right-0 h-20 z-50 bg-white/90 backdrop-blur-md border-b border-[rgba(23,30,25,0.1)] text-[#171e19]">
      <div className="max-w-[1240px] mx-auto px-5 h-full flex items-center justify-between gap-4">
        {/* Logo */}
        <Link to="/" className="font-disp text-3xl uppercase tracking-normal flex items-baseline">
          ArogyaDrishti<span className="text-[#ffe17c] text-4xl leading-none">.</span>
        </Link>

        {/* Links */}
        <nav className="hidden md:flex items-center gap-7 text-sm font-medium">
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
                className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gray-200 bg-gray-50/80 hover:bg-gray-100 transition text-xs font-semibold text-gray-800"
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
              <span className="hidden sm:inline">Sign In</span>
            </Link>
          )}

          <Link to="/upload" className="btn-pill">
            Upload report
          </Link>
        </div>
      </div>
    </header>
  )
}
