# ArogyaDrishti (HexaDisease)
## AI-Driven Multi-Disease Early Detection, Biomarker Literacy, and Longitudinal Health Tracking
**Academic & Technical Project Report**  
*Focus Domain:* 6 Core Cardiorenal-Metabolic & Vascular Conditions  
*Date:* November 2026  

---

## 1. Executive Abstract

**Abstract—** Modern clinical medicine frequently encounters patients who experience subtle, non-specific physiological symptoms or undergo routine preventive blood tests but lack the medical literacy to interpret numerical lab biomarkers. Consequently, individuals either panic unnecessarily or neglect borderline laboratory elevations until disease progresses to an irreversible chronic state. This project introduces **ArogyaDrishti (HexaDisease)**, a specialized machine learning and medical literacy platform focused strictly on the **six most closely related tabular disease domains**: Diabetes Mellitus, Cerebrovascular Stroke, Heart Failure & Cardiac Risk, Chronic Kidney Disease (CKD), Hypertension / Maternal Vascular Risk, and Clinical Anemia. The system incorporates automated regex-driven laboratory document ingestion (PDF, image, and raw text), multi-model classification (Random Forest, Logistic Regression, Decision Trees, and Support Vector Machines), deterministic clinical consensus rule validation (ADA, ACC/AHA, KDIGO, ACOG, and WHO standards), and 4-tier early-stage severity grading. Beyond binary diagnosis, the platform demystifies complex biomarkers (e.g., WBC, Creatinine, Fasting Glucose, Hemoglobin, CPK) in plain human language, prescribes daily non-pharmaceutical preventive actions (specifically curated dietary fruits, hydration, and exercise), and features a persistent dual-engine database (Neon Serverless Postgres on Vercel Cloud with local SQLite fallback) that performs longitudinal report-to-report delta ($\Delta$) tracking over time. Empirical validation demonstrated exceptional diagnostic fidelity, including 100.0% accuracy on renal and hematologic markers, 85.0% on heart failure mortality risk, 95.2% on stroke, and 75.0% on population-scale diabetes indicators.

---

## 2. Project Motivation & Clinical Objectives ("Why I Made That")

### 2.1 The Clinical Gap
Millions of individuals undergo routine health checkups each year. However, laboratory reports are delivered in dense clinical terminology laden with cryptic abbreviations (e.g., eGFR, HbA1c, LVEF, CPK, uACR) and statistical reference limits. Regular people face two acute dilemmas:
1. **Health Anxiety & Unnecessary Clinic Visits:** Seeing a slightly flagged value (such as a transient rise in CPK after an unaccustomed gym workout or mild urea elevation from simple dehydration) causes anxiety and emergency doctor visits when lifestyle hydration or rest was all that was needed.
2. **The "Silent Killer" Neglect:** Subtle borderline elevations (such as a Fasting Blood Glucose of 112 mg/dL or a Systolic Blood Pressure of 126 mmHg) produce zero pain or outward symptoms. Patients ignore them for years until they wake up with irreversible Stage 2 Type 2 Diabetes, hypertensive kidney disease, or myocardial damage.

### 2.2 Primary Project Objectives
* **Early-Stage Detection in the 100% Reversible Window:** Predict not just disease presence, but the exact severity stage (Stage 0: Normal $\to$ Stage 1: Pre-Disease Early Warning $\to$ Stage 2: Established $\to$ Stage 3: Severe). Catching patients in Stage 1 allows lifestyle reversal before pharmaceutical dependency.
* **Biomarker Demystification & Health Literacy:** Explain each laboratory parameter in plain words: what it is, its biological role in the human body, whether the current value is high or low, and how far it deviates from healthy bounds.
* **Actionable Daily Natural Controls (Diet, Fruits & Exercise):** Rather than leaving patients stranded, provide immediate dietary modifications, clinically supported fruits (e.g., pomegranates for hemoglobin, berries for glycemic control, watermelon for renal flush), and daily physical routines.
* **Longitudinal Report-to-Report Tracking:** Enable users to store medical records over months and years, running automated side-by-side comparative analyses to compute net biomarker deltas ($\pm\Delta$) and determine if lifestyle interventions are succeeding.
* **Production Cloud Deployment:** Architect a dual-engine database and REST API optimized for 1-click Vercel serverless deployment using Neon PostgreSQL.

