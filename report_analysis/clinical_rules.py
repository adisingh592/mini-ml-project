"""
HexaDisease - Clinical Rule Engine
Deterministic laboratory reference ranges and triage cut-offs strictly for the 6 core diseases:
1. Diabetes Mellitus (ADA 2024 Standards of Care)
2. Cerebrovascular Stroke & Vascular Pressures (AHA/ASA Guidelines)
3. Heart Failure & Cardiac Lipids (ACC/AHA / NCEP ATP III)
4. Chronic Kidney Disease (KDIGO 2012 / CKD-EPI 2021)
5. Hypertension & Maternal Vascular Risk (ACOG Practice Bulletins)
6. Clinical Anemia (WHO Diagnostic Criteria)
"""

NORMAL, BORDERLINE, ABNORMAL, URGENT = 0, 1, 2, 3
SEVERITY_LABELS = {
    NORMAL: "Normal",
    BORDERLINE: "Borderline",
    ABNORMAL: "Abnormal",
    URGENT: "Urgent"
}

def finding(condition, parameter, value, unit, severity, message, reference, kb_disease=None):
    return {
        "condition": condition,
        "parameter": parameter,
        "value": value,
        "unit": unit,
        "severity": severity,
        "status": SEVERITY_LABELS[severity],
        "message": message,
        "reference": reference,
        "kb_disease": kb_disease,
    }

def is_female(v):
    return str(v.get("sex", "")).lower() == "female"

