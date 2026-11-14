/**
 * Global application state for HexaDisease 6-Disease Diagnostic Platform.
 * Connects Upload, Analysis, Results, Guidance, and Interactive Lab to the Flask REST API.
 */
import React, { createContext, useContext, useState } from 'react'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [reportType, setReportType]     = useState('Auto-detect')
  const [analysis, setAnalysis]         = useState(null)
  const [loading, setLoading]           = useState(false)
  const [error, setError]               = useState(null)

  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

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

  // Save current report to database history
  async function saveCurrentReport(patientName = 'Self Routine Checkup', patientAge = 45, patientGender = 'Unspecified') {
    if (!analysis) throw new Error('No analysis available to save.')
    const res = await fetch(`${API_BASE}/api/reports/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        analysis,
        patient_name: patientName,
        patient_age: patientAge,
        patient_gender: patientGender,
        filename: uploadedFile?.name || 'Medical_Report.pdf'
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to save report')
    return data
  }

  // Fetch all historical reports
  async function fetchReportHistory() {
    const res = await fetch(`${API_BASE}/api/reports/history`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to fetch history')
    return data.reports || []
  }

  // Compare two reports by ID
  async function compareReports(id1, id2) {
    const res = await fetch(`${API_BASE}/api/reports/compare?report1=${id1}&report2=${id2}`)
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
    const res = await fetch(`${API_BASE}/api/reports/${id}`, { method: 'DELETE' })
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
      API_BASE
    }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
