"""
HexaDisease - Early-Stage Detection & Clinical Staging Engine
Specializes in early detection of the 6 cardiorenal-metabolic diseases:
1. Diabetes Mellitus (Pre-Diabetes / Impaired Fasting Glucose Staging)
2. Cerebrovascular Stroke (Pre-Hypertensive & Vascular Shear Staging)
3. Heart Failure (ACC/AHA Stages A, B, C, D)
4. Chronic Kidney Disease (KDIGO Stages G1 to G5)
5. Hypertension / Maternal Vascular Risk (Pre-eclampsia & Hemodynamic Staging)
6. Clinical Anemia (WHO Mild, Moderate, Severe Staging)
"""

def stage_diabetes(v):
    fpg = v.get("fasting_glucose")
    hba1c = v.get("hba1c")
    pp = v.get("pp_glucose") or v.get("random_glucose")

    if (fpg and fpg >= 200) or (hba1c and hba1c >= 9.0) or (pp and pp >= 300):
        return {
            "disease": "Diabetes Mellitus",
            "stage_code": "STAGE_3",
            "stage_name": "Stage 3: Advanced Uncontrolled Diabetes",
            "is_early_stage": False,
            "badge_color": "red",
            "risk_level": "High",
            "explanation": "Marked glycemic elevation with heightened microvascular and neuropathic risks.",
            "early_precaution": "Requires immediate physician coordination, possible medication titration, and tight glucose tracking.",
            "actionable_next_step": "Schedule urgent endocrinology visit and begin intensive carbohydrate restriction."
        }
    elif (fpg and fpg >= 126) or (hba1c and hba1c >= 6.5) or (pp and pp >= 200):
        return {
            "disease": "Diabetes Mellitus",
            "stage_code": "STAGE_2",
            "stage_name": "Stage 2: Early-Onset Type 2 Diabetes",
            "is_early_stage": False,
            "badge_color": "orange",
            "risk_level": "Moderate-High",
            "explanation": "Laboratory values confirm Type 2 Diabetes criteria under ADA guidelines.",
            "early_precaution": "Begin strict glycemic nutrition, 150 minutes of weekly aerobic exercise, and physician consultation.",
            "actionable_next_step": "Consult your primary physician for formal diabetes management plan."
        }
    elif (fpg and fpg >= 100) or (hba1c and hba1c >= 5.7) or (pp and pp >= 140):
        return {
            "disease": "Diabetes Mellitus",
            "stage_code": "STAGE_1",
            "stage_name": "Stage 1: Pre-Diabetes / Impaired Glycemia (EARLY WARNING WINDOW)",
            "is_early_stage": True,
            "badge_color": "amber",
            "risk_level": "Early Warning",
            "explanation": "Your blood sugar is elevated above normal but has NOT yet crossed into irreversible diabetes. THIS IS THE 100% REVERSIBLE WINDOW!",
            "early_precaution": "By replacing white carbs with fibrous vegetables, eating low-GI fruits (berries, green apples, cherries), and taking 15-minute walks after meals, you can prevent diabetes from ever developing.",
            "actionable_next_step": "Adopt post-meal brisk walks, eliminate sugary drinks, and re-test HbA1c in 90 days to verify normal return."
        }
    else:
        return {
            "disease": "Diabetes Mellitus",
            "stage_code": "STAGE_0",
            "stage_name": "Stage 0: Normal Glycemic Homeostasis",
            "is_early_stage": False,
            "badge_color": "emerald",
            "risk_level": "Optimal",
            "explanation": "Fasting glucose and HbA1c are within healthy non-diabetic reference ranges.",
            "early_precaution": "Continue maintaining balanced meals and regular activity.",
            "actionable_next_step": "Maintain routine annual blood glucose screening."
        }