# -------------------------------------------------------------
# 1. DIABETES MELLITUS (ADA 2024 Standards of Care)
# -------------------------------------------------------------
def check_diabetes(v):
    out = []
    ref = "ADA Standards of Care: HbA1c >=6.5% / FPG >=126 / 2-h PG >=200 / random PG >=200 mg/dL = diabetes"
    c, kb = "Diabetes Mellitus", "Diabetes"

    if "hba1c" in v:
        x = v["hba1c"]
        if x >= 6.5:
            out.append(finding(c, "HbA1c", x, "%", ABNORMAL, "In the diabetes range (>= 6.5%).", ref, kb))
        elif x >= 5.7:
            out.append(finding(c, "HbA1c", x, "%", BORDERLINE, "Prediabetes range (5.7 - 6.4%).", ref, kb))
        else:
            out.append(finding(c, "HbA1c", x, "%", NORMAL, "Normal (< 5.7%).", ref))

    if "fasting_glucose" in v:
        x = v["fasting_glucose"]
        if x < 54:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", URGENT, "Critically low blood sugar (< 54 mg/dL, Level 2 hypoglycemia).", ref, kb))
        elif x >= 126:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", ABNORMAL, "In the diabetes range (>= 126 mg/dL).", ref, kb))
        elif x >= 100:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", BORDERLINE, "Impaired fasting glucose / prediabetes (100 - 125 mg/dL).", ref, kb))
        elif x < 70:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", BORDERLINE, "Mild hypoglycemia (< 70 mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", NORMAL, "Normal (70 - 99 mg/dL).", ref))

    if "pp_glucose" in v:
        x = v["pp_glucose"]
        if x >= 200:
            out.append(finding(c, "Post-Prandial Glucose", x, "mg/dL", ABNORMAL, "In the diabetes range (>= 200 mg/dL).", ref, kb))
        elif x >= 140:
            out.append(finding(c, "Post-Prandial Glucose", x, "mg/dL", BORDERLINE, "Impaired glucose tolerance (140 - 199 mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Post-Prandial Glucose", x, "mg/dL", NORMAL, "Normal (< 140 mg/dL).", ref))

    if "random_glucose" in v:
        x = v["random_glucose"]
        if x >= 400:
            out.append(finding(c, "Random Glucose", x, "mg/dL", URGENT, "Severe hyperglycemia (>= 400 mg/dL) - risk of diabetic ketoacidosis.", ref, kb))
        elif x >= 200:
            out.append(finding(c, "Random Glucose", x, "mg/dL", ABNORMAL, "In the diabetes range (>= 200 mg/dL).", ref, kb))
        elif x < 54:
            out.append(finding(c, "Random Glucose", x, "mg/dL", URGENT, "Severely low blood glucose (< 54 mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Random Glucose", x, "mg/dL", NORMAL, "Below diabetes diagnostic cut-off (< 200 mg/dL).", ref))

    if v.get("urine_sugar", 0) >= 1:
        out.append(finding(c, "Urine Sugar", v["urine_sugar"], "grade", BORDERLINE, "Glycosuria present - suggests blood glucose exceeded renal threshold.", ref, kb))
        
    return out

# -------------------------------------------------------------
# 2. CEREBROVASCULAR STROKE RISK & BLOOD PRESSURE
# -------------------------------------------------------------
def check_stroke_and_vascular_bp(v):
    out = []
    ref_bp = "2017 ACC/AHA: <120/<80 normal, 120-129/<80 elevated, 130-139 or 80-89 stage 1, >=140 or >=90 stage 2, >180/120 crisis"
    
    if "systolic_bp" in v and "diastolic_bp" in v:
        s, d = v["systolic_bp"], v["diastolic_bp"]
        val = f"{s:.0f}/{d:.0f}"
        c, kb = "Cerebrovascular Stroke Risk", "Stroke"

        if s > 180 or d > 120:
            out.append(finding(c, "Blood Pressure", val, "mmHg", URGENT, "Hypertensive Crisis (> 180/120) - extreme acute stroke risk.", ref_bp, kb))
        elif s >= 140 or d >= 90:
            out.append(finding(c, "Blood Pressure", val, "mmHg", ABNORMAL, "Stage 2 Hypertension (>= 140/90) - significant long-term stroke predictor.", ref_bp, kb))
        elif s >= 130 or d >= 80:
            out.append(finding(c, "Blood Pressure", val, "mmHg", ABNORMAL, "Stage 1 Hypertension (130-139 / 80-89 mmHg).", ref_bp, kb))
        elif s >= 120:
            out.append(finding(c, "Blood Pressure", val, "mmHg", BORDERLINE, "Elevated blood pressure (120-129 / < 80 mmHg).", ref_bp, kb))
        elif s < 90 or d < 60:
            out.append(finding(c, "Blood Pressure", val, "mmHg", BORDERLINE, "Hypotension (< 90/60 mmHg).", ref_bp))
        else:
            out.append(finding(c, "Blood Pressure", val, "mmHg", NORMAL, "Normal healthy blood pressure (< 120/80 mmHg).", ref_bp))

    if v.get("stroke_history"):
        out.append(finding("Cerebrovascular Stroke Risk", "Stroke History", "Reported", "", ABNORMAL, "Prior TIA/Stroke reported - secondary prophylaxis indicated.", "AHA/ASA Guidelines", "Stroke"))

    return out

# -------------------------------------------------------------
# 3. HEART FAILURE & CARDIAC RISK (AHA/ACC / NCEP ATP III)
# -------------------------------------------------------------
def check_heart_failure_and_lipids(v):
    out = []
    c, kb = "Heart Failure & Cardiac Risk", "Heart_Disease"
    
    if "ejection_fraction" in v:
        x = v["ejection_fraction"]
        ref_ef = "2022 AHA/ACC/HFSA heart failure: EF <=40% HFrEF (reduced), 41-49% HFmrEF, >=50% HFpEF (preserved)"
        if x <= 40:
            out.append(finding(c, "Ejection Fraction (LVEF)", x, "%", ABNORMAL, "Reduced ejection fraction (<= 40%) - characteristic of systolic heart failure.", ref_ef, kb))
        elif x < 50:
            out.append(finding(c, "Ejection Fraction (LVEF)", x, "%", BORDERLINE, "Mildly reduced ejection fraction (41 - 49%).", ref_ef, kb))
        else:
            out.append(finding(c, "Ejection Fraction (LVEF)", x, "%", NORMAL, "Normal preserved ejection fraction (>= 50%).", ref_ef))

    if "cpk" in v:
        x = v["cpk"]
        ref_cpk = "Reference CPK: 30 - 200 U/L"
        if x > 500:
            out.append(finding(c, "CPK (Creatine Kinase)", x, "U/L", ABNORMAL, "Markedly elevated CPK - suggests myocardial or skeletal muscle stress.", ref_cpk, kb))
        elif x > 200:
            out.append(finding(c, "CPK (Creatine Kinase)", x, "U/L", BORDERLINE, "Mildly elevated CPK.", ref_cpk, kb))
        else:
            out.append(finding(c, "CPK (Creatine Kinase)", x, "U/L", NORMAL, "Normal CPK.", ref_cpk))

    ref_lip = "NCEP ATP III lipid risk guidelines"
    if "total_cholesterol" in v:
        x = v["total_cholesterol"]
        sev, msg = (ABNORMAL, "High (>= 240 mg/dL) - atherogenic risk.") if x >= 240 else \
                   (BORDERLINE, "Borderline high (200 - 239 mg/dL).") if x >= 200 else (NORMAL, "Desirable (< 200 mg/dL).")
        out.append(finding(c, "Total Cholesterol", x, "mg/dL", sev, msg, ref_lip, kb if sev else None))

    if "ldl" in v:
        x = v["ldl"]
        sev, msg = (ABNORMAL, "Very high (>= 190 mg/dL).") if x >= 190 else \
                   (ABNORMAL, "High (160 - 189 mg/dL).") if x >= 160 else \
                   (BORDERLINE, "Borderline high (130 - 159 mg/dL).") if x >= 130 else (NORMAL, "Acceptable (< 130 mg/dL).")
        out.append(finding(c, "LDL Cholesterol", x, "mg/dL", sev, msg, ref_lip, kb if sev else None))

    if "hdl" in v:
        x, low = v["hdl"], 50 if is_female(v) else 40
        if x < low:
            out.append(finding(c, "HDL Cholesterol", x, "mg/dL", BORDERLINE, f"Low HDL (< {low} mg/dL) - reduces cardioprotection.", ref_lip, kb))
        else:
            out.append(finding(c, "HDL Cholesterol", x, "mg/dL", NORMAL, f"Acceptable (>= {low} mg/dL).", ref_lip))

    if "triglycerides" in v:
        x = v["triglycerides"]
        sev, msg = (URGENT, "Critical hypertriglyceridemia (>= 1000 mg/dL) - acute pancreatitis risk.") if x >= 1000 else \
                   (ABNORMAL, "High (>= 200 mg/dL).") if x >= 200 else \
                   (BORDERLINE, "Borderline elevated (150 - 199 mg/dL).") if x >= 150 else (NORMAL, "Normal (< 150 mg/dL).")
        out.append(finding(c, "Triglycerides", x, "mg/dL", sev, msg, ref_lip, kb if sev else None))

    return out

# -------------------------------------------------------------
# 4. CHRONIC KIDNEY DISEASE (KDIGO 2012 / CKD-EPI 2021)
# -------------------------------------------------------------
def egfr_ckd_epi_2021(creatinine, age, female):
    kappa, alpha = (0.7, -0.241) if female else (0.9, -0.302)
    ratio = creatinine / kappa
    egfr = 142 * min(ratio, 1) ** alpha * max(ratio, 1) ** -1.200 * 0.9938 ** age
    return egfr * 1.012 if female else egfr

def check_kidney(v):
    out = []
    ref = "KDIGO 2012 CKD staging: eGFR >=90 G1, 60-89 G2, 45-59 G3a, 30-44 G3b, 15-29 G4, <15 G5"
    c, kb = "Chronic Kidney Disease (CKD)", "Chronic_Kidney_Disease"

    if "creatinine" in v and "age" in v and "sex" in v:
        egfr = round(egfr_ckd_epi_2021(v["creatinine"], v["age"], is_female(v)), 1)
        v["egfr"] = egfr
        if egfr < 15:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", URGENT, "Kidney failure range (Stage G5, < 15).", ref, kb))
        elif egfr < 30:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", ABNORMAL, "Severely reduced kidney function (Stage G4, 15 - 29).", ref, kb))
        elif egfr < 60:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", ABNORMAL, "Moderately reduced kidney function (Stage G3, 30 - 59).", ref, kb))
        elif egfr < 90:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", BORDERLINE if egfr < 75 else NORMAL,
                               "Mildly reduced (Stage G2, 60 - 89) - significant in presence of proteinuria.", ref, kb if egfr < 75 else None))
        else:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", NORMAL, "Normal kidney function (Stage G1, >= 90).", ref))
    elif "creatinine" in v:
        x, high = v["creatinine"], 1.1 if is_female(v) else 1.3
        if x > high:
            out.append(finding(c, "Serum Creatinine", x, "mg/dL", ABNORMAL, f"Elevated above normal upper limit ({high} mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Serum Creatinine", x, "mg/dL", NORMAL, f"Within normal limits (<= {high} mg/dL).", ref))

    if "urea" in v:
        x = v["urea"]
        if x > 100:
            out.append(finding(c, "Blood Urea", x, "mg/dL", ABNORMAL, "Severely elevated blood urea (> 100 mg/dL).", ref, kb))
        elif x > 45:
            out.append(finding(c, "Blood Urea", x, "mg/dL", BORDERLINE, "Elevated blood urea (> 45 mg/dL) - azotemia.", ref, kb))
        else:
            out.append(finding(c, "Blood Urea", x, "mg/dL", NORMAL, "Normal (15 - 45 mg/dL).", ref))

    if v.get("urine_albumin", 0) >= 1:
        sev = ABNORMAL if v["urine_albumin"] >= 2 else BORDERLINE
        out.append(finding(c, "Urine Albumin (Proteinuria)", v["urine_albumin"], "grade", sev, "Protein in urine detected - direct marker of glomerular membrane injury.", ref, kb))

    return out

