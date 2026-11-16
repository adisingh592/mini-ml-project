/**
 * Global application state for HexaDisease 6-Disease Diagnostic Platform.
 * Connects Upload, Analysis, Results, Guidance, Interactive Lab,
 * and Account-Wise Authentication & Longitudinal Tracking to the Flask REST API.
 */
import React, { createContext, useContext, useState, useEffect } from 'react'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [reportType, setReportType]     = useState('Auto-detect')
  const [analysis, setAnalysis]         = useState(null)
  const [loading, setLoading]           = useState(false)
  const [error, setError]               = useState(null)

  // User Authentication State
  const [user, setUser]                 = useState(() => {
    try {
      const stored = localStorage.getItem('hexadisease_user')
      return stored ? JSON.parse(stored) : null
    } catch {
      return null
    }
  })
  const [token, setToken]               = useState(() => {
    return localStorage.getItem('hexadisease_token') || null
  })
  const [authLoading, setAuthLoading]   = useState(false)

  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  // Verify stored token on initial load
  useEffect(() => {
    if (!token) return

    async function verifySession() {
      try {
        const res = await fetch(`${API_BASE}/api/auth/me`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        const data = await res.json()
        if (data.authenticated && data.user) {
          setUser(data.user)
          localStorage.setItem('hexadisease_user', JSON.stringify(data.user))
        } else {
          // Token expired or invalid
          setUser(null)
          setToken(null)
          localStorage.removeItem('hexadisease_user')
          localStorage.removeItem('hexadisease_token')
        }
      } catch (err) {
        console.warn('Auth verification error:', err)
      }
    }

    verifySession()
  }, [token, API_BASE])

  // Authentication Handlers
  async function login(email, password) {
    setAuthLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Login failed')

      setUser(data.user)
      setToken(data.token)
      localStorage.setItem('hexadisease_user', JSON.stringify(data.user))
      localStorage.setItem('hexadisease_token', data.token)
      return data
    } finally {
      setAuthLoading(false)
    }
  }

  async function register(formData) {
    setAuthLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Registration failed')

      setUser(data.user)
      setToken(data.token)
      localStorage.setItem('hexadisease_user', JSON.stringify(data.user))
      localStorage.setItem('hexadisease_token', data.token)
      return data
    } finally {
      setAuthLoading(false)
    }
  }

  async function logout() {
    try {
      if (token) {
        await fetch(`${API_BASE}/api/auth/logout`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        })
      }
    } catch (err) {
      console.warn('Logout network error:', err)
    } finally {
      setUser(null)
      setToken(null)
      localStorage.removeItem('hexadisease_user')
      localStorage.removeItem('hexadisease_token')
    }
  }

  // Analyze report from File object
  async function runAnalysis(file) {
    setLoading(true)
    setError(null)
    setAnalysis(null)
    try {
      const form = new FormData()
      form.append('file', file)

      let res
      try {
        res = await fetch(`${API_BASE}/api/analyze`, { method: 'POST', body: form })
      } catch (networkErr) {
        throw new Error(
          `Cannot reach API at ${API_BASE}. Make sure the Flask server is running (python api.py).`
        )
      }

      const text = await res.text()
      if (!text || text.trim() === '') {
        throw new Error(`Server returned empty response (HTTP ${res.status}).`)
      }

      let data
      try {
        data = JSON.parse(text)
      } catch {
        throw new Error(`Server returned non-JSON response: ${text.slice(0, 150)}`)
      }

      if (!res.ok) throw new Error(data.error || `Server error ${res.status}`)
      setAnalysis(data)
      setUploadedFile({ name: file.name, size: file.size })
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Analyze report from text string
  async function runAnalysisText(reportText, sampleName = "clinical_report.txt") {
    setLoading(true)
    setError(null)
    try {
      let res
      try {
        res = await fetch(`${API_BASE}/api/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: reportText })
        })
      } catch (netErr) {
        throw new Error(`Cannot reach API at ${API_BASE}.`)
      }

      const text = await res.text()
      let data = JSON.parse(text)
      if (!res.ok) throw new Error(data.error || 'Server error')
      
      setAnalysis(data)
      setUploadedFile({ name: sampleName, size: reportText.length })
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Direct single-disease prediction
  async function runPredict(disease, features) {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disease, features })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Prediction failed')
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Save current report to database history (Strictly requires authentication for privacy)
  async function saveCurrentReport(patientName = 'Self Routine Checkup', patientAge = 45, patientGender = 'Unspecified') {
    if (!analysis) throw new Error('No analysis available to save.')
    if (!token || !user) {
      throw new Error('Authentication required: Please sign in or create an account to securely save and isolate your medical reports.')
    }

    const headers = { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }

    const payloadName = user?.name ? (patientName === 'Self Routine Checkup' ? user.name : patientName) : (user?.name || patientName)
    const payloadAge = user?.age || patientAge
    const payloadGender = user?.gender || patientGender

    const res = await fetch(`${API_BASE}/api/reports/save`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        analysis,
        patient_name: payloadName,
        patient_age: payloadAge,
        patient_gender: payloadGender,
        filename: uploadedFile?.name || 'Medical_Report.pdf'
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to save report')
    return data
  }

  // Fetch historical reports (filtered to current user account if logged in)
  async function fetchReportHistory() {
    const headers = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const res = await fetch(`${API_BASE}/api/reports/history`, { headers })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to fetch history')
    return data.reports || []
  }

  // Compare two reports by ID
  async function compareReports(id1, id2) {
    const headers = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const res = await fetch(`${API_BASE}/api/reports/compare?report1=${id1}&report2=${id2}`, { headers })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Comparison failed')
    return data.comparison
  }

  // Fetch full biomarker encyclopedia
  async function fetchBiomarkerEncyclopedia() {
    const res = await fetch(`${API_BASE}/api/biomarkers/encyclopedia`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to fetch encyclopedia')
    return data.encyclopedia || {}
  }

  // Delete a report
  async function deleteReport(id) {
    const headers = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const res = await fetch(`${API_BASE}/api/reports/${id}`, { method: 'DELETE', headers })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Delete failed')
    return data
  }

  return (
    <AppContext.Provider value={{
      uploadedFile, setUploadedFile,
      reportType, setReportType,
      analysis, setAnalysis,
      loading, error, setError,
      runAnalysis, runAnalysisText, runPredict,
      saveCurrentReport, fetchReportHistory, compareReports,
      fetchBiomarkerEncyclopedia, deleteReport,
      // Auth Exports
      user, token, isAuthenticated: Boolean(user && token),
      authLoading, login, register, logout,
      API_BASE
    }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
