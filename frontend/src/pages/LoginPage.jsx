import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { 
  Lock, Mail, User, Heart, Shield, CheckCircle2, 
  AlertCircle, ArrowRight, Sparkles, LogIn, UserPlus, Droplet
} from 'lucide-react'

export default function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login, register, isAuthenticated, user, logout } = useApp()

  const [mode, setMode] = useState('login') // 'login' | 'register'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [age, setAge] = useState(38)
  const [gender, setGender] = useState('Male')
  const [bloodGroup, setBloodGroup] = useState('B+')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [successMsg, setSuccessMsg] = useState(null)

  // Redirect if already logged in
  if (isAuthenticated && user) {
    return (
      <div className="min-h-[75vh] flex items-center justify-center px-4 py-16">
        <div className="max-w-md w-full bg-white border border-[rgba(23,30,25,0.1)] rounded-3xl p-8 text-center shadow-lg">
          <div className="w-16 h-16 bg-emerald-100 text-emerald-800 rounded-full flex items-center justify-center mx-auto mb-4 font-disp text-2xl font-bold">
            {user.name ? user.name[0].toUpperCase() : 'U'}
          </div>
          <h2 className="text-2xl font-disp font-bold text-[#171e19]">Currently Logged In</h2>
          <p className="text-sm font-semibold text-gray-700 mt-1">{user.name}</p>
          <p className="text-xs text-gray-500">{user.email}</p>
          
          <div className="my-6 p-4 bg-gray-50 border border-gray-100 rounded-2xl text-left text-xs space-y-1.5">
            <div className="flex justify-between">
              <span className="opacity-60">Age / Gender:</span>
              <span className="font-semibold">{user.age || 'N/A'} yrs · {user.gender || 'N/A'}</span>
            </div>
            <div className="flex justify-between">
              <span className="opacity-60">Blood Group:</span>
              <span className="font-semibold text-rose-700 font-mono">{user.blood_group || 'N/A'}</span>
            </div>
            <div className="flex justify-between">
              <span className="opacity-60">Data Isolation:</span>
              <span className="font-semibold text-emerald-700">Account-Protected Active</span>
            </div>
          </div>

          <div className="flex flex-col gap-2.5">
            <Link 
              to="/tracker" 
              className="btn-accent py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2"
            >
              Open My Health Tracker &rarr;
            </Link>
            <button 
              onClick={logout}
              className="py-2.5 px-4 border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-xl transition"
            >
              Sign Out from this Device
            </button>
          </div>
        </div>
      </div>
    )
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setSuccessMsg(null)
    setLoading(true)

    try {
      if (mode === 'login') {
        await login(email, password)
        navigate('/tracker')
      } else {
        await register({
          email,
          password,
          name,
          age: parseInt(age, 10) || 45,
          gender,
          blood_group: bloodGroup
        })
        navigate('/tracker')
      }
    } catch (err) {
      setError(err.message || 'Authentication failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-16">
      <div className="max-w-[480px] w-full">
        {/* Brand / Title Header */}
        <div className="text-center mb-8">
          <span className="badge-tag">Secure Account Portal</span>
          <h1 className="disp text-[clamp(2.4rem,5vw,3.2rem)] mt-3">
            {mode === 'login' ? 'Sign In to ' : 'Create Your '}
            <span className="hl">Account</span>
          </h1>
          <p className="mt-2 text-xs sm:text-sm opacity-70 max-w-sm mx-auto">
            Store, track, and isolate your routine blood test results and early-stage disease risks across checkups.
          </p>
        </div>

        {/* Auth Box */}
        <div className="bg-white border border-[rgba(23,30,25,0.12)] rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
          {/* Tabs */}
          <div className="grid grid-cols-2 p-1 bg-gray-100 rounded-2xl mb-6">
            <button
              type="button"
              onClick={() => { setMode('login'); setError(null); }}
              className={`py-2.5 text-xs sm:text-sm font-bold rounded-xl transition flex items-center justify-center gap-1.5 ${
                mode === 'login'
                  ? 'bg-white text-[#171e19] shadow-sm'
                  : 'text-gray-500 hover:text-[#171e19]'
              }`}
            >
              <LogIn className="w-3.5 h-3.5" />
              Sign In
            </button>
            <button
              type="button"
              onClick={() => { setMode('register'); setError(null); }}
              className={`py-2.5 text-xs sm:text-sm font-bold rounded-xl transition flex items-center justify-center gap-1.5 ${
                mode === 'register'
                  ? 'bg-white text-[#171e19] shadow-sm'
                  : 'text-gray-500 hover:text-[#171e19]'
              }`}
            >
              <UserPlus className="w-3.5 h-3.5" />
              Register
            </button>
          </div>

          {error && (
            <div className="mb-5 p-3.5 bg-red-50 border border-red-200 text-red-700 rounded-xl text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {successMsg && (
            <div className="mb-5 p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{successMsg}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === 'register' && (
              <>
                <div>
                  <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">
                    Full Name
                  </label>
                  <div className="relative">
                    <User className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      required
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="e.g. Rahul Sharma"
                      className="w-full pl-10 pr-4 py-2.5 text-sm bg-gray-50/70 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:border-[#171e19] transition"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2.5">
                  <div>
                    <label className="block text-[11px] font-bold text-gray-700 uppercase tracking-wider mb-1">
                      Age
                    </label>
                    <input
                      type="number"
                      required
                      min={1}
                      max={120}
                      value={age}
                      onChange={(e) => setAge(e.target.value)}
                      className="w-full px-3 py-2 text-sm bg-gray-50/70 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:border-[#171e19]"
                    />
                  </div>
                  <div>
                    <label className="block text-[11px] font-bold text-gray-700 uppercase tracking-wider mb-1">
                      Gender
                    </label>
                    <select
                      value={gender}
                      onChange={(e) => setGender(e.target.value)}
                      className="w-full px-2 py-2 text-sm bg-gray-50/70 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:border-[#171e19]"
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[11px] font-bold text-gray-700 uppercase tracking-wider mb-1">
                      Blood
                    </label>
                    <select
                      value={bloodGroup}
                      onChange={(e) => setBloodGroup(e.target.value)}
                      className="w-full px-2 py-2 text-sm bg-gray-50/70 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:border-[#171e19] font-mono"
                    >
                      <option value="A+">A+</option>
                      <option value="A-">A-</option>
                      <option value="B+">B+</option>
                      <option value="B-">B-</option>
                      <option value="O+">O+</option>
                      <option value="O-">O-</option>
                      <option value="AB+">AB+</option>
                      <option value="AB-">AB-</option>
                    </select>
                  </div>
                </div>
              </>
            )}

            <div>
              <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full pl-10 pr-4 py-2.5 text-sm bg-gray-50/70 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:border-[#171e19] transition"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-2.5 text-sm bg-gray-50/70 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:border-[#171e19] transition"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 btn-accent py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg transition"
            >
              {loading ? (
                <span>Processing...</span>
              ) : mode === 'login' ? (
                <>
                  <span>Sign In to Account</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              ) : (
                <>
                  <span>Create Account &amp; Protect Reports</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Feature Highlights */}
        <div className="mt-8 grid grid-cols-3 gap-3 text-center">
          <div className="p-3 bg-white/60 border border-[rgba(23,30,25,0.06)] rounded-2xl">
            <Shield className="w-4 h-4 mx-auto text-emerald-600 mb-1" />
            <span className="text-[11px] font-bold block text-gray-800">Account Isolated</span>
            <span className="text-[10px] text-gray-500">Personal lab history</span>
          </div>
          <div className="p-3 bg-white/60 border border-[rgba(23,30,25,0.06)] rounded-2xl">
            <Heart className="w-4 h-4 mx-auto text-rose-600 mb-1" />
            <span className="text-[11px] font-bold block text-gray-800">6 Tabular Diseases</span>
            <span className="text-[10px] text-gray-500">Early detection ML</span>
          </div>
          <div className="p-3 bg-white/60 border border-[rgba(23,30,25,0.06)] rounded-2xl">
            <Sparkles className="w-4 h-4 mx-auto text-amber-600 mb-1" />
            <span className="text-[11px] font-bold block text-gray-800">Longitudinal</span>
            <span className="text-[10px] text-gray-500">Compare checkups</span>
          </div>
        </div>
      </div>
    </div>
  )
}
