import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { 
  History, TrendingUp, TrendingDown, Minus, ArrowRight, ShieldCheck, 
  AlertTriangle, RefreshCw, CheckCircle2, Calendar, FileText, ChevronRight,
  Activity, ArrowUpRight, Scale, Heart, Sparkles, Trash2
} from 'lucide-react'

export default function TrackerPage() {
  const navigate = useNavigate()
  const { 
    fetchReportHistory, compareReports, deleteReport, 
    setAnalysis, setUploadedFile, user, isAuthenticated 
  } = useApp()
  
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedIds, setSelectedIds] = useState([])
  const [comparison, setComparison] = useState(null)
  const [comparing, setComparing] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadHistory()
  }, [user])

  async function loadHistory() {
    setLoading(true)
    setError(null)
    try {
      const reps = await fetchReportHistory()
      setReports(reps)
      if (reps.length >= 2) {
        // Pre-select latest two reports for instant comparison
        const id1 = reps[1].id // earlier
        const id2 = reps[0].id // latest
        setSelectedIds([id1, id2])
        runCompare(id1, id2)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function runCompare(id1, id2) {
    setComparing(true)
    try {
      const cmp = await compareReports(id1, id2)
      setComparison(cmp)
    } catch (err) {
      setError('Comparison failed: ' + err.message)
    } finally {
      setComparing(false)
    }
  }

  function handleSelectReport(id) {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter(x => x !== id))
    } else {
      if (selectedIds.length >= 2) {
        // Keep the second one and add new one
        const updated = [selectedIds[1], id]
        setSelectedIds(updated)
        runCompare(updated[0], updated[1])
      } else {
        const updated = [...selectedIds, id]
        setSelectedIds(updated)
        if (updated.length === 2) {
          runCompare(updated[0], updated[1])
        }
      }
    }
  }

  async function handleDelete(e, id) {
    e.stopPropagation()
    if (!window.confirm(`Delete report #${id} from history?`)) return
    try {
      await deleteReport(id)
      setSelectedIds(selectedIds.filter(x => x !== id))
      if (comparison && (comparison.report_old_id === id || comparison.report_new_id === id)) {
        setComparison(null)
      }
      await loadHistory()
    } catch (err) {
      alert('Delete failed: ' + err.message)
    }
  }

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto min-h-screen">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-8 border-b border-[rgba(23,30,25,0.1)]">
        <div>
          <span className="badge-tag">Longitudinal Health Tracking &amp; History</span>
          <h1 className="disp text-[clamp(2.8rem,6vw,4.5rem)] mt-3">
            Health Progress <span className="hl">&amp; Comparison</span>
          </h1>
          <p className="mt-2 text-base opacity-70 max-w-2xl">
            Track your biomarker trajectories over time. When you complete routine checkups, compare your latest lab report with past baselines to see if your diet, fruits, and exercise are actively reversing early disease risks.
          </p>
        </div>
        
        <div className="flex gap-3">
          <button 
            onClick={loadHistory} 
            className="p-3 border border-[rgba(23,30,25,0.15)] rounded-xl hover:bg-gray-50 flex items-center gap-2 text-sm font-semibold transition"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <Link 
            to="/upload" 
            className="btn-accent px-5 py-3 rounded-xl text-sm font-bold flex items-center gap-2"
          >
            Upload New Report
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Account Info / Status Banner */}
      <div className="mt-8 p-4 rounded-2xl border transition-all shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white border-[rgba(23,30,25,0.08)]">
        {isAuthenticated && user ? (
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-full bg-[#171e19] text-[#ffe17c] flex items-center justify-center font-bold text-base flex-shrink-0">
              {user.name ? user.name[0].toUpperCase() : 'U'}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm text-[#171e19]">{user.name}</span>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                  Account Active · Private Records
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-0.5">
                {user.email} · {user.age} yrs · {user.gender} · Blood: <span className="font-mono font-semibold text-rose-700">{user.blood_group}</span>
              </p>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-amber-100 text-amber-900 rounded-xl flex-shrink-0">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-sm text-[#171e19]">Guest Mode Active</span>
              <p className="text-xs text-gray-500 mt-0.5">
                Sign In to isolate your reports to your personal account and track your health progress across devices.
              </p>
            </div>
          </div>
        )}

        <div>
          {isAuthenticated ? (
            <Link 
              to="/login"
              className="text-xs font-semibold px-3 py-1.5 rounded-xl border border-gray-200 hover:bg-gray-50 transition text-gray-700 inline-block"
            >
              Manage Account &rarr;
            </Link>
          ) : (
            <Link 
              to="/login"
              className="btn-accent text-xs font-bold px-4 py-2 rounded-xl inline-block"
            >
              Sign In / Register &rarr;
            </Link>
          )}
        </div>
      </div>

      {/* Reports Timeline / Cards */}
      <div className="mt-10">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <History className="w-5 h-5 opacity-70" />
            Saved Medical Reports ({reports.length})
          </h2>
          <span className="text-xs opacity-60">
            {reports.length >= 2 ? 'Select any 2 reports to generate a side-by-side progression analysis' : 'Upload at least 2 reports to unlock progress comparison'}
          </span>
        </div>

        {reports.length === 0 ? (
          <div className="p-12 text-center border-2 border-dashed border-[rgba(23,30,25,0.15)] rounded-2xl bg-gray-50/50">
            <FileText className="w-12 h-12 mx-auto opacity-30 mb-3" />
            <h3 className="text-lg font-bold">No saved reports in database yet</h3>
            <p className="text-sm opacity-60 mt-1 max-w-md mx-auto">
              Upload a routine blood or metabolic lab report to begin tracking your long-term health trajectory.
            </p>
            <Link to="/upload" className="btn-accent inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold mt-5">
              Upload First Report
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {reports.map((r) => {
              const isSelected = selectedIds.includes(r.id)
              const isUrgent = r.overall_severity === 'Urgent'
              const isAbnormal = r.overall_severity === 'Abnormal'
              const isBorderline = r.is_early_stage

              return (
                <div 
                  key={r.id}
                  onClick={() => handleSelectReport(r.id)}
                  className={`p-6 rounded-2xl border transition cursor-pointer relative shadow-sm ${
                    isSelected 
                      ? 'border-[#171e19] ring-2 ring-[#ffe17c] bg-white shadow-md' 
                      : 'border-[rgba(23,30,25,0.1)] bg-white hover:border-gray-400'
                  }`}
                >
                  <div className="flex justify-between items-start mb-3">
                    <span className="text-xs font-mono opacity-50 flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {r.upload_date.slice(0, 10)}
                    </span>
                    <button 
                      onClick={(e) => handleDelete(e, r.id)}
                      className="p-1 opacity-40 hover:opacity-100 hover:text-red-600 transition"
                      title="Delete report"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-gray-100 border border-gray-200 flex items-center justify-center font-bold text-lg text-[#171e19]">
                      {r.health_score}
                      <span className="text-[9px] opacity-40 block font-normal -mt-3.5">/100</span>
                    </div>
                    <div>
                      <h4 className="font-bold text-base leading-snug">{r.patient_name}</h4>
                      <small className="text-xs opacity-60 block truncate max-w-[190px]">{r.filename}</small>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-gray-100 space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="opacity-60">Primary Assessment:</span>
                      <span className="font-semibold">{r.primary_condition}</span>
                    </div>
                    <div className="flex justify-between items-center text-xs">
                      <span className="opacity-60">Clinical Stage:</span>
                      <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                        isUrgent ? 'bg-red-100 text-red-800' : 
                        isBorderline ? 'bg-amber-100 text-amber-800' : 
                        isAbnormal ? 'bg-orange-100 text-orange-800' : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {r.stage_name ? r.stage_name.split(':')[0] : r.overall_severity}
                      </span>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 flex justify-between items-center text-xs font-semibold">
                    <span className="text-xs opacity-50">
                      {r.total_biomarkers} markers ({r.abnormal_count} flagged)
                    </span>
                    <span className={`px-2 py-1 rounded text-[11px] font-bold ${isSelected ? 'bg-[#ffe17c] text-[#171e19]' : 'bg-gray-100 text-gray-600'}`}>
                      {isSelected ? '✓ Selected' : 'Click to Compare'}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Side-by-Side Comparison Dashboard */}
      {comparison && (
        <div className="mt-16 bg-[#171e19] text-white rounded-3xl p-8 lg:p-12 shadow-2xl border border-white/10">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-8 border-b border-white/10">
            <div>
              <span className="badge-tag !bg-white/10 !text-[#ffe17c] !border-[#ffe17c]/30">
                Longitudinal Report-to-Report Progress
              </span>
              <h2 className="disp text-3xl lg:text-4xl mt-3 text-white">
                {comparison.headline}
              </h2>
              <p className="mt-2 text-sm text-[#b7c6c2]">
                Comparing baseline ({comparison.date_old}) against follow-up ({comparison.date_new}) for <b className="text-white">{comparison.patient_name}</b>.
              </p>
            </div>

            {/* Score Progression Badge */}
            <div className="flex items-center gap-4 bg-white/5 border border-white/10 p-5 rounded-2xl">
              <div>
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2] block">Baseline Score</span>
                <span className="font-mono text-3xl font-bold text-gray-300">{comparison.score_old}</span>
              </div>
              <ArrowRight className="w-5 h-5 text-[#ffe17c]" />
              <div>
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2] block">Current Score</span>
                <span className="font-mono text-3xl font-bold text-white">{comparison.score_new}</span>
              </div>
              <div className="ml-2 pl-4 border-l border-white/15 text-right">
                <span className={`text-xs uppercase font-bold block ${comparison.score_delta >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                  {comparison.score_delta >= 0 ? `+${comparison.score_delta} pts` : `${comparison.score_delta} pts`}
                </span>
                <span className="text-[10px] text-[#b7c6c2]">Net Progress</span>
              </div>
            </div>
          </div>

          {/* Quick Metrics Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
            <div className="p-5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <div>
                <b className="font-mono text-3xl text-emerald-400">{comparison.improved_count}</b>
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2] block mt-1">Biomarkers Improved</span>
              </div>
              <TrendingUp className="w-8 h-8 text-emerald-400 opacity-80" />
            </div>
            <div className="p-5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <div>
                <b className="font-mono text-3xl text-[#ffe17c]">{comparison.stable_count}</b>
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2] block mt-1">Holding Steady</span>
              </div>
              <Minus className="w-8 h-8 text-[#ffe17c] opacity-80" />
            </div>
            <div className="p-5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <div>
                <b className="font-mono text-3xl text-red-400">{comparison.worsened_count}</b>
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2] block mt-1">Requiring Focus</span>
              </div>
              <TrendingDown className="w-8 h-8 text-red-400 opacity-80" />
            </div>
          </div>

          {/* Biomarker Trajectory Table */}
          <div className="mt-10 bg-white/5 border border-white/10 rounded-2xl overflow-hidden">
            <div className="px-6 py-4 bg-white/5 border-b border-white/10 flex justify-between items-center">
              <h3 className="font-bold text-sm text-white tracking-wide uppercase">Parameter-by-Parameter Trajectory</h3>
              <span className="text-xs text-[#b7c6c2]">{comparison.deltas.length} biomarkers evaluated</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-[11px] uppercase tracking-wider text-[#b7c6c2] bg-white/5 border-b border-white/10">
                  <tr>
                    <th className="py-3 px-6">Biomarker</th>
                    <th className="py-3 px-4">Baseline ({comparison.date_old})</th>
                    <th className="py-3 px-4">Follow-up ({comparison.date_new})</th>
                    <th className="py-3 px-4">Net Change (Δ)</th>
                    <th className="py-3 px-4">Trend Status</th>
                    <th className="py-3 px-6">Clinical Meaning</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {comparison.deltas.map((d, idx) => {
                    const isImp = d.trend === 'IMPROVED'
                    const isWor = d.trend === 'WORSENED'

                    return (
                      <tr key={idx} className="hover:bg-white/5 transition">
                        <td className="py-3.5 px-6 font-semibold text-white">
                          {d.parameter}
                        </td>
                        <td className="py-3.5 px-4 font-mono text-gray-300">
                          {d.old_value !== null ? `${d.old_value} ${d.unit}` : '—'}
                        </td>
                        <td className="py-3.5 px-4 font-mono text-white font-bold">
                          {d.new_value !== null ? `${d.new_value} ${d.unit}` : '—'}
                        </td>
                        <td className="py-3.5 px-4 font-mono text-xs">
                          <span className={isImp ? 'text-emerald-400 font-bold' : isWor ? 'text-red-400 font-bold' : 'text-gray-400'}>
                            {d.diff} ({d.pct_change})
                          </span>
                        </td>
                        <td className="py-3.5 px-4">
                          <span className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider inline-flex items-center gap-1 ${
                            isImp ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' :
                            isWor ? 'bg-red-500/20 text-red-300 border border-red-500/30' :
                            'bg-gray-500/20 text-gray-300 border border-gray-500/30'
                          }`}>
                            {isImp ? <TrendingUp className="w-3 h-3" /> : isWor ? <TrendingDown className="w-3 h-3" /> : <Minus className="w-3 h-3" />}
                            {d.trend}
                          </span>
                        </td>
                        <td className="py-3.5 px-6 text-xs text-[#b7c6c2]">
                          {d.clinical_note}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Personalized "What To Do Next" Section */}
          <div className="mt-8 p-8 rounded-2xl bg-[#ffe17c] text-[#171e19]">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-5 h-5 text-[#171e19]" />
              <h3 className="font-bold text-lg uppercase tracking-wide">
                Personalized Clinical Next Steps Based on Trajectory
              </h3>
            </div>
            <div className="space-y-2.5 mt-4">
              {comparison.what_to_do_next.map((step, i) => (
                <div key={i} className="flex items-start gap-3 text-sm leading-relaxed">
                  <CheckCircle2 className="w-4 h-4 text-[#171e19] flex-shrink-0 mt-1" />
                  <span>{step}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
