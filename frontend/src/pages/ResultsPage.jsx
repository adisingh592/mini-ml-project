import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { 
  ArrowRight, AlertTriangle, ShieldCheck, Activity, AlertCircle, 
  Sparkles, Apple, Save, History, CheckCircle2 
} from 'lucide-react'

export default function ResultsPage() {
  const navigate = useNavigate()
  const { analysis, loading, saveCurrentReport } = useApp()
  const [patientName, setPatientName] = useState('Self Routine Checkup')
  const [saving, setSaving] = useState(false)
  const [savedId, setSavedId] = useState(null)

  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  const findings = analysis.findings || []
  const conditions = analysis.conditions || []
  const modelResults = (analysis.model_results || []).filter(m => m.status === 'ran')

  const totalParams = findings.length || Object.keys(analysis.extracted_values || {}).length
  const aboveRange = findings.filter(f => f.status === 'ABNORMAL' || f.status === 'URGENT' || f.status === 'BORDERLINE').length
  const inRange = Math.max(0, totalParams - aboveRange)

  const primary = conditions.find(c => c.severity > 0) || conditions[0]
  const conditionName = primary?.condition || '6-Disease Panel'
  const flagged = findings.filter(f => f.status !== 'NORMAL')

  const isUrgent = analysis.overall_severity === 'Urgent'
  const isAbnormal = analysis.overall_severity === 'Abnormal'
  const staging = analysis.staging || {}
  const primaryStage = staging.primary_stage || {}
  const healthScore = analysis.health_score || (aboveRange > 0 ? 72 : 96)
  const paramBreakdowns = analysis.parameter_breakdowns || {}

  async function handleSave() {
    setSaving(true)
    try {
      const res = await saveCurrentReport(patientName, 45, 'Unspecified')
      setSavedId(res.report_id)
    } catch (err) {
      alert('Save failed: ' + err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto min-h-screen">
      <span className="badge-tag">Step 3 of 3 · Screening &amp; Preventive Action</span>
      
      <h1 className="disp text-[clamp(3.4rem,9vw,6.5rem)] mt-6">
        Screening <span className="hl">results</span>
      </h1>
      <p className="mt-4 text-lg opacity-70 max-w-xl">
        Early-stage assessment, diagnostic confidence, and practical daily actions (diet, fruits, and exercises) to halt disease progression.
      </p>

      {/* Early Stage Warning Alert Banner */}
      {staging.has_early_warning && (
        <div className="mt-8 p-6 bg-gradient-to-r from-amber-500/10 via-[#ffe17c]/25 to-amber-500/10 border-2 border-amber-400 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-start gap-3.5">
            <div className="p-2.5 rounded-xl bg-amber-400 text-[#171e19] flex-shrink-0 mt-0.5">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-900 bg-amber-200/90 px-2.5 py-0.5 rounded-md">
                Critical Early Detection Window · Reversible Stage
              </span>
              <h3 className="font-bold text-lg text-[#171e19] mt-1">
                {primaryStage.stage_name}
              </h3>
              <p className="text-xs text-gray-700 mt-1 max-w-2xl leading-relaxed">
                {staging.early_stage_alert}
              </p>
            </div>
          </div>
          <div className="flex gap-2 self-end md:self-center">
            <Link 
              to="/guidance" 
              className="btn-accent whitespace-nowrap text-xs font-bold px-4 py-2.5 rounded-xl flex items-center gap-1.5"
            >
              See Diet &amp; Fruits <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      )}

      {/* 4 Metric Tiles */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-5 mt-10">
        <div className="p-6 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-white shadow-sm">
          <b className="disp text-[clamp(3.5rem,5vw,5rem)] block text-[#171e19]">{healthScore}</b>
          <span className="text-xs font-bold uppercase tracking-[0.16em] opacity-60">Health Index (/100)</span>
        </div>
        <div className="p-6 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-white shadow-sm">
          <b className="disp text-[clamp(3.5rem,5vw,5rem)] block text-[#171e19]">{totalParams}</b>
          <span className="text-xs font-bold uppercase tracking-[0.16em] opacity-60">Biomarkers Measured</span>
        </div>
        <div className={`p-6 border rounded-2xl shadow-sm ${aboveRange > 0 ? 'bg-[#ffe17c] text-[#171e19] border-transparent' : 'bg-white border-[rgba(23,30,25,0.1)]'}`}>
          <b className="disp text-[clamp(3.5rem,5vw,5rem)] block">{aboveRange}</b>
          <span className="text-xs font-bold uppercase tracking-[0.16em] opacity-80">Outside Standard Range</span>
        </div>
        <div className="p-6 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-white shadow-sm">
          <b className="disp text-[clamp(3.5rem,5vw,5rem)] block text-[#171e19]">{inRange}</b>
          <span className="text-xs font-bold uppercase tracking-[0.16em] opacity-60">Within Reference Limits</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        {/* Left Dark Outcome Panel */}
        <div className="bg-[#171e19] text-white border border-[rgba(183,198,194,0.1)] rounded-2xl p-8 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <span className={`badge-tag !bg-transparent ${isUrgent ? '!text-red-400 !border-red-400/40' : isAbnormal ? '!text-[#ffe17c] !border-[#ffe17c]/40' : '!text-emerald-400 !border-emerald-400/40'}`}>
                {primaryStage.stage_name || analysis.decision}
              </span>
            </div>

            <h3 className="disp text-3xl mt-2 leading-tight">
              {conditionName}: {aboveRange > 0 ? 'Precautionary Steps Recommended' : 'Within Normal Baseline'}
            </h3>
            
            <p className="mt-4 text-sm text-[#b7c6c2] leading-relaxed">
              {primaryStage.explanation || analysis.recommended_action}
            </p>

            {/* Daily Precautionary Advice */}
            {primaryStage.early_precaution && (
              <div className="mt-5 p-4 rounded-xl bg-white/5 border border-white/10">
                <span className="text-[11px] uppercase font-bold text-[#ffe17c] block mb-1">
                  Daily Precautions to Prevent Progression:
                </span>
                <p className="text-xs text-gray-300 leading-relaxed">
                  {primaryStage.early_precaution}
                </p>
              </div>
            )}

            {/* Model Breakdown */}
            {modelResults.length > 0 && (
              <div className="mt-6 pt-5 border-t border-[rgba(183,198,194,0.15)] space-y-2.5">
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2]/80 font-bold block">
                  Trained Model Inferences:
                </span>
                <div className="space-y-2 max-h-[160px] overflow-y-auto pr-1">
                  {modelResults.map((m, idx) => (
                    <div key={idx} className="bg-white/5 border border-white/10 p-2.5 rounded-lg flex justify-between items-center text-xs">
                      <div>
                        <span className="text-white font-medium block">{m.label}</span>
                        <span className="text-[10px] text-[#b7c6c2]">Features: {m.features_used} · Category: {m.category || 'Tabular'}</span>
                      </div>
                      <div className="text-right">
                        <span className={`font-mono font-bold text-sm ${m.probability >= 50 ? 'text-[#ffe17c]' : 'text-emerald-400'}`}>
                          {m.probability}%
                        </span>
                        <span className="block text-[10px] text-[#b7c6c2]">{m.probability >= 50 ? 'Elevated' : 'Low Risk'}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Action Footer */}
          <div className="flex flex-wrap gap-3 mt-8 items-center pt-4 border-t border-white/10">
            <Link to="/guidance" className="btn-y flex items-center gap-2">
              See Clinical Guidance &amp; Diet <ArrowRight size={16} />
            </Link>
            <Link to="/tracker" className="btn-o flex items-center gap-2 text-xs">
              <History className="w-3.5 h-3.5" />
              Health Tracker
            </Link>
            <Link to="/biomarkers" className="btn-ghost text-xs">
              Biomarker Guide
            </Link>
          </div>
        </div>

        {/* Right Flagged Values & Recommended Fruits Panel */}
        <div className="bg-white border border-[rgba(23,30,25,0.1)] rounded-2xl p-8 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center pb-3 border-b border-[rgba(23,30,25,0.1)]">
              <span className="text-xs font-bold uppercase tracking-wider opacity-60">
                Flagged Biomarkers &amp; Fruit Diet ({flagged.length})
              </span>
              <span className="text-xs font-mono opacity-50">Reference Targets</span>
            </div>

            <div className="divide-y divide-[rgba(23,30,25,0.08)] max-h-[380px] overflow-y-auto pr-2">
              {flagged.length > 0 ? (
                flagged.map((f, i) => {
                  const isUrgent = f.status === 'URGENT'
                  const rawKey = Object.keys(analysis.extracted_values || {}).find(k => k.toLowerCase().includes(f.parameter.toLowerCase().slice(0, 4))) || f.parameter.toLowerCase().replace(/ /g, '_')
                  const breakdown = paramBreakdowns[rawKey] || {}

                  return (
                    <div key={i} className="py-4 text-sm">
                      <div className="flex justify-between items-center">
                        <b className="text-[#171e19]">{f.parameter}</b>
                        <span className="font-mono text-xs flex items-center gap-2">
                          <b className="text-sm">{f.value} {f.unit}</b>
                          <span className={isUrgent ? 'bg-red-600 text-white px-2 py-0.5 rounded text-[10px] font-bold' : 'chip-hi'}>
                            {f.status}
                          </span>
                        </span>
                      </div>
                      <p className="text-xs opacity-70 mt-1 leading-relaxed">{f.message}</p>
                      
                      {/* Fruits Pill */}
                      {breakdown.recommended_fruits && (
                        <div className="mt-2 flex items-center gap-1.5 flex-wrap">
                          <Apple className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
                          <span className="text-[11px] font-bold text-emerald-800">Fruits:</span>
                          <span className="text-[11px] text-gray-600 truncate max-w-sm">
                            {breakdown.recommended_fruits[0]}
                          </span>
                        </div>
                      )}
                    </div>
                  )
                })
              ) : (
                <div className="py-12 text-center text-sm opacity-60">
                  <ShieldCheck size={36} className="mx-auto text-emerald-500 mb-2" />
                  All extracted laboratory biomarkers are within normal physiological bounds.
                </div>
              )}
            </div>
          </div>

          {/* Save to History Card */}
          <div className="mt-6 pt-5 border-t border-gray-100 bg-gray-50/70 -mx-8 -mb-8 p-6 rounded-b-2xl">
            <span className="text-xs font-bold uppercase tracking-wider opacity-70 block mb-2">
              Save Report to Track Future Routine Checkups
            </span>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
                placeholder="Patient / Profile Name"
                className="flex-1 px-3 py-2 text-xs border border-gray-200 rounded-xl bg-white"
              />
              <button 
                onClick={handleSave}
                disabled={saving || savedId}
                className="px-4 py-2 bg-[#171e19] text-white rounded-xl text-xs font-bold hover:bg-black transition flex items-center gap-1.5"
              >
                <Save className="w-3.5 h-3.5" />
                {savedId ? 'Saved ✓' : saving ? 'Saving...' : 'Save to Tracker'}
              </button>
            </div>
            {savedId && (
              <p className="text-[11px] text-emerald-700 mt-2 font-medium flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Report saved! <Link to="/tracker" className="underline font-bold">Open Health Tracker &amp; Compare Reports &rarr;</Link>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