def stage_stroke(v):
    sys_bp = v.get("systolic_bp") or v.get("bp")
    dia_bp = v.get("diastolic_bp")
    age = v.get("age", 45)
    glucose = v.get("fasting_glucose") or v.get("avg_glucose_level", 90)

    if (sys_bp and sys_bp >= 160) or (dia_bp and dia_bp >= 100):
        return {
            "disease": "Cerebrovascular Stroke Risk",
            "stage_code": "STAGE_3",
            "stage_name": "Stage 3: Severe Cerebrovascular Threat / Stage 2 HTN",
            "is_early_stage": False,
            "badge_color": "red",
            "risk_level": "Critical",
            "explanation": "Severe arterial blood pressure creates significant shear stress on brain cerebral vessels.",
            "early_precaution": "Urgent medical pressure control required. Watch for sudden numbness, slurred speech, or facial drooping.",
            "actionable_next_step": "Seek same-day medical attention for antihypertensive therapy."
        }
    elif (sys_bp and sys_bp >= 140) or (dia_bp and dia_bp >= 90) or (glucose >= 160 and age >= 60):
        return {
            "disease": "Cerebrovascular Stroke Risk",
            "stage_code": "STAGE_2",
            "stage_name": "Stage 2: Moderate Ischemic Vascular Strain",
            "is_early_stage": False,
            "badge_color": "orange",
            "risk_level": "Moderate",
            "explanation": "Persistent hypertension and elevated vascular resistance increase long-term stroke probability.",
            "early_precaution": "Adopt low-salt DASH diet, eliminate tobacco exposure, and engage in daily aerobic walking.",
            "actionable_next_step": "Consult doctor for blood pressure optimization and carotid vascular screening."
        }
    elif (sys_bp and sys_bp >= 120) or (dia_bp and dia_bp >= 80):
        return {
            "disease": "Cerebrovascular Stroke Risk",
            "stage_code": "STAGE_1",
            "stage_name": "Stage 1: Pre-Hypertensive Arterial Stress (EARLY WARNING WINDOW)",
            "is_early_stage": True,
            "badge_color": "amber",
            "risk_level": "Early Warning",
            "explanation": "Early arterial stiffening detected. Blood pressure is starting to creep up before any stroke symptoms appear.",
            "early_precaution": "Boost dietary potassium with bananas, melons, and coconut water. Reduce sodium by avoiding packaged snacks.",
            "actionable_next_step": "Begin 30-min daily brisk walking and practice 5-minute deep breathing exercises daily."
        }
    else:
        return {
            "disease": "Cerebrovascular Stroke Risk",
            "stage_code": "STAGE_0",
            "stage_name": "Stage 0: Optimal Cerebral Hemodynamics",
            "is_early_stage": False,
            "badge_color": "emerald",
            "risk_level": "Optimal",
            "explanation": "Blood pressure and vascular metrics reflect healthy, low-risk arterial flow.",
            "early_precaution": "Keep arterial walls flexible with heart-healthy omega-3s and hydration.",
            "actionable_next_step": "Continue routine checkups."
        }

