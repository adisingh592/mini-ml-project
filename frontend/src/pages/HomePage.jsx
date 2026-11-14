import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Check, X, Cpu, ArrowRight, Activity, ShieldCheck, Database } from 'lucide-react'

const CYCLING_MODELS = [
  {
    disease: 'Diabetes Mellitus',
    modelName: 'Random Forest Classifier (BRFSS)',
    parameters: ['Blood Glucose', 'HbA1c', 'BMI', 'Blood Pressure'],
    metric: '75.0% accuracy · 74.9% F1-score',
    barWidth: '75%',
    category: 'Endocrine & Metabolic',
  },
  {
    disease: 'Cerebrovascular Stroke',
    modelName: 'Random Forest Risk Ensemble',
    parameters: ['Systolic BP', 'Diastolic BP', 'Avg Glucose', 'BMI', 'Smoking Status'],
    metric: '80.5% accuracy · 85.7% F1-score',
    barWidth: '85%',
    category: 'Vascular / Neurological',
  },
  {
    disease: 'Heart Failure & Cardiac Risk',
    modelName: 'Random Forest Mortality Model',
    parameters: ['Ejection Fraction (LVEF)', 'CPK', 'Serum Creatinine', 'Blood Pressure'],
    metric: '85.0% accuracy · 84.3% F1-score',
    barWidth: '85%',
    category: 'Cardiovascular',
  },
  {
    disease: 'Chronic Kidney Disease (CKD)',
    modelName: 'Logistic Regression Classifier (Apollo)',
    parameters: ['Serum Creatinine', 'Blood Urea', 'Urine Albumin', 'eGFR Staging'],
    metric: '100.0% accuracy · 100.0% F1-score',
    barWidth: '100%',
    category: 'Renal System',
  },
  {
    disease: 'Hypertension / Maternal Vascular Risk',
    modelName: 'Random Forest Hemodynamics Model',
    parameters: ['Systolic BP', 'Diastolic BP', 'Blood Sugar (BS)', 'Heart Rate', 'Body Temp'],
    metric: '84.2% accuracy · 84.3% F1-score',
    barWidth: '84%',
    category: 'Vascular & Hemodynamics',
  },
  {
    disease: 'Clinical Anemia',
    modelName: 'Logistic Regression CBC Classifier',
    parameters: ['Hemoglobin (Hb)', 'Hematocrit (PCV)', 'RBC Count', 'Platelet Count'],
    metric: '100.0% accuracy · 100.0% F1-score',
    barWidth: '100%',
    category: 'Hematology / Oxygen Transport',
  },
]

