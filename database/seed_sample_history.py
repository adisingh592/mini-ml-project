"""
HexaDisease - Historical Report Seeder
Populates database with two sequential reports for a patient to showcase:
- Report 1 (Baseline - 90 Days Ago): Early Stage 1 Pre-diabetes & Pre-hypertensive Stress
- Report 2 (Follow-up - Today): Substantial improvement from daily walking & dietary fruits
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

for p in (os.path.join(PROJECT_ROOT, "report_analysis"), CURRENT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

from analyze_report import analyze_report_text
from db import save_report, list_reports, init_db

def seed():
    init_db()
    
    print("Seeding baseline report (3 months ago)...")
    text_baseline = """
    PATIENT HEALTH CHECKUP REPORT - METABOLIC & HEMATOLOGY PANEL
    Patient Name: Priya Sharma    Age: 46    Sex: Female
    Date: 2026-08-15
    
    CLINICAL BIOCHEMISTRY:
    Fasting Blood Glucose: 138 mg/dL
    HbA1c: 6.3 %
    Systolic Blood Pressure: 142 mmHg
    Diastolic Blood Pressure: 92 mmHg
    Serum Creatinine: 1.25 mg/dL
    Blood Urea: 44 mg/dL
    
    COMPLETE BLOOD COUNT:
    Hemoglobin: 11.2 g/dL
    Total WBC Count: 11400 cells/uL
    RBC Count: 4.1 million/uL
    Platelet Count: 240000 /uL
    """
    res1 = analyze_report_text(text_baseline, use_ml=True, source_description="Baseline Checkup (August 2026)")
    id1 = save_report(
        analysis=res1,
        patient_name="Priya Sharma",
        patient_age=46,
        patient_gender="Female",
        filename="Priya_Sharma_August_Baseline.pdf"
    )
    print(f"Baseline report saved with ID: {id1}")

    print("Seeding follow-up report (Today)...")
    text_followup = """
    PATIENT HEALTH CHECKUP REPORT - FOLLOW-UP EVALUATION
    Patient Name: Priya Sharma    Age: 46    Sex: Female
    Date: 2026-11-15
    
    CLINICAL BIOCHEMISTRY:
    Fasting Blood Glucose: 110 mg/dL
    HbA1c: 5.8 %
    Systolic Blood Pressure: 124 mmHg
    Diastolic Blood Pressure: 82 mmHg
    Serum Creatinine: 1.05 mg/dL
    Blood Urea: 32 mg/dL
    
    COMPLETE BLOOD COUNT:
    Hemoglobin: 12.4 g/dL
    Total WBC Count: 7800 cells/uL
    RBC Count: 4.6 million/uL
    Platelet Count: 260000 /uL
    """
    res2 = analyze_report_text(text_followup, use_ml=True, source_description="Follow-up Checkup (November 2026)")
    id2 = save_report(
        analysis=res2,
        patient_name="Priya Sharma",
        patient_age=46,
        patient_gender="Female",
        filename="Priya_Sharma_November_Followup.pdf"
    )
    print(f"Follow-up report saved with ID: {id2}")

    print(f"Seeding completed. Total reports in DB: {len(list_reports())}")

if __name__ == "__main__":
    seed()
