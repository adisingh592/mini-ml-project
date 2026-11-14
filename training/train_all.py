"""
HexaDisease - Master Multi-Disease Training Orchestrator
Executes training pipelines sequentially for all 6 closely related tabular diseases:
1. Diabetes Mellitus (Metabolic)
2. Cerebrovascular Stroke (Vascular / Neurological)
3. Heart Failure & Cardiac Risk (Cardiovascular)
4. Chronic Kidney Disease (CKD) (Renal)
5. Hypertension / Maternal Vascular Risk (Vascular)
6. Clinical Anemia (Hematology / Oxygen Transport)
"""

import os
import sys
import subprocess
import time
import pandas as pd

DISEASES = [
    ("diabetes", "Diabetes Mellitus", "training/diabetes/train.py"),
    ("stroke", "Cerebrovascular Stroke", "training/stroke/train.py"),
    ("heart_disease", "Heart Failure & Cardiac Risk", "training/heart_disease/train.py"),
    ("kidney_disease", "Chronic Kidney Disease (CKD)", "training/kidney_disease/train.py"),
    ("hypertension_maternal_risk", "Hypertension & Maternal Risk", "training/hypertension_maternal_risk/train.py"),
    ("anemia", "Clinical Anemia", "training/anemia/train.py")
]

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 70)
    print("HEXADISEASE - MASTER 6-DISEASE MODEL TRAINING PIPELINE")
    print("=" * 70)
    print(f"Working Directory: {root_dir}")
    print(f"Executing models for 6 core diseases...\n")
    
    start_time = time.time()
    summary = []
    
    for slug, name, script_rel in DISEASES:
        script_path = os.path.join(root_dir, script_rel)
        print("\n" + "#" * 60)
        print(f"RUNNING: {name.upper()} ({slug})")
        print("#" * 60)
        
        t0 = time.time()
        # Run training script using the current python executable
        ret = subprocess.run([sys.executable, script_path], cwd=root_dir)
        elapsed = round(time.time() - t0, 1)
        
        # Check output comparison csv
        csv_path = os.path.join(root_dir, "results", "tabular", slug, "model_comparison.csv")
        model_path = os.path.join(root_dir, "models", "tabular", slug, f"{slug}_model.pkl")
        
        if ret.returncode == 0 and os.path.exists(csv_path) and os.path.exists(model_path):
            df_comp = pd.read_csv(csv_path)
            best_row = df_comp.sort_values(by="F1-Score", ascending=False).iloc[0]
            summary.append({
                "Disease": name,
                "Best Architecture": best_row["Model"],
                "Accuracy": f"{best_row['Accuracy']*100:.1f}%",
                "F1-Score": f"{best_row['F1-Score']*100:.1f}%",
                "Status": "SUCCESS",
                "Time": f"{elapsed}s"
            })
        else:
            summary.append({
                "Disease": name,
                "Best Architecture": "N/A",
                "Accuracy": "N/A",
                "F1-Score": "N/A",
                "Status": f"FAILED (Exit {ret.returncode})",
                "Time": f"{elapsed}s"
            })
            
    total_elapsed = round(time.time() - start_time, 1)
    print("\n" + "=" * 70)
    print("6-DISEASE TRAINING SUMMARY")
    print("=" * 70)
    summary_df = pd.DataFrame(summary)
    print(summary_df.to_string(index=False))
    print(f"\nTotal Pipeline Execution Time: {total_elapsed}s")
    
    summary_csv = os.path.join(root_dir, "results", "tabular", "all_models_summary.csv")
    summary_df.to_csv(summary_csv, index=False)
    print(f"Saved master summary to: {summary_csv}")

if __name__ == "__main__":
    main()
