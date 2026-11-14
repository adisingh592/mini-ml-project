"""
HexaDisease - Medical Report Parser
Extracts clinical laboratory biomarkers from clinical report text
strictly tailored for the 6 core tabular disease domains.
"""

import re

PARAMETERS = {
    # 1. Glycemic & Metabolic (Diabetes)
    "hba1c": ("HbA1c", "%", r"hb\s*a1c|\ba1c\b|glyc(?:at|osyl)ated\s*ha?emoglobin", None),
    "fasting_glucose": ("Fasting Blood Glucose", "mg/dL",
                        r"fasting\s*(?:blood|plasma)?\s*(?:sugar|glucose)|\bfbs\b|\bfbg\b|\bfpg\b|glucose[\s,\-]*\(?fasting", None),
    "pp_glucose": ("Post-Prandial Glucose", "mg/dL",
                   r"post\s*-?\s*prandial\s*(?:blood|plasma)?\s*(?:sugar|glucose)|\bppbs\b|\bppbg\b|glucose[\s,\-]*\(?(?:pp|post)", None),
    "random_glucose": ("Random Blood Glucose", "mg/dL",
                       r"random\s*(?:blood|plasma)?\s*(?:sugar|glucose)|\brbs\b|\brbg\b|estimated\s*average\s*glucose|\beag\b|^\s*(?:blood\s*|plasma\s*|serum\s*)?(?:sugar|glucose)\b",
                       r"fasting|prandial|\bpp\b|urine|\bfbs\b|\bppbs\b"),
    
    # 2. Hematology (Clinical Anemia)
    "hemoglobin": ("Hemoglobin", "g/dL", r"ha?emoglobin|\bhgb\b|\bhb\b", r"a1c|glyc|corpuscular|\bmch|urine"),
    "pcv": ("Hematocrit / PCV", "%", r"\bpcv\b|ha?ematocrit|\bhct\b|packed\s*cell\s*volume", None),
    "rbc": ("RBC Count", "million/uL", r"\brbc\b|red\s*blood\s*cell", r"morphology|urine|\brbc\s*/\s*hpf"),
    "wbc": ("Total WBC Count", "cells/uL", r"\bwbc\b|\btlc\b|total\s*leu[ck]ocyte|white\s*blood\s*cell|\btc\b", r"morphology"),
    "platelets": ("Platelet Count", "/uL", r"platelet|\bplt\b", r"volume|\bmpv\b|distribution"),

    # 3. Cardiovascular & Lipids (Heart Failure & Stroke)
    "total_cholesterol": ("Total Cholesterol", "mg/dL", r"total\s*cholesterol|cholesterol[\s,\-]*total|serum\s*cholesterol|^\s*cholesterol\b", r"hdl|ldl|ratio"),
    "hdl": ("HDL Cholesterol", "mg/dL", r"\bhdl\b", r"ratio|non[\s\-]*hdl"),
    "ldl": ("LDL Cholesterol", "mg/dL", r"\bldl\b", r"ratio"),
    "triglycerides": ("Triglycerides", "mg/dL", r"triglyceride|\btgl?\b", None),
    "ejection_fraction": ("Ejection Fraction (LVEF)", "%", r"ejection\s*fraction|\blvef\b|\bef\b", None),
    "cpk": ("Creatine Kinase (CPK)", "U/L", r"creatin(?:in)?e\s*(?:phospho)?\s*kinase|\bcpk\b|\bck\b", r"mb\b|\bck-?mb"),

    # 4. Renal Function (Chronic Kidney Disease)
    "creatinine": ("Serum Creatinine", "mg/dL", r"creatinine", r"kinase|phospho|clearance|ratio|urine|\bacr\b|albumin"),
    "urea": ("Blood Urea", "mg/dL", r"blood\s*urea|serum\s*urea|^\s*urea\b", r"nitrogen|\bbun\b|ratio"),
    "bun": ("Blood Urea Nitrogen", "mg/dL", r"\bbun\b|urea\s*nitrogen", r"ratio"),
    "sodium": ("Serum Sodium", "mmol/L", r"\bsodium\b|^\s*(?:serum\s*|s\.?\s*)?na\+?\b", None),
    "potassium": ("Serum Potassium", "mmol/L", r"\bpotassium\b|^\s*(?:serum\s*|s\.?\s*)?k\+?\b", None),
    "specific_gravity": ("Urine Specific Gravity", "", r"specific\s*gravity|\bsp\.?\s*gr", None),

    # 5. Hemodynamics & Maternal Parameters
    "heart_rate": ("Heart Rate / Pulse", "bpm", r"heart\s*rate|pulse|pulse\s*rate|\bbpm\b", None),
    "body_temperature": ("Body Temperature", "°F", r"body\s*temp(?:erature)?|temperature|temp", None),
    "bmi": ("BMI", "kg/m2", r"\bbmi\b|body\s*mass\s*index", None),
    "height": ("Height", "cm", r"\bheight\b", None),
    "weight": ("Weight", "kg", r"\bweight\b", r"birth|molecular")
}

