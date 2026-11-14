"""
HexaDisease - Universal Cloud & Local Database Engine
Optimized for Vercel Serverless Deployment:
- Primary Engine: PostgreSQL (Neon Serverless Postgres via Vercel Marketplace / DATABASE_URL)
- Local Zero-Config Engine: SQLite (database/hexadisease.db)
Provides persistent storage, historical tracking, and multi-report comparison.
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timezone

DB_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(DB_DIR, exist_ok=True)
SQLITE_PATH = os.path.join(DB_DIR, "hexadisease.db")

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")

# Check if PostgreSQL driver is available if DATABASE_URL is set
USE_POSTGRES = False
pg_pool = None

if DATABASE_URL and (DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")):
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        USE_POSTGRES = True
        print(f"[DATABASE] Connected to Cloud PostgreSQL (Neon / Vercel): {DATABASE_URL.split('@')[-1]}")
    except ImportError:
        print("[DATABASE WARNING] DATABASE_URL provided but psycopg2 not installed; falling back to SQLite.")
        USE_POSTGRES = False

def get_connection():
    """Returns database connection for either PostgreSQL (Neon) or SQLite."""
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Initializes schema for patients, reports, and biomarker logs."""
    conn = get_connection()
    cur = conn.cursor()
    
    if USE_POSTGRES:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                age INT,
                gender VARCHAR(20),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                patient_name VARCHAR(120) NOT NULL,
                patient_age INT,
                patient_gender VARCHAR(20),
                filename VARCHAR(255) NOT NULL,
                upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                health_score INT NOT NULL,
                overall_severity VARCHAR(50) NOT NULL,
                primary_condition VARCHAR(120) NOT NULL,
                stage_name VARCHAR(255),
                is_early_stage BOOLEAN DEFAULT FALSE,
                total_biomarkers INT DEFAULT 0,
                abnormal_count INT DEFAULT 0,
                extracted_values_json TEXT NOT NULL,
                analysis_json TEXT NOT NULL
            );
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                patient_age INTEGER,
                patient_gender TEXT,
                filename TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                health_score INTEGER NOT NULL,
                overall_severity TEXT NOT NULL,
                primary_condition TEXT NOT NULL,
                stage_name TEXT,
                is_early_stage INTEGER DEFAULT 0,
                total_biomarkers INTEGER DEFAULT 0,
                abnormal_count INTEGER DEFAULT 0,
                extracted_values_json TEXT NOT NULL,
                analysis_json TEXT NOT NULL
            );
        """)

    conn.commit()
    cur.close()
    conn.close()
    print("[DATABASE] Schema initialized successfully.")

# Run init_db on module import
try:
    init_db()
except Exception as e:
    print(f"[DATABASE INIT ERROR] {e}")

def calculate_health_score(analysis):
    """Computes a 0 to 100 overall clinical health score from report analysis."""
    findings = analysis.get("findings", [])
    if not findings:
        return 95
        
    score = 100
    for f in findings:
        sev = f.get("severity", 0)
        if sev == 3:  # URGENT
            score -= 22
        elif sev == 2:  # ABNORMAL
            score -= 12
        elif sev == 1:  # BORDERLINE
            score -= 5
            
    return max(15, min(100, score))

def save_report(analysis, patient_name="Self Routine Checkup", patient_age=45, patient_gender="Unspecified", filename="Lab_Report.pdf"):
    """Saves report analysis to database."""
    conn = get_connection()
    cur = conn.cursor()
    
    findings = analysis.get("findings", [])
    extracted_values = analysis.get("extracted_values", {})
    conditions = analysis.get("conditions", [])
    primary = conditions[0] if conditions else {"condition": "6-Disease Panel", "status": "Normal"}
    
    staging = analysis.get("staging", {})
    primary_stage = staging.get("primary_stage", {})
    stage_name = primary_stage.get("stage_name", "Stage 0: Normal Baseline")
    is_early = 1 if primary_stage.get("is_early_stage") else 0
    
    health_score = calculate_health_score(analysis)
    overall_severity = analysis.get("overall_severity", "Normal")
    primary_condition = primary.get("condition", "General Clinical Screening")
    
    total_biomarkers = len(findings) if findings else len(extracted_values)
    abnormal_count = len([f for f in findings if f.get("severity", 0) > 0])
    
    values_json = json.dumps(extracted_values)
    analysis_json = json.dumps(analysis)
    
    now_iso = datetime.now(timezone.utc).isoformat()
    
    if USE_POSTGRES:
        cur.execute("""
            INSERT INTO reports (
                patient_name, patient_age, patient_gender, filename, upload_date,
                health_score, overall_severity, primary_condition, stage_name,
                is_early_stage, total_biomarkers, abnormal_count,
                extracted_values_json, analysis_json
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            patient_name, patient_age, patient_gender, filename, now_iso,
            health_score, overall_severity, primary_condition, stage_name,
            bool(is_early), total_biomarkers, abnormal_count, values_json, analysis_json
        ))
        report_id = cur.fetchone()[0]
    else:
        cur.execute("""
            INSERT INTO reports (
                patient_name, patient_age, patient_gender, filename, upload_date,
                health_score, overall_severity, primary_condition, stage_name,
                is_early_stage, total_biomarkers, abnormal_count,
                extracted_values_json, analysis_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            patient_name, patient_age, patient_gender, filename, now_iso,
            health_score, overall_severity, primary_condition, stage_name,
            is_early, total_biomarkers, abnormal_count, values_json, analysis_json
        ))
        report_id = cur.lastrowid

    conn.commit()
    cur.close()
    conn.close()
    return report_id

def list_reports():
    """Lists all historical reports with clinical metadata."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, patient_name, patient_age, patient_gender, filename,
               upload_date, health_score, overall_severity, primary_condition,
               stage_name, is_early_stage, total_biomarkers, abnormal_count
        FROM reports
        ORDER BY id DESC;
    """)
    rows = cur.fetchall()
    
    reports = []
    for r in rows:
        if USE_POSTGRES:
            reports.append({
                "id": r[0],
                "patient_name": r[1],
                "patient_age": r[2],
                "patient_gender": r[3],
                "filename": r[4],
                "upload_date": str(r[5]),
                "health_score": r[6],
                "overall_severity": r[7],
                "primary_condition": r[8],
                "stage_name": r[9],
                "is_early_stage": bool(r[10]),
                "total_biomarkers": r[11],
                "abnormal_count": r[12]
            })
        else:
            reports.append({
                "id": r["id"],
                "patient_name": r["patient_name"],
                "patient_age": r["patient_age"],
                "patient_gender": r["patient_gender"],
                "filename": r["filename"],
                "upload_date": str(r["upload_date"]),
                "health_score": r["health_score"],
                "overall_severity": r["overall_severity"],
                "primary_condition": r["primary_condition"],
                "stage_name": r["stage_name"],
                "is_early_stage": bool(r["is_early_stage"]),
                "total_biomarkers": r["total_biomarkers"],
                "abnormal_count": r["abnormal_count"]
            })
            
    cur.close()
    conn.close()
    return reports

def get_report(report_id):
    """Retrieves full single report record."""
    conn = get_connection()
    cur = conn.cursor()
    
    if USE_POSTGRES:
        cur.execute("SELECT * FROM reports WHERE id = %s;", (report_id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            return None
        # Format response
        res = {
            "id": row[0],
            "patient_name": row[1],
            "patient_age": row[2],
            "patient_gender": row[3],
            "filename": row[4],
            "upload_date": str(row[5]),
            "health_score": row[6],
            "overall_severity": row[7],
            "primary_condition": row[8],
            "stage_name": row[9],
            "is_early_stage": bool(row[10]),
            "total_biomarkers": row[11],
            "abnormal_count": row[12],
            "extracted_values": json.loads(row[13]),
            "analysis": json.loads(row[14])
        }
    else:
        cur.execute("SELECT * FROM reports WHERE id = ?;", (report_id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            return None
        res = {
            "id": row["id"],
            "patient_name": row["patient_name"],
            "patient_age": row["patient_age"],
            "patient_gender": row["patient_gender"],
            "filename": row["filename"],
            "upload_date": str(row["upload_date"]),
            "health_score": row["health_score"],
            "overall_severity": row["overall_severity"],
            "primary_condition": row["primary_condition"],
            "stage_name": row["stage_name"],
            "is_early_stage": bool(row["is_early_stage"]),
            "total_biomarkers": row["total_biomarkers"],
            "abnormal_count": row["abnormal_count"],
            "extracted_values": json.loads(row["extracted_values_json"]),
            "analysis": json.loads(row["analysis_json"])
        }
        
    cur.close()
    conn.close()
    return res

def delete_report(report_id):
    """Deletes a report by ID."""
    conn = get_connection()
    cur = conn.cursor()
    if USE_POSTGRES:
        cur.execute("DELETE FROM reports WHERE id = %s;", (report_id,))
    else:
        cur.execute("DELETE FROM reports WHERE id = ?;", (report_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True