---

## 3. The 6 Target Diseases & Their Biological Interconnectivity

Unlike disjointed medical prediction tools that group unrelated illnesses, HexaDisease is strictly scoped around the **Cardiorenal-Metabolic and Vascular Axis**. In human physiology, these six conditions are deeply interconnected through shared hemodynamic, glycemic, and microvascular feedback loops:

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

1. **Diabetes Mellitus (Metabolic Axis):** Insulin resistance and pancreatic $\beta$-cell exhaustion leading to persistent hyperglycemia and microvascular injury that damages kidney glomeruli and accelerates arterial atherosclerosis.
2. **Cerebrovascular Stroke (Vascular / Neurological Axis):** Arterial stiffening, endothelial shear stress, and carotid plaque rupture causing cerebral ischemia or hemorrhage, accelerated by hypertension and hyperglycemia.
3. **Heart Failure & Cardiac Risk (Cardiovascular Axis):** Left ventricular myocardial exhaustion, reduced ejection fraction (LVEF), and enzyme leakage under ischemic strain compounded by cardiorenal azotemia.
4. **Chronic Kidney Disease (CKD) (Renal Axis):** Glomerular filtration degradation and nephron loss causing nitrogenous waste (creatinine, urea) retention and proteinuria, leading directly to secondary renal anemia.
5. **Hypertension / Maternal Vascular Risk (Vascular Axis):** Acute systemic vascular resistance, preeclampsia risk, and gestational placental perfusion pressure spikes.
6. **Clinical Anemia (Hematology / Oxygen Transport Axis):** Depleted hemoglobin and erythrocyte counts reducing arterial oxygen-carrying capacity, exacerbating both myocardial failure and tissue hypoxia in renal disease.

---

## 4. Datasets Used, Features & Official Direct Links

To ensure clinical validity and benchmark reproducibility, all datasets were curated from internationally accredited medical repositories:

