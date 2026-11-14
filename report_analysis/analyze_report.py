"""
HexaDisease - Unified Medical Report Analyzer
Coordinates document reading, regex biomarker extraction, deterministic clinical rules,
trained 6-disease ML models, and evidence-based clinical guidance.
"""

import os
import sys
import json
from datetime import datetime, timezone

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

for path in (CURRENT_DIR, os.path.join(PROJECT_ROOT, "recommendation")):
    if path not in sys.path:
        sys.path.append(path)

from clinical_rules import (
    NORMAL, BORDERLINE, ABNORMAL, URGENT, SEVERITY_LABELS, run_clinical_rules
)
from report_parser import parse_report, normalize_manual_values, display_name, unit_of
from report_reader import read_report, ReportReadError
from model_bridge import run_models

try:
    from early_stage_engine import evaluate_all_stages
except ImportError:
    evaluate_all_stages = lambda v: {"primary_stage": {"stage_name": "Normal Baseline", "is_early_stage": False}, "all_stages": []}

try:
    from biomarker_encyclopedia import explain_parameter_level
except ImportError:
    explain_parameter_level = lambda k, v: {"parameter": k, "current_value": v, "status": "MEASURED"}

try:
    from recommendation_system import get_recommendation
except ImportError:
    get_recommendation = None

ML_FLAG_THRESHOLD = 70.0

DECISIONS = {
    URGENT: (
        "URGENT - SEEK IMMEDIATE MEDICAL CARE",
        "One or more lab readings or screening models indicate a critical health risk. Seek emergency medical attention today."
    ),
    ABNORMAL: (
        "CONSULT A DOCTOR FOR EVALUATION",
        "Clinical parameters exceed normal reference limits. Schedule a doctor appointment within 1-2 weeks."
    ),
    BORDERLINE: (
        "BORDERLINE ELEVATION - LIFESTYLE MODIFICATION & RE-TEST",
        "Biomarkers indicate mild elevation or early risk pattern. Adopt preventive lifestyle measures and re-test in 3-6 months."
    ),
    NORMAL: (
        "NO CLINICAL ABNORMALITY DETECTED",
        "All extracted parameters are within normal physiological thresholds. Maintain routine health screenings."
    )
}

def combine_with_models(findings, model_results):
    notes = []
    for result in model_results:
        if result.get("status") != "ran":
            continue
        kb = result.get("kb_disease")
        rule_severity = max(
            (f["severity"] for f in findings if f.get("kb_disease") == kb),
            default=NORMAL
        )
        prob = result["probability"]

        if result["positive"] and prob >= ML_FLAG_THRESHOLD and rule_severity == NORMAL:
            findings.append({
                "condition": result["label"],
                "parameter": "ML Model Ensemble",
                "value": f"{prob}%",
                "unit": "confidence",
                "severity": BORDERLINE,
                "status": SEVERITY_LABELS[BORDERLINE],
                "message": f"The trained model estimates elevated risk ({prob}% probability). Further clinical evaluation is recommended.",
                "reference": "HexaDisease 6-Disease Trained Classifier",
                "kb_disease": kb,
            })
        elif not result["positive"] and rule_severity >= ABNORMAL:
            notes.append(
                f"{result['label']}: ML estimated low probability ({prob}%), but lab values exceed diagnostic cutoffs. Lab values take clinical precedence."
            )
    return notes

def summarize_conditions(findings):
    conditions = {}
    for f in findings:
        c = conditions.setdefault(f["condition"], {
            "condition": f["condition"],
            "severity": NORMAL,
            "kb_disease": None,
            "evidence": []
        })
        c["severity"] = max(c["severity"], f["severity"])
        if f["severity"] > NORMAL:
            c["evidence"].append(f"{f['parameter']} {f['value']} {f['unit']}".strip() + f" - {f['message']}")
            c["kb_disease"] = c["kb_disease"] or f.get("kb_disease")
            
    for c in conditions.values():
        c["status"] = SEVERITY_LABELS[c["severity"]]
    return sorted(conditions.values(), key=lambda c: -c["severity"])

def build_guidance(conditions):
    guidance = []
    if get_recommendation is None:
        return guidance

    seen = set()
    for c in conditions:
        if c["severity"] == NORMAL:
            continue
        kb_key = c.get("kb_disease") or c["condition"]
        if kb_key in seen:
            continue
        seen.add(kb_key)

        rec = get_recommendation(kb_key)
        if not rec:
            continue

        entry = {
            "for": rec.get("name", c["condition"]),
            "category": rec.get("category", ""),
            "food_prefer": rec.get("food", {}).get("prefer", []),
            "food_limit": rec.get("food", {}).get("limit", []),
            "exercise": rec.get("exercise", {}).get("recommended", []),
            "exercise_precautions": rec.get("exercise", {}).get("precautions", []),
            "lifestyle": rec.get("lifestyle", []),
            "warning_signs": rec.get("warning_signs", []),
            "when_to_seek_help": rec.get("when_to_seek_help", [])
        }
        guidance.append(entry)

    return guidance

def analyze_values(values, use_ml=True, source_description="Manual Input"):
    findings = run_clinical_rules(values)
    model_results = []
    notes = []

    if use_ml:
        model_results = run_models(values)
        notes = combine_with_models(findings, model_results)

    conditions = summarize_conditions(findings)
    overall_severity = max((c["severity"] for c in conditions), default=NORMAL)
    decision_title, decision_desc = DECISIONS[overall_severity]

    guidance = build_guidance(conditions)
    staging = evaluate_all_stages(values)
    
    parameter_breakdowns = {}
    for k, v in values.items():
        parameter_breakdowns[k] = explain_parameter_level(k, v)

    # Calculate overall 0-100 health score
    health_score = 100
    for f in findings:
        sev = f.get("severity", 0)
        if sev == 3:
            health_score -= 22
        elif sev == 2:
            health_score -= 12
        elif sev == 1:
            health_score -= 5
    health_score = max(15, min(100, health_score))

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source_description,
        "health_score": health_score,
        "decision": decision_title,
        "recommended_action": decision_desc,
        "overall_severity": SEVERITY_LABELS[overall_severity],
        "staging": staging,
        "parameter_breakdowns": parameter_breakdowns,
        "extracted_values": values,
        "findings": findings,
        "model_results": model_results,
        "conditions": conditions,
        "guidance": guidance,
        "notes": notes
    }

def analyze_report_text(text, use_ml=True, source_description="Raw Text"):
    values = parse_report(text)
    return analyze_values(values, use_ml=use_ml, source_description=source_description)

def analyze_report_file(path, use_ml=True):
    text, direct_values = read_report(path)
    if direct_values is not None:
        values = normalize_manual_values(direct_values)
    else:
        values = parse_report(text)
    return analyze_values(values, use_ml=use_ml, source_description=os.path.basename(path))

if __name__ == "__main__":
    sample_text = """
    Patient: John Doe    Age: 58    Sex: Male
    Fasting Blood Glucose: 168 mg/dL
    HbA1c: 7.8 %
    Blood Pressure: 148/92 mmHg
    Serum Creatinine: 1.6 mg/dL
    Blood Urea: 56 mg/dL
    Total Cholesterol: 245 mg/dL
    Hemoglobin: 10.4 g/dL
    """
    res = analyze_report_text(sample_text)
    print("Decision:", res["decision"])
    print("Overall Severity:", res["overall_severity"])
    print(f"Extracted {len(res['extracted_values'])} parameters.")
    print(f"Ran {len(res['model_results'])} models:")
    for m in res["model_results"]:
        print(f"  * {m['label']}: {m.get('probability')}% (Status: {m['status']})")
