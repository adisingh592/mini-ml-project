# HexaDisease: 6-Disease Cardiorenal-Metabolic AI Screening Platform
### Specialized Multi-Disease Triage, Machine Learning Classification & Clinical Guidance

Derived and cloned from **SehatSetu / ArogyaDrishti**, this project focuses exclusively on **The 6 Most Closely Related Tabular Diseases** that form the critical cardiorenal-metabolic-vascular axis in clinical medicine.

---

## 📌 The 6 Core Tabular Diseases & Biological Rationale

In clinical physiology, these 6 conditions do not exist in silos; their laboratory biomarkers cross-communicate and accelerate mutual systemic pathology:

```
                  ┌─────────────────────────────────────────┐
                  │       Cardiorenal-Vascular Axis         │
                  └────────────────────┬────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
  [1. Diabetes]                [2. Stroke]                   [3. Heart Failure]
  Glucose / HbA1c              BP / Atherosclerosis          LVEF / CPK / Lipids
        │                              │                              │
        └──────────────────────────────┼──────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
  [4. Kidney Disease]          [5. Maternal/HTN]             [6. Clinical Anemia]
  Creatinine / eGFR            Gestational Pressure          Hemoglobin / PCV
```

1. **Diabetes Mellitus (Metabolic)**: Glycemic dysregulation and microvascular injury that damages glomeruli and accelerates atherosclerosis.
2. **Cerebrovascular Stroke (Vascular / Neurological)**: Acute neurological deficits driven by chronic uncontrolled hypertension, carotid plaque, and elevated blood glucose.
3. **Heart Failure & Cardiac Risk (Cardiovascular)**: Left ventricular dysfunction (reduced LVEF), cardiorenal azotemia, and myocardial strain compounded by dyslipidemia.
4. **Chronic Kidney Disease (CKD) (Renal)**: Glomerular filtration degradation (eGFR, serum creatinine, proteinuria) which induces secondary renal anemia and cardiorenal syndrome.
5. **Hypertension / Maternal Vascular Risk (Vascular)**: Hemodynamic strain, preeclampsia threshold monitoring, and acute vascular resistance.
6. **Clinical Anemia (Hematology / Oxygen Transport)**: Deficient oxygen-carrying capacity (hemoglobin, hematocrit/PCV) which exacerbates both cardiac failure and tissue hypoxia in CKD.

---

## 📊 Model Coverage & Evaluation Benchmarks

All 6 models are trained and saved under `models/tabular/<disease>/` with evaluation reports in `results/tabular/<disease>/`:

| # | Disease / Condition | Domain | Best ML Architecture | Test Accuracy | F1-Score | Primary Clinical Inputs |
|:-|:---|:---|:---|:---:|:---:|:---|
| 1 | **Diabetes Mellitus** | Metabolic | Random Forest (BRFSS) | **75.0%** | **74.9%** | Fasting Glucose, HbA1c, BMI, BP, Cholesterol |
| 2 | **Cerebrovascular Stroke** | Vascular / Neuro | Random Forest Ensemble | **80.5%** | **85.7%** | Systolic BP, Diastolic BP, Glucose, BMI, Smoking |
| 3 | **Heart Failure & Cardiac Risk** | Cardiovascular | Random Forest Mortality | **85.0%** | **84.3%** | Ejection Fraction (LVEF), CPK, Creatinine, Sodium |
| 4 | **Chronic Kidney Disease (CKD)** | Renal | Logistic Regression | **100.0%** | **100.0%** | Serum Creatinine, Blood Urea, Urine Albumin, eGFR |
| 5 | **Hypertension / Maternal Risk** | Vascular | Random Forest Classifier | **84.2%** | **84.3%** | Systolic BP, Diastolic BP, Blood Sugar (BS), HR |
| 6 | **Clinical Anemia** | Hematology | Logistic Regression CBC | **100.0%** | **100.0%** | Hemoglobin (Hb), Hematocrit (PCV), RBC Count |

---

## 📁 Repository Structure