def stage_heart_failure(v):
    ef = v.get("ejection_fraction")
    cpk = v.get("cpk") or v.get("creatinine_phosphokinase")
    cr = v.get("serum_creatinine")

    if ef and ef <= 40:
        return {
            "disease": "Heart Failure & Cardiac Stress",
            "stage_code": "STAGE_C",
            "stage_name": "ACC/AHA Stage C: Heart Failure with Reduced EF (HFrEF)",
            "is_early_stage": False,
            "badge_color": "red",
            "risk_level": "Severe",
            "explanation": "Significant reduction in left ventricular pumping efficiency (< 40%).",
            "early_precaution": "Strict cardiology supervision, strict sodium restriction (1,500 mg/day), daily weight monitoring.",
            "actionable_next_step": "Urgent cardiology evaluation for guideline-directed medical therapy."
        }
    elif (ef and ef <= 49) or (cpk and cpk >= 400):
        return {
            "disease": "Heart Failure & Cardiac Stress",
            "stage_code": "STAGE_B",
            "stage_name": "ACC/AHA Stage B: Pre-Heart Failure (EARLY WARNING WINDOW)",
            "is_early_stage": True,
            "badge_color": "amber",
            "risk_level": "Early Warning",
            "explanation": "Early structural or functional cardiac stress detected (mildly reduced EF or myocardial enzyme leakage). You may feel mild shortness of breath when walking briskly.",
            "early_precaution": "Eliminate processed sodium, consume cardioprotective berries and pomegranate, and avoid alcohol.",
            "actionable_next_step": "Schedule an echocardiogram and cardiac checkup to prevent progression to symptomatic heart failure."
        }
    elif (v.get("systolic_bp", 0) >= 130 or v.get("fasting_glucose", 0) >= 126 or (cr and cr >= 1.3)):
        return {
            "disease": "Heart Failure & Cardiac Stress",
            "stage_code": "STAGE_A",
            "stage_name": "ACC/AHA Stage A: At High Risk for Heart Failure",
            "is_early_stage": True,
            "badge_color": "amber",
            "risk_level": "At-Risk",
            "explanation": "Presence of comorbid hypertension, diabetes, or renal stress that elevates cardiac workload.",
            "early_precaution": "Controlling blood pressure and glucose now completely protects your heart muscle from hypertrophy.",
            "actionable_next_step": "Maintain BP < 120/80 and HbA1c < 6.0%."
        }
    else:
        return {
            "disease": "Heart Failure & Cardiac Stress",
            "stage_code": "STAGE_0",
            "stage_name": "Optimal Myocardial Function",
            "is_early_stage": False,
            "badge_color": "emerald",
            "risk_level": "Optimal",
            "explanation": "Normal ejection fraction and cardiac enzymes indicate vigorous ventricular health.",
            "early_precaution": "Maintain regular aerobic conditioning.",
            "actionable_next_step": "Maintain routine cardiac screening."
        }

def stage_kidney_disease(v):
    cr = v.get("serum_creatinine")
    alb = v.get("urine_albumin")
    urea = v.get("blood_urea")

    if (cr and cr >= 3.0) or (alb and alb >= 300):
        return {
            "disease": "Chronic Kidney Disease (CKD)",
            "stage_code": "STAGE_G4_G5",
            "stage_name": "KDIGO Stage G4/G5: Advanced / Severe Kidney Impairment",
            "is_early_stage": False,
            "badge_color": "red",
            "risk_level": "Severe",
            "explanation": "Substantial reduction in glomerular filtration; waste products are accumulating rapidly.",
            "early_precaution": "Strict nephrology management, low-protein diet, strict potassium and phosphorus control.",
            "actionable_next_step": "Urgent nephrologist consultation."
        }
    elif (cr and cr >= 1.5) or (alb and alb >= 30):
        return {
            "disease": "Chronic Kidney Disease (CKD)",
            "stage_code": "STAGE_G3",
            "stage_name": "KDIGO Stage G3: Moderate Kidney Dysfunction",
            "is_early_stage": False,
            "badge_color": "orange",
            "risk_level": "Moderate",
            "explanation": "Notable decline in nephron filtration efficiency. Urine protein leakage or elevated creatinine.",
            "early_precaution": "Control blood pressure below 120/80, stop NSAID painkillers completely, and drink 2.5L water.",
            "actionable_next_step": "Consult nephrologist for eGFR calculation and ultrasound."
        }
    elif (cr and cr >= 1.2) or (urea and urea >= 45):
        return {
            "disease": "Chronic Kidney Disease (CKD)",
            "stage_code": "STAGE_G2",
            "stage_name": "KDIGO Stage G2: Early Mild Renal Stress (EARLY WARNING WINDOW)",
            "is_early_stage": True,
            "badge_color": "amber",
            "risk_level": "Early Warning",
            "explanation": "Mild kidney filtration strain detected. Often caused by mild chronic dehydration or early hypertension.",
            "early_precaution": "Drink 2.5 to 3 liters of clean water daily, eat kidney-friendly cranberries and watermelon, and reduce table salt.",
            "actionable_next_step": "Hydrate well and re-test serum creatinine and urine analysis in 30 days."
        }
    else:
        return {
            "disease": "Chronic Kidney Disease (CKD)",
            "stage_code": "STAGE_G1",
            "stage_name": "KDIGO Stage G1: Healthy Normal Glomerular Filtration",
            "is_early_stage": False,
            "badge_color": "emerald",
            "risk_level": "Optimal",
            "explanation": "Serum creatinine, urea, and urine albumin reflect pristine renal filtration.",
            "early_precaution": "Maintain adequate daily hydration.",
            "actionable_next_step": "Routine annual urine and creatinine check."
        }

