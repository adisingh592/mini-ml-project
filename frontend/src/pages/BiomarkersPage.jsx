import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { 
  BookOpen, Search, Filter, Apple, Activity, Heart, ShieldCheck, 
  AlertCircle, Droplets, ArrowRight, Sparkles, CheckCircle2 
} from 'lucide-react'

export default function BiomarkersPage() {
  const { fetchBiomarkerEncyclopedia } = useApp()
  const [encyclopedia, setEncyclopedia] = useState({})
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchBiomarkerEncyclopedia()
        setEncyclopedia(data)
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

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto min-h-screen">
      <div className="pb-8 border-b border-[rgba(23,30,25,0.1)]">
        <span className="badge-tag">Medical Literacy &amp; Reference Guide</span>
        <h1 className="disp text-[clamp(2.8rem,6vw,4.5rem)] mt-3">
          Biomarker <span className="hl">Encyclopedia</span>
        </h1>
        <p className="mt-2 text-base opacity-70 max-w-2xl">
          Understand your routine blood test results without confusing medical jargon. Learn what each parameter does for your body, reference ranges, and natural daily ways (fruits, diet, exercise) to maintain healthy levels before disease develops.
        </p>

        {/* Search & Category Filter */}
        <div className="mt-8 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="relative w-full md:w-96">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 opacity-40" />
            <input 
              type="text"
              placeholder="Search WBC, Creatinine, Glucose, Hemoglobin..."
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
                    ? 'bg-[#171e19] text-white' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {loading ? (
        <div className="py-20 text-center">
          <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm opacity-60">Loading clinical encyclopedia...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-10">
          {filtered.map((b, idx) => (
            <div 
              key={idx}
              className="bg-white border border-[rgba(23,30,25,0.1)] rounded-2xl p-7 shadow-sm hover:shadow-md transition flex flex-col justify-between"
            >
              <div>
                <div className="flex justify-between items-start mb-3">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-md">
                    {b.category}
                  </span>
                  <span className="font-mono text-xs font-bold bg-gray-100 px-2.5 py-1 rounded text-gray-700">
                    Normal: {b.optimal_range}
                  </span>
                </div>

                <h3 className="text-xl font-bold text-[#171e19]">{b.display_name}</h3>
                
                {/* Physiological Function */}
                <div className="mt-4 p-4 rounded-xl bg-gray-50 border border-gray-100">
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500 block mb-1">
                    Function in Human Body:
                  </span>
                  <p className="text-sm text-gray-700 leading-relaxed">
                    {b.importance}
                  </p>
                </div>

                {/* Routine Checkup Guidance */}
                <div className="mt-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500 block mb-1">
                    Routine Checkup Guidance:
                  </span>
                  <p className="text-xs text-gray-600 leading-relaxed">
                    {b.early_warning}
                  </p>
                </div>

                {/* Recommended Fruits */}
                {b.how_to_control?.recommended_fruits && (
                  <div className="mt-5 pt-4 border-t border-gray-100">
                    <span className="text-xs font-bold uppercase tracking-wider text-[#171e19] flex items-center gap-1.5 mb-2.5">
                      <Apple className="w-4 h-4 text-emerald-600" />
                      Recommended Fruits to Balance This Biomarker:
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
              </div>

              {/* Daily Control Footer */}
              <div className="mt-6 pt-4 border-t border-gray-100 flex justify-between items-center text-xs text-gray-500">
                <span className="flex items-center gap-1">
                  <Activity className="w-3.5 h-3.5 text-blue-600" />
                  {b.how_to_control?.exercises?.slice(0, 40)}...
                </span>
                <span className="font-semibold text-[#171e19]">100% Reversible Early</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