PLAUSIBLE = {
    "hba1c": (3.0, 20.0),
    "fasting_glucose": (20.0, 1000.0),
    "pp_glucose": (20.0, 1000.0),
    "random_glucose": (20.0, 1000.0),
    "hemoglobin": (2.0, 25.0),
    "pcv": (5.0, 75.0),
    "rbc": (0.5, 10.0),
    "wbc": (500.0, 500000.0),
    "platelets": (1000.0, 3000000.0),
    "total_cholesterol": (50.0, 700.0),
    "hdl": (5.0, 200.0),
    "ldl": (10.0, 500.0),
    "triglycerides": (20.0, 5000.0),
    "ejection_fraction": (5.0, 95.0),
    "cpk": (5.0, 50000.0),
    "creatinine": (0.1, 30.0),
    "urea": (2.0, 400.0),
    "bun": (1.0, 200.0),
    "sodium": (100.0, 180.0),
    "potassium": (1.5, 10.0),
    "specific_gravity": (1.000, 1.050),
    "heart_rate": (30.0, 220.0),
    "body_temperature": (94.0, 108.0),
    "bmi": (10.0, 90.0),
    "height": (50.0, 250.0),
    "weight": (10.0, 400.0),
    "age": (0.0, 120.0),
    "systolic_bp": (60.0, 300.0),
    "diastolic_bp": (30.0, 200.0)
}

FLAGS = {
    "smoking": r"smok(?:er|ing|es)?",
    "hypertension": r"hypertension|hypertensive|\bhtn\b",
    "diabetes_history": r"diabet(?:es|ic)",
    "stroke_history": r"stroke|\btia\b",
    "heart_disease": r"heart\s*disease|cardiac|coronary|\bcad\b|myocardial"
}

def display_name(key):
    if key in PARAMETERS:
        return PARAMETERS[key][0]
    return key.replace("_", " ").title()

def unit_of(key):
    if key in PARAMETERS:
        return PARAMETERS[key][1]
    if "bp" in key:
        return "mmHg"
    return ""

def _parse_first_float(line):
    matches = re.findall(r"\b\d+(?:\.\d+)?\b", line)
    for m in matches:
        try:
            return float(m)
        except ValueError:
            pass
    return None

def _extract_bp(text):
    match = re.search(r"\b(?:bp|blood\s*pressure)?\s*[:\s]?\s*(\d{2,3})\s*/\s*(\d{2,3})\s*(?:mm\s*hg)?\b", text, re.I)
    if match:
        s = float(match.group(1))
        d = float(match.group(2))
        if 60 <= s <= 300 and 30 <= d <= 200:
            return s, d
    return None, None

def _extract_demographics(text):
    demo = {}
    age_match = re.search(r"\b(?:age|years?\s*old)[\s:]*(\d{1,3})\b", text, re.I)
    if age_match:
        val = float(age_match.group(1))
        if 0 <= val <= 120:
            demo["age"] = val
            
    sex_match = re.search(r"\b(?:sex|gender)[\s:]*(male|female|m|f)\b", text, re.I)
    if sex_match:
        s = sex_match.group(1).lower()
        demo["sex"] = "male" if s in ["m", "male"] else "female"
        
    return demo

def _extract_flags(text):
    flags = {}
    for flag_key, pattern in FLAGS.items():
        m = re.search(rf"\b({pattern})[\s:]*(yes|no|positive|negative|true|false)\b", text, re.I)
        if m:
            ans = m.group(2).lower()
            flags[flag_key] = ans in ["yes", "positive", "true"]
    return flags

def parse_report(text):
    """
    Parses a clinical report string and extracts structured lab biomarker readings.
    """
    extracted = {}
    
    # 1. Extract demographics
    extracted.update(_extract_demographics(text))
    
    # 2. Extract Blood Pressure
    s_bp, d_bp = _extract_bp(text)
    if s_bp is not None:
        extracted["systolic_bp"] = s_bp
        extracted["diastolic_bp"] = d_bp
        
    # 3. Extract Medical History flags
    extracted.update(_extract_flags(text))
    
    # 4. Line by line parameter extraction
    lines = text.splitlines()
    for line in lines:
        clean_line = line.strip()
        if not clean_line or len(clean_line) < 3:
            continue
            
        for param, (name, unit, pattern, exclude) in PARAMETERS.items():
            if param in extracted:
                continue
                
            if re.search(pattern, clean_line, re.I):
                if exclude and re.search(exclude, clean_line, re.I):
                    continue
                    
                val = _parse_first_float(clean_line)
                if val is not None:
                    # Check plausibility
                    low, high = PLAUSIBLE.get(param, (0, 1e6))
                    if low <= val <= high:
                        extracted[param] = val

    # Qualitative urine markers
    if re.search(r"urine\s*albumin|proteinuria", text, re.I):
        if re.search(r"\b(trace|1\+|\+)\b", text, re.I):
            extracted["urine_albumin"] = 1
        elif re.search(r"\b(2\+\+|2\+)\b", text, re.I):
            extracted["urine_albumin"] = 2
        elif re.search(r"\b(3\+\+\+|3\+)\b", text, re.I):
            extracted["urine_albumin"] = 3
        elif re.search(r"\b(nil|negative|normal)\b", text, re.I):
            extracted["urine_albumin"] = 0

    if re.search(r"urine\s*(?:sugar|glucose)", text, re.I):
        if re.search(r"\b(trace|1\+|\+)\b", text, re.I):
            extracted["urine_sugar"] = 1
        elif re.search(r"\b(2\+\+|2\+)\b", text, re.I):
            extracted["urine_sugar"] = 2
        elif re.search(r"\b(nil|negative|normal)\b", text, re.I):
            extracted["urine_sugar"] = 0

    return extracted

def normalize_manual_values(v_dict):
    out = {}
    for k, val in v_dict.items():
        if val is None:
            continue
        try:
            val_f = float(val)
            low, high = PLAUSIBLE.get(k, (-1e9, 1e9))
            if low <= val_f <= high:
                out[k] = val_f
        except ValueError:
            s = str(val).lower()
            if s in ["true", "yes", "positive"]:
                out[k] = True
            elif s in ["false", "no", "negative"]:
                out[k] = False
            elif k == "sex" and s in ["male", "m", "female", "f"]:
                out[k] = "male" if s in ["m", "male"] else "female"
    return out