const HERO_REPORT_EXAMPLES = [
  {
    fileName: 'diabetes-fasting-panel.pdf',
    title: 'hexadisease / diabetes-fasting-panel.pdf',
    tests: [
      { name: 'Fasting Blood Glucose', value: '165 mg/dL', status: 'HIGH', isAlert: true },
      { name: 'HbA1c', value: '7.6 %', status: 'HIGH', isAlert: true },
      { name: 'Total Cholesterol', value: '224 mg/dL', status: 'BORDERLINE', isAlert: true },
    ],
    model: 'Diabetes Mellitus model',
    flagTitle: 'Glycemic elevation',
    flagHex: '#FFE17C',
    category: 'Metabolic',
  },
  {
    fileName: 'stroke-vascular-triage.pdf',
    title: 'hexadisease / stroke-vascular-triage.pdf',
    tests: [
      { name: 'Systolic Blood Pressure', value: '174 mmHg', status: 'URGENT', isAlert: true },
      { name: 'Diastolic Blood Pressure', value: '102 mmHg', status: 'HIGH', isAlert: true },
      { name: 'Average Glucose', value: '182.5 mg/dL', status: 'HIGH', isAlert: true },
    ],
    model: 'Stroke Risk model',
    flagTitle: 'Hypertensive crisis cut-off',
    flagHex: '#FFE17C',
    category: 'Vascular / Neurological',
  },
  {
    fileName: 'cardiac-heart-failure.pdf',
    title: 'hexadisease / cardiac-heart-failure.pdf',
    tests: [
      { name: 'Ejection Fraction (LVEF)', value: '34.0 %', status: 'REDUCED', isAlert: true },
      { name: 'Creatine Kinase (CPK)', value: '445 U/L', status: 'HIGH', isAlert: true },
      { name: 'Total Cholesterol', value: '252 mg/dL', status: 'HIGH', isAlert: true },
    ],
    model: 'Cardiac Heart Failure model',
    flagTitle: 'Systolic dysfunction pattern',
    flagHex: '#FFE17C',
    category: 'Cardiovascular',
  },
  {
    fileName: 'renal-ckd-panel.pdf',
    title: 'hexadisease / renal-ckd-panel.pdf',
    tests: [
      { name: 'Serum Creatinine', value: '2.85 mg/dL', status: 'HIGH', isAlert: true },
      { name: 'Blood Urea', value: '84 mg/dL', status: 'HIGH', isAlert: true },
      { name: 'Urine Albumin', value: '2+ (Proteinuria)', status: 'ABNORMAL', isAlert: true },
    ],
    model: 'CKD Kidney model',
    flagTitle: 'Stage 4 CKD azotemia',
    flagHex: '#FFE17C',
    category: 'Renal',
  },
  {
    fileName: 'maternal-vascular-risk.pdf',
    title: 'hexadisease / maternal-vascular-risk.pdf',
    tests: [
      { name: 'Blood Pressure', value: '158/104 mmHg', status: 'HIGH', isAlert: true },
      { name: 'Heart Rate / Pulse', value: '98 bpm', status: 'BORDERLINE', isAlert: true },
      { name: 'Blood Sugar (BS)', value: '8.0 mmol/L', status: 'BORDERLINE', isAlert: true },
    ],
    model: 'Maternal Vascular model',
    flagTitle: 'Preeclampsia risk window',
    flagHex: '#FFE17C',
    category: 'Vascular',
  },
  {
    fileName: 'cbc-anemia-scan.pdf',
    title: 'hexadisease / cbc-anemia-scan.pdf',
    tests: [
      { name: 'Hemoglobin (Hb)', value: '7.8 g/dL', status: 'SEVERE', isAlert: true },
      { name: 'Hematocrit (PCV)', value: '25.4 %', status: 'LOW', isAlert: true },
      { name: 'RBC Count', value: '3.15 M/uL', status: 'LOW', isAlert: true },
    ],
    model: 'CBC Anemia model',
    flagTitle: 'Critical hypoxia threshold',
    flagHex: '#FFE17C',
    category: 'Hematology',
  },
]

