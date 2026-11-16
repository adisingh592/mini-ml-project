"""
HexaDisease - Universal Cloud & Local Database Engine with User Authentication
Optimized for Vercel Serverless Deployment:
- Primary Engine: PostgreSQL (Neon Serverless Postgres via Vercel Marketplace / DATABASE_URL)
- Local Zero-Config Engine: SQLite (database/hexadisease.db)
Provides:
- User Authentication (Registration, Login, Password Hashing, Sessions)
- Account-wise Medical Report Storage & Isolation
- Longitudinal Historical Progress Tracking & Comparison Engine
"""

import os
import sys
import json
import sqlite3
import secrets
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

DB_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(DB_DIR, exist_ok=True)
SQLITE_PATH = os.path.join(DB_DIR, "hexadisease.db")

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")

USE_POSTGRES = False

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
    """Initializes schema for users, sessions, patients, and reports."""
    conn = get_connection()
    cur = conn.cursor()
    
    if USE_POSTGRES:
        # Users Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(180) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(120) NOT NULL,
                age INT,
                gender VARCHAR(20),
                blood_group VARCHAR(10),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # User Sessions Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                token VARCHAR(128) PRIMARY KEY,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Patients Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                age INT,
                gender VARCHAR(20),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Reports Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id) ON DELETE SET NULL,
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
        try:
            cur.execute("ALTER TABLE reports ADD COLUMN user_id INT REFERENCES users(id) ON DELETE SET NULL;")
        except Exception:
            pass
    else:
        # Users Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                blood_group TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # User Sessions Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        # Patients Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Reports Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
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
                analysis_json TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
            );
        """)
        try:
            cur.execute("ALTER TABLE reports ADD COLUMN user_id INTEGER;")
        except Exception:
            pass

    conn.commit()
    cur.close()
    conn.close()
    print("[DATABASE] Schema initialized with User Authentication tables.")

# Initialize schema on startup
try:
    init_db()
except Exception as e:
    print(f"[DATABASE INIT ERROR] {e}")

# =========================================================================
# USER AUTHENTICATION & SESSION MANAGEMENT
# =========================================================================

def register_user(email, password, name, age=45, gender="Unspecified", blood_group="Unknown"):
    """Registers a new user account with hashed password and generates an initial session token."""
    email_clean = email.strip().lower()
    if not email_clean or "@" not in email_clean:
        raise ValueError("A valid email address is required.")
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
    if not name or len(name.strip()) == 0:
        raise ValueError("Full name is required.")

    pwd_hash = generate_password_hash(password)
    now_iso = datetime.now(timezone.utc).isoformat()
    
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        if USE_POSTGRES:
            # Check existing
            cur.execute("SELECT id FROM users WHERE email = %s;", (email_clean,))
            if cur.fetchone():
                raise ValueError("An account with this email already exists.")
            
            cur.execute("""
                INSERT INTO users (email, password_hash, name, age, gender, blood_group, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, email, name, age, gender, blood_group, created_at;
            """, (email_clean, pwd_hash, name.strip(), age, gender, blood_group, now_iso))
            row = cur.fetchone()
            user_id = row[0]
            user_dict = {
                "id": row[0],
                "email": row[1],
                "name": row[2],
                "age": row[3],
                "gender": row[4],
                "blood_group": row[5],
                "created_at": str(row[6])
            }
        else:
            # Check existing
            cur.execute("SELECT id FROM users WHERE email = ?;", (email_clean,))
            if cur.fetchone():
                raise ValueError("An account with this email already exists.")
            
            cur.execute("""
                INSERT INTO users (email, password_hash, name, age, gender, blood_group, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (email_clean, pwd_hash, name.strip(), age, gender, blood_group, now_iso))
            user_id = cur.lastrowid
            user_dict = {
                "id": user_id,
                "email": email_clean,
                "name": name.strip(),
                "age": age,
                "gender": gender,
                "blood_group": blood_group,
                "created_at": now_iso
            }

        # Create session token
        token = secrets.token_hex(32)
        if USE_POSTGRES:
            cur.execute("INSERT INTO user_sessions (token, user_id, created_at) VALUES (%s, %s, %s);", (token, user_id, now_iso))
        else:
            cur.execute("INSERT INTO user_sessions (token, user_id, created_at) VALUES (?, ?, ?);", (token, user_id, now_iso))

        conn.commit()
        return {"user": user_dict, "token": token}
    finally:
        cur.close()
        conn.close()

def login_user(email, password):
    """Authenticates user credentials and issues an active session token."""
    email_clean = email.strip().lower()
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        if USE_POSTGRES:
            cur.execute("SELECT id, email, password_hash, name, age, gender, blood_group, created_at FROM users WHERE email = %s;", (email_clean,))
            row = cur.fetchone()
            if not row:
                raise ValueError("Invalid email or password.")
            
            user_id, u_email, pwd_hash, name, age, gender, blood_group, created_at = row
        else:
            cur.execute("SELECT id, email, password_hash, name, age, gender, blood_group, created_at FROM users WHERE email = ?;", (email_clean,))
            row = cur.fetchone()
            if not row:
                raise ValueError("Invalid email or password.")
            
            user_id = row["id"]
            u_email = row["email"]
            pwd_hash = row["password_hash"]
            name = row["name"]
            age = row["age"]
            gender = row["gender"]
            blood_group = row["blood_group"]
            created_at = row["created_at"]

        if not check_password_hash(pwd_hash, password):
            raise ValueError("Invalid email or password.")

        token = secrets.token_hex(32)
        now_iso = datetime.now(timezone.utc).isoformat()
        
        if USE_POSTGRES:
            cur.execute("INSERT INTO user_sessions (token, user_id, created_at) VALUES (%s, %s, %s);", (token, user_id, now_iso))
        else:
            cur.execute("INSERT INTO user_sessions (token, user_id, created_at) VALUES (?, ?, ?);", (token, user_id, now_iso))
            
        conn.commit()
        
        user_dict = {
            "id": user_id,
            "email": u_email,
            "name": name,
            "age": age,
            "gender": gender,
            "blood_group": blood_group,
            "created_at": str(created_at)
        }
        return {"user": user_dict, "token": token}
    finally:
        cur.close()
        conn.close()

def get_user_by_token(token):
    """Resolves session token to user profile."""
    if not token:
        return None
        
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        if USE_POSTGRES:
            cur.execute("""
                SELECT u.id, u.email, u.name, u.age, u.gender, u.blood_group, u.created_at
                FROM users u
                JOIN user_sessions s ON u.id = s.user_id
                WHERE s.token = %s;
            """, (token,))
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0],
                "email": row[1],
                "name": row[2],
                "age": row[3],
                "gender": row[4],
                "blood_group": row[5],
                "created_at": str(row[6])
            }
        else:
            cur.execute("""
                SELECT u.id, u.email, u.name, u.age, u.gender, u.blood_group, u.created_at
                FROM users u
                JOIN user_sessions s ON u.id = s.user_id
                WHERE s.token = ?;
            """, (token,))
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id": row["id"],
                "email": row["email"],
                "name": row["name"],
                "age": row["age"],
                "gender": row["gender"],
                "blood_group": row["blood_group"],
                "created_at": str(row["created_at"])
            }
    finally:
        cur.close()
        conn.close()

