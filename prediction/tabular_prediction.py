"""
HexaDisease - Tabular Disease Prediction Module
Provides high-performance inference for the 6 core diseases:
1. diabetes
2. stroke
3. heart_disease
4. kidney_disease
5. hypertension_maternal_risk
6. anemia
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

def get_project_root():
    curr = os.path.dirname(os.path.abspath(__file__))
    while curr and os.path.dirname(curr) != curr:
        if os.path.exists(os.path.join(curr, "models")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(r"E:\New folder (7)")

PROJECT_ROOT = get_project_root()
MODELS_DIR = os.path.join(PROJECT_ROOT, "models", "tabular")
RECOMMENDATION_DIR = os.path.join(PROJECT_ROOT, "recommendation")

if RECOMMENDATION_DIR not in sys.path:
    sys.path.append(RECOMMENDATION_DIR)

try:
    from recommendation_system import get_recommendation, display_recommendation
except ImportError:
    get_recommendation = None
    display_recommendation = None

SUPPORTED_DISEASES = {
    "diabetes": {
        "title": "Diabetes Mellitus",
        "category": "Metabolic",
        "folder": "diabetes",
        "model_file": "diabetes_model.pkl",
        "preprocessor_file": "diabetes_preprocessor.pkl",
    },
    "stroke": {
        "title": "Cerebrovascular Stroke",
        "category": "Vascular / Neurological",
        "folder": "stroke",
        "model_file": "stroke_model.pkl",
        "preprocessor_file": "stroke_preprocessor.pkl",
    },
    "heart_disease": {
        "title": "Heart Failure & Cardiac Risk",
        "category": "Cardiovascular",
        "folder": "heart_disease",
        "model_file": "heart_disease_model.pkl",
        "preprocessor_file": "heart_disease_preprocessor.pkl",
    },
    "kidney_disease": {
        "title": "Chronic Kidney Disease (CKD)",
        "category": "Renal",
        "folder": "kidney_disease",
        "model_file": "kidney_disease_model.pkl",
        "preprocessor_file": "kidney_disease_preprocessor.pkl",
    },
    "hypertension_maternal_risk": {
        "title": "Hypertension / Maternal Vascular Risk",
        "category": "Vascular",
        "folder": "hypertension_maternal_risk",
        "model_file": "hypertension_maternal_risk_model.pkl",
        "preprocessor_file": "hypertension_maternal_risk_preprocessor.pkl",
    },
    "anemia": {
        "title": "Clinical Anemia",
        "category": "Hematology / Oxygen Transport",
        "folder": "anemia",
        "model_file": "anemia_model.pkl",
        "preprocessor_file": "anemia_preprocessor.pkl",
    }
}

def normalize_disease_key(name):
    clean = name.lower().strip().replace(" ", "_").replace("-", "_")
    if "diabet" in clean:
        return "diabetes"
    if "stroke" in clean:
        return "stroke"
    if "heart" in clean or "cardiac" in clean:
        return "heart_disease"
    if "kidney" in clean or "ckd" in clean or "renal" in clean:
        return "kidney_disease"
    if "maternal" in clean or "hypertension" in clean or "vascular" in clean:
        return "hypertension_maternal_risk"
    if "anemia" in clean or "anaemia" in clean or "hemoglobin" in clean:
        return "anemia"
    return clean

def load_tabular_model_and_preprocessor(disease_name):
    key = normalize_disease_key(disease_name)
    info = SUPPORTED_DISEASES.get(key)
    if not info:
        print(f"Error: Disease '{disease_name}' not supported. Supported: {list(SUPPORTED_DISEASES.keys())}")
        return None, None
        
    folder = os.path.join(MODELS_DIR, info["folder"])
    model_path = os.path.join(folder, info["model_file"])
    preproc_path = os.path.join(folder, info["preprocessor_file"])
    
    if not os.path.exists(model_path) or not os.path.exists(preproc_path):
        print(f"Warning: Model artifacts for '{key}' not found at {model_path}.")
        return None, None
        
    model = joblib.load(model_path)
    preprocessor = joblib.load(preproc_path)
    return model, preprocessor

def predict_tabular_disease(disease_name, input_data, show_recommendation=False):
    key = normalize_disease_key(disease_name)
    info = SUPPORTED_DISEASES.get(key, {"title": disease_name, "category": "General"})
    
    model, preprocessor = load_tabular_model_and_preprocessor(key)
    if model is None or preprocessor is None:
        return {
            "disease": info.get("title", disease_name),
            "disease_key": key,
            "status": "Model Not Found",
            "prediction": None,
            "confidence": None
        }
        
    feature_names = preprocessor.get("feature_names", [])
    
    # Format input data
    if isinstance(input_data, dict):
        df_input = pd.DataFrame([input_data])
    elif isinstance(input_data, (list, np.ndarray)):
        if feature_names and len(feature_names) == len(input_data):
            df_input = pd.DataFrame([input_data], columns=feature_names)
        else:
            df_input = pd.DataFrame([input_data])
    else:
        df_input = input_data.copy()
        
    # Reindex columns to match feature_names if available
    if feature_names:
        for f in feature_names:
            if f not in df_input.columns:
                df_input[f] = np.nan
        df_input = df_input[feature_names]
        
    try:
        imputer = preprocessor.get("imputer")
        scaler = preprocessor.get("scaler")
        
        X_imputed = imputer.transform(df_input) if imputer else df_input.values
        X_scaled = scaler.transform(X_imputed) if scaler else X_imputed
    except Exception as e:
        return {
            "disease": info.get("title", disease_name),
            "disease_key": key,
            "status": "Preprocessing Failed",
            "error": str(e)
        }
        
    prediction = int(model.predict(X_scaled)[0])
    
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_scaled)[0]
        # probability of positive class (index 1)
        classes = list(getattr(model, "classes_", range(len(probs))))
        pos_idx = classes.index(1) if 1 in classes else len(probs) - 1
        probability = float(probs[pos_idx] * 100.0)
        confidence = float(np.max(probs) * 100.0)
    else:
        probability = 85.0 if prediction == 1 else 15.0
        confidence = 85.0
        
    predicted_label = "Positive (Elevated Risk / Condition Detected)" if prediction == 1 else "Negative (Normal / Low Risk)"
    
    result = {
        "disease": info.get("title", disease_name),
        "disease_key": key,
        "category": info.get("category", "Clinical"),
        "prediction_raw": prediction,
        "prediction_label": predicted_label,
        "probability": round(probability, 1),
        "confidence": round(confidence, 1),
        "status": "success"
    }
    
    if show_recommendation and display_recommendation is not None:
        display_recommendation(key, confidence=f"{result['confidence']}%")
        
    return result

if __name__ == "__main__":
    print("Testing 6-Disease Prediction Module:")
    for k, v in SUPPORTED_DISEASES.items():
        print(f" - {v['title']} ({k})")
