"""
HexaDisease - Recommendation System Module
Retrieves verified clinical guidance strictly for the 6 core diseases:
1. Diabetes Mellitus (Metabolic)
2. Cerebrovascular Stroke (Vascular / Neurological)
3. Heart Failure & Cardiac Risk (Cardiovascular)
4. Chronic Kidney Disease (CKD) (Renal)
5. Hypertension / Maternal Vascular Risk (Vascular)
6. Clinical Anemia (Hematology / Oxygen Transport)
"""

import os
import json

CONFIDENCE_THRESHOLD = 70.0

def load_knowledge_base():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_folder, "disease_information.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("diseases", {})
    except Exception as e:
        print(f"Error loading disease_information.json: {e}")
        return {}

def clean_disease_name(name):
    clean = name.lower().strip()
    clean = clean.replace("'", "").replace("-", " ").replace("_", " ")
    return clean

KEY_MAP = {
    "diabetes": "Diabetes",
    "diabetic": "Diabetes",
    "stroke": "Stroke",
    "cerebrovascular": "Stroke",
    "heart": "Heart_Disease",
    "cardiac": "Heart_Disease",
    "heart_disease": "Heart_Disease",
    "heart failure": "Heart_Disease",
    "kidney": "Chronic_Kidney_Disease",
    "ckd": "Chronic_Kidney_Disease",
    "chronic kidney disease": "Chronic_Kidney_Disease",
    "maternal": "Maternal_Health_Risk",
    "maternal_risk": "Maternal_Health_Risk",
    "hypertension": "Maternal_Health_Risk",
    "maternal_health_risk": "Maternal_Health_Risk",
    "hypertension_maternal_risk": "Maternal_Health_Risk",
    "anemia": "Anemia",
    "anaemia": "Anemia",
    "hemoglobin": "Anemia"
}

def get_recommendation(disease_name):
    kb = load_knowledge_base()
    if not kb:
        return None
        
    user_clean = clean_disease_name(disease_name)
    
    # 1. Exact match in knowledge base keys
    for key, val in kb.items():
        if clean_disease_name(key) == user_clean:
            return val
            
    # 2. Check standard alias mapping
    for alias, kb_key in KEY_MAP.items():
        if alias in user_clean or user_clean in alias:
            if kb_key in kb:
                return kb[kb_key]
                
    # 3. Fuzzy substring search
    for key, info in kb.items():
        db_clean = clean_disease_name(key)
        if user_clean in db_clean or db_clean in user_clean:
            return info
            
    return None

def display_recommendation(disease_name, confidence=None, category=None):
    info = get_recommendation(disease_name)
    if info is None:
        print(f"No clinical recommendation found for '{disease_name}'.")
        return
        
    print("=" * 60)
    print(f"CLINICAL GUIDANCE: {info.get('name', disease_name).upper()}")
    if confidence:
        print(f"Model Screening Confidence: {confidence}")
    print("=" * 60)
    print(f"Category: {info.get('category')}")
    print(f"Overview: {info.get('description')}\n")
    
    if "food" in info:
        print("[NUTRITIONAL GUIDELINES]")
        print("Prefer:")
        for item in info["food"].get("prefer", []):
            print(f"  + {item}")
        print("Limit:")
        for item in info["food"].get("limit", []):
            print(f"  - {item}")
            
    if "exercise" in info:
        print("\n[PHYSICAL ACTIVITY]")
        for item in info["exercise"].get("recommended", []):
            print(f"  * {item}")

if __name__ == "__main__":
    for d in ["diabetes", "stroke", "heart", "ckd", "hypertension", "anemia"]:
        rec = get_recommendation(d)
        print(f"Lookup '{d}' -> Found: {rec.get('name') if rec else 'None'}")
