"""
HexaDisease - Multi-Report Comparison & Progress Tracking Engine
Compares historical medical reports across time to evaluate:
- Biomarker trajectories (improved, worsened, stable)
- Health score progression
- Staging migration (e.g. Stage 1 Pre-diabetes -> Normal or Stage 2)
- Clinical "What To Do Next" comparative recommendations
"""

import sys
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.join(PROJECT_ROOT, "report_analysis"))

try:
    from biomarker_encyclopedia import get_biomarker_info
except ImportError:
    get_biomarker_info = lambda k: None

def compare_two_reports(rep_old, rep_new):
    """
    Compares rep_old (earlier baseline) with rep_new (recent follow-up).
    Returns detailed parameter deltas, clinical trajectories, and next steps.
    """
    vals_old = rep_old.get("extracted_values", {})
    vals_new = rep_new.get("extracted_values", {})
    
    score_old = rep_old.get("health_score", 80)
    score_new = rep_new.get("health_score", 80)
    score_delta = score_new - score_old
    
    stage_old = rep_old.get("stage_name", "Baseline Stage")
    stage_new = rep_new.get("stage_name", "Current Stage")
    
    date_old_str = rep_old.get("upload_date", "")[:10]
    date_new_str = rep_new.get("upload_date", "")[:10]
    
    all_keys = sorted(list(set(list(vals_old.keys()) + list(vals_new.keys()))))
    biomarker_deltas = []
    
    improved_count = 0
    worsened_count = 0
    stable_count = 0
    
    for key in all_keys:
        val1 = vals_old.get(key)
        val2 = vals_new.get(key)
        
        info = get_biomarker_info(key)
        display_name = info["display_name"] if info else key.replace("_", " ").title()
        unit = info["unit"] if info else ""
        ref_min = info["reference_min"] if info else None
        ref_max = info["reference_max"] if info else None
        
        # If numeric values
        try:
            n1 = float(val1) if val1 is not None else None
            n2 = float(val2) if val2 is not None else None
        except Exception:
            n1, n2 = None, None
            
        trend = "STABLE"
        diff_str = "N/A"
        pct_str = "0%"
        clinical_note = ""
        
        if n1 is not None and n2 is not None:
            diff = round(n2 - n1, 2)
            pct = round(((n2 - n1) / abs(n1)) * 100, 1) if n1 != 0 else 0
            diff_str = f"{'+' if diff > 0 else ''}{diff} {unit}".strip()
            pct_str = f"{'+' if pct > 0 else ''}{pct}%"
            
            # Determine whether moving closer to optimal is an improvement
            # For markers where lower is generally better (glucose, creatinine, BP, urea, cpk)
            lower_is_better = any(m in key for m in ["glucose", "sugar", "bp", "systolic", "diastolic", "creatinine", "urea", "cpk", "albumin"])
            higher_is_better = any(m in key for m in ["hemo", "hb", "rbc", "ef", "ejection", "platelet"])
            
            if ref_min is not None and ref_max is not None:
                dist1 = max(0, n1 - ref_max) + max(0, ref_min - n1)
                dist2 = max(0, n2 - ref_max) + max(0, ref_min - n2)
                
                if dist2 < dist1:
                    trend = "IMPROVED"
                    improved_count += 1
                    clinical_note = f"Normalized towards healthy reference ({ref_min} - {ref_max}). Excellent progress!"
                elif dist2 > dist1:
                    trend = "WORSENED"
                    worsened_count += 1
                    clinical_note = f"Moved further outside healthy reference ({ref_min} - {ref_max}). Needs attention."
                else:
                    trend = "STABLE"
                    stable_count += 1
                    clinical_note = "Holding steady within observed range."
            else:
                if lower_is_better:
                    if diff < 0:
                        trend = "IMPROVED"
                        improved_count += 1
                        clinical_note = f"Decreased by {abs(pct)}%, relieving physiological strain."
                    elif diff > 0:
                        trend = "WORSENED"
                        worsened_count += 1
                        clinical_note = f"Increased by {pct}%. Lifestyle adjustments recommended."
                    else:
                        trend = "STABLE"
                        stable_count += 1
                elif higher_is_better:
                    if diff > 0:
                        trend = "IMPROVED"
                        improved_count += 1
                        clinical_note = f"Increased by {pct}%, restoring healthy capacity."
                    elif diff < 0:
                        trend = "WORSENED"
                        worsened_count += 1
                        clinical_note = f"Decreased by {abs(pct)}%. Recommended foods can help rebound."
                    else:
                        trend = "STABLE"
                        stable_count += 1
        elif n1 is None and n2 is not None:
            trend = "NEW"
            clinical_note = f"Newly measured at {n2} {unit}."
        elif n1 is not None and n2 is None:
            trend = "NOT_TESTED"
            clinical_note = f"Tested in previous report ({n1} {unit}) but omitted in current checkup."

        biomarker_deltas.append({
            "key": key,
            "parameter": display_name,
            "unit": unit,
            "old_value": val1,
            "new_value": val2,
            "diff": diff_str,
            "pct_change": pct_str,
            "trend": trend,
            "clinical_note": clinical_note
        })

    # Overall trajectory calculation
    if improved_count > worsened_count and score_delta >= 0:
        overall_trend = "POSITIVE_PROGRESS"
        headline = "Great Health Progression! Your Lifestyle Interventions are Working"
        badge_style = "emerald"
    elif worsened_count > improved_count or score_delta < -5:
        overall_trend = "REGRESSION_WARNING"
        headline = "Health Indicators Need Attention - Adjust Routine to Prevent Progression"
        badge_style = "red"
    else:
        overall_trend = "STABLE_MAINTENANCE"
        headline = "Stable Physiological Baseline Maintained"
        badge_style = "blue"

    # Personalized "What to do next" guidance
    what_to_do_next = []
    
    if score_delta > 5:
        what_to_do_next.append(
            f"Your overall health score improved by +{score_delta} points (from {score_old} to {score_new}). "
            "Keep adhering to your current nutritional plan, hydration, and exercise habits."
        )
    elif score_delta < -5:
        what_to_do_next.append(
            f"Your health score softened by {abs(score_delta)} points (from {score_old} to {score_new}). "
            "Review your dietary sodium, sugar, and daily physical activity to stop further progression."
        )
        
    for d in biomarker_deltas:
        if d["trend"] == "WORSENED":
            what_to_do_next.append(
                f"For {d['parameter']} ({d['old_value']} -> {d['new_value']} {d['unit']}): "
                "Consult the recommended fruits and dietary adjustments in the parameter breakdown to reverse this trend."
            )
        elif d["trend"] == "IMPROVED":
            what_to_do_next.append(
                f"Success noted on {d['parameter']} ({d['old_value']} -> {d['new_value']} {d['unit']}): "
                "Your routine is effectively moving this biomarker towards optimal limits."
            )

    if not what_to_do_next:
        what_to_do_next.append("Continue current health routines and schedule your next routine panel in 3 to 6 months.")

    return {
        "report_old_id": rep_old.get("id"),
        "report_new_id": rep_new.get("id"),
        "date_old": date_old_str,
        "date_new": date_new_str,
        "patient_name": rep_new.get("patient_name", rep_old.get("patient_name", "Patient")),
        "score_old": score_old,
        "score_new": score_new,
        "score_delta": score_delta,
        "stage_old": stage_old,
        "stage_new": stage_new,
        "overall_trend": overall_trend,
        "headline": headline,
        "badge_style": badge_style,
        "improved_count": improved_count,
        "worsened_count": worsened_count,
        "stable_count": stable_count,
        "deltas": biomarker_deltas,
        "what_to_do_next": what_to_do_next
    }