# -------------------------------------------------------------
# 5. HYPERTENSION & MATERNAL VASCULAR RISK (ACOG Guidelines)
# -------------------------------------------------------------
def check_maternal_and_hypertension_risk(v):
    out = []
    c, kb = "Hypertension / Maternal Vascular Risk", "Maternal_Health_Risk"
    ref = "ACOG Practice Bulletin #222: Gestational Hypertension & Preeclampsia (>=140/90; severe range >=160/110)"
    
    if "systolic_bp" in v and "diastolic_bp" in v:
        s, d = v["systolic_bp"], v["diastolic_bp"]
        val = f"{s:.0f}/{d:.0f}"
        if s >= 160 or d >= 110:
            out.append(finding(c, "Vascular Pressure", val, "mmHg", URGENT, "Severe-range hypertension (>= 160/110) - acute maternal vascular emergency cut-off.", ref, kb))
        elif s >= 140 or d >= 90:
            out.append(finding(c, "Vascular Pressure", val, "mmHg", ABNORMAL, "Hypertensive threshold (>= 140/90) - diagnostic for gestational/vascular hypertension.", ref, kb))
        elif s >= 130 or d >= 80:
            out.append(finding(c, "Vascular Pressure", val, "mmHg", BORDERLINE, "Elevated hemodynamic baseline (130-139 / 80-89 mmHg).", ref, kb))

    if "heart_rate" in v:
        hr = v["heart_rate"]
        ref_hr = "Resting maternal hemodynamics: 60 - 100 bpm"
        if hr > 110:
            out.append(finding(c, "Heart Rate", hr, "bpm", BORDERLINE, "Tachycardia (> 110 bpm) - reflects hyperdynamic circulation or dehydration.", ref_hr, kb))
        elif hr < 50:
            out.append(finding(c, "Heart Rate", hr, "bpm", BORDERLINE, "Bradycardia (< 50 bpm).", ref_hr))

    if "body_temperature" in v:
        temp = v["body_temperature"]
        ref_temp = "Normal body temperature: 97.0 - 99.0 °F"
        if temp >= 100.4:
            out.append(finding(c, "Body Temperature", temp, "°F", ABNORMAL, "Fever (>= 100.4 °F / 38 °C) - systemic inflammation or maternal infection.", ref_temp, kb))

    return out