def stage_hypertension_maternal(v):
    sys_bp = v.get("systolic_bp") or v.get("bp")
    dia_bp = v.get("diastolic_bp")
    bs = v.get("blood_glucose") or v.get("fasting_glucose")

    if (sys_bp and sys_bp >= 160) or (dia_bp and dia_bp >= 110):
        return {
            "disease": "Hypertension & Maternal Risk",
            "stage_code": "STAGE_3",
            "stage_name": "Severe Hypertension / Severe Preeclampsia Alert",
            "is_early_stage": False,
            "badge_color": "red",
            "risk_level": "Urgent",
            "explanation": "Critical blood pressure thresholds reached. Danger of severe gestational end-organ complications.",
            "early_precaution": "Seek immediate emergency obstetric or medical triage.",
            "actionable_next_step": "Immediate hospital evaluation required."
        }
    elif (sys_bp and sys_bp >= 140) or (dia_bp and dia_bp >= 90):
        return {
            "disease": "Hypertension & Maternal Risk",
            "stage_code": "STAGE_2",
            "stage_name": "Stage 2: Established Hypertension / Gestational Risk",
            "is_early_stage": False,
            "badge_color": "orange",
            "risk_level": "High Risk",
            "explanation": "Persistent blood pressure elevation requiring clinical evaluation and close monitoring.",
            "early_precaution": "Rest on left lateral side (if pregnant), limit sodium, and consult physician.",
            "actionable_next_step": "Schedule clinic visit for pressure protocol and fetal/maternal monitoring."
        }
    elif (sys_bp and sys_bp >= 120) or (dia_bp and dia_bp >= 80):
        return {
            "disease": "Hypertension & Maternal Risk",
            "stage_code": "STAGE_1",
            "stage_name": "Stage 1: Pre-Hypertensive Hemodynamic Stress (EARLY WARNING WINDOW)",
            "is_early_stage": True,
            "badge_color": "amber",
            "risk_level": "Early Warning",
            "explanation": "Mild hemodynamic elevation detected before full preeclampsia or chronic hypertension sets in.",
            "early_precaution": "Eat potassium-rich bananas, melons, and leafy greens. Ensure 8 hours of sleep and avoid strenuous lifting.",
            "actionable_next_step": "Monitor blood pressure daily at home in the morning and evening."
        }
    else:
        return {
            "disease": "Hypertension & Maternal Risk",
            "stage_code": "STAGE_0",
            "stage_name": "Optimal Hemodynamic Profile",
            "is_early_stage": False,
            "badge_color": "emerald",
            "risk_level": "Optimal",
            "explanation": "Blood pressure and metabolic values are completely balanced.",
            "early_precaution": "Continue healthy balanced nutrition and gentle daily activity.",
            "actionable_next_step": "Routine prenatal / annual checkup."
        }