function HeroInteractiveReportMockup() {
  const [index, setIndex] = useState(0)
  const [fade, setFade] = useState(true)
  const [isPaused, setIsPaused] = useState(false)

  useEffect(() => {
    if (isPaused) return

    const timer = setInterval(() => {
      setFade(false)
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % HERO_REPORT_EXAMPLES.length)
        setFade(true)
      }, 250)
    }, 3200)

    return () => clearInterval(timer)
  }, [isPaused])

  const current = HERO_REPORT_EXAMPLES[index]

  return (
    <div
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      className="max-w-[1000px] mx-auto mt-16 border border-[rgba(23,30,25,0.1)] bg-white shadow-2xl rounded-xl overflow-hidden text-left transition-all"
    >
      {/* Top Window Bar */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-[rgba(23,30,25,0.1)] bg-[#f8f9fa]">
        <div className="flex items-center gap-1.5">
          <i className="w-2.5 h-2.5 rounded-full bg-[#ff5f56]" />
          <i className="w-2.5 h-2.5 rounded-full bg-[#ffbd2e]" />
          <i className="w-2.5 h-2.5 rounded-full bg-[#27c93f]" />
        </div>
        <b className="mx-auto text-xs font-mono font-medium opacity-70 pr-10 flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-[#ffe17c] animate-ping" />
          {current.title}
        </b>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-[200px_1fr_240px] min-h-[300px]">
        {/* Left pane */}
        <div className="border-r border-[rgba(23,30,25,0.1)] p-5 text-xs space-y-1 hidden md:block bg-[#fafbfc]">
          <p className="bg-[#ffe17c] font-bold p-2 rounded text-[#171e19] truncate shadow-sm transition-all duration-300">
            {current.fileName}
          </p>
          <p className="p-2 opacity-70 hover:opacity-100 transition-opacity">Biomarkers parsed</p>
          <p className="p-2 opacity-70 hover:opacity-100 transition-opacity">Meta-Classifier active</p>
          <p className="p-2 opacity-70 hover:opacity-100 transition-opacity">WHO / ADA guidance</p>

          <div className="pt-6 mt-4 border-t border-gray-200/60">
            <span className="text-[10px] text-gray-400 font-mono block mb-2 uppercase tracking-wider">
              6 Closely Related Models
            </span>
            <div className="flex gap-1">
              {HERO_REPORT_EXAMPLES.map((_, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setIndex(i)}
                  className={`h-1.5 rounded-full transition-all ${
                    index === i ? 'w-5 bg-[#171e19]' : 'w-1.5 bg-gray-300 hover:bg-gray-400'
                  }`}
                  aria-label={`Show example ${i + 1}`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Middle preview card */}
        <div className="bg-[#f8f9fa] p-6 relative flex items-center justify-center min-h-[260px]">
          <div
            className={`bg-white text-[#171e19] w-full max-w-[380px] p-5 rounded-lg shadow-md border border-gray-100 transition-all duration-300 ease-out ${
              fade ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-[0.98] translate-y-1'
            }`}
          >
            {current.tests.map((test, i) => (
              <div
                key={i}
                className={`flex justify-between items-center py-2.5 ${
                  i < current.tests.length - 1 ? 'border-b border-gray-100' : ''
                } text-sm`}
              >
                <span className="font-medium text-[#171e19]">{test.name}</span>
                <span className="font-mono text-xs flex items-center gap-1.5">
                  <span className="font-bold">{test.value}</span>
                  <span className={test.isAlert ? 'chip-hi' : 'chip-ok'}>{test.status}</span>
                </span>
              </div>
            ))}
          </div>

          {/* Floating animated cursor & tooltip badge */}
          <div
            className={`absolute right-[6%] bottom-[12%] flex gap-1 items-start transition-all duration-300 ease-out ${
              fade ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}
          >
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="#171e19"
              stroke="#fff"
              strokeWidth="1.5"
              className="drop-shadow-md"
            >
              <path d="M4 3l16 7-7 2-2 7z" />
            </svg>
            <span className="bg-[#171e19] text-[#ffe17c] text-[11px] font-bold font-mono px-2.5 py-1 rounded-md shadow-lg mt-2.5 border border-white/10 flex items-center gap-1.5 whitespace-nowrap">
              <span className="w-1.5 h-1.5 rounded-full bg-[#ffe17c] animate-pulse" />
              {current.model}
            </span>
          </div>
        </div>

        {/* Right pane */}
        <div className="border-l border-[rgba(23,30,25,0.1)] p-5 text-xs hidden md:block bg-[#fafbfc]">
          <h4 className="disp text-lg mb-1">Clinical Flag</h4>
          <p
            className={`opacity-80 font-medium text-xs transition-opacity duration-300 ${
              fade ? 'opacity-80' : 'opacity-20'
            }`}
          >
            {current.flagTitle}
          </p>
          <div className="flex items-center gap-2 mt-3 font-mono text-xs">
            <i className="w-5 h-5 rounded bg-[#ffe17c] border border-[rgba(23,30,25,0.1)] shadow-sm" />
            {current.flagHex}
          </div>
          <div className="flex gap-1.5 mt-3">
            <i className="w-5 h-4 border border-[rgba(23,30,25,0.1)] rounded bg-[#171e19]" />
            <i className="w-5 h-4 border border-[rgba(23,30,25,0.1)] rounded bg-gray-200" />
            <i className="w-5 h-4 border border-[rgba(23,30,25,0.1)] rounded bg-gray-100" />
          </div>
          <div className="mt-6 pt-3 border-t border-gray-200/60 text-[10px] text-gray-500 font-mono">
            Model {index + 1} of {HERO_REPORT_EXAMPLES.length} · Auto-rotating
          </div>
        </div>
      </div>
    </div>
  )
}

function ModelPickerLiveCard() {
  const [index, setIndex] = useState(0)
  const [fade, setFade] = useState(true)

  useEffect(() => {
    const timer = setInterval(() => {
      setFade(false)
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % CYCLING_MODELS.length)
        setFade(true)
      }, 250)
    }, 2800)

    return () => clearInterval(timer)
  }, [])

  const current = CYCLING_MODELS[index]

  return (
    <div className="p-8 border border-[rgba(183,198,194,0.1)] rounded-2xl bg-[#171e19] text-white flex flex-col justify-between hover:-translate-y-1 transition-all min-h-[420px] relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-[#ffe17c]/5 rounded-full blur-2xl pointer-events-none" />

      <div>
        <div className="flex items-center justify-between mb-1">
          <h3 className="disp text-3xl tracking-wide">Meta-Classifier Router</h3>
          <span className="flex items-center gap-1.5 text-[11px] font-mono text-[#ffe17c] bg-[#ffe17c]/10 px-2 py-0.5 rounded-full border border-[#ffe17c]/20">
            <span className="w-1.5 h-1.5 rounded-full bg-[#ffe17c] animate-ping" />
            6 MODELS
          </span>
        </div>
        <p className="mt-1.5 text-xs text-[#b7c6c2]/80 leading-relaxed min-h-[34px]">
          <span className="text-[#ffe17c] font-medium">{current.parameters.slice(0, 2).join(' & ')}</span> route directly to the{' '}
          <span className="text-white font-medium">{current.disease}</span> classifier.
        </p>
      </div>

      <div
        className={`my-4 transition-all duration-300 ease-out ${
          fade ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
        }`}
      >
        <div className="flex items-center gap-2 mb-2">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#b7c6c2] bg-white/5 px-2 py-0.5 rounded">
            {current.category}
          </span>
        </div>

        <div className="inline-block bg-[#ffe17c] text-[#171e19] text-xs font-bold font-mono px-2.5 py-1 rounded shadow-sm">
          TARGET: {current.disease}
        </div>

        <div className="text-white font-disp text-2xl tracking-wide uppercase mt-2.5 flex items-center gap-2">
          <Cpu size={18} className="text-[#ffe17c] flex-shrink-0" />
          <span className="truncate">{current.modelName}</span>
        </div>

        <div className="mt-3">
          <span className="text-[11px] uppercase tracking-wider text-[#b7c6c2]/70 font-semibold block mb-1.5">
            Key Features Evaluated:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {current.parameters.map((param, i) => (
              <span
                key={i}
                className="bg-white/10 hover:bg-white/15 text-xs font-mono px-2.5 py-1 rounded text-[#ffe17c] border border-white/5 transition-colors"
              >
                {param}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="space-y-3 pt-3 border-t border-[rgba(183,198,194,0.12)]">
        <div className="flex justify-between items-center text-[11px] font-mono text-[#b7c6c2]">
          <span>{current.metric}</span>
          <span className="text-[#ffe17c] font-bold">{index + 1} of {CYCLING_MODELS.length}</span>
        </div>

        <div className="h-2 rounded-full bg-white/10 overflow-hidden">
          <div
            className="h-full rounded-full bg-[#ffe17c] transition-all duration-700 ease-out shadow-[0_0_8px_rgba(255,225,124,0.5)]"
            style={{ width: current.barWidth }}
          />
        </div>

        <div className="flex justify-center gap-1.5 pt-1">
          {CYCLING_MODELS.map((_, i) => (
            <button
              key={i}
              type="button"
              onClick={() => setIndex(i)}
              aria-label={`View ${CYCLING_MODELS[i].disease} model`}
              className={`h-1.5 rounded-full transition-all duration-300 ${
                index === i ? 'w-6 bg-[#ffe17c]' : 'w-1.5 bg-white/20 hover:bg-white/40'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export default function HomePage() {
  const [openFaq, setOpenFaq] = useState(0)

  const faqs = [
    {
      q: 'Why are these 6 specific tabular diseases chosen together?',
      a: 'Diabetes, Stroke, Heart Failure, Chronic Kidney Disease, Hypertension/Maternal Risk, and Clinical Anemia form the most closely interrelated cardiorenal-metabolic-vascular axis in medicine. A perturbation in blood pressure, glucose, or hemoglobin directly cascades across the heart, kidneys, and brain.',
    },
    {
      q: 'Can I test single diseases directly without uploading a full PDF?',
      a: 'Yes! Visit the Interactive Lab (/predict) to select any of the 6 diseases, input clinical parameters manually (e.g. Glucose, BP, Creatinine, Hb), and see instant machine learning predictions with probabilities.',
    },
    {
      q: 'How does the Meta-Classifier handle missing demographics?',
      a: 'Through Adaptive Population Imputation: standard healthy adult population baselines (Age: 45, BMI: 24.2) are used if not stated, while unmeasured laboratory values are filled via median imputers. All assumptions are transparently disclosed.',
    },
  ]

  return (
    <div>
      {/* ── Hero Section with Grid Background ── */}
      <section className="bg-white grid-bg text-center py-24 px-5">
        <div className="max-w-[1240px] mx-auto">
          <span className="badge-tag">The 6 Core Tabular Diseases Panel</span>
          
          <h1 className="disp text-[clamp(3.6rem,11vw,8.5rem)] mt-8 mx-auto max-w-[1100px] leading-[0.9]">
            The 6 Tabular Diseases, <span className="hl">Predicted</span>
          </h1>
          
          <p className="text-lg opacity-75 max-w-[40rem] mx-auto mt-7 leading-relaxed font-normal">
            Specialized multi-disease AI screening platform focused exclusively on the 6 most closely related
            vascular, metabolic, renal, and hematological diseases. Ingest reports, run trained models, and receive clinical guidance.
          </p>

          {/* Quick Upload CTA Form */}
          <div className="flex flex-col sm:flex-row gap-3 max-w-[640px] mx-auto mt-10">
            <Link
              to="/upload"
              className="flex-1 flex items-center px-6 border border-[rgba(23,30,25,0.2)] rounded-lg bg-white text-left text-sm opacity-90 min-h-[60px] hover:border-[#171e19] transition-colors"
            >
              Upload PDF or image of your lab report
            </Link>
            <Link to="/upload" className="btn-y">
              Upload report
            </Link>
            <Link to="/predict" className="btn-ghost flex items-center justify-center gap-2 text-sm font-bold">
              Interactive Lab <ArrowRight size={16} />
            </Link>
          </div>
          <p className="mt-4 text-xs opacity-60">
            Covers: Diabetes · Stroke · Heart Failure · CKD · Hypertension/Maternal · Anemia
          </p>

          {/* Mock Interactive Report Window */}
          <HeroInteractiveReportMockup />
        </div>
      </section>

      {/* ── Test Parameters Strip ── */}
      <section className="border-y border-[rgba(23,30,25,0.1)] py-5 bg-[#f8f9fa]">
        <div className="max-w-[1240px] mx-auto px-5 flex flex-wrap gap-x-10 gap-y-3 justify-center items-center text-xs font-bold uppercase tracking-[0.16em]">
          <span className="opacity-50">Core Lab Biomarkers:</span>
          <span>Glucose &amp; HbA1c</span>
          <span>Blood Pressure</span>
          <span>Ejection Fraction</span>
          <span>Creatinine &amp; eGFR</span>
          <span>Hemoglobin &amp; PCV</span>
          <span>Cholesterol &amp; Lipids</span>
        </div>
      </section>

      {/* ── Split Comparison ── */}
      <section className="grid grid-cols-1 md:grid-cols-2">
        <div className="bg-[#171e19] text-white p-12 lg:p-24 flex flex-col justify-center">
          <h2 className="disp text-[clamp(2.6rem,5vw,4.5rem)] text-[#b7c6c2] mb-6">
            Isolated Siloed Testing
          </h2>
          <ul className="space-y-4 text-base md:text-lg text-[#b7c6c2]">
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Evaluating kidney failure without considering blood pressure and glucose links</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Missing how severe anemia accelerates cardiac failure and stroke risk</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Reading disconnected numbers without a multi-system meta-classifier</span>
            </li>
          </ul>
        </div>

        <div className="bg-[#272727] text-white p-12 lg:p-24 flex flex-col justify-center border-l-0 md:border-l-4 border-[#ffe17c]">
          <h2 className="disp text-[clamp(2.6rem,5vw,4.5rem)] mb-6">
            The <span className="text-[#ffe17c]">HexaDisease</span> Integration
          </h2>
          <ul className="space-y-4 text-base md:text-lg">
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Single ingestion routes to all matching models across the 6 diseases</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Dual-layer evaluation: clinical deterministic cutoffs + scikit-learn models</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Direct interactive laboratory to test and fine-tune individual clinical parameters</span>
            </li>
          </ul>
        </div>
      </section>

      {/* ── Bento Grid ── */}
      <section className="py-24 px-5">
        <div className="max-w-[1240px] mx-auto">
          <div className="max-w-[720px] mb-14">
            <h2 className="disp text-[clamp(2.8rem,6vw,5rem)]">
              Engineered for <span className="hl">6 diseases</span>
            </h2>
            <p className="mt-5 text-lg opacity-70">
              A specialized architecture connecting document ingestion, adaptive median imputation,
              6 trained ML classifiers, and deterministic WHO/ADA/AHA guidelines.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="md:col-span-2 p-8 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-[#f8f9fa] flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <h3 className="disp text-3xl">Auto-Extracts Core Biomarkers</h3>
                <p className="mt-2 text-sm opacity-70 max-w-sm">From complete blood counts to renal and lipid panels, regex and OCR parse numbers into standard units.</p>
              </div>
              <div className="mt-8 grid grid-cols-2 gap-2">
                <div className="flex justify-between items-center p-3 bg-white text-[#171e19] rounded-lg text-sm border border-gray-100">
                  <span>Fasting glucose</span>
                  <b className="font-mono text-xs">165 mg/dL</b>
                </div>
                <div className="flex justify-between items-center p-3 bg-white text-[#171e19] rounded-lg text-sm border border-gray-100">
                  <span>Serum Creatinine</span>
                  <b className="font-mono text-xs">2.85 mg/dL</b>
                </div>
                <div className="flex justify-between items-center p-3 bg-white text-[#171e19] rounded-lg text-sm border border-gray-100">
                  <span>Hemoglobin</span>
                  <b className="font-mono text-xs">7.8 g/dL</b>
                </div>
                <div className="flex justify-between items-center p-3 bg-white text-[#171e19] rounded-lg text-sm border border-gray-100">
                  <span>Blood Pressure</span>
                  <b className="font-mono text-xs">158/104 mmHg</b>
                </div>
              </div>
            </div>

            <ModelPickerLiveCard />

            <div className="p-8 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-[#f8f9fa] flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <h3 className="disp text-3xl">Evidence Guidance</h3>
                <p className="mt-2 text-sm opacity-70">Deterministic nutritional and clinical advice from WHO, ADA, AHA, and KDIGO.</p>
              </div>
              <div className="mt-8 flex flex-wrap gap-2">
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">Cardioprotective DASH</span>
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">Renal protein control</span>
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">Heme iron optimization</span>
              </div>
            </div>

            <div className="md:col-span-2 p-8 border border-[rgba(183,198,194,0.1)] rounded-2xl bg-[#171e19] text-white flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <h3 className="disp text-3xl">Dual Safety Triaging</h3>
                <p className="mt-2 text-sm opacity-70">Deterministic clinical cuts safeguard against any edge case misclassifications.</p>
              </div>
              <div className="mt-8 bg-[#0c110e] border border-[rgba(183,198,194,0.15)] rounded-lg p-4 font-mono text-xs text-[#b7c6c2] leading-relaxed">
                <div>creatinine &nbsp;&nbsp;&nbsp;2.85 mg/dL &nbsp;<span className="text-[#ffe17c] font-bold">STAGE 4 CKD</span></div>
                <div>hemoglobin &nbsp;&nbsp;&nbsp;7.8 g/dL &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#ffe17c] font-bold">SEVERE ANEMIA</span></div>
                <div>blood pressure 158/104 mmHg &nbsp;<span className="text-[#ffe17c] font-bold">STAGE 2 VASCULAR</span></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── FAQ ── */}
      <section className="py-24 px-5 bg-[#f8f9fa]">
        <div className="max-w-[1240px] mx-auto">
          <div className="max-w-[720px] mb-12">
            <h2 className="disp text-[clamp(2.8rem,6vw,4.5rem)]">
              Frequently <span className="hl">asked</span>
            </h2>
          </div>

          <div className="max-w-[820px] space-y-2">
            {faqs.map((faq, idx) => (
              <div key={idx} className="border-t border-[rgba(23,30,25,0.1)] last:border-b">
                <button
                  type="button"
                  onClick={() => setOpenFaq(openFaq === idx ? -1 : idx)}
                  className="w-full py-6 flex justify-between items-center text-left text-lg md:text-xl font-medium"
                >
                  <span>{faq.q}</span>
                  <span
                    className={`w-8 h-8 rounded-full bg-[#ffe17c] text-[#171e19] flex items-center justify-center text-xl transition-transform ${
                      openFaq === idx ? 'rotate-45' : ''
                    }`}
                  >
                    +
                  </span>
                </button>
                {openFaq === idx && (
                  <p className="pb-6 text-sm md:text-base opacity-75 max-w-2xl leading-relaxed">
                    {faq.a}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Bottom CTA ── */}
      <section className="bg-[#ffe17c] text-[#171e19] py-28 px-5 text-center relative overflow-hidden">
        <div className="max-w-[1240px] mx-auto relative z-10">
          <h2 className="disp text-[clamp(3.2rem,8vw,6.5rem)]">
            Analyze your clinical panel now
          </h2>
          <p className="text-lg md:text-2xl max-w-xl mx-auto mt-6 opacity-90">
            Upload your medical document or enter values directly in our interactive 6-disease laboratory.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-3 max-w-[560px] mx-auto bg-[#171e19] p-3 rounded-xl shadow-2xl">
            <Link
              to="/upload"
              className="flex-1 flex items-center px-5 rounded-lg bg-transparent text-white/80 text-sm border border-white/20 min-h-[54px]"
            >
              Upload PDF or image
            </Link>
            <Link to="/upload" className="btn-y !bg-[#ffe17c] !text-[#171e19]">
              Upload report
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
