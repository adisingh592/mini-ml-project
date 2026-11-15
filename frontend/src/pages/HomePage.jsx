import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  Check, X, Cpu, ArrowRight, Activity, ShieldCheck, Database,
  Sparkles, Apple, FileText, CheckCircle2, TrendingUp, Info, Play, Pause,
  RotateCcw, SkipForward, Video, Zap
} from 'lucide-react'

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
    id: 'diabetes',
    fileName: 'diabetes-fasting-panel.pdf',
    disease: 'Diabetes Mellitus',
    category: 'Endocrine & Metabolic',
    tests: [
      { name: 'Fasting Blood Glucose', value: '165 mg/dL', ref: '70 – 99 mg/dL', status: 'HIGH', isAlert: true, delta: '+66 mg/dL elevation' },
      { name: 'HbA1c Glycated Hemoglobin', value: '7.6 %', ref: '< 5.7 %', status: 'HIGH', isAlert: true, delta: 'Elevated glycemic marker' },
      { name: 'Total Cholesterol', value: '224 mg/dL', ref: '< 200 mg/dL', status: 'BORDERLINE', isAlert: true, delta: 'Borderline lipid elevation' },
    ],
    model: 'Random Forest Meta-Classifier',
    probability: 78.5,
    stage: 'Pre-Diabetes (Reversible Window)',
    flagTitle: 'Stage 1 Glycemic Dysregulation',
    flagHex: '#FFE17C',
    fruits: 'Pomegranate, Berries & Green Apples',
    dietAction: 'High-fiber millets; reduce refined sugars',
    exercise: '30 mins daily brisk walking',
  },
  {
    id: 'stroke',
    fileName: 'stroke-vascular-triage.pdf',
    disease: 'Cerebrovascular Stroke',
    category: 'Vascular / Neurological',
    tests: [
      { name: 'Systolic Blood Pressure', value: '174 mmHg', ref: '< 120 mmHg', status: 'URGENT', isAlert: true, delta: 'Critical vascular pressure' },
      { name: 'Diastolic Blood Pressure', value: '102 mmHg', ref: '< 80 mmHg', status: 'HIGH', isAlert: true, delta: 'Elevated arterial strain' },
      { name: 'Average Blood Glucose', value: '182.5 mg/dL', ref: '< 140 mg/dL', status: 'HIGH', isAlert: true, delta: 'Systemic endothelial risk' },
    ],
    model: 'Random Forest Risk Ensemble',
    probability: 80.5,
    stage: 'Stage 2 Hypertensive Crisis Risk',
    flagTitle: 'Hypertensive Crisis Cut-off',
    flagHex: '#FF5F56',
    fruits: 'Bananas (Potassium), Watermelon & Citrus',
    dietAction: 'Strict low-sodium DASH diet (< 1500mg/day)',
    exercise: 'Gentle continuous walking & deep breathing',
  },
  {
    id: 'heart_disease',
    fileName: 'cardiac-heart-failure.pdf',
    disease: 'Heart Failure & Cardiac Risk',
    category: 'Cardiovascular',
    tests: [
      { name: 'Ejection Fraction (LVEF)', value: '34.0 %', ref: '50 – 70 %', status: 'REDUCED', isAlert: true, delta: 'Systolic pump reduction' },
      { name: 'Creatine Kinase (CPK)', value: '445 U/L', ref: '38 – 174 U/L', status: 'HIGH', isAlert: true, delta: 'Myocardial strain marker' },
      { name: 'Serum Creatinine', value: '1.65 mg/dL', ref: '0.6 – 1.2 mg/dL', status: 'HIGH', isAlert: true, delta: 'Cardiorenal link active' },
    ],
    model: 'Random Forest Mortality Model',
    probability: 85.0,
    stage: 'HFrEF Stage B (Reduced Ejection Fraction)',
    flagTitle: 'Systolic Dysfunction Pattern',
    flagHex: '#FFE17C',
    fruits: 'Papaya, Kiwi & Fresh Pomegranate',
    dietAction: 'Fluid regulation & heart-healthy fats',
    exercise: 'Physician-monitored walking routine',
  },
  {
    id: 'kidney_disease',
    fileName: 'renal-ckd-panel.pdf',
    disease: 'Chronic Kidney Disease (CKD)',
    category: 'Renal System',
    tests: [
      { name: 'Serum Creatinine', value: '2.85 mg/dL', ref: '0.6 – 1.2 mg/dL', status: 'HIGH', isAlert: true, delta: '+1.65 mg/dL elevation' },
      { name: 'Blood Urea', value: '84 mg/dL', ref: '15 – 45 mg/dL', status: 'HIGH', isAlert: true, delta: 'Elevated nitrogenous waste' },
      { name: 'Urine Albumin', value: '2+ (Proteinuria)', ref: 'Negative', status: 'ABNORMAL', isAlert: true, delta: 'Glomerular filter breakdown' },
    ],
    model: 'Logistic Regression ARFF Model',
    probability: 92.4,
    stage: 'Stage 3b Moderate-to-Severe Azotemia',
    flagTitle: 'Renal Filtration Impairment',
    flagHex: '#FFE17C',
    fruits: 'Blueberries, Apples & Strawberries',
    dietAction: 'Controlled dietary protein (0.6g/kg) & low salt',
    exercise: 'Light aerobic movement & daily hydration',
  },
  {
    id: 'maternal_risk',
    fileName: 'maternal-vascular-risk.pdf',
    disease: 'Hypertension / Maternal Risk',
    category: 'Vascular & Hemodynamics',
    tests: [
      { name: 'Blood Pressure', value: '158/104 mmHg', ref: '< 120/80 mmHg', status: 'HIGH', isAlert: true, delta: 'Preeclampsia threshold' },
      { name: 'Heart Rate / Pulse', value: '98 bpm', ref: '60 – 80 bpm', status: 'BORDERLINE', isAlert: true, delta: 'Tachycardia tendency' },
      { name: 'Blood Sugar (BS)', value: '8.0 mmol/L', ref: '< 5.5 mmol/L', status: 'BORDERLINE', isAlert: true, delta: 'Gestational glycemic rise' },
    ],
    model: 'Random Forest Hemodynamics Model',
    probability: 84.2,
    stage: 'Preeclampsia Hemodynamic Risk Window',
    flagTitle: 'Maternal Vascular Strain',
    flagHex: '#FFE17C',
    fruits: 'Guava, Oranges & Pears',
    dietAction: 'Magnesium & Calcium enriched balanced meals',
    exercise: 'Prenatal walking & lateral resting',
  },
  {
    id: 'anemia',
    fileName: 'cbc-anemia-scan.pdf',
    disease: 'Clinical Anemia',
    category: 'Hematology / Oxygen Transport',
    tests: [
      { name: 'Hemoglobin (Hb)', value: '7.8 g/dL', ref: '12.0 – 16.0 g/dL', status: 'SEVERE', isAlert: true, delta: 'Critical hypoxia threshold' },
      { name: 'Hematocrit (PCV)', value: '25.4 %', ref: '37 – 48 %', status: 'LOW', isAlert: true, delta: 'Low red cell volume' },
      { name: 'RBC Count', value: '3.15 M/uL', ref: '4.2 – 5.4 M/uL', status: 'LOW', isAlert: true, delta: 'Circulating oxygen reduction' },
    ],
    model: 'Logistic Regression CBC Classifier',
    probability: 99.2,
    stage: 'Stage 2 Moderate-to-Severe Hypoxia',
    flagTitle: 'Critical Hypoxia Risk',
    flagHex: '#FF5F56',
    fruits: 'Pomegranate, Beetroot, Amla & Dates',
    dietAction: 'Vitamin C paired with dietary iron (Sprouts/Greens)',
    exercise: 'Low-strain light walking; avoid exhaustion',
  },
]

