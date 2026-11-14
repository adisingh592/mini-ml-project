"""
HexaDisease - Report-to-Model Bridge with Meta-Classifier & Adaptive Imputer
Maps clinical parameters parsed from lab documents onto the 6 trained tabular models:
1. Diabetes Mellitus (Metabolic)
2. Cerebrovascular Stroke (Vascular / Neurological)
3. Heart Failure & Cardiac Risk (Cardiovascular)
4. Chronic Kidney Disease (CKD) (Renal)
5. Hypertension / Maternal Vascular Risk (Vascular)
6. Clinical Anemia (Hematology / Oxygen Transport)
"""

import math
import os
import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABULAR_MODELS_DIR = os.path.join(PROJECT_ROOT, "models", "tabular")

POPULATION_DEFAULTS = {
    "age": 45.0,
    "bmi": 24.2,
    "sex": "female",
    "smoking": False,
    "hypertension": False,
    "body_temperature": 98.6,
    "heart_rate": 72.0
}

def flag(v, key, derived=None):
    stated = v.get(key)
    if key == "smoking" and stated == "former":
        stated = False
    if not isinstance(stated, bool):
        stated = None
    if stated is True or derived is True:
        return True
    if stated is False or derived is False:
        return False
    return None

def has_hypertension(v):
    if "systolic_bp" in v:
        return v["systolic_bp"] >= 130 or v.get("diastolic_bp", 80) >= 80
    return None

def has_diabetes(v):
    if v.get("hba1c") is not None:
        return v["hba1c"] >= 6.5
    if v.get("fasting_glucose") is not None:
        return v["fasting_glucose"] >= 126
    return None

def has_anaemia(v):
    if v.get("hemoglobin") is None:
        return None
    return v["hemoglobin"] < (12.0 if str(v.get("sex", "")).lower() == "female" else 13.0)

def any_glucose(v):
    for key in ("random_glucose", "fasting_glucose", "pp_glucose"):
        if v.get(key) is not None:
            return v[key]
    return None

def as01(x):
    return None if x is None else (1 if x else 0)

def yes_no(x):
    return None if x is None else ("yes" if x else "no")