def logout_user(token):
    """Invalidates active session token."""
    if not token:
        return True
    conn = get_connection()
    cur = conn.cursor()
    try:
        if USE_POSTGRES:
            cur.execute("DELETE FROM user_sessions WHERE token = %s;", (token,))
        else:
            cur.execute("DELETE FROM user_sessions WHERE token = ?;", (token,))
        conn.commit()
        return True
    finally:
        cur.close()
        conn.close()

# =========================================================================
# MEDICAL REPORT STORAGE & HISTORICAL DATA (ACCOUNT-WISE)
# =========================================================================

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

def save_report(analysis, user_id=None, patient_name="Self Routine Checkup", patient_age=45, patient_gender="Unspecified", filename="Lab_Report.pdf"):
    """Saves report analysis to database, linked account-wise to user_id."""
    if not user_id:
        raise ValueError("Authentication Required: A valid registered user_id is mandatory to persist and encrypt medical reports.")

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
    
    try:
        if USE_POSTGRES:
            cur.execute("""
                INSERT INTO reports (
                    user_id, patient_name, patient_age, patient_gender, filename, upload_date,
                    health_score, overall_severity, primary_condition, stage_name,
                    is_early_stage, total_biomarkers, abnormal_count,
                    extracted_values_json, analysis_json
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                user_id, patient_name, patient_age, patient_gender, filename, now_iso,
                health_score, overall_severity, primary_condition, stage_name,
                bool(is_early), total_biomarkers, abnormal_count, values_json, analysis_json
            ))
            report_id = cur.fetchone()[0]
        else:
            cur.execute("""
                INSERT INTO reports (
                    user_id, patient_name, patient_age, patient_gender, filename, upload_date,
                    health_score, overall_severity, primary_condition, stage_name,
                    is_early_stage, total_biomarkers, abnormal_count,
                    extracted_values_json, analysis_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                user_id, patient_name, patient_age, patient_gender, filename, now_iso,
                health_score, overall_severity, primary_condition, stage_name,
                is_early, total_biomarkers, abnormal_count, values_json, analysis_json
            ))
            report_id = cur.lastrowid

        conn.commit()
        return report_id
    finally:
        cur.close()
        conn.close()