```text
HexaDisease/
├── api.py                                # Production Flask REST API with CORS
├── requirements.txt                      # Python dependencies (scikit-learn, pandas, flask)
├── start_dev.bat                         # One-click Windows development startup
├── README.md                             # Platform architecture & documentation
│
├── datasets/                             # Dedicated datasets ONLY for the 6 diseases
│   ├── diabetes/                         # CDC BRFSS 50/50 balanced health indicators CSV
│   ├── stroke/                           # Kaggle Stroke Prediction dataset CSV
│   ├── heart_disease/                    # UCI Heart Failure clinical records CSV
│   ├── kidney_disease/                   # Apollo Hospitals CKD full ARFF dataset
│   ├── hypertension_maternal_risk/       # UCI Maternal Health Risk dataset CSV
│   └── anemia/                           # Clinical Anemia & Hemoglobin dataset CSV
│
├── training/                             # Dedicated standalone training scripts
│   ├── train_all.py                      # Master pipeline that trains all 6 models
│   ├── diabetes/train.py                 # Evaluates LR, DT, RF, SVM on Diabetes
│   ├── stroke/train.py                   # Evaluates LR, DT, RF, SVM on Stroke
│   ├── heart_disease/train.py            # Evaluates LR, DT, RF, SVM on Heart Failure
│   ├── kidney_disease/train.py           # Evaluates LR, DT, RF, SVM on CKD
│   ├── hypertension_maternal_risk/train.py # Evaluates LR, DT, RF, SVM on Maternal Risk
│   └── anemia/train.py                   # Evaluates LR, DT, RF, SVM on Anemia
│
├── models/tabular/                       # Saved trained models (*_model.pkl & *_preprocessor.pkl)
│   ├── diabetes/
│   ├── stroke/
│   ├── heart_disease/
│   ├── kidney_disease/
│   ├── hypertension_maternal_risk/
│   └── anemia/
│
├── results/tabular/                      # Confusion matrices, CSV comparisons & text reports
│   ├── all_models_summary.csv            # Master benchmark comparison
│   ├── diabetes/
│   ├── stroke/
│   ├── heart_disease/
│   ├── kidney_disease/
│   ├── hypertension_maternal_risk/
│   └── anemia/
│
├── prediction/                           # Direct tabular inference engine
│   └── tabular_prediction.py             # Single-disease prediction API & feature alignment
│
├── report_analysis/                      # Ingestion, OCR & clinical triage engine
│   ├── analyze_report.py                 # Master report triage coordinator
│   ├── model_bridge.py                   # 6-disease Meta-Classifier & population imputer
│   ├── clinical_rules.py                 # Deterministic cuts (WHO, ADA, AHA, KDIGO, ACOG)
│   ├── report_parser.py                  # Regex biomarker extractor
│   ├── report_reader.py                  # PDF / Image OCR / TXT reader
│   └── sample_reports/                   # 6 realistic sample lab reports for testing
│
├── recommendation/                       # Evidence-based health guidance
│   ├── disease_information.json          # Curated KB for ONLY these 6 diseases
│   └── recommendation_system.py          # Deterministic diet, activity & lifestyle retriever
│
└── frontend/                             # React 19 + Vite + Tailwind CSS Web Application
    ├── index.html                        # Anton & DM Sans editorial typography
    ├── package.json                      # React 19, Lucide, Tailwind, Framer Motion
    └── src/
        ├── context/AppContext.jsx        # API transport & global state
        ├── pages/HomePage.jsx            # Live 6-model cycling ticker & bento cards
        ├── pages/UploadPage.jsx          # Drag-and-drop ingestion & 6 sample presets
        ├── pages/AnalysisPage.jsx        # Extracted parameters table & meta-classifier routing
        ├── pages/ResultsPage.jsx         # Diagnostic risk summary, early staging, and fruits/diet
        ├── pages/TrackerPage.jsx         # Longitudinal health progress tracker & report comparison
        ├── pages/BiomarkersPage.jsx      # Plain-language biomarker encyclopedia & checkup guide
        ├── pages/GuidancePage.jsx        # 3-tier actionable nutrition & clinical precautions
        └── pages/PredictPage.jsx         # Interactive 6-disease laboratory for manual parameter testing
```

---

## 🔬 Early-Stage Detection & Disease Staging

A central pillar of this platform is **catching disease in the 100% reversible window** before permanent tissue damage occurs:

1. **Diabetes Mellitus**: Stage 0 (Optimal) $\to$ **Stage 1 (Pre-Diabetes / Impaired Fasting Glucose: FPG 100-125, HbA1c 5.7-6.4% - *Reversible Window!*)** $\to$ Stage 2 (Early Onset Type 2) $\to$ Stage 3 (Uncontrolled / Complicated).
2. **Cerebrovascular Stroke**: Stage 0 (Optimal) $\to$ **Stage 1 (Pre-Hypertensive Arterial Stress: BP 120-129/<80 - *Reversible Window!*)** $\to$ Stage 2 (Moderate Ischemic Strain) $\to$ Stage 3 (Severe Vascular Crisis).
3. **Heart Failure**: ACC/AHA Stage A (At-Risk / Asymptomatic) $\to$ **Stage B (Pre-Heart Failure: EF 41-49%, CPK elevation - *Early Warning!*)** $\to$ Stage C (Symptomatic) $\to$ Stage D (Advanced).
4. **Chronic Kidney Disease**: KDIGO Stage G1 (Optimal) $\to$ **Stage G2 (Early Mild Renal Stress: eGFR 60-89, Creatinine 1.2-1.4 - *Reversible with Hydration & Salt Cut!*)** $\to$ Stage G3 (Moderate) $\to$ Stage G4/G5 (Severe).
5. **Hypertension / Maternal Vascular Risk**: Optimal $\to$ **Stage 1 (Pre-Hypertensive Hemodynamic Stress: 120-139 / 80-89)** $\to$ Stage 2 (Established Hypertension) $\to$ Stage 3 (Severe Alert).
6. **Clinical Anemia**: Optimal O₂ $\to$ **WHO Stage 1 (Mild / Latent Anemia: Hb 11.0-11.9 g/dL - *100% Reversible with Iron Fruits!*)** $\to$ Stage 2 (Moderate) $\to$ Stage 3 (Severe).

