import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { 
  BookOpen, Search, Filter, Apple, Activity, Heart, ShieldCheck, 
  AlertCircle, Droplets, ArrowRight, Sparkles, CheckCircle2,
  TrendingUp, TrendingDown, Check, Sliders, Info, HelpCircle
} from 'lucide-react'

export default function BiomarkersPage() {
  const { fetchBiomarkerEncyclopedia } = useApp()
  const [encyclopedia, setEncyclopedia] = useState({})
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')

  // Top Interactive Comparison Calculator State
  const [calculatorKey, setCalculatorKey] = useState('fasting_glucose')
  const [calculatorValue, setCalculatorValue] = useState(115)

  // Card-level test values map: { [key]: value }
  const [cardTestValues, setCardTestValues] = useState({})

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchBiomarkerEncyclopedia()
        setEncyclopedia(data)
        // Initialize default test values
        const defaults = {}
        Object.values(data).forEach(b => {
          defaults[b.key] = b.reference_max ? Math.round(b.reference_max * 1.15 * 10) / 10 : 100
        })
        setCardTestValues(defaults)
      } catch (err) {
        console.error('Failed to load encyclopedia:', err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const biomarkers = Object.values(encyclopedia)
  const categories = ['All', ...new Set(biomarkers.map(b => b.category))]

  const filtered = biomarkers.filter(b => {
    const matchesSearch = 
      b.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      b.key.toLowerCase().includes(searchTerm.toLowerCase()) ||
      b.importance.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCat = selectedCategory === 'All' || b.category === selectedCategory
    return matchesSearch && matchesCat
  })

  // Function to compute difference and clinical meaning for any biomarker reading
  function evaluateBiomarkerDifference(biomarker, val) {
    if (!biomarker) return null
    const num = parseFloat(val)
    if (isNaN(num)) return null

    const min = biomarker.reference_min ?? 0
    const max = biomarker.reference_max ?? 100
    const unit = biomarker.unit || ''

    if (num < min) {
      const delta = Math.round((min - num) * 10) / 10
      const pct = min > 0 ? Math.round((delta / min) * 100) : 0
      return {
        status: 'LOW',
        label: `Low (-${delta} ${unit} below normal)`,
        badgeClass: 'bg-blue-100 text-blue-900 border-blue-200',
        barPercent: Math.max(8, Math.min(30, (num / min) * 30)),
        importanceOfDiff: biomarker.low_explanation || 'Level is reduced below healthy physiological requirements.',
        deltaText: `-${delta} ${unit} (-${pct}%)`,
        isAbnormal: true,
      }
    } else if (num > max) {
      const delta = Math.round((num - max) * 10) / 10
      const pct = max > 0 ? Math.round((delta / max) * 100) : 0
      return {
        status: 'HIGH',
        label: `High (+${delta} ${unit} above normal)`,
        badgeClass: 'bg-amber-100 text-amber-950 border-amber-300 font-bold',
        barPercent: Math.min(100, 70 + Math.min(30, ((num - max) / max) * 30)),
        importanceOfDiff: biomarker.high_explanation || 'Level is elevated above safe clinical thresholds.',
        deltaText: `+${delta} ${unit} (+${pct}%)`,
        isAbnormal: true,
      }
    } else {
      const span = max - min || 1
      const normalizedInBand = Math.round(35 + ((num - min) / span) * 30)
      return {
        status: 'OPTIMAL',
        label: `Normal (${num} ${unit} within healthy range)`,
        badgeClass: 'bg-emerald-100 text-emerald-900 border-emerald-200 font-bold',
        barPercent: normalizedInBand,
        importanceOfDiff: 'Reading is within optimal physiological limits. Normal cell function and organ health are maintained.',
        deltaText: 'Within Normal Bounds (0 delta)',
        isAbnormal: false,
      }
    }
  }

  const activeCalcBiomarker = encyclopedia[calculatorKey] || biomarkers[0]
  const activeEvaluation = evaluateBiomarkerDifference(activeCalcBiomarker, calculatorValue)

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto min-h-screen">
      {/* ── Page Header ── */}
      <div className="pb-8 border-b border-[rgba(23,30,25,0.1)]">
        <span className="badge-tag">Patient Medical Literacy &amp; Reference Guide</span>
        <h1 className="disp text-[clamp(2.8rem,6vw,4.5rem)] mt-3">
          Biomarker Reference <span className="hl">&amp; Range Comparison</span>
        </h1>
        <p className="mt-2 text-base opacity-75 max-w-3xl leading-relaxed">
          Demystifying routine lab tests. Compare all your biomarkers against standard normal values, understand the exact biological importance of being low or high, and discover targeted fruits, diet, and exercises to naturally normalize readings before disease escalates.
        </p>

        {/* ── TOP SECTION: Interactive Biomarker Comparison & Difference Calculator ── */}
        {activeCalcBiomarker && (
          <div className="mt-10 p-6 md:p-8 bg-[#171e19] text-white rounded-3xl shadow-xl border border-white/10 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-80 h-80 bg-[#ffe17c]/5 rounded-full blur-3xl pointer-events-none" />

            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
              <div>
                <span className="text-[11px] font-mono uppercase tracking-wider text-[#ffe17c] font-bold flex items-center gap-1.5">
                  <Sliders size={14} />
                  Live Value Tester &amp; Difference Calculator
                </span>
                <h2 className="disp text-2xl md:text-3xl mt-1 text-white">
                  Compare Your Lab Value with Normal Bounds
                </h2>
              </div>

              {/* Biomarker Selector Dropdown */}
              <div className="flex items-center gap-2">
                <label className="text-xs text-gray-300 font-semibold whitespace-nowrap">
                  Select Biomarker:
                </label>
                <select
                  value={calculatorKey}
                  onChange={(e) => {
                    setCalculatorKey(e.target.value)
                    const b = encyclopedia[e.target.value]
                    if (b) setCalculatorValue(b.reference_max ? Math.round(b.reference_max * 1.15 * 10) / 10 : 100)
                  }}
                  className="bg-white/10 text-[#ffe17c] font-bold border border-white/20 rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#ffe17c]"
                >
                  {biomarkers.map((b) => (
                    <option key={b.key} value={b.key} className="bg-[#171e19] text-white">
                      {b.display_name} ({b.unit})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Calculator Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-6 items-start">
              {/* Left Input & Visual Range Spectrum */}
              <div className="lg:col-span-6 space-y-5">
                <div>
                  <div className="flex justify-between items-baseline mb-2">
                    <span className="text-sm font-bold text-gray-200">
                      Enter Measured Reading:
                    </span>
                    <span className="text-xs font-mono text-[#ffe17c]">
                      Standard Normal: <b className="text-white">{activeCalcBiomarker.optimal_range}</b>
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    <input
                      type="number"
                      step="any"
                      value={calculatorValue}
                      onChange={(e) => setCalculatorValue(e.target.value)}
                      className="bg-white/10 border-2 border-[#ffe17c]/50 rounded-2xl px-5 py-3 text-2xl font-bold font-mono text-white focus:outline-none focus:border-[#ffe17c] w-48 shadow-inner"
                    />
                    <span className="text-base font-bold font-mono text-gray-300">
                      {activeCalcBiomarker.unit}
                    </span>
                  </div>

                  {/* Quick Preset Buttons */}
                  <div className="flex flex-wrap gap-2 mt-3 text-xs font-mono">
                    <span className="text-gray-400 self-center mr-1">Presets:</span>
                    <button
                      type="button"
                      onClick={() => setCalculatorValue(activeCalcBiomarker.reference_min)}
                      className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-blue-300 transition"
                    >
                      Low Bound ({activeCalcBiomarker.reference_min})
                    </button>
                    <button
                      type="button"
                      onClick={() => setCalculatorValue(Math.round(((activeCalcBiomarker.reference_min + activeCalcBiomarker.reference_max) / 2) * 10) / 10)}
                      className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-emerald-300 transition"
                    >
                      Optimal ({Math.round(((activeCalcBiomarker.reference_min + activeCalcBiomarker.reference_max) / 2) * 10) / 10})
                    </button>
                    <button
                      type="button"
                      onClick={() => setCalculatorValue(Math.round(activeCalcBiomarker.reference_max * 1.25 * 10) / 10)}
                      className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-amber-300 transition"
                    >
                      Elevated ({Math.round(activeCalcBiomarker.reference_max * 1.25 * 10) / 10})
                    </button>
                  </div>
                </div>

                {/* Visual Range Spectrum Meter */}
                <div className="p-5 rounded-2xl bg-white/5 border border-white/10">
                  <div className="flex justify-between items-center text-xs font-mono text-gray-400 mb-2">
                    <span>Low (&lt; {activeCalcBiomarker.reference_min})</span>
                    <span className="text-emerald-400 font-bold">Optimal Normal Zone</span>
                    <span>High (&gt; {activeCalcBiomarker.reference_max})</span>
                  </div>

                  {/* Range Bar */}
                  <div className="relative h-4 rounded-full overflow-hidden bg-white/10 flex">
                    <div className="w-[30%] bg-blue-500/40" title="Low Range" />
                    <div className="w-[40%] bg-emerald-500/70" title="Normal Range" />
                    <div className="w-[30%] bg-rose-500/60" title="High Range" />
                  </div>

                  {/* User Pin on Bar */}
                  {activeEvaluation && (
                    <div className="relative h-6 mt-1">
                      <div
                        className="absolute -top-1 -translate-x-1/2 flex flex-col items-center transition-all duration-300"
                        style={{ left: `${activeEvaluation.barPercent}%` }}
                      >
                        <div className="w-3 h-3 rotate-45 bg-[#ffe17c] border border-[#171e19]" />
                        <span className="text-[10px] font-mono font-bold text-[#ffe17c] mt-0.5 whitespace-nowrap">
                          Your Value: {calculatorValue}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Right: Difference Evaluation & Health Importance */}
              <div className="lg:col-span-6 bg-white/5 p-6 rounded-2xl border border-white/10 space-y-4">
                {activeEvaluation && (
                  <>
                    <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-white/10">
                      <div>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400 block">
                          Biomarker Difference Status:
                        </span>
                        <div className="flex items-center gap-2 mt-1">
                          <span className={`px-3 py-1 rounded-full text-xs border font-mono ${activeEvaluation.badgeClass}`}>
                            {activeEvaluation.status}: {activeEvaluation.deltaText}
                          </span>
                        </div>
                      </div>

                      <div className="text-right">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400 block">
                          Clinical Recovery:
                        </span>
                        <span className="text-xs font-bold text-emerald-400">
                          100% Reversible Early
                        </span>
                      </div>
                    </div>

                    {/* Importance of This Difference on the Body */}
                    <div>
                      <h4 className="text-xs font-bold uppercase tracking-wider text-[#ffe17c] flex items-center gap-1.5 mb-1.5">
                        <Info size={14} />
                        Importance of This Difference on Your Body:
                      </h4>
                      <p className="text-sm text-gray-200 leading-relaxed font-normal bg-black/30 p-3.5 rounded-xl border border-white/10">
                        {activeEvaluation.importanceOfDiff}
                      </p>
                    </div>

                    {/* Actionable Fruits to Control this Difference */}
                    {activeCalcBiomarker.how_to_control?.recommended_fruits && (
                      <div className="pt-2">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-300 flex items-center gap-1.5 mb-1.5">
                          <Apple size={14} />
                          Target Fruits to Bring Difference Back to Normal:
                        </h4>
                        <div className="space-y-1.5 text-xs text-gray-300">
                          {activeCalcBiomarker.how_to_control.recommended_fruits.slice(0, 2).map((fr, fIdx) => (
                            <div key={fIdx} className="flex items-start gap-2">
                              <CheckCircle2 size={13} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                              <span>{fr}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Routine Walking / Exercise */}
                    {activeCalcBiomarker.how_to_control?.exercises && (
                      <div className="pt-2 border-t border-white/10 flex items-center gap-2 text-xs text-gray-300">
                        <Activity size={14} className="text-amber-300 flex-shrink-0" />
                        <span><b className="text-white">Daily Habit:</b> {activeCalcBiomarker.how_to_control.exercises}</span>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ── Search & Category Filter ── */}
        <div className="mt-12 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="relative w-full md:w-96">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 opacity-40" />
            <input 
              type="text"
              placeholder="Search by name, key, or organ (e.g. Glucose, Creatinine, Hb, WBC)..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[rgba(23,30,25,0.15)] bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#ffe17c]"
            />
          </div>

          <div className="flex gap-2 overflow-x-auto w-full md:w-auto pb-1">
            {categories.map((cat, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition ${
                  selectedCategory === cat 
                    ? 'bg-[#171e19] text-white shadow-sm' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ── Encyclopedia Grid Cards ── */}
      {loading ? (
        <div className="py-20 text-center">
          <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm opacity-60">Loading clinical biomarker encyclopedia...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-10">
          {filtered.map((b) => {
            const currentCardVal = cardTestValues[b.key] ?? b.reference_max
            const evalResult = evaluateBiomarkerDifference(b, currentCardVal)

            return (
              <div 
                key={b.key}
                className="bg-white border border-[rgba(23,30,25,0.12)] rounded-2xl p-7 shadow-sm hover:shadow-md transition flex flex-col justify-between"
              >
                <div>
                  {/* Category & Optimal Range Header */}
                  <div className="flex flex-wrap justify-between items-start gap-2 mb-3">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-md">
                      {b.category}
                    </span>
                    <span className="font-mono text-xs font-bold bg-[#171e19] text-[#ffe17c] px-3 py-1 rounded-full shadow-sm">
                      Normal Range: {b.optimal_range}
                    </span>
                  </div>

                  <h3 className="text-2xl font-bold text-[#171e19]">{b.display_name}</h3>
                  
                  {/* Function in Human Body */}
                  <div className="mt-4 p-4 rounded-xl bg-gray-50 border border-gray-100">
                    <span className="text-xs font-bold uppercase tracking-wider text-gray-500 block mb-1">
                      Function in Human Body:
                    </span>
                    <p className="text-sm text-gray-800 leading-relaxed">
                      {b.importance}
                    </p>
                  </div>

                  {/* ── IMPORTANCE OF DIFFERENCE (HIGH vs LOW) ── */}
                  <div className="mt-4 space-y-3">
                    <span className="text-xs font-bold uppercase tracking-wider text-[#171e19] block">
                      Importance of Difference (Abnormal Levels):
                    </span>

                    {/* High Level Impact */}
                    {b.high_explanation && (
                      <div className="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200/80 text-xs text-amber-950">
                        <div className="flex items-center gap-1.5 font-bold text-amber-900 mb-1">
                          <TrendingUp size={14} className="text-amber-700" />
                          <span>When Level is Above Normal (Elevation Difference):</span>
                        </div>
                        <p className="leading-relaxed opacity-90">
                          {b.high_explanation}
                        </p>
                      </div>
                    )}

                    {/* Low Level Impact */}
                    {b.low_explanation && (
                      <div className="p-3.5 rounded-xl bg-blue-50/70 border border-blue-200/80 text-xs text-blue-950">
                        <div className="flex items-center gap-1.5 font-bold text-blue-900 mb-1">
                          <TrendingDown size={14} className="text-blue-700" />
                          <span>When Level is Below Normal (Deficiency Difference):</span>
                        </div>
                        <p className="leading-relaxed opacity-90">
                          {b.low_explanation}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Routine Checkup Early Warning */}
                  {b.early_warning && (
                    <div className="mt-4 p-3 rounded-xl bg-emerald-50/60 border border-emerald-200 text-xs text-emerald-950">
                      <span className="font-bold text-emerald-900 block mb-0.5">
                        Routine Checkup Guidance &amp; Reversibility:
                      </span>
                      <p className="leading-relaxed opacity-90">
                        {b.early_warning}
                      </p>
                    </div>
                  )}

                  {/* ── Interactive Inline Test Box on Card ── */}
                  <div className="mt-5 p-4 rounded-xl bg-gray-50 border border-gray-200">
                    <div className="flex justify-between items-center text-xs mb-2">
                      <span className="font-bold text-[#171e19] flex items-center gap-1">
                        <Sliders size={13} />
                        Test Your Reading:
                      </span>
                      {evalResult && (
                        <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${evalResult.badgeClass}`}>
                          {evalResult.label}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <input
                        type="number"
                        step="any"
                        value={currentCardVal}
                        onChange={(e) => setCardTestValues({ ...cardTestValues, [b.key]: e.target.value })}
                        className="w-32 px-3 py-1.5 text-sm font-bold font-mono bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffe17c]"
                        placeholder="Enter value"
                      />
                      <span className="text-xs font-mono text-gray-500 font-semibold">{b.unit}</span>
                      <span className="text-[11px] text-gray-500 ml-auto">
                        Normal: {b.optimal_range}
                      </span>
                    </div>
                  </div>

                  {/* Recommended Fruits to Balance This Biomarker */}
                  {b.how_to_control?.recommended_fruits && (
                    <div className="mt-5 pt-4 border-t border-gray-100">
                      <span className="text-xs font-bold uppercase tracking-wider text-[#171e19] flex items-center gap-1.5 mb-2.5">
                        <Apple className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                        Target Fruits to Balance This Biomarker:
                      </span>
                      <div className="space-y-1.5">
                        {b.how_to_control.recommended_fruits.map((fr, fIdx) => (
                          <div key={fIdx} className="flex items-start gap-2 text-xs text-gray-700">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                            <span>{fr}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Dietary Action */}
                  {b.how_to_control?.diet_actions && (
                    <div className="mt-3 text-xs text-gray-600">
                      <span className="font-bold text-[#171e19] block mb-0.5">Dietary Adjustment:</span>
                      <p className="leading-relaxed">{b.how_to_control.diet_actions}</p>
                    </div>
                  )}
                </div>

                {/* Daily Control Footer */}
                <div className="mt-6 pt-4 border-t border-gray-100 flex flex-wrap justify-between items-center gap-2 text-xs text-gray-600">
                  <span className="flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5 text-blue-600 flex-shrink-0" />
                    <span><b>Exercise:</b> {b.how_to_control?.exercises?.slice(0, 48)}...</span>
                  </span>
                  <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    100% Reversible Early
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