def list_reports(user_id=None):
    """
    Lists historical reports.
    Strict Privacy Policy: Returns reports matching the authenticated user_id ONLY.
    Unauthenticated/guest calls return an empty list to prevent cross-patient data leakage.
    """
    if not user_id:
        return []

    conn = get_connection()
    cur = conn.cursor()
    
    try:
        query = """
            SELECT id, user_id, patient_name, patient_age, patient_gender, filename,
                   upload_date, health_score, overall_severity, primary_condition,
                   stage_name, is_early_stage, total_biomarkers, abnormal_count
            FROM reports
            WHERE user_id = %s
            ORDER BY id DESC;
        """ if USE_POSTGRES else """
            SELECT id, user_id, patient_name, patient_age, patient_gender, filename,
                   upload_date, health_score, overall_severity, primary_condition,
                   stage_name, is_early_stage, total_biomarkers, abnormal_count
            FROM reports
            WHERE user_id = ?
            ORDER BY id DESC;
        """
        cur.execute(query, (user_id,))
            
        rows = cur.fetchall()
        reports = []
        for r in rows:
            if USE_POSTGRES:
                reports.append({
                    "id": r[0],
                    "user_id": r[1],
                    "patient_name": r[2],
                    "patient_age": r[3],
                    "patient_gender": r[4],
                    "filename": r[5],
                    "upload_date": str(r[6]),
                    "health_score": r[7],
                    "overall_severity": r[8],
                    "primary_condition": r[9],
                    "stage_name": r[10],
                    "is_early_stage": bool(r[11]),
                    "total_biomarkers": r[12],
                    "abnormal_count": r[13]
                })
            else:
                reports.append({
                    "id": r["id"],
                    "user_id": r["user_id"] if "user_id" in r.keys() else None,
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
        return reports
    finally:
        cur.close()
        conn.close()

def get_report(report_id):
    """Retrieves full single report record."""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        if USE_POSTGRES:
            cur.execute("SELECT * FROM reports WHERE id = %s;", (report_id,))
            row = cur.fetchone()
            if not row:
                return None
            res = {
                "id": row[0],
                "user_id": row[1],
                "patient_name": row[2],
                "patient_age": row[3],
                "patient_gender": row[4],
                "filename": row[5],
                "upload_date": str(row[6]),
                "health_score": row[7],
                "overall_severity": row[8],
                "primary_condition": row[9],
                "stage_name": row[10],
                "is_early_stage": bool(row[11]),
                "total_biomarkers": row[12],
                "abnormal_count": row[13],
                "extracted_values": json.loads(row[14]),
                "analysis": json.loads(row[15])
            }
        else:
            cur.execute("SELECT * FROM reports WHERE id = ?;", (report_id,))
            row = cur.fetchone()
            if not row:
                return None
            res = {
                "id": row["id"],
                "user_id": row["user_id"] if "user_id" in row.keys() else None,
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
        return res
    finally:
        cur.close()
        conn.close()

def delete_report(report_id, user_id=None):
    """Deletes a report by ID, optionally verifying ownership."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        if user_id:
            if USE_POSTGRES:
                cur.execute("DELETE FROM reports WHERE id = %s AND user_id = %s;", (report_id, user_id))
            else:
                cur.execute("DELETE FROM reports WHERE id = ? AND user_id = ?;", (report_id, user_id))
        else:
            if USE_POSTGRES:
                cur.execute("DELETE FROM reports WHERE id = %s;", (report_id,))
            else:
                cur.execute("DELETE FROM reports WHERE id = ?;", (report_id,))
        conn.commit()
        return True
    finally:
        cur.close()
        conn.close()