---

## 🍎 Plain-Language Biomarker Encyclopedia & Recommended Fruits

Regular users often panic or struggle to interpret routine checkup bloodwork. For every biomarker (WBC, RBC, Hemoglobin, Fasting Glucose, HbA1c, Serum Creatinine, Blood Urea, Ejection Fraction, Systolic/Diastolic BP, CPK, Platelets), the platform provides:
- **Exact Reference Range & Delta ($\Delta$)**: Shows whether a reading is optimal, slightly elevated, or critical.
- **Why It Matters to Your Body**: Clear, human explanation of the biological function.
- **Routine Checkup Reassurance**: Explains common benign causes (e.g., dehydration, post-workout CPK, minor seasonal viral WBC shifts) so users do not unnecessarily panic or rush to emergency clinics.
- **How to Control on a Daily Level**:
  - **Recommended Fruits**: Clinically documented fruits that normalize specific biomarkers (e.g., Pomegranates & Amla for Hemoglobin; Green Apples & Cherries for Glucose; Bananas, Watermelon & Cantaloupe for Blood Pressure; Cranberries & Blueberries for Kidneys).
  - **Specific Dietary Actions**: Concrete low-GI, low-sodium, and antioxidant dietary habits.
  - **Exercise Regimen**: Gentle postprandial walks, 150 min/week aerobic conditioning, and stress reduction.

---

## 📈 Multi-Report History Tracking & Side-by-Side Comparison

Health is a continuous journey. When a user undergoes a follow-up lab test 3 months later:
- **Persistent Storage**: Automatically saves reports under user/patient profiles.
- **Trajectory Analysis**: Directly compares Report A (baseline) against Report B (follow-up).
- **Biomarker Deltas**: Calculates parameter changes ($old \to new$, $\pm \Delta$, $\%$ change) with `Improved` (Green), `Stable` (Blue), and `Worsened` (Red) trend indicators.
- **Personalized "What To Do Next"**: Congratulates positive improvements and generates tailored daily steps for any parameter requiring further attention.

---

## ☁️ Cloud Database Architecture for Vercel

The platform features a **dual-engine database architecture**:
- **Vercel Cloud Production**: Integrates with **PostgreSQL via Neon Serverless Postgres** (the official Vercel Marketplace database). Automatically activates when `DATABASE_URL` is set in Vercel environment variables.
- **Local Development**: Automatically falls back to **SQLite** (`database/hexadisease.db`) with identical relational schemas and zero setup required.
- **One-Click Vercel Deploy**: Configured via `vercel.json` with multi-service routing (`api.py` as serverless function and `frontend/dist` as global CDN static assets).

---

## 🚀 Quick Startup Guide

### 1. One-Click Windows Startup
Double-click `start_dev.bat` in the root folder. It will automatically launch:
* The Python Flask REST API on `http://localhost:8000`
* The React 19 web application on `http://localhost:5173`

### 2. Manual Startup
**Backend:**
```bash
python api.py
```

**Frontend:**
```bash
cd frontend
pnpm install
pnpm run dev
```

### 3. Re-train All 6 Models
```bash
python training/train_all.py
```

---

## 🌐 REST API Endpoints

* `GET /api/health`: System health and ML availability check.
* `GET /api/diseases`: Metadata, parameters, architectures, and benchmark metrics for all 6 models.
* `POST /api/analyze`: Multipart document upload (`file`) or JSON (`text`) analyzing clinical reports.
* `POST /api/predict`: Direct single-disease manual prediction (`{"disease": "diabetes", "features": {...}}`).
* `POST /api/reports/save`: Persist an analyzed report with patient details.
* `GET /api/reports/history`: Fetch all saved reports in chronological order.
* `GET /api/reports/<id>`: Retrieve single report details and full parameter breakdowns.
* `GET /api/reports/compare?report1=X&report2=Y`: Generate side-by-side comparative trajectory and "What To Do Next" guidance.
* `GET /api/biomarkers/encyclopedia`: Complete educational dictionary with reference ranges, importance, control tips, and recommended fruits.


---

## ⚕️ Clinical Disclaimer
This software is intended as an academic screening aid and educational platform. Model predictions and deterministic cutoffs do not constitute a definitive medical diagnosis. Users should always consult qualified healthcare providers regarding laboratory tests and treatment plans.