def stage_anemia(v):
    hb = v.get("hemo") or v.get("hb") or v.get("hemoglobin")
    rbc = v.get("rbc")
    wbc = v.get("wbc")

    if hb and hb < 8.0:
        return {
            "disease": "Clinical Anemia",
            "stage_code": "STAGE_3",
            "stage_name": "WHO Stage 3: Severe Hypoxemic Anemia",
            "is_early_stage": False,
            "badge_color": "red",
            "risk_level": "Severe",
            "explanation": "Critically low hemoglobin (< 8.0 g/dL). Extreme tissue hypoxia and cardiovascular strain.",
            "early_precaution": "Immediate medical evaluation for intravenous iron or clinical transfusion assessment.",
            "actionable_next_step": "Seek hospital medical care immediately."
        }
    elif hb and hb < 11.0:
        return {
            "disease": "Clinical Anemia",
            "stage_code": "STAGE_2",
            "stage_name": "WHO Stage 2: Moderate Functional Anemia",
            "is_early_stage": False,
            "badge_color": "orange",
            "risk_level": "Moderate",
            "explanation": "Hemoglobin between 8.0 and 10.9 g/dL. Noticeable fatigue, paleness, and breathlessness on exertion.",
            "early_precaution": "Initiate medical oral iron supplements along with dietary iron and Vitamin C.",
            "actionable_next_step": "Consult doctor for iron profile (serum ferritin) and corrective prescription."
        }
    elif (hb and hb < 12.0) or (rbc and rbc < 4.2):
        return {
            "disease": "Clinical Anemia",
            "stage_code": "STAGE_1",
            "stage_name": "WHO Stage 1: Mild / Latent Anemia (EARLY WARNING WINDOW)",
            "is_early_stage": True,
            "badge_color": "amber",
            "risk_level": "Early Warning",
            "explanation": "Hemoglobin has dipped slightly below normal (11.0 - 11.9 g/dL). THIS IS FULLY REVERSIBLE WITH DIET!",
            "early_precaution": "Eat pomegranates, spinach, beets, amla, and dried dates. Cook in cast iron and avoid tea/coffee with meals.",
            "actionable_next_step": "Incorporate iron-rich fruits daily and re-test CBC in 60 days to verify normal recovery."
        }
    else:
        return {
            "disease": "Clinical Anemia",
            "stage_code": "STAGE_0",
            "stage_name": "Optimal Oxygen Transport Capacity",
            "is_early_stage": False,
            "badge_color": "emerald",
            "risk_level": "Optimal",
            "explanation": "Hemoglobin, RBC, and hematocrit reflect robust red cell counts and oxygenation.",
            "early_precaution": "Maintain iron-rich diverse nutrition.",
            "actionable_next_step": "Routine annual CBC check."
        }

def evaluate_all_stages(extracted_values):
    """Evaluates clinical stages across all 6 core disease modalities."""
    stages = [
        stage_diabetes(extracted_values),
        stage_stroke(extracted_values),
        stage_heart_failure(extracted_values),
        stage_kidney_disease(extracted_values),
        stage_hypertension_maternal(extracted_values),
        stage_anemia(extracted_values)
    ]
    
    # Priority sorting: severe stages first, then early warning stages, then normal
    order_map = {"STAGE_3": 3, "STAGE_2": 2, "STAGE_1": 1, "STAGE_B": 1.5, "STAGE_A": 1.2, "STAGE_G3": 2, "STAGE_G2": 1.2, "STAGE_G4_G5": 3, "STAGE_0": 0, "STAGE_G1": 0}
    stages_sorted = sorted(stages, key=lambda s: -order_map.get(s["stage_code"], 0))
    
    # Check if there is an early warning window active
    has_early_warning = any(s["is_early_stage"] for s in stages)
    primary_stage = stages_sorted[0]
    
    return {
        "primary_stage": primary_stage,
        "all_stages": stages_sorted,
        "has_early_warning": has_early_warning,
        "early_stage_alert": (
            "EARLY PRE-DISEASE STAGE DETECTED! You have caught this during the early reversible window. "
            "By taking daily action with the diet, recommended fruits, and gentle exercise below, you can restore normal "
            "reference limits before this advances into an established disease."
        ) if has_early_warning else None
    }