const TOUR_STEPS = [
  {
    step: 0,
    timestamp: '00:01',
    chapter: '1. Ingest PDF',
    badge: 'Step 1 of 4: Document Ingestion',
    title: '1. Ingest Lab Report',
    cursorTarget: { x: '13%', y: '28%' },
    cursorLabel: '1. Scanning Lab PDF...',
    actionHighlight: 'left_file',
    caption: 'High-speed OCR scans uploaded report and extracts raw clinical values.',
    shortExplanation: 'Upload PDF / photo → OCR extracts clinical parameters instantly.',
  },
  {
    step: 1,
    timestamp: '00:02',
    chapter: '2. Audit Bounds',
    badge: 'Step 2 of 4: Biomarker Normalization',
    title: '2. Extract & Inspect Biomarkers',
    cursorTarget: { x: '45%', y: '36%' },
    cursorLabel: '2. Auditing Biomarkers...',
    actionHighlight: 'middle_biomarker',
    caption: 'Audits values against WHO/ADA normal intervals; flags out-of-range metrics with delta alerts.',
    shortExplanation: 'Audits values against normal limits; flags out-of-bounds metrics.',
  },
  {
    step: 2,
    timestamp: '00:03',
    chapter: '3. AI Staging',
    badge: 'Step 3 of 4: Multi-Disease AI Prediction',
    title: '3. Predict Disease Risk & Staging',
    cursorTarget: { x: '51%', y: '75%' },
    cursorLabel: '3. Computing ML Risk...',
    actionHighlight: 'middle_model',
    caption: 'Trained Machine Learning model computes risk probability and pinpoints reversible early stage.',
    shortExplanation: 'Specialized ML classifier calculates risk probability & reversible early stage.',
  },
  {
    step: 3,
    timestamp: '00:04',
    chapter: '4. Fruits & Diet',
    badge: 'Step 4 of 4: Preventive Nutrition & Fruits',
    title: '4. Prescribe Fruits & Lifestyle Plan',
    cursorTarget: { x: '86%', y: '42%' },
    cursorLabel: '4. Prescribing Fruits & Habits...',
    actionHighlight: 'right_action',
    caption: 'Prescribes disease-targeting fruits, dietary adjustments & daily walking to halt disease growth early.',
    shortExplanation: 'Recommends targeted fruits, dietary habits & daily walking to reverse early risk.',
  },
]

