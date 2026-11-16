"""
HexaDisease Flask API
High-performance REST API for the 6 Closely Related Tabular Diseases:
1. Diabetes Mellitus (Metabolic)
2. Cerebrovascular Stroke (Vascular / Neurological)
3. Heart Failure & Cardiac Risk (Cardiovascular)
4. Chronic Kidney Disease (CKD) (Renal)
5. Hypertension / Maternal Vascular Risk (Vascular)
6. Clinical Anemia (Hematology / Oxygen Transport)
"""

import os
import sys
import json
import tempfile
import traceback
from flask import Flask, request, jsonify, make_response

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(CURRENT_DIR, "report_analysis")
RECOM_DIR = os.path.join(CURRENT_DIR, "recommendation")
PRED_DIR = os.path.join(CURRENT_DIR, "prediction")
DB_DIR = os.path.join(CURRENT_DIR, "database")

for p in (REPORT_DIR, RECOM_DIR, PRED_DIR, DB_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# Import Database & Tracking Engines
try:
    from db import (
        save_report, list_reports, get_report, delete_report,
        register_user, login_user, get_user_by_token, logout_user
    )
    from comparison_engine import compare_two_reports
    from biomarker_encyclopedia import BIOMARKER_ENCYCLOPEDIA, get_biomarker_info
    DB_AVAILABLE = True
except Exception as e:
    DB_AVAILABLE = False
    print(f"[WARNING] Database engine warning: {e}")

# Import Analysis and Prediction Engines
try:
    from analyze_report import analyze_report_file, analyze_report_text
    from tabular_prediction import predict_tabular_disease, SUPPORTED_DISEASES
    ML_AVAILABLE = True
    ML_IMPORT_ERROR = None
except Exception as e:
    ML_AVAILABLE = False
    ML_IMPORT_ERROR = str(e)
    SUPPORTED_DISEASES = {}
    print(f"[WARNING] ML pipeline not fully loaded: {e}")

app = Flask(__name__)
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt", ".json"}

DISEASE_METADATA = [
    {
        "id": "diabetes",
        "name": "Diabetes Mellitus",
        "category": "Metabolic",
        "best_model": "Diabetes & Glycemic Assessment Model",
        "accuracy": "75.0%",
        "primary_inputs": ["Blood Glucose (Fasting/PP)", "HbA1c", "BMI", "Blood Pressure", "Cholesterol"],
        "description": "Evaluates risk of Type 2 Diabetes and glycemic dysregulation using validated clinical indicators."
    },
    {
        "id": "stroke",
        "name": "Cerebrovascular Stroke",
        "category": "Vascular / Neurological",
        "best_model": "Cerebrovascular Stroke Risk Model",
        "accuracy": "80.5%",
        "primary_inputs": ["Systolic BP", "Diastolic BP", "Average Glucose", "BMI", "Smoking Status", "Age"],
        "description": "Multi-factorial vascular risk model evaluating acute and long-term cerebrovascular stroke likelihood."
    },
    {
        "id": "heart_disease",
        "name": "Heart Failure & Cardiac Risk",
        "category": "Cardiovascular",
        "best_model": "Cardiac Function & Heart Failure Model",
        "accuracy": "85.0%",
        "primary_inputs": ["Ejection Fraction (LVEF)", "CPK", "Serum Creatinine", "Serum Sodium", "Blood Pressure", "Platelets"],
        "description": "Assesses myocardial function, ejection fraction reduction, and cardiorenal heart failure risk."
    },
    {
        "id": "kidney_disease",
        "name": "Chronic Kidney Disease (CKD)",
        "category": "Renal",
        "best_model": "Kidney Function & Renal Filtration Model",
        "accuracy": "100.0%",
        "primary_inputs": ["Serum Creatinine", "Blood Urea", "eGFR", "Urine Albumin (Proteinuria)", "Specific Gravity"],
        "description": "Detects renal parenchymal impairment, glomerular filtering degradation, and nephropathy."
    },
    {
        "id": "hypertension_maternal_risk",
        "name": "Hypertension / Maternal Vascular Risk",
        "category": "Vascular",
        "best_model": "Vascular & Maternal Health Model",
        "accuracy": "84.2%",
        "primary_inputs": ["Systolic Blood Pressure", "Diastolic Blood Pressure", "Blood Glucose (BS)", "Heart Rate", "Body Temp"],
        "description": "Monitors gestational hypertension, preeclampsia cutoffs, and maternal hemodynamic strain."
    },
    {
        "id": "anemia",
        "name": "Clinical Anemia",
        "category": "Hematology / Oxygen Transport",
        "best_model": "Anemia & Oxygen Transport Model",
        "accuracy": "100.0%",
        "primary_inputs": ["Hemoglobin (Hb)", "Hematocrit (PCV)", "RBC Count", "WBC", "Platelets"],
        "description": "Quantifies circulating oxygenation capacity, microcytic/macrocytic anemia, and WHO severity stages."
    }
]

def cors_response(data, status=200):
    if isinstance(data, dict) or isinstance(data, list):
        resp = make_response(json.dumps(data), status)
    else:
        resp = make_response(data, status)
    resp.headers["Content-Type"] = "application/json"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    resp.headers["Access-Control-Max-Age"] = "86400"
    return resp

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

@app.route("/")
def index():
    return cors_response({
        "name": "HexaDisease AI Diagnostic API",
        "version": "2.0",
        "panel": "6 Closely Related Tabular Diseases",
        "status": "running",
        "ml_available": ML_AVAILABLE,
        "endpoints": {
            "health": "GET /api/health",
            "diseases": "GET /api/diseases",
            "analyze": "POST /api/analyze",
            "predict": "POST /api/predict"
        }
    })

@app.route("/api/health")
def health():
    return cors_response({
        "status": "ok",
        "ml_available": ML_AVAILABLE,
        "ml_error": ML_IMPORT_ERROR,
        "disease_count": len(DISEASE_METADATA)
    })

@app.route("/api/diseases", methods=["GET"])
def get_diseases():
    return cors_response({
        "total": len(DISEASE_METADATA),
        "diseases": DISEASE_METADATA
    })

@app.route("/api/analyze", methods=["GET", "POST", "OPTIONS"])
def analyze():
    if request.method in ("GET", "OPTIONS"):
        return cors_response({"message": "Send a POST request with a 'file' (multipart) or JSON {'text': '...'}"})

    if not ML_AVAILABLE:
        return cors_response({
            "error": f"ML pipeline failed to load: {ML_IMPORT_ERROR}",
            "decision": "SERVICE UNAVAILABLE",
            "conditions": [], "findings": [], "guidance": [],
            "extracted_values": {}, "model_results": [], "notes": []
        }, 503)

    try:
        # File upload
        if "file" in request.files:
            uploaded = request.files["file"]
            if not uploaded.filename:
                return cors_response({"error": "No file selected"}, 400)

            suffix = os.path.splitext(uploaded.filename)[1].lower()
            if suffix not in ALLOWED_EXTENSIONS:
                return cors_response({"error": f"Unsupported file type '{suffix}'. Use PDF, PNG, JPG, TXT, or JSON."}, 400)

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                uploaded.save(tmp.name)
                tmp_path = tmp.name

            try:
                result = analyze_report_file(tmp_path, use_ml=True)
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

        # Raw text or JSON
        elif request.is_json and request.json.get("text"):
            result = analyze_report_text(request.json["text"], use_ml=True)

        elif request.is_json and request.json.get("values"):
            from analyze_report import analyze_values
            result = analyze_values(request.json["values"], use_ml=True, source_description="Manual Input Values")

        else:
            return cors_response({"error": "Send a 'file' field (multipart) or JSON {'text': '...'}"}, 400)

        return cors_response(_make_serialisable(result))

    except Exception:
        err = traceback.format_exc()
        print(f"[ERROR] /api/analyze failed:\n{err}")
        return cors_response({
            "error": "Analysis execution failed on server.",
            "detail": err.splitlines()[-1],
            "decision": "ERROR",
            "conditions": [], "findings": [], "guidance": [],
            "extracted_values": {}, "model_results": [], "notes": []
        }, 500)

@app.route("/api/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    if not request.is_json:
        return cors_response({"error": "JSON body required: {'disease': '...', 'features': {...}}"}, 400)

    data = request.json
    disease = data.get("disease")
    features = data.get("features", {})

    if not disease:
        return cors_response({"error": "Missing 'disease' parameter in JSON."}, 400)

    try:
        res = predict_tabular_disease(disease, features, show_recommendation=False)
        return cors_response(_make_serialisable(res))
    except Exception as e:
        return cors_response({"error": f"Prediction failed: {str(e)}"}, 500)

# =========================================================================
# USER AUTHENTICATION & SESSION MANAGEMENT ENDPOINTS
# =========================================================================

def get_current_user():
    """Extracts user profile from Authorization Bearer token or custom header."""
    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    elif "X-Session-Token" in request.headers:
        token = request.headers.get("X-Session-Token", "").strip()
    elif "token" in request.args:
        token = request.args.get("token", "").strip()

    if not token or not DB_AVAILABLE:
        return None
    try:
        return get_user_by_token(token)
    except Exception as e:
        print(f"[AUTH ERROR] Token resolution failed: {e}")
        return None

@app.route("/api/auth/register", methods=["POST", "OPTIONS"])
def api_register():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    if not DB_AVAILABLE:
        return cors_response({"error": "Database service unavailable"}, 503)

    if not request.is_json:
        return cors_response({"error": "JSON payload required."}, 400)

    data = request.json
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    name = data.get("name", "").strip()
    age = data.get("age", 45)
    gender = data.get("gender", "Unspecified")
    blood_group = data.get("blood_group", "O+")

    if not email or not password or not name:
        return cors_response({"error": "Name, email, and password are required."}, 400)

    if len(password) < 6:
        return cors_response({"error": "Password must be at least 6 characters long."}, 400)

    try:
        res = register_user(
            email=email,
            password=password,
            name=name,
            age=age,
            gender=gender,
            blood_group=blood_group
        )
        return cors_response({
            "success": True,
            "message": f"Account created successfully for {name}!",
            "user": res["user"],
            "token": res["token"]
        }, 201)
    except ValueError as ve:
        return cors_response({"error": str(ve)}, 400)
    except Exception as e:
        return cors_response({"error": f"Registration failed: {str(e)}"}, 500)

@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
def api_login():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    if not DB_AVAILABLE:
        return cors_response({"error": "Database service unavailable"}, 503)

    if not request.is_json:
        return cors_response({"error": "JSON payload required."}, 400)

    data = request.json
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return cors_response({"error": "Email and password are required."}, 400)

    try:
        res = login_user(email=email, password=password)
        return cors_response({
            "success": True,
            "message": f"Welcome back, {res['user']['name']}!",
            "user": res["user"],
            "token": res["token"]
        }, 200)
    except ValueError as ve:
        return cors_response({"error": str(ve)}, 401)
    except Exception as e:
        return cors_response({"error": f"Login failed: {str(e)}"}, 500)

@app.route("/api/auth/me", methods=["GET", "OPTIONS"])
def api_auth_me():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    user = get_current_user()
    if user:
        return cors_response({
            "authenticated": True,
            "user": user
        })
    else:
        return cors_response({
            "authenticated": False,
            "user": None
        })

@app.route("/api/auth/logout", methods=["POST", "OPTIONS"])
def api_logout():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    auth_header = request.headers.get("Authorization", "")
    token = auth_header[7:].strip() if auth_header.startswith("Bearer ") else request.headers.get("X-Session-Token", "")
    if token and DB_AVAILABLE:
        logout_user(token)

    return cors_response({"success": True, "message": "Signed out successfully."})

# =========================================================================
# LONGITUDINAL HEALTH TRACKING & REPORT COMPARISON ENDPOINTS
# =========================================================================

@app.route("/api/reports/save", methods=["POST", "OPTIONS"])
def api_save_report():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    if not request.is_json:
        return cors_response({"error": "JSON payload required."}, 400)

    data = request.json
    analysis = data.get("analysis")
    if not analysis:
        return cors_response({"error": "Missing 'analysis' object in payload."}, 400)

    current_user = get_current_user()
    user_id = current_user["id"] if current_user else None

    # Use logged-in user profile details if not explicitly overridden in payload
    patient_name = data.get("patient_name") or (current_user["name"] if current_user else "Self Routine Checkup")
    patient_age = data.get("patient_age") or (current_user["age"] if current_user else 45)
    patient_gender = data.get("patient_gender") or (current_user["gender"] if current_user else "Unspecified")
    filename = data.get("filename", "Routine_Lab_Report.pdf")

    try:
        report_id = save_report(
            analysis=analysis,
            user_id=user_id,
            patient_name=patient_name,
            patient_age=patient_age,
            patient_gender=patient_gender,
            filename=filename
        )
        return cors_response({
            "success": True,
            "report_id": report_id,
            "user_id": user_id,
            "message": f"Report saved successfully under patient '{patient_name}'."
        }, 201)
    except Exception as e:
        return cors_response({"error": f"Failed to persist report: {str(e)}"}, 500)

@app.route("/api/reports/history", methods=["GET", "OPTIONS"])
def api_report_history():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    try:
        current_user = get_current_user()
        if current_user:
            # Strictly return account-isolated reports for logged-in user
            reports = list_reports(user_id=current_user["id"])
        else:
            # For guest sessions, list guest reports (or all reports)
            reports = list_reports(user_id=None)

        return cors_response({
            "reports": reports,
            "count": len(reports),
            "user": current_user
        })
    except Exception as e:
        return cors_response({"error": f"Failed to fetch history: {str(e)}"}, 500)
    except Exception as e:
        return cors_response({"error": f"Failed to fetch history: {str(e)}"}, 500)

@app.route("/api/reports/<int:report_id>", methods=["GET", "DELETE", "OPTIONS"])
def api_single_report(report_id):
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    if request.method == "DELETE":
        try:
            delete_report(report_id)
            return cors_response({"success": True, "message": f"Report {report_id} deleted."})
        except Exception as e:
            return cors_response({"error": f"Delete failed: {str(e)}"}, 500)

    try:
        report = get_report(report_id)
        if not report:
            return cors_response({"error": f"Report {report_id} not found."}, 404)
        return cors_response({"report": report})
    except Exception as e:
        return cors_response({"error": f"Failed to fetch report {report_id}: {str(e)}"}, 500)

@app.route("/api/reports/compare", methods=["GET", "OPTIONS"])
def api_compare_reports():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    id1 = request.args.get("report1")
    id2 = request.args.get("report2")

    if not id1 or not id2:
        return cors_response({"error": "Both 'report1' and 'report2' query params required."}, 400)

    try:
        r1 = get_report(int(id1))
        r2 = get_report(int(id2))

        if not r1 or not r2:
            return cors_response({"error": "One or both reports could not be found."}, 404)

        # Sort chronologically so r1 is earlier baseline, r2 is recent
        if r1["id"] > r2["id"]:
            r1, r2 = r2, r1

        comparison = compare_two_reports(r1, r2)
        return cors_response({"comparison": _make_serialisable(comparison)})
    except Exception as e:
        return cors_response({"error": f"Comparison calculation failed: {str(e)}"}, 500)

@app.route("/api/biomarkers/encyclopedia", methods=["GET", "OPTIONS"])
def api_biomarker_encyclopedia():
    if request.method == "OPTIONS":
        return cors_response({}, 200)

    try:
        return cors_response({"encyclopedia": BIOMARKER_ENCYCLOPEDIA})
    except Exception as e:
        return cors_response({"error": f"Encyclopedia lookup failed: {str(e)}"}, 500)


def _make_serialisable(obj):
    if isinstance(obj, dict):
        return {k: _make_serialisable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_make_serialisable(i) for i in obj]
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[HexaDisease API] Running on port {port} | 6 Tabular Models Online: {ML_AVAILABLE}")
    app.run(host="0.0.0.0", port=port, debug=False)
