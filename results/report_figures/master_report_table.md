# HexaDisease: Optimal Machine Learning Diagnostic Performance

| Condition | Clinical Axis | Optimal Classifier | Accuracy | Precision | Recall | F1-Score | Specificity |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Diabetes Mellitus** | Metabolic | Random Forest | 75.0% | 75.2% | 75.0% | 74.9% | 70.4% |
| **Cerebrovascular Stroke** | Vascular / Neurological | Logistic Regression | 95.2% | 95.4% | 95.2% | 93.0% | 100.0% |
| **Heart Failure & Cardiac Risk** | Cardiovascular | Random Forest | 85.0% | 85.1% | 85.0% | 84.3% | 95.1% |
| **Chronic Kidney Disease (CKD)** | Renal Axis | Logistic Regression | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| **Hypertension & Maternal Risk** | Vascular Axis | Random Forest | 95.1% | 95.1% | 95.1% | 95.1% | 96.6% |
| **Clinical Anemia** | Hematology / O₂ Transport | Logistic Regression | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

### Key Benchmark Takeaways for Project Report
- **Ensemble Bagging Performance**: Random Forest demonstrated the highest F1-scores and robustness across high-dimensional, non-linear clinical datasets (Heart Failure, Maternal Hypertension, and Diabetes).
- **Linear Separability**: Direct quantitative clinical lab cutoffs in Renal diagnostics (Serum Creatinine, Blood Urea) and Hematology (Hemoglobin concentration) achieved 100% sensitivity and specificity under regularized Logistic Regression.
- **Vascular Risk Detection**: High specificity (>95%) across all cardiovascular and stroke classifiers minimizes catastrophic false negative clinical triage.