function HeroInteractiveReportMockup() {
  const [diseaseIndex, setDiseaseIndex] = useState(0)
  const [tourStep, setTourStep] = useState(0)
  const [isPaused, setIsPaused] = useState(false)
  const [playbackSpeed, setPlaybackSpeed] = useState(1.5) // 1.5x Fast by default!
  const [clickPulse, setClickPulse] = useState(false)

  // Step duration adjusted by playback speed:
  // 1x = 1600ms, 1.5x = 1060ms, 2x = 750ms
  const stepDuration = Math.round(1600 / playbackSpeed)

  // Video cycle timer
  useEffect(() => {
    if (isPaused) return

    const timer = setInterval(() => {
      setClickPulse(true)
      setTimeout(() => setClickPulse(false), Math.min(300, Math.round(stepDuration * 0.3)))

      setTourStep((prevStep) => {
        if (prevStep === TOUR_STEPS.length - 1) {
          // Advance to next disease on completion of full 4-step loop
          setDiseaseIndex((prevD) => (prevD + 1) % HERO_REPORT_EXAMPLES.length)
          return 0
        }
        return prevStep + 1
      })
    }, stepDuration)

    return () => clearInterval(timer)
  }, [isPaused, playbackSpeed, stepDuration])

  const current = HERO_REPORT_EXAMPLES[diseaseIndex]
  const currentTour = TOUR_STEPS[tourStep]

  const handleSelectStep = (s) => {
    setTourStep(s)
    setClickPulse(true)
    setTimeout(() => setClickPulse(false), 300)
  }

  const handleSelectDisease = (idx) => {
    setDiseaseIndex(idx)
    setTourStep(0)
    setClickPulse(true)
    setTimeout(() => setClickPulse(false), 300)
  }

  const handleRestart = () => {
    setTourStep(0)
    setClickPulse(true)
    setTimeout(() => setClickPulse(false), 300)
  }

  const handleNextDisease = () => {
    setDiseaseIndex((prev) => (prev + 1) % HERO_REPORT_EXAMPLES.length)
    setTourStep(0)
    setClickPulse(true)
    setTimeout(() => setClickPulse(false), 300)
  }

  // Fast, nimble cursor transition
  const cursorTransition = playbackSpeed >= 2
    ? 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)'
    : playbackSpeed >= 1.5
    ? 'all 0.30s cubic-bezier(0.16, 1, 0.3, 1)'
    : 'all 0.42s cubic-bezier(0.16, 1, 0.3, 1)'

  const progressPercent = ((tourStep + 1) / TOUR_STEPS.length) * 100

  return (
    <div
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      className="max-w-[1060px] mx-auto mt-14 border-2 border-[#171e19]/15 bg-white shadow-2xl rounded-2xl overflow-hidden text-left transition-all relative ring-1 ring-black/5"
    >
      {/* ── Top Video Bar with Live Recording Badge & Speed Controls ── */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 border-b border-[rgba(23,30,25,0.12)] bg-[#171e19] text-white">
        {/* Left: macOS dots & Video File Tag */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <i className="w-2.5 h-2.5 rounded-full bg-[#ff5f56]" />
            <i className="w-2.5 h-2.5 rounded-full bg-[#ffbd2e]" />
            <i className="w-2.5 h-2.5 rounded-full bg-[#27c93f]" />
          </div>
          <div className="flex items-center gap-1.5 text-xs font-mono font-medium text-gray-300">
            <Video size={13} className="text-[#ffe17c]" />
            <span className="hidden sm:inline font-bold text-white">AI DEMO VIDEO:</span>
            <span className="text-[#ffe17c]">{current.fileName}</span>
          </div>
        </div>

        {/* Center: Live Recording & Timecode Counter */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 bg-red-950/80 border border-red-500/40 text-red-300 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold shadow-inner">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
            <span>REC {currentTour.timestamp} / 00:04</span>
          </div>
          <span className="text-[10px] font-mono text-gray-400 hidden md:inline">1080P · 60FPS</span>
        </div>

        {/* Right: Video Controls (Speed, Restart, Play/Pause, Next) */}
        <div className="flex items-center gap-2">
          {/* Speed Pills */}
          <div className="flex items-center bg-white/10 p-0.5 rounded-lg border border-white/15 text-[10px] font-mono">
            {[1, 1.5, 2].map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => setPlaybackSpeed(s)}
                className={`px-1.5 py-0.5 rounded font-bold transition ${
                  playbackSpeed === s
                    ? 'bg-[#ffe17c] text-[#171e19] shadow-sm'
                    : 'text-gray-300 hover:text-white'
                }`}
                title={`Playback speed ${s}x`}
              >
                {s === 2 ? '2x Turbo' : `${s}x`}
              </button>
            ))}
          </div>

          {/* Restart Button */}
          <button
            type="button"
            onClick={handleRestart}
            className="p-1 rounded-md text-gray-300 hover:text-white hover:bg-white/10 transition"
            title="Restart video (0:00)"
          >
            <RotateCcw size={13} />
          </button>

          {/* Play/Pause Button */}
          <button
            type="button"
            onClick={() => setIsPaused(!isPaused)}
            className="text-xs font-bold px-2.5 py-1 rounded-md bg-[#ffe17c] text-[#171e19] hover:bg-amber-300 flex items-center gap-1 transition shadow-sm"
            title={isPaused ? 'Resume video' : 'Pause video'}
          >
            {isPaused ? <Play size={12} className="fill-[#171e19]" /> : <Pause size={12} className="fill-[#171e19]" />}
            <span>{isPaused ? 'Play' : 'Pause'}</span>
          </button>

          {/* Next Disease Button */}
          <button
            type="button"
            onClick={handleNextDisease}
            className="text-[11px] font-mono px-2 py-1 rounded-md bg-white/10 hover:bg-white/20 text-gray-200 flex items-center gap-1 transition hidden sm:flex"
            title="Next disease video"
          >
            <span>Next</span>
            <SkipForward size={12} />
          </button>
        </div>
      </div>

      {/* ── Main Mockup Workspace Area (with Fast Gliding Cursor) ── */}
      <div className="relative min-h-[360px] select-none bg-[#fbfcfd]">
        {/* Floating Fast-Gliding Cursor with Action Tag */}
        <div
          className="absolute pointer-events-none z-40 flex items-start gap-1.5"
          style={{
            left: currentTour.cursorTarget.x,
            top: currentTour.cursorTarget.y,
            transition: cursorTransition,
            transform: 'translate(-6px, -6px)',
          }}
        >
          <div className="relative">
            {/* Realistic Desktop Cursor SVG */}
            <svg
              width="26"
              height="26"
              viewBox="0 0 24 24"
              fill="#171e19"
              stroke="#ffffff"
              strokeWidth="1.5"
              className="drop-shadow-xl filter drop-shadow-[0_4px_8px_rgba(0,0,0,0.35)]"
            >
              <path d="M4 3l16 7-7 2-2 7z" />
            </svg>
            {/* Fast Click Ripple Effect */}
            {clickPulse && (
              <span className="absolute -top-2 -left-2 w-8 h-8 rounded-full bg-[#ffe17c] opacity-90 animate-ping pointer-events-none" />
            )}
          </div>

          {/* Fast Animated Cursor Action Tag */}
          <div className="bg-[#171e19] text-[#ffe17c] text-[11px] font-bold font-mono px-2.5 py-1 rounded-lg shadow-xl border border-white/20 whitespace-nowrap flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#ffe17c] animate-pulse" />
            {currentTour.cursorLabel}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-[220px_1fr_260px] min-h-[350px]">
          {/* ── Left Pane: Document Ingestion (Step 1) ── */}
          <div className={`border-r border-[rgba(23,30,25,0.1)] p-5 text-xs space-y-2.5 hidden md:block bg-[#fafbfc] transition-colors relative ${tourStep === 0 ? 'bg-[#ffe17c]/15 ring-2 ring-inset ring-[#ffe17c]' : ''}`}>
            {/* Laser Scanning Line Animation when Step 0 is active */}
            {tourStep === 0 && (
              <div className="absolute inset-0 pointer-events-none overflow-hidden z-20">
                <div className="w-full h-1 bg-gradient-to-r from-transparent via-[#ffe17c] to-transparent shadow-[0_0_12px_#ffe17c] animate-laser-scan" />
              </div>
            )}

            <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400 block mb-1">
              1. Document Ingested
            </span>

            <div className={`p-2.5 rounded-xl font-bold transition-all shadow-sm flex items-center gap-2 ${tourStep === 0 ? 'bg-[#171e19] text-[#ffe17c] ring-2 ring-[#ffe17c]' : 'bg-[#ffe17c] text-[#171e19]'}`}>
              <FileText size={15} />
              <span className="truncate">{current.fileName}</span>
            </div>

            <div className="space-y-1 text-gray-600">
              <div className="p-2 rounded hover:bg-gray-100 flex items-center justify-between text-[11px]">
                <span>Biomarkers Parsed</span>
                <b className="font-mono">{current.tests.length} tests</b>
              </div>
              <div className="p-2 rounded hover:bg-gray-100 flex items-center justify-between text-[11px]">
                <span>Meta-Classifier</span>
                <span className="text-emerald-700 font-bold">ACTIVE</span>
              </div>
              <div className="p-2 rounded hover:bg-gray-100 flex items-center justify-between text-[11px]">
                <span>Guidelines</span>
                <span className="text-gray-700 font-mono">WHO / ADA</span>
              </div>
            </div>

            {/* Quick Disease Switcher in Left Pane */}
            <div className="pt-4 mt-3 border-t border-gray-200/70">
              <span className="text-[10px] text-gray-400 font-mono block mb-2 uppercase tracking-wider">
                6 Tabular Diseases:
              </span>
              <div className="flex flex-wrap gap-1">
                {HERO_REPORT_EXAMPLES.map((ex, i) => (
                  <button
                    key={ex.id}
                    type="button"
                    onClick={() => handleSelectDisease(i)}
                    className={`px-2 py-1 rounded text-[10px] font-semibold transition ${
                      diseaseIndex === i
                        ? 'bg-[#171e19] text-[#ffe17c]'
                        : 'bg-gray-200/70 text-gray-600 hover:bg-gray-300'
                    }`}
                  >
                    {ex.disease.split(' ')[0]}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* ── Middle Preview Card: Biomarkers & Staging (Steps 2 & 3) ── */}
          <div className="bg-[#f8f9fa] p-6 relative flex flex-col items-center justify-center min-h-[300px]">
            {/* Floating Biomarker Inspection Tooltip (Step 2) */}
            {tourStep === 1 && (
              <div className="absolute top-4 left-6 right-6 md:right-auto md:max-w-xs z-30 bg-[#171e19] text-white p-3.5 rounded-xl shadow-2xl border-2 border-[#ffe17c] text-xs animate-in fade-in zoom-in-95 duration-200">
                <div className="flex items-center justify-between text-[10px] font-mono text-[#ffe17c] mb-1">
                  <span>STEP 2 · AUDITING BIOMARKER</span>
                  <span className="font-bold px-1.5 py-0.5 bg-red-500/20 text-red-300 rounded">{current.tests[0].status}</span>
                </div>
                <b className="block text-white text-sm font-bold">{current.tests[0].name}</b>
                <p className="text-[11px] text-[#b7c6c2] mt-1 leading-relaxed">
                  Measured: <b className="text-white font-mono">{current.tests[0].value}</b>. Normal bound is{' '}
                  <span className="font-mono text-emerald-400">{current.tests[0].ref}</span> ({current.tests[0].delta}).
                </p>
              </div>
            )}

            {/* Test Parameters Card */}
            <div
              className={`bg-white text-[#171e19] w-full max-w-[420px] p-5 rounded-2xl shadow-md border transition-all duration-200 ${
                tourStep === 1 ? 'border-amber-400 ring-2 ring-amber-300 shadow-xl' : 'border-gray-200'
              }`}
            >
              <div className="flex justify-between items-center pb-2.5 mb-2.5 border-b border-gray-100 text-xs">
                <span className="font-bold uppercase tracking-wider text-gray-500 text-[10px]">
                  Extracted Biomarker
                </span>
                <span className="font-bold uppercase tracking-wider text-gray-500 text-[10px]">
                  Measured &amp; Status
                </span>
              </div>

              {current.tests.map((test, i) => (
                <div
                  key={i}
                  className={`flex justify-between items-center py-2 px-2 rounded-lg text-sm transition-colors ${
                    i === 0 && tourStep === 1 ? 'bg-amber-50 font-bold' : ''
                  } ${i < current.tests.length - 1 ? 'border-b border-gray-100' : ''}`}
                >
                  <div>
                    <span className="font-medium text-[#171e19] block">{test.name}</span>
                    <small className="text-[10px] text-gray-400 font-mono">Ref: {test.ref}</small>
                  </div>
                  <span className="font-mono text-xs flex items-center gap-1.5">
                    <span className="font-bold">{test.value}</span>
                    <span className={test.isAlert ? 'chip-hi' : 'chip-ok'}>{test.status}</span>
                  </span>
                </div>
              ))}

              {/* Step 3 Highlight: AI Model Classification Card */}
              <div
                className={`mt-4 pt-3.5 border-t border-gray-100 rounded-xl p-3 transition-all duration-200 ${
                  tourStep === 2 ? 'bg-[#171e19] text-white ring-2 ring-[#ffe17c] shadow-lg' : 'bg-gray-50 text-[#171e19]'
                }`}
              >
                <div className="flex justify-between items-center text-xs">
                  <div className="flex items-center gap-1.5">
                    <Cpu size={14} className={tourStep === 2 ? 'text-[#ffe17c]' : 'text-[#171e19]'} />
                    <b className="font-semibold">{current.model}</b>
                  </div>
                  <span className={`font-mono text-xs font-bold px-2 py-0.5 rounded ${tourStep === 2 ? 'bg-[#ffe17c] text-[#171e19]' : 'bg-[#171e19] text-[#ffe17c]'}`}>
                    {current.probability}% Risk
                  </span>
                </div>

                {/* Fast Dynamic Risk Fill Bar */}
                <div className="mt-2 w-full bg-white/20 h-1.5 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-[#ffe17c] transition-all duration-300" 
                    style={{ width: `${current.probability}%` }} 
                  />
                </div>

                <div className="mt-2 text-[11px] flex items-center justify-between">
                  <span className="opacity-70">Clinical Staging:</span>
                  <span className={`font-bold ${tourStep === 2 ? 'text-[#ffe17c]' : 'text-amber-600'}`}>
                    {current.stage}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* ── Right Pane: Clinical Action Plan & Fruits (Step 4) ── */}
          <div className={`border-l border-[rgba(23,30,25,0.1)] p-5 text-xs hidden md:flex flex-col justify-between bg-[#fafbfc] transition-colors ${tourStep === 3 ? 'bg-[#ffe17c]/15 ring-2 ring-inset ring-[#ffe17c]' : ''}`}>
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400 block mb-1">
                4. Actionable Next Steps
              </span>

              <h4 className="disp text-xl mb-1 text-[#171e19]">{current.flagTitle}</h4>
              <p className="text-[11px] text-gray-600 leading-relaxed mt-1">
                Early detection allows targeted lifestyle adjustments before permanent organ degradation occurs.
              </p>

              {/* Recommended Fruits Section */}
              <div className={`mt-4 p-3 rounded-xl border transition-all ${tourStep === 3 ? 'bg-white border-amber-300 shadow-md ring-1 ring-amber-300' : 'bg-white/80 border-gray-200'}`}>
                <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-800 mb-1">
                  <Apple size={14} className="text-emerald-600 flex-shrink-0" />
                  <span>Target Fruits:</span>
                </div>
                <p className="text-[11px] text-gray-700 leading-relaxed font-medium">
                  {current.fruits}
                </p>
              </div>

              {/* Daily Habit & Walking */}
              <div className="mt-3 p-3 rounded-xl bg-white/80 border border-gray-200">
                <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-0.5">
                  Daily Physical Action:
                </span>
                <p className="text-[11px] text-gray-700 leading-relaxed">
                  {current.exercise}
                </p>
              </div>
            </div>

            <div className="pt-3 border-t border-gray-200/60 flex items-center justify-between text-[10px] text-gray-500 font-mono">
              <span>Model {diseaseIndex + 1} of {HERO_REPORT_EXAMPLES.length}</span>
              <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Reversible Stage</span>
            </div>
          </div>
        </div>

        {/* ── Video Subtitles / Closed Captions [CC] Overlay ── */}
        <div className="p-2.5 bg-[#171e19] text-white border-t border-white/10 flex items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 overflow-hidden">
            <span className="bg-[#ffe17c] text-[#171e19] font-mono font-bold text-[10px] px-1.5 py-0.5 rounded tracking-wider uppercase flex-shrink-0">
              CC · {currentTour.timestamp}
            </span>
            <span className="font-bold text-[#ffe17c] flex-shrink-0">{currentTour.chapter}:</span>
            <span className="text-gray-200 text-[11px] truncate hidden sm:inline">{currentTour.caption}</span>
            <span className="text-gray-200 text-[11px] truncate sm:hidden">{currentTour.shortExplanation}</span>
          </div>
          <div className="flex items-center gap-2 text-[10px] font-mono text-gray-400 flex-shrink-0">
            <span className="text-emerald-400 font-bold hidden md:inline">● AUTO-PLAYING</span>
            <span>{playbackSpeed}x</span>
          </div>
        </div>
      </div>

      {/* ── Interactive Video Progress Bar & Chapter Scrubber ── */}
      <div className="p-4 bg-[#0d120f] text-white border-t border-white/10">
        {/* Scrubber Track with Chapter Markers */}
        <div className="relative mb-3">
          {/* Background Track with Click-to-Seek */}
          <div className="w-full h-2 bg-white/20 rounded-full overflow-hidden cursor-pointer relative">
            {/* Active Continuous Video Progress Fill */}
            <div
              className="h-full bg-gradient-to-r from-[#ffe17c] to-amber-400 transition-all duration-300 relative"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          {/* Chapter Tick Marks */}
          <div className="flex justify-between items-center mt-1.5 text-[10px] font-mono text-gray-400">
            {TOUR_STEPS.map((s, idx) => (
              <button
                key={s.step}
                type="button"
                onClick={() => handleSelectStep(idx)}
                className={`transition hover:text-white flex items-center gap-1 ${
                  tourStep === idx ? 'text-[#ffe17c] font-bold' : ''
                }`}
              >
                <span className={`w-1.5 h-1.5 rounded-full ${tourStep === idx ? 'bg-[#ffe17c] animate-pulse' : 'bg-gray-500'}`} />
                <span>{s.timestamp} {s.chapter}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Bottom Control Bar: Disease Switcher Tabs & Quick Actions */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-white/10 text-xs">
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
            <span className="text-[10px] font-mono text-gray-400 uppercase tracking-wider mr-1">
              Select Disease Video:
            </span>
            {HERO_REPORT_EXAMPLES.map((ex, i) => (
              <button
                key={ex.id}
                type="button"
                onClick={() => handleSelectDisease(i)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  diseaseIndex === i
                    ? 'bg-[#ffe17c] text-[#171e19] font-bold shadow-md'
                    : 'bg-white/10 text-gray-300 hover:bg-white/20'
                }`}
              >
                {ex.disease.split(' ')[0]}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[11px] text-gray-300 font-mono hidden md:inline">
              Fast Video Demo · <span className="text-[#ffe17c] font-bold">Auto-loops 6 Diseases</span>
            </span>
            <button
              type="button"
              onClick={handleNextDisease}
              className="text-xs font-bold px-3 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-[#ffe17c] border border-white/10 transition flex items-center gap-1"
            >
              <span>Next Disease</span>
              <SkipForward size={12} />
            </button>
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
          <span className="badge-tag">AI Early Disease Detection &amp; Prevention</span>
          
          <h1 className="disp text-[clamp(3.4rem,10vw,7.8rem)] mt-8 mx-auto max-w-[1100px] leading-[0.95]">
            Detect Diseases Early. <span className="hl">Understand Your Lab Reports.</span>
          </h1>
          
          <p className="text-lg opacity-75 max-w-[42rem] mx-auto mt-7 leading-relaxed font-normal">
            Understand complex blood test parameters without medical jargon. Identify early-stage risk across 6 closely related cardiorenal-metabolic diseases, and receive personalized daily fruit, diet, and exercise guidance before conditions escalate.
          </p>

          {/* Quick Upload CTA Form */}
          <div className="flex flex-col sm:flex-row gap-3 max-w-[660px] mx-auto mt-10">
            <Link
              to="/upload"
              className="flex-1 flex items-center px-6 border border-[rgba(23,30,25,0.2)] rounded-lg bg-white text-left text-sm opacity-90 min-h-[60px] hover:border-[#171e19] transition-colors"
            >
              Upload PDF or photo of your routine blood test
            </Link>
            <Link to="/upload" className="btn-y">
              Upload Lab Report
            </Link>
            <Link to="/predict" className="btn-ghost flex items-center justify-center gap-2 text-sm font-bold">
              Disease Predictor <ArrowRight size={16} />
            </Link>
          </div>
          <p className="mt-4 text-xs opacity-60">
            Covers 6 Core Cardiorenal-Metabolic Diseases: Diabetes Mellitus · Stroke · Heart Failure · Chronic Kidney Disease · Hypertension · Clinical Anemia
          </p>

          {/* Mock Interactive Report Window */}
          <HeroInteractiveReportMockup />
        </div>
      </section>

      {/* ── Test Parameters Strip ── */}
      <section className="border-y border-[rgba(23,30,25,0.1)] py-5 bg-[#f8f9fa]">
        <div className="max-w-[1240px] mx-auto px-5 flex flex-wrap gap-x-10 gap-y-3 justify-center items-center text-xs font-bold uppercase tracking-[0.16em]">
          <span className="opacity-50">Routine Checkup Biomarkers Monitored:</span>
          <span>Glucose &amp; HbA1c</span>
          <span>Blood Pressure</span>
          <span>Ejection Fraction</span>
          <span>Creatinine &amp; eGFR</span>
          <span>Hemoglobin &amp; PCV</span>
          <span>Lipids &amp; Electrolytes</span>
        </div>
      </section>

      {/* ── Split Comparison: Isolated Siloed Testing vs Unified ArogyaDrishti ── */}
      <section className="grid grid-cols-1 md:grid-cols-2">
        <div className="bg-[#171e19] text-white p-12 lg:p-24 flex flex-col justify-center">
          <span className="text-xs font-bold uppercase tracking-wider text-red-400 mb-2">The Common Problem</span>
          <h2 className="disp text-[clamp(2.4rem,4.5vw,4.2rem)] text-[#b7c6c2] mb-6">
            Confusing &amp; Siloed Lab Reports
          </h2>
          <ul className="space-y-4 text-base md:text-lg text-[#b7c6c2]">
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Complex medical terminology leaves patients unsure of their true health risks</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Evaluating kidney markers in isolation misses how blood pressure and glucose accelerate renal failure</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Early reversible stages (Pre-diabetes, Stage 1 CKD) are overlooked until severe symptoms appear</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>No practical guidance on which fruits, daily diet, or exercise can normalize numbers</span>
            </li>
          </ul>
        </div>

        <div className="bg-[#272727] text-white p-12 lg:p-24 flex flex-col justify-center border-l-0 md:border-l-4 border-[#ffe17c]">
          <span className="text-xs font-bold uppercase tracking-wider text-[#ffe17c] mb-2">The ArogyaDrishti Solution</span>
          <h2 className="disp text-[clamp(2.4rem,4.5vw,4.2rem)] mb-6">
            Unified AI <span className="text-[#ffe17c]">Health Intelligence</span>
          </h2>
          <ul className="space-y-4 text-base md:text-lg">
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Translates every biomarker into plain language, explaining its biological function and reference status</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Multi-system Meta-Classifier evaluates interconnected risks across heart, brain, kidneys, and blood</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Detects early reversible disease stages and warns you in time to make natural lifestyle changes</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Provides actionable daily fruit, dietary, and exercise prescriptions to reverse abnormal parameters</span>
            </li>
          </ul>
        </div>
      </section>

      {/* ── Bento Grid: Core Capabilities & Clinical Pipeline ── */}
      <section className="py-24 px-5">
        <div className="max-w-[1240px] mx-auto">
          <div className="max-w-[760px] mb-14">
            <span className="badge-tag">Clinical Architecture &amp; Features</span>
            <h2 className="disp text-[clamp(2.8rem,6vw,4.8rem)] mt-3">
              Engineered for <span className="hl">Early Prevention</span>
            </h2>
            <p className="mt-4 text-lg opacity-70">
              A complete pipeline connecting document OCR extraction, 6 trained machine learning models, deterministic medical staging guidelines, and longitudinal health progress tracking.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="md:col-span-2 p-8 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-[#f8f9fa] flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 bg-white px-2.5 py-1 rounded border border-gray-200">
                  Feature 1 · Automated Ingestion
                </span>
                <h3 className="disp text-3xl mt-3">Automated Biomarker Extraction</h3>
                <p className="mt-2 text-sm opacity-70 max-w-md">From complete blood counts to renal and lipid panels, regex and OCR extract numbers, normalize units, and compare against standard reference intervals.</p>
              </div>
              <div className="mt-8 grid grid-cols-2 gap-2">
                <div className="flex justify-between items-center p-3 bg-white text-[#171e19] rounded-lg text-sm border border-gray-100">
                  <span>Fasting Glucose</span>
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
                <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 bg-white px-2.5 py-1 rounded border border-gray-200">
                  Feature 2 · Targeted Nutrition
                </span>
                <h3 className="disp text-3xl mt-3">Targeted Fruit &amp; Diet Plan</h3>
                <p className="mt-2 text-sm opacity-70">Specific fruits and dietary interventions proven to modulate blood glucose, renal filtration, and systolic blood pressure.</p>
              </div>
              <div className="mt-8 flex flex-wrap gap-2">
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">Pomegranates &amp; Berries</span>
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">DASH Diet Guidelines</span>
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">Renal Protein Control</span>
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">Heme Iron Boosters</span>
              </div>
            </div>

            <div className="md:col-span-2 p-8 border border-[rgba(183,198,194,0.1)] rounded-2xl bg-[#171e19] text-white flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#ffe17c] bg-white/10 px-2.5 py-1 rounded border border-white/10">
                  Feature 3 · Clinical Safety Triaging
                </span>
                <h3 className="disp text-3xl mt-3">Dual Safety Triaging &amp; Early Staging</h3>
                <p className="mt-2 text-sm opacity-70">Deterministic clinical cutoffs (WHO, ADA, AHA, KDIGO) combine with statistical models to detect early reversible stages with zero misclassification.</p>
              </div>
              <div className="mt-8 bg-[#0c110e] border border-[rgba(183,198,194,0.15)] rounded-lg p-4 font-mono text-xs text-[#b7c6c2] leading-relaxed">
                <div>creatinine &nbsp;&nbsp;&nbsp;2.85 mg/dL &nbsp;<span className="text-[#ffe17c] font-bold">STAGE 4 CKD AZOTEMIA</span></div>
                <div>hemoglobin &nbsp;&nbsp;&nbsp;7.8 g/dL &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#ffe17c] font-bold">SEVERE ANEMIA (HYPOXIA RISK)</span></div>
                <div>blood pressure 158/104 mmHg &nbsp;<span className="text-[#ffe17c] font-bold">STAGE 2 HYPERTENSIVE VASCULAR STRAIN</span></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── FAQ Section ── */}
      <section className="py-24 px-5 bg-[#f8f9fa]">
        <div className="max-w-[1240px] mx-auto">
          <div className="max-w-[720px] mb-12">
            <span className="badge-tag">Common Inquiries</span>
            <h2 className="disp text-[clamp(2.8rem,6vw,4.5rem)] mt-3">
              Frequently Asked <span className="hl">Questions</span>
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
          <span className="text-xs font-bold uppercase tracking-wider opacity-80 block mb-2">Get Started in Seconds</span>
          <h2 className="disp text-[clamp(3.2rem,8vw,6.5rem)]">
            Analyze Your Health Panel Now
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
              Upload Lab Report
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
