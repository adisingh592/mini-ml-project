import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { 
  Activity, ArrowRight, CheckCircle2, AlertTriangle, ShieldCheck, 
  Sparkles, Apple, Info, X, ChevronDown, ChevronUp, Save
} from 'lucide-react'

export default function AnalysisPage() {
  const navigate = useNavigate()
  const { analysis, uploadedFile, loading, saveCurrentReport } = useApp()
  const [selectedParam, setSelectedParam] = useState(null)
  const [saving, setSaving] = useState(false)
  const [savedId, setSavedId] = useState(null)
  const [patientName, setPatientName] = useState('Self Routine Checkup')

  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  const findings = analysis.findings || []
  const conditions = analysis.conditions || []
  const modelResults = (analysis.model_results || []).filter(m => m.status === 'ran')
  const topCondition = conditions.find(c => c.severity > 0) || conditions[0]
  const valuesCount = Object.keys(analysis.extracted_values || {}).length
  const staging = analysis.staging || {}
  const primaryStage = staging.primary_stage || {}
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
      <span className="badge-tag">Step 2 of 3 · Biomarker Parsing &amp; Early Staging</span>
      
      <h1 className="disp text-[clamp(3.4rem,9vw,6.5rem)] mt-6">
        Your report, <span className="hl">parsed</span>
      </h1>
      <p className="mt-4 text-lg opacity-70 max-w-xl">
        Extracted biomarkers evaluated against clinical reference ranges, early-stage disease windows, and machine learning models.
      </p>

      {/* Early Stage Warning Alert Banner */}
      {staging.has_early_warning && (
        <div className="mt-8 p-6 bg-gradient-to-r from-amber-500/10 via-[#ffe17c]/20 to-amber-500/10 border-2 border-amber-400/40 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start gap-3.5">
            <div className="p-2.5 rounded-xl bg-amber-400 text-[#171e19] flex-shrink-0 mt-0.5">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-900 bg-amber-200/80 px-2.5 py-0.5 rounded-md">
                Critical Early Detection Window · 100% Reversible
              </span>
              <h3 className="font-bold text-lg text-[#171e19] mt-1">
                {primaryStage.stage_name}
              </h3>
              <p className="text-xs text-gray-700 mt-1 max-w-2xl leading-relaxed">
                {staging.early_stage_alert}
              </p>
            </div>
          </div>
          <Link 
            to="/results" 
            className="btn-accent whitespace-nowrap text-xs font-bold px-4 py-2.5 rounded-xl flex items-center gap-1.5 self-end md:self-center"
          >
            View Prevention Plan <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      )}

      {/* Stepper */}
      <ol className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-8">
        <li className="p-5 border border-[rgba(23,30,25,0.1)] rounded-xl bg-white flex gap-3.5 items-center shadow-sm">
          <div className="w-3 h-3 rounded-full bg-[#ffe17c] ring-2 ring-[#171e19] flex-shrink-0" />
          <div>
            <b className="block text-sm font-bold">Document Ingested</b>
            <small className="text-xs opacity-60 truncate block max-w-[200px]">{uploadedFile?.name || 'Medical Report'}</small>
          </div>
        </li>
        <li className="p-5 border border-[rgba(23,30,25,0.1)] rounded-xl bg-white flex gap-3.5 items-center shadow-sm">
          <div className="w-3 h-3 rounded-full bg-[#ffe17c] ring-2 ring-[#171e19] flex-shrink-0" />
          <div>
            <b className="block text-sm font-bold">Biomarkers Read &amp; Staged</b>
            <small className="text-xs opacity-60">{findings.length || valuesCount} laboratory tests analyzed</small>
          </div>
        </li>
        <li className="p-5 border border-[rgba(23,30,25,0.1)] rounded-xl bg-white flex gap-3.5 items-center shadow-sm">
          <div className="w-3 h-3 rounded-full bg-[#ffe17c] ring-2 ring-[#171e19] flex-shrink-0" />
          <div>
            <b className="block text-sm font-bold">Meta-Classifier Active</b>
            <small className="text-xs opacity-60">
              {modelResults.length} of 6 models activated
            </small>
          </div>
        </li>
      </ol>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        {/* Left: Extracted Parameters Table with Click-to-Learn */}
        <div className="bg-white border border-[rgba(23,30,25,0.1)] rounded-2xl p-8 shadow-sm">
          <div className="flex justify-between items-center pb-3 border-b border-[rgba(23,30,25,0.1)]">
            <span className="text-xs font-bold uppercase tracking-wider opacity-60">
              Extracted Parameters (Click any parameter to understand &amp; control)
            </span>
            <span className="text-xs font-mono opacity-50">{findings.length || valuesCount} markers</span>
          </div>

          <div className="divide-y divide-[rgba(23,30,25,0.08)] max-h-[480px] overflow-y-auto pr-2">
            {findings.length > 0 ? (
              findings.map((f, i) => {
                const isUrgent = f.status === 'URGENT'
                const isAbnormal = f.status === 'ABNORMAL' || f.status === 'BORDERLINE'
                const rawKey = Object.keys(analysis.extracted_values || {}).find(k => k.toLowerCase().includes(f.parameter.toLowerCase().slice(0, 4))) || f.parameter.toLowerCase().replace(/ /g, '_')
                const breakdown = paramBreakdowns[rawKey] || {}

                return (
                  <div 
                    key={i} 
                    onClick={() => setSelectedParam(breakdown.parameter ? breakdown : {
                      parameter: f.parameter,
                      current_value: f.value,
                      unit: f.unit,
                      status: f.status,
                      importance: f.message || "Monitored clinical indicator.",
                      clinical_meaning: f.message,
                      recommended_fruits: ["Pomegranate", "Green Apples", "Berries"],
                      diet_actions: "Maintain balanced nutrition and consult standard clinical reference ranges.",
                      exercises: "Moderate daily 20-30 min walking.",
                      daily_precautions: "Hydrate well and track progress."
                    })}
                    className="py-3.5 text-sm hover:bg-gray-50 rounded-lg px-2 -mx-2 transition cursor-pointer flex justify-between items-center group"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-[#171e19] group-hover:text-blue-600 transition">
                          {f.parameter}
                        </span>
                        <Info className="w-3.5 h-3.5 opacity-30 group-hover:opacity-100 transition text-blue-600" />
                      </div>
                      <small className="text-[11px] opacity-50 font-mono">{f.condition}</small>
                    </div>
                    <span className="font-mono text-xs flex items-center gap-2">
                      <span className="font-bold">{f.value} {f.unit}</span>
                      <span className={isUrgent ? 'bg-red-600 text-white px-2 py-0.5 rounded text-[10px] font-bold' : isAbnormal ? 'chip-hi' : 'chip-ok'}>
                        {f.status}
                      </span>
                    </span>
                  </div>
                )
              })
            ) : (
              Object.entries(analysis.extracted_values || {}).map(([key, val], i) => {
                const breakdown = paramBreakdowns[key] || {}
                return (
                  <div 
                    key={i} 
                    onClick={() => setSelectedParam(breakdown.parameter ? breakdown : null)}
                    className="flex justify-between items-center py-3.5 text-sm hover:bg-gray-50 rounded-lg px-2 -mx-2 transition cursor-pointer"
                  >
                    <span className="font-medium text-[#171e19] capitalize">{key.replace(/_/g, ' ')}</span>
                    <span className="font-mono text-xs flex items-center gap-2">
                      {val}
                      <span className="chip-ok">MEASURED</span>
                    </span>
                  </div>
                )
              })
            )}
          </div>

          {/* Quick Save to Profile */}
          <div className="mt-6 pt-5 border-t border-[rgba(23,30,25,0.1)] flex flex-col sm:flex-row gap-3 items-center justify-between">
            <div className="w-full sm:w-auto flex-1">
              <input 
                type="text"
                placeholder="Patient Name (e.g. John Doe)"
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
                className="w-full px-3 py-1.5 border border-gray-200 rounded-lg text-xs"
              />
            </div>
            <button
              onClick={handleSave}
              disabled={saving || savedId}
              className="w-full sm:w-auto px-4 py-2 bg-[#171e19] text-white rounded-lg text-xs font-bold hover:bg-black transition flex items-center justify-center gap-1.5"
            >
              <Save className="w-3.5 h-3.5" />
              {savedId ? 'Saved to Tracker ✓' : saving ? 'Saving...' : 'Save to Health Tracker'}
            </button>
          </div>
        </div>

        {/* Right: Dark Routing & Early Prevention Panel */}
        <div className="bg-[#171e19] text-white border border-[rgba(183,198,194,0.1)] rounded-2xl p-8 flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-4">
              <span className="badge-tag !bg-transparent !text-[#ffe17c] !border-[#ffe17c]/30">
                Meta-Classifier Routing &amp; Severity
              </span>
              <span className="text-xs font-mono text-[#b7c6c2]">
                {modelResults.length} Models Ran
              </span>
            </div>

            <h3 className="disp text-3xl mb-3">
              {primaryStage.stage_name || (topCondition ? `${topCondition.condition}` : 'Multi-Disease')}
            </h3>
            
            <p className="text-sm text-[#b7c6c2] leading-relaxed">
              {primaryStage.explanation || 'Biomarkers extracted from your document were mapped to model feature vectors using adaptive median population baselines.'}
            </p>

            {primaryStage.early_precaution && (
              <div className="mt-5 p-4 rounded-xl bg-white/5 border border-white/10">
                <span className="text-[11px] uppercase font-bold text-[#ffe17c] block mb-1">
                  Daily Precautionary Actions:
                </span>
                <p className="text-xs text-gray-300 leading-relaxed">
                  {primaryStage.early_precaution}
                </p>
              </div>
            )}

            {/* Model Breakdown */}
            {modelResults.length > 0 && (
              <div className="mt-6 space-y-2 max-h-[180px] overflow-y-auto pr-1">
                {modelResults.map((m, idx) => (
                  <div key={idx} className="bg-white/5 border border-white/10 p-2.5 rounded-lg flex justify-between items-center text-xs">
                    <div>
                      <b className="text-white block font-medium">{m.label}</b>
                      <span className="text-[10px] text-[#b7c6c2]">
                        Coverage: {m.coverage}% · Category: {m.category || 'Tabular'}
                      </span>
                    </div>
                    <div className="text-right">
                      <span className={`font-mono font-bold ${m.positive ? 'text-[#ffe17c]' : 'text-emerald-400'}`}>
                        {m.probability}% Risk
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-3 mt-8 items-center pt-4 border-t border-white/10">
            <Link to="/results" className="btn-y flex items-center gap-2">
              Review Diagnostic Results <ArrowRight size={16} />
            </Link>
            <Link to="/tracker" className="btn-o flex items-center gap-2 text-xs">
              Open Health Tracker
            </Link>
          </div>
        </div>
      </div>

      {/* Parameter Details Modal */}
      {selectedParam && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-xl w-full p-8 shadow-2xl relative max-h-[90vh] overflow-y-auto border border-gray-100">
            <button 
              onClick={() => setSelectedParam(null)}
              className="absolute top-6 right-6 p-2 rounded-full hover:bg-gray-100 text-gray-500 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-md">
              {selectedParam.category || 'Clinical Biomarker'}
            </span>

            <h3 className="text-2xl font-bold text-[#171e19] mt-3">
              {selectedParam.parameter}
            </h3>
            
            <div className="mt-3 flex items-center gap-3">
              <span className="text-xl font-bold font-mono text-[#171e19]">
                {selectedParam.current_value} {selectedParam.unit}
              </span>
              <span className="text-xs px-2.5 py-1 rounded-full font-bold bg-[#ffe17c] text-[#171e19]">
                {selectedParam.status || 'ANALYZED'}
              </span>
            </div>

            {selectedParam.level_assessment && (
              <p className="text-xs font-mono text-gray-500 mt-1">
                {selectedParam.level_assessment}
              </p>
            )}

            {/* Importance to human body */}
            <div className="mt-6 p-4 rounded-xl bg-gray-50 border border-gray-100">
              <span className="text-xs font-bold uppercase tracking-wider text-gray-600 block mb-1">
                Why is this important to your body?
              </span>
              <p className="text-sm text-gray-700 leading-relaxed">
                {selectedParam.importance}
              </p>
            </div>

            {/* Recommended Fruits */}
            {selectedParam.recommended_fruits && (
              <div className="mt-5">
                <span className="text-xs font-bold uppercase tracking-wider text-[#171e19] flex items-center gap-1.5 mb-2">
                  <Apple className="w-4 h-4 text-emerald-600" />
                  Recommended Fruits to Control &amp; Balance:
                </span>
                <div className="space-y-1.5">
                  {selectedParam.recommended_fruits.map((fr, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-xs text-gray-700">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                      <span>{fr}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Daily Exercises & Diet */}
            <div className="mt-5 pt-4 border-t border-gray-100 space-y-3">
              {selectedParam.diet_actions && (
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500 block mb-0.5">
                    Dietary Focus:
                  </span>
                  <p className="text-xs text-gray-700 leading-relaxed">
                    {selectedParam.diet_actions}
                  </p>
                </div>
              )}
              {selectedParam.exercises && (
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500 block mb-0.5">
                    Physical Exercise:
                  </span>
                  <p className="text-xs text-gray-700 leading-relaxed">
                    {selectedParam.exercises}
                  </p>
                </div>
              )}
            </div>

            <button 
              onClick={() => setSelectedParam(null)}
              className="mt-6 w-full py-2.5 bg-[#171e19] text-white rounded-xl text-xs font-bold hover:bg-black transition"
            >
              Close Breakdown
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