def brfss_age_group(age):
    if age is None:
        age = POPULATION_DEFAULTS["age"]
    if age < 25:
        return 1
    return min(13, int((age - 25) // 5) + 2)

def sex01(v):
    s = v.get("sex") or POPULATION_DEFAULTS["sex"]
    return 1 if str(s).lower() == "male" else 0

# -------------------------------------------------------------
# 1. PER-MODEL FEATURE BUILDERS
# -------------------------------------------------------------
def build_diabetes(v, assumed_tracker):
    bmi = v.get("bmi")
    if bmi is None:
        if v.get("weight") and v.get("height"):
            h_m = v["height"] / 100.0
            bmi = round(v["weight"] / (h_m * h_m), 1)
        else:
            bmi = POPULATION_DEFAULTS["bmi"]
            assumed_tracker.add("BMI (default 24.2)")

    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    raw = {
        "HighBP": as01(flag(v, "hypertension", has_hypertension(v))),
        "HighChol": as01(v["total_cholesterol"] >= 240) if "total_cholesterol" in v else None,
        "CholCheck": 1 if "total_cholesterol" in v else None,
        "BMI": bmi,
        "Smoker": as01(flag(v, "smoking")),
        "Stroke": as01(flag(v, "stroke_history")),
        "HeartDiseaseorAttack": as01(flag(v, "heart_disease")),
        "PhysActivity": None,
        "Fruits": None,
        "Veggies": None,
        "HvyAlcoholConsump": None,
        "AnyHealthcare": 1,
        "NoDocbcCost": 0,
        "GenHlth": None,
        "MentHlth": 0,
        "PhysHlth": 0,
        "DiffWalk": None,
        "Sex": sex01(v),
        "Age": brfss_age_group(age),
        "Education": None,
        "Income": None
    }
    return raw, assumed_tracker

def build_stroke(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    sex = v.get("sex") or POPULATION_DEFAULTS["sex"]
    smoking = v.get("smoking")
    
    raw = {
        "gender": str(sex).capitalize(),
        "age": age,
        "hypertension": as01(flag(v, "hypertension", has_hypertension(v))),
        "heart_disease": as01(flag(v, "heart_disease")),
        "ever_married": None,
        "work_type": None,
        "Residence_type": None,
        "avg_glucose_level": any_glucose(v),
        "bmi": v.get("bmi") or POPULATION_DEFAULTS["bmi"],
        "smoking_status": None if smoking is None else
            ("formerly smoked" if smoking == "former" else "smokes" if smoking else "never smoked")
    }
    return raw, assumed_tracker

def build_heart(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    raw = {
        "age": age,
        "anaemia": as01(has_anaemia(v)),
        "creatinine_phosphokinase": v.get("cpk"),
        "diabetes": as01(flag(v, "diabetes_history", has_diabetes(v))),
        "ejection_fraction": v.get("ejection_fraction"),
        "high_blood_pressure": as01(flag(v, "hypertension", has_hypertension(v))),
        "platelets": v.get("platelets"),
        "serum_creatinine": v.get("creatinine"),
        "serum_sodium": v.get("sodium"),
        "sex": sex01(v),
        "smoking": as01(flag(v, "smoking")),
        "time": None
    }
    return raw, assumed_tracker

def build_kidney(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    raw = {
        "age": age,
        "bp": v.get("diastolic_bp"),
        "sg": v.get("specific_gravity"),
        "al": v.get("urine_albumin"),
        "su": v.get("urine_sugar"),
        "rbc": None, "pc": None, "pcc": None, "ba": None,
        "bgr": any_glucose(v),
        "bu": v.get("urea"),
        "sc": v.get("creatinine"),
        "sod": v.get("sodium"),
        "pot": v.get("potassium"),
        "hemo": v.get("hemoglobin"),
        "pcv": v.get("pcv"),
        "wbcc": v.get("wbc"),
        "rbcc": v.get("rbc"),
        "htn": yes_no(flag(v, "hypertension", has_hypertension(v))),
        "dm": yes_no(flag(v, "diabetes_history", has_diabetes(v))),
        "cad": yes_no(flag(v, "heart_disease")),
        "appet": None,
        "pe": None,
        "ane": yes_no(has_anaemia(v))
    }
    return raw, assumed_tracker

def build_hypertension_maternal_risk(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = 29.0
        assumed_tracker.add("Maternal Age (default 29)")
        
    s_bp = v.get("systolic_bp")
    if s_bp is None:
        s_bp = 120.0
        assumed_tracker.add("Systolic BP (default 120)")
        
    d_bp = v.get("diastolic_bp")
    if d_bp is None:
        d_bp = 80.0
        assumed_tracker.add("Diastolic BP (default 80)")
        
    # Convert glucose to mmol/L (dataset unit is mmol/L e.g. 7.0 - 15.0)
    gluc = any_glucose(v)
    if gluc is not None:
        bs_mmol = round(gluc / 18.0, 1) if gluc > 30 else float(gluc)
    else:
        bs_mmol = 7.5
        assumed_tracker.add("Blood Glucose (default 7.5 mmol/L)")
        
    body_temp = v.get("body_temperature") or POPULATION_DEFAULTS["body_temperature"]
    heart_rate = v.get("heart_rate") or POPULATION_DEFAULTS["heart_rate"]
    
    raw = {
        "Age": age,
        "SystolicBP": s_bp,
        "DiastolicBP": d_bp,
        "BS": bs_mmol,
        "BodyTemp": body_temp,
        "HeartRate": heart_rate
    }
    return raw, assumed_tracker

def build_anemia(v, assumed_tracker):
    hb = v.get("hemoglobin")
    if hb is None:
        hb = 12.5
        assumed_tracker.add("Hemoglobin (default 12.5 g/dL)")

    raw = {
        "%Red Pixel": None,
        "%Green pixel": None,
        "%Blue pixel": None,
        "Hb": hb
    }
    return raw, assumed_tracker

# -------------------------------------------------------------
# 2. 6-DISEASE META-CLASSIFIER CATALOG
# -------------------------------------------------------------
MODEL_CATALOG = [
    {
        "folder": "diabetes",
        "slug": "diabetes",
        "label": "Diabetes Mellitus Model",
        "category": "Metabolic",
        "builder": build_diabetes,
        "primary_markers": ["fasting_glucose", "hba1c", "random_glucose", "pp_glucose", "bmi"],
        "secondary_markers": ["total_cholesterol", "hdl", "ldl", "triglycerides", "systolic_bp", "age"],
        "min_primary_threshold": 1,
        "base_weight": 1.0,
        "kb_disease": "Diabetes"
    },
    {
        "folder": "stroke",
        "slug": "stroke",
        "label": "Cerebrovascular Stroke Risk Model",
        "category": "Vascular / Neurological",
        "builder": build_stroke,
        "primary_markers": ["systolic_bp", "diastolic_bp", "fasting_glucose", "random_glucose"],
        "secondary_markers": ["bmi", "smoking", "age", "heart_disease"],
        "min_primary_threshold": 1,
        "base_weight": 0.9,
        "kb_disease": "Stroke"
    },
    {
        "folder": "heart_disease",
        "slug": "heart_disease",
        "label": "Heart Failure & Cardiac Risk Model",
        "category": "Cardiovascular",
        "builder": build_heart,
        "primary_markers": ["ejection_fraction", "cpk", "total_cholesterol", "ldl", "hdl", "triglycerides"],
        "secondary_markers": ["systolic_bp", "creatinine", "sodium", "fasting_glucose"],
        "min_primary_threshold": 1,
        "base_weight": 0.9,
        "kb_disease": "Heart_Disease"
    },
    {
        "folder": "kidney_disease",
        "slug": "kidney_disease",
        "label": "Chronic Kidney Disease (CKD) Model",
        "category": "Renal",
        "builder": build_kidney,
        "primary_markers": ["creatinine", "urea", "bun", "urine_albumin", "specific_gravity"],
        "secondary_markers": ["hemoglobin", "sodium", "potassium", "wbc", "rbc", "systolic_bp"],
        "min_primary_threshold": 1,
        "base_weight": 1.0,
        "kb_disease": "Chronic_Kidney_Disease"
    },
    {
        "folder": "hypertension_maternal_risk",
        "slug": "hypertension_maternal_risk",
        "label": "Hypertension & Maternal Risk Model",
        "category": "Vascular",
        "builder": build_hypertension_maternal_risk,
        "primary_markers": ["systolic_bp", "diastolic_bp", "heart_rate", "body_temperature"],
        "secondary_markers": ["fasting_glucose", "random_glucose", "age"],
        "min_primary_threshold": 1,
        "base_weight": 0.95,
        "kb_disease": "Maternal_Health_Risk"
    },
    {
        "folder": "anemia",
        "slug": "anemia",
        "label": "Clinical Anemia CBC Model",
        "category": "Hematology / Oxygen Transport",
        "builder": build_anemia,
        "primary_markers": ["hemoglobin", "pcv", "rbc"],
        "secondary_markers": ["platelets", "wbc"],
        "min_primary_threshold": 1,
        "base_weight": 1.0,
        "kb_disease": "Anemia"
    }
]

def compute_model_affinity(catalog_item, extracted_values):
    primaries = [m for m in catalog_item["primary_markers"] if extracted_values.get(m) is not None]
    secondaries = [m for m in catalog_item["secondary_markers"] if extracted_values.get(m) is not None]

    p_score = len(primaries) / len(catalog_item["primary_markers"]) if catalog_item["primary_markers"] else 0
    s_score = len(secondaries) / len(catalog_item["secondary_markers"]) if catalog_item["secondary_markers"] else 0

    has_primary = len(primaries) >= catalog_item["min_primary_threshold"]
    total_score = (p_score * 0.7 + s_score * 0.3) * catalog_item["base_weight"]

    return {
        "catalog": catalog_item,
        "has_primary": has_primary,
        "primary_hits": primaries,
        "total_hits": len(primaries) + len(secondaries),
        "affinity_score": round(total_score, 3)
    }

def select_models(extracted_values):
    scored = [compute_model_affinity(item, extracted_values) for item in MODEL_CATALOG]
    selected = [s for s in scored if s["has_primary"]]
    
    if not selected:
        scored.sort(key=lambda x: (x["total_hits"], x["affinity_score"]), reverse=True)
        candidates = [s for s in scored if s["total_hits"] > 0]
        selected = candidates[:2] if candidates else scored[:1]
        
    return selected

def assemble_features(feature_names, raw):
    row, covered = [], 0
    for name in feature_names:
        name = str(name)
        source_key, value = None, None
        if name in raw:
            source_key, value = name, raw[name]
        else:
            for key in sorted(raw, key=len, reverse=True):
                if name.startswith(key + "_"):
                    source_key = key
                    if raw[key] is not None:
                        category = name[len(key) + 1:].lower()
                        value = 1.0 if category == str(raw[key]).lower() else 0.0
                    break
        if value is None or source_key is None:
            row.append(math.nan)
        else:
            row.append(float(value))
            covered += 1
    return row, covered

def load_model(folder):
    model_path = os.path.join(TABULAR_MODELS_DIR, folder, f"{folder}_model.pkl")
    preproc_path = os.path.join(TABULAR_MODELS_DIR, folder, f"{folder}_preprocessor.pkl")
    if not (os.path.exists(model_path) and os.path.exists(preproc_path)):
        return None, None
    return joblib.load(model_path), joblib.load(preproc_path)

def positive_probability(model, X):
    if not hasattr(model, "predict_proba"):
        return float(model.predict(X)[0])
    probs = model.predict_proba(X)[0]
    classes = list(getattr(model, "classes_", range(len(probs))))
    index = classes.index(1) if 1 in classes else len(probs) - 1
    return float(probs[index])

def run_models(values):
    """
    Executes the Meta-Classifier and adaptive inference strictly for the 6 core models.
    """
    try:
        import numpy as np
        import pandas as pd
    except ImportError:
        return [{"model": "all", "status": "unavailable", "reason": "numpy/pandas/scikit-learn not available"}]

    selected_affinities = select_models(values)
    results = []

    for selection in selected_affinities:
        item = selection["catalog"]
        folder = item["folder"]
        
        entry = {
            "model": folder,
            "label": item["label"],
            "category": item.get("category", "Clinical"),
            "kb_disease": item.get("kb_disease"),
            "affinity_score": selection["affinity_score"],
            "primary_markers_matched": selection["primary_hits"]
        }

        try:
            model, preprocessor = load_model(folder)
        except Exception as e:
            entry.update(status="unavailable", reason=f"could not load model: {e}")
            results.append(entry)
            continue

        if model is None:
            entry.update(status="unavailable", reason="model artifacts not found")
            results.append(entry)
            continue

        assumed_tracker = set()
        raw, assumed = item["builder"](values, assumed_tracker)
        feature_names = preprocessor.get("feature_names") or []

        row, covered = assemble_features(feature_names, raw)
        coverage_pct = round((covered / len(feature_names)) * 100, 1) if feature_names else 0.0
        
        entry["coverage"] = coverage_pct
        entry["features_used"] = f"{covered}/{len(feature_names)}"
        entry["assumptions"] = list(assumed)

        try:
            X = pd.DataFrame([row], columns=feature_names)
            imputer, scaler = preprocessor.get("imputer"), preprocessor.get("scaler")
            X_ready = imputer.transform(X) if imputer is not None else X.values
            X_ready = scaler.transform(X_ready) if scaler is not None else X_ready

            raw_prob = positive_probability(model, np.asarray(X_ready))
            calibrated_prob = round(raw_prob * 100, 1)

            entry.update(
                status="ran",
                probability=calibrated_prob,
                positive=calibrated_prob >= 50.0
            )
        except Exception as e:
            entry.update(status="unavailable", reason=f"prediction failed: {e}")

        results.append(entry)

    results.sort(key=lambda r: (r.get("status") == "ran", r.get("probability", 0)), reverse=True)
    return results
