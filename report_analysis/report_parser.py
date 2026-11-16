"""
HexaDisease - Medical Report Parser
Extracts clinical laboratory biomarkers from clinical report text
strictly tailored for the 6 core tabular disease domains.
Supports both single-line key-value reports and multi-line tabular PDF/OCR reports.
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
    "hemoglobin": ("Hemoglobin", "g/dL", r"ha?emoglobin\s*(?:\(hb\))?|\bhgb\b|\bhb\b", r"a1c|glyc|corpuscular|\bmch|urine"),
    "pcv": ("Hematocrit / PCV", "%", r"\bpcv\b|ha?ematocrit|\bhct\b|packed\s*cell\s*volume", None),
    "rbc": ("RBC Count", "million/uL", r"red\s*blood\s*cell\s*count|\brbc\b", r"morphology|urine|\brbc\s*/\s*hpf"),
    "wbc": ("Total WBC Count", "cells/uL", r"total\s*(?:leukocyte|white\s*blood\s*cell)\s*count|\bwbc\b|\btlc\b|total\s*leu[ck]ocyte|\btc\b", r"morphology"),
    "platelets": ("Platelet Count", "/uL", r"platelet\s*count|platelet|\bplt\b", r"volume|\bmpv\b|distribution"),
    "ferritin": ("Serum Ferritin", "ng/mL", r"serum\s*ferritin|\bferritin\b", None),

    # 3. Cardiovascular & Lipids (Heart Failure & Stroke)
    "total_cholesterol": ("Total Cholesterol", "mg/dL", r"total\s*(?:serum\s*)?cholesterol|cholesterol[\s,\-]*total|serum\s*cholesterol|^\s*cholesterol\b", r"hdl|ldl|ratio"),
    "hdl": ("HDL Cholesterol", "mg/dL", r"\bhdl\b|high[\s\-]*density\s*lipoprotein", r"ratio|non[\s\-]*hdl"),
    "ldl": ("LDL Cholesterol", "mg/dL", r"\bldl\b|low[\s\-]*density\s*lipoprotein", r"ratio"),
    "triglycerides": ("Triglycerides", "mg/dL", r"triglycerides?|\btgl?\b", None),
    "ejection_fraction": ("Ejection Fraction (LVEF)", "%", r"ejection\s*fraction|\blvef\b|\bef\b", None),
    "cpk": ("Creatine Kinase (CPK)", "U/L", r"total\s*creatine\s*kinase|creatin(?:in)?e\s*(?:phospho)?\s*kinase|\bcpk\b|\bck\b", r"mb\b|\bck-?mb"),
    "ck_mb": ("Creatine Kinase-MB (CK-MB)", "ng/mL", r"creatine\s*kinase[\s\-]*mb|\bck[\s\-]*mb\b", None),
    "troponin": ("Troponin", "ng/mL", r"high[\s\-]*sensitivity\s*troponin|troponin(?:\s*[-–]?\s*[it])?|\b(?:hs-)?c?tni\b|\b(?:hs-)?c?tnt\b", None),
    "nt_probnp": ("NT-proBNP", "pg/mL", r"nt[\s\-]*probnp|\bbnp\b|brain\s*natriuretic", None),
    "crp": ("C-Reactive Protein (CRP)", "mg/L", r"(?:hs-)?crp\b|c[\s\-]*reactive\s*protein", None),

    # 4. Renal Function (Chronic Kidney Disease)
    "creatinine": ("Serum Creatinine", "mg/dL", r"serum\s*creatinine|\bcreatinine\b", r"kinase|phospho|clearance|ratio|urine|\bacr\b|albumin"),
    "urea": ("Blood Urea", "mg/dL", r"blood\s*urea|serum\s*urea|^\s*urea\b", r"nitrogen|\bbun\b|ratio"),
    "bun": ("Blood Urea Nitrogen", "mg/dL", r"\bbun\b|urea\s*nitrogen", r"ratio"),
    "egfr": ("Estimated GFR (eGFR)", "mL/min/1.73m²", r"estimated\s*gfr|\begfr\b|glomerular\s*filtration", None),
    "sodium": ("Serum Sodium", "mmol/L", r"\bsodium\b|^\s*(?:serum\s*|s\.?\s*)?na\+?\b", None),
    "potassium": ("Serum Potassium", "mmol/L", r"\bpotassium\b|^\s*(?:serum\s*|s\.?\s*)?k\+?\b", None),
    "specific_gravity": ("Urine Specific Gravity", "", r"specific\s*gravity|\bsp\.?\s*gr", None),

    # 5. Hemodynamics & Maternal Parameters
    "systolic_bp": ("Systolic Blood Pressure", "mmHg", r"resting\s*systolic(?:\s*blood)?\s*pressure|systolic(?:\s*blood)?\s*pressure|\bsystolic\b|\btrestbps\b|\bsbp\b", None),
    "diastolic_bp": ("Diastolic Blood Pressure", "mmHg", r"resting\s*diastolic(?:\s*blood)?\s*pressure|diastolic(?:\s*blood)?\s*pressure|\bdiastolic\b|\bdbp\b", None),
    "heart_rate": ("Heart Rate / Pulse", "bpm", r"(?:maximum\s*)?heart\s*rate|pulse|pulse\s*rate|\bthalach\b|\bbpm\b", None),
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
    "ferritin": (1.0, 10000.0),
    "total_cholesterol": (50.0, 700.0),
    "hdl": (5.0, 200.0),
    "ldl": (10.0, 500.0),
    "triglycerides": (20.0, 5000.0),
    "ejection_fraction": (5.0, 95.0),
    "cpk": (5.0, 50000.0),
    "ck_mb": (0.1, 1000.0),
    "troponin": (0.001, 50000.0),
    "nt_probnp": (5.0, 100000.0),
    "crp": (0.1, 500.0),
    "creatinine": (0.1, 30.0),
    "urea": (2.0, 400.0),
    "bun": (1.0, 200.0),
    "egfr": (1.0, 200.0),
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

def _parse_first_float(s):
    """
    Parses the first valid float from a string, safely handling comma thousand-separators (e.g. 7,400 or 245,000).
    """
    if not s:
        return None
    cleaned = s.replace(",", "")
    m = re.search(r"[-+]?\b\d+(?:\.\d+)?\b", cleaned)
    if m:
        try:
            return float(m.group(0))
        except ValueError:
            pass
    return None

def _extract_bp(text):
    """
    Finds blood pressure in formats like:
    - 142/90 or 142 / 90
    - BP: 142/90 mmHg
    - 142 / 90 mmHg
    """
    match = re.search(r"\b(?:bp|blood\s*pressure)?\s*[:\s]?\s*(\d{2,3})\s*/\s*(\d{2,3})\s*(?:mm\s*hg)?\b", text, re.I)
    if match:
        s = float(match.group(1))
        d = float(match.group(2))
        if 60 <= s <= 300 and 30 <= d <= 200:
            return s, d
    return None, None

def _extract_demographics(text):
    demo = {}
    
    # Age matching (e.g. "Age: 54", "54 Years", "54 Yrs", "Age / Gender: 54 Years / Male")
    age_match = re.search(r"\b(?:age|years?\s*old)[\s:/]*(\d{1,3})\b", text, re.I)
    if age_match:
        val = float(age_match.group(1))
        if 0 <= val <= 120:
            demo["age"] = val
    else:
        # Fallback for "54 Years / Male" or "54 yrs"
        alt_age = re.search(r"\b(\d{1,3})\s*(?:years|yrs)\b", text, re.I)
        if alt_age:
            val = float(alt_age.group(1))
            if 0 <= val <= 120:
                demo["age"] = val

    # Gender matching
    sex_match = re.search(r"\b(?:sex|gender)[\s:/]*(male|female|m|f)\b", text, re.I)
    if sex_match:
        s = sex_match.group(1).lower()
        demo["sex"] = "male" if s in ["m", "male"] else "female"
    else:
        # Fallback for "Male" / "Female" standalone tokens near patient details
        if re.search(r"\b(?:years?\s*/\s*)?male\b", text, re.I):
            demo["sex"] = "male"
        elif re.search(r"\b(?:years?\s*/\s*)?female\b", text, re.I):
            demo["sex"] = "female"
            
    return demo

def _extract_flags(text):
    flags = {}
    for flag_key, pattern in FLAGS.items():
        m = re.search(rf"\b({pattern})[\s:]*(yes|no|positive|negative|true|false)\b", text, re.I)
        if m:
            ans = m.group(2).lower()
            flags[flag_key] = ans in ["yes", "positive", "true"]
    return flags

def _is_section_header(line):
    """
    Returns True if the line represents a panel or section header (e.g. '1. COMPLETE BLOOD COUNT (HEMATOLOGY PANEL)')
    rather than an individual clinical parameter.
    """
    if re.match(r"^\d+\.\s+[A-Z\s\(\)\-\&]+(?:PANEL|PROFILE|SECTION|COUNT|TEST|PARAMETERS)", line, re.I):
        return True
    if re.match(r"^(?:Test\s*Parameter|Observed\s*Value|Reference\s*Interval|Unit|Flag)\b", line, re.I):
        return True
    return False

def parse_report(text):
    """
    Parses a clinical report string and extracts structured lab biomarker readings.
    Supports single-line key-value reports, colon/dash separated reports, and
    multi-line tabular PDF/OCR formats.
    """
    extracted = {}
    
    # 1. Extract demographics (Age, Gender)
    extracted.update(_extract_demographics(text))
    
    # 2. Extract combined Blood Pressure (e.g. 142/90)
    s_bp, d_bp = _extract_bp(text)
    if s_bp is not None:
        extracted["systolic_bp"] = s_bp
        extracted["diastolic_bp"] = d_bp
        
    # 3. Extract Medical History flags
    extracted.update(_extract_flags(text))
    
    # 4. Multi-line and single-line biomarker parameter extraction
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    
    for i, line in enumerate(lines):
        if len(line) < 2 or _is_section_header(line):
            continue
            
        for param, (name, unit, pattern, exclude) in PARAMETERS.items():
            if param in extracted:
                continue
                
            match = re.search(pattern, line, re.I)
            if not match:
                continue
                
            if exclude and re.search(exclude, line, re.I):
                continue
                
            val = None
            
            # Step A: Check if the value appears on the SAME line AFTER the parameter keyword
            # Example: "Fasting Blood Sugar: 168 mg/dL"
            text_after = line[match.end():].strip()
            if text_after:
                val = _parse_first_float(text_after)
                
            # Step B: If not after the keyword, check if the entire line has a single number
            # (only if the line does not start with a numbering bullet like '1. ')
            if val is None and not re.match(r"^\d+[\.\)]\s*", line):
                val = _parse_first_float(line)
                
            # Step C: If still None, look ahead 1 to 4 lines (handles multi-line table column PDF extractions)
            # Example:
            # Line i:   "Fasting Blood Glucose (FBG)"
            # Line i+1: "168.0"
            # Line i+2: "mg/dL"
            if val is None:
                for lookahead in range(1, 5):
                    if i + lookahead >= len(lines):
                        break
                    candidate_line = lines[i + lookahead]
                    
                    # Stop if lookahead encounters another test parameter name or section header
                    if _is_section_header(candidate_line):
                        break
                    if any(re.search(p[2], candidate_line, re.I) for p in PARAMETERS.values() if p[2] != pattern):
                        break
                        
                    cand_val = _parse_first_float(candidate_line)
                    if cand_val is not None:
                        val = cand_val
                        break
                        
            # Validate plausibility
            if val is not None:
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