# -------------------------------------------------------------
# 6. CLINICAL ANEMIA (WHO Guidelines)
# -------------------------------------------------------------
def check_anemia(v):
    out = []
    c, kb = "Clinical Anemia", "Anemia"
    ref = "WHO: Hb <13 g/dL (men) / <12 g/dL (women); moderate 8-10.9; severe <8; critical <7 g/dL"

    if "hemoglobin" in v:
        x = v["hemoglobin"]
        low = 12.0 if is_female(v) else 13.0
        if x < 7.0:
            out.append(finding(c, "Hemoglobin", x, "g/dL", URGENT, "Critical severe anemia (< 7.0 g/dL) - clinical transfusion evaluation range.", ref, kb))
        elif x < 8.0:
            out.append(finding(c, "Hemoglobin", x, "g/dL", ABNORMAL, "Severe anemia (7.0 - 7.9 g/dL) - urgent medical correction required.", ref, kb))
        elif x < 11.0:
            out.append(finding(c, "Hemoglobin", x, "g/dL", ABNORMAL, "Moderate anemia (8.0 - 10.9 g/dL) - limits tissue oxygen delivery.", ref, kb))
        elif x < low:
            out.append(finding(c, "Hemoglobin", x, "g/dL", BORDERLINE, f"Mild anemia (< {low} g/dL).", ref, kb))
        elif x > 18.5:
            out.append(finding(c, "Hemoglobin", x, "g/dL", ABNORMAL, "Elevated hemoglobin (> 18.5 g/dL) - polycythemia risk.", ref))
        else:
            out.append(finding(c, "Hemoglobin", x, "g/dL", NORMAL, f"Normal hemoglobin (>= {low} g/dL).", ref))

    if "pcv" in v:
        x = v["pcv"]
        ref_pcv = "Hematocrit (PCV): 36 - 46% (female) / 41 - 50% (male)"
        low_pcv = 36.0 if is_female(v) else 41.0
        if x < 25.0:
            out.append(finding(c, "Hematocrit (PCV)", x, "%", ABNORMAL, "Significantly low packed cell volume (< 25%).", ref_pcv, kb))
        elif x < low_pcv:
            out.append(finding(c, "Hematocrit (PCV)", x, "%", BORDERLINE, f"Low hematocrit (< {low_pcv}%).", ref_pcv, kb))

    if "rbc" in v:
        x = v["rbc"]
        ref_rbc = "RBC count: 4.0 - 5.4 M/uL (women) / 4.5 - 5.9 M/uL (men)"
        if x < 3.8:
            out.append(finding(c, "RBC Count", x, "million/uL", BORDERLINE, "Low circulating red blood cell count (< 3.8 M/uL).", ref_rbc, kb))

    return out

# -------------------------------------------------------------
# MASTER RULE RUNNER FOR 6 DISEASES
# -------------------------------------------------------------
def run_clinical_rules(values):
    """
    Evaluates clinical laboratory parameters against deterministic rules
    strictly for the 6 core tabular diseases.
    """
    findings = []
    findings.extend(check_diabetes(values))
    findings.extend(check_stroke_and_vascular_bp(values))
    findings.extend(check_heart_failure_and_lipids(values))
    findings.extend(check_kidney(values))
    findings.extend(check_maternal_and_hypertension_risk(values))
    findings.extend(check_anemia(values))
    return findings