| Disease Modality | Dataset Source & Citation | Samples & Features | Official Dataset Link / Repository |
| :--- | :--- | :--- | :--- |
| **Diabetes Mellitus** | CDC Behavioral Risk Factor Surveillance System (BRFSS 2015 50-50 Balanced Split) | 70,692 patient records<br/>21 clinical & lifestyle features | [Kaggle CDC BRFSS Dataset](https://www.kaggle.com/datasets/alexteb/diabetes-health-indicators-dataset) |
| **Cerebrovascular Stroke** | Kaggle Healthcare Stroke Prediction Callset (McKinsey & Co. Hospital Dataset) | 5,110 patient records<br/>11 physiological attributes | [Kaggle Stroke Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset) |
| **Heart Failure & Cardiac Risk** | UCI Machine Learning Repository / BMC Medical Informatics (Chicco & Jurman, 2020) | 299 clinical records<br/>12 serum & cardiac attributes | [UCI Heart Failure Dataset](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records) |
| **Chronic Kidney Disease (CKD)** | UCI Machine Learning Repository / Apollo Hospitals Clinical ARFF (Soundarapandian et al.) | 400 patient records<br/>24 multi-analyte lab features | [UCI CKD Dataset](https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease) |
| **Hypertension / Maternal Risk** | UCI Machine Learning Repository / Daffodil International Hospital Risk (Ahmed et al.) | 1,014 maternal records<br/>6 hemodynamic features | [UCI Maternal Health Risk Dataset](https://archive.ics.uci.edu/dataset/863/maternal+health+risk) |
| **Clinical Anemia** | Kaggle Complete Blood Count (CBC) & Conjunctival Diagnostic Callset | 1,421 patient records<br/>5 complete CBC features | [Kaggle Anemia CBC Dataset](https://www.kaggle.com/datasets/biswaranjanrao/anemia-dataset) |

---

## 5. Machine Learning Models & Comparative Benchmarking

Each disease modality was trained under a stratified 80/20 train-test evaluation across four distinct algorithmic families:
* **Logistic Regression (LR):** Interpretable linear log-odds classifier providing probabilistic confidence.
* **Decision Tree (DT):** Non-linear hierarchical rule-based classifier based on Gini impurity.
* **Random Forest (RF):** Ensemble bagging with bootstrap aggregation and multiple decision trees.
* **Support Vector Machine (SVM):** Maximum-margin hyperplane with Radial Basis Function (RBF) kernel.

### 5.1 Benchmark Performance Summary

| Condition | Clinical Axis | Optimal Classifier | Accuracy | Precision | Recall | F1-Score | Specificity |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Diabetes Mellitus** | Metabolic | Random Forest (100 Trees) | **75.0%** | 75.2% | 75.0% | **74.9%** | 70.4% |
| **Cerebrovascular Stroke** | Vascular / Neuro | Logistic Regression / RF | **95.2%** | 95.4% | 95.2% | **93.0%** | 100.0% |
| **Heart Failure & Cardiac Risk** | Cardiovascular | Random Forest Ensemble | **85.0%** | 85.1% | 85.0% | **84.3%** | 95.1% |
| **Chronic Kidney Disease (CKD)** | Renal Axis | Logistic Regression | **100.0%** | 100.0% | 100.0% | **100.0%** | 100.0% |
| **Hypertension & Maternal Risk** | Vascular Axis | Random Forest Classifier | **95.1%** | 95.1% | 95.1% | **95.1%** | 96.6% |
| **Clinical Anemia** | Hematology | Logistic Regression CBC | **100.0%** | 100.0% | 100.0% | **100.0%** | 100.0% |

### 5.2 Key Algorithmic Insights
1. **Ensemble Supremacy in Heterogeneous Phenotypes:** Random Forest outperformed linear models in Heart Failure (85.0%), Maternal Hypertension (95.1%), and Diabetes (75.0%) due to its capability to capture non-linear threshold interactions (e.g. LVEF < 40% combined with CPK > 300).
2. **Linear Determinism in Direct Laboratory Biomarkers:** Chronic Kidney Disease and Clinical Anemia achieved 100.0% accuracy under regularized Logistic Regression because renal (creatinine, blood urea, albumin) and hematologic (hemoglobin, RBC) biomarkers follow mathematically sharp diagnostic boundaries established by clinical consensus (KDIGO and WHO).

---

## 6. Visual Analytics & Scientific Figures

Five high-resolution 300 DPI figures were generated and saved in `results/report_figures/`:
* **Figure 1 (Performance Heatmap):** `fig1_master_performance_heatmap.png` — High-level summary of model metrics across all diseases.
* **Figure 2 (Architecture Comparison):** `fig2_model_architecture_comparison.png` — 4-panel algorithmic comparison for methodology sections.
* **Figure 3 (Confusion Matrix Panel):** `fig3_confusion_matrices_panel.png` — Multi-class validation and error analysis.
* **Figure 4 (Biomarker Correlation Heatmap):** `fig4_biomarker_correlation_heatmap.png` — Pearson correlation matrix illustrating the cardiorenal-metabolic syndrome.
* **Figure 5 (Radar Profile):** `fig5_model_radar_profile.png` — Spider chart summarizing overall diagnostic balance.

---

## 7. Frontend & Backend Tech Stack Architecture

The application is structured into decoupled frontend and backend microservices:

| Layer | Technology | Role & Implementation Details |
| :--- | :--- | :--- |
| **Frontend Framework** | React 19 & Vite 8 | Ultra-fast client build (820ms), responsive component tree, client-side routing, and real-time state management. |
| **Styling & UX** | Tailwind CSS & Lucide Icons | Publication-grade aesthetics, responsive data tables, fluid typography, and accessible visual alert badges. |
| **REST API Server** | Python 3 & Flask with CORS | Microservices routing endpoints for document analysis (`/api/analyze`), manual testing (`/api/predict`), and report history. |
| **Machine Learning** | Scikit-Learn, NumPy & Pandas | Trained model pipelines with `StandardScaler` preprocessors serialized into compact, production-ready `.pkl` files. |
| **Document Ingestion** | PyMuPDF (fitz) & Regex Parser | Multi-format parser extracting clinical numbers from PDF, digital scans, and plain text with plausible-range validation. |
| **Cloud Database (Vercel)** | Neon Serverless PostgreSQL | Official Vercel Marketplace PostgreSQL integration via `DATABASE_URL`; persistent relational storage for reports and tracking. |
| **Local Zero-Config DB** | SQLite (`hexadisease.db`) | Automatic fallback for local development with identical schema and zero cloud setup requirements. |
| **Cloud Hosting** | Vercel Functions & Edge CDN | `vercel.json` multi-service deployment combining serverless Python functions with global edge static frontend assets. |

---

## 8. Biomarker Literacy, Recommended Fruits & Daily Controls

For every parameter, the platform provides:
* **White Blood Cells (WBC) (Normal: 4,500 – 11,000 cells/mcL):** Immune defense soldiers. Mild elevations often reflect benign post-viral shifts. *Fruits:* Citrus, Papaya, Kiwi.
* **Hemoglobin (Hb) (Normal: 12.0 – 17.5 g/dL):** Oxygen delivery protein. *Fruits:* Pomegranates (highest clinically documented booster), Amla, Dates, Figs.
* **Fasting Glucose (Normal: 70 – 99 mg/dL):** Baseline insulin sensitivity. *Fruits:* Green Apples, Tart Cherries (low GI 22), Blueberries, Jamun. *Controls:* 15-minute gentle postprandial walks.
* **Serum Creatinine (Normal: 0.6 – 1.2 mg/dL):** Glomerular filtration efficiency. *Fruits:* Cranberries, Watermelon (natural hydration and urea flushing).
* **Systolic Blood Pressure (Normal: 90 – 119 mmHg):** Arterial pumping pressure. *Fruits:* Bananas & Cantaloupe (high potassium), Watermelon (L-citrulline). *Controls:* DASH diet, 5-minute deep breathing.
* **Ejection Fraction (EF) (Normal: 50% – 70%):** Myocardial pumping capacity. *Fruits:* Pomegranates, Blueberries, Papaya. *Controls:* Sodium restricted to 1,500 mg/day.

---

## 9. Longitudinal Multi-Report Comparison & Progress Tracking

The longitudinal comparison engine subtracts baseline values from follow-up values ($\Delta = \text{Current} - \text{Baseline}$):
* **Net Biomarker Deltas:** Computes absolute change and percentage progression.
* **Trajectory Badging:** Flags markers as `IMPROVED` (Green), `STABLE` (Blue), or `WORSENED` (Red).
* **Health Score Progression:** Quantifies overall wellness shift (e.g. from 66 to 85 out of 100).
* **Automated Clinical Action Plan:** Recommends next dietary steps and schedule for follow-up testing.

---

## 10. Conclusion & Clinical Disclaimer

**Conclusion:** ArogyaDrishti demonstrates that combining machine learning classifiers with plain-language biomarker education and longitudinal progress tracking bridges the critical divide between laboratory diagnostic data and patient empowerment. By focusing on early reversible windows, common individuals can take daily control of their health through diet, fruits, and exercise before chronic cardiorenal-metabolic diseases take root.

**Clinical Disclaimer:** This software and technical report are intended strictly as an academic screening aid and educational literacy platform. Model outputs and algorithmic stage assessments do not constitute a definitive medical diagnosis. Users must always consult a licensed medical practitioner for clinical treatment decisions.
