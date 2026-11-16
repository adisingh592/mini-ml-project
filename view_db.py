#!/usr/bin/env python3
"""
HexaDisease - Interactive Database Inspector (MySQL Workbench Equivalent for HexaDisease)
Allows administrators and developers to inspect all database records, view users,
browse saved medical reports, and execute arbitrary SQL queries.
"""

import os
import sys
import json
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "hexadisease.db")

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
USE_POSTGRES = False

if DATABASE_URL and (DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")):
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        USE_POSTGRES = True
    except ImportError:
        USE_POSTGRES = False

def get_connection():
    if USE_POSTGRES:
        return psycopg2.connect(DATABASE_URL)
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def print_separator(char="=", length=90):
    print(char * length)

def view_summary():
    conn = get_connection()
    cur = conn.cursor()
    print_separator("=")
    engine_name = "Cloud PostgreSQL (Neon)" if USE_POSTGRES else f"Local SQLite ({os.path.relpath(DB_PATH, PROJECT_ROOT)})"
    print(f"  HEXADISEASE DATABASE INSPECTOR  |  Engine: {engine_name}")
    print_separator("=")

    try:
        if USE_POSTGRES:
            cur.execute("SELECT COUNT(*) FROM users;")
            users_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM reports;")
            reports_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM user_sessions;")
            sessions_count = cur.fetchone()[0]
        else:
            cur.execute("SELECT COUNT(*) FROM users;")
            users_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM reports;")
            reports_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM user_sessions;")
            sessions_count = cur.fetchone()[0]

        print(f"Total Registered Users:  {users_count}")
        print(f"Total Saved Reports:     {reports_count}")
        print(f"Active User Sessions:    {sessions_count}")
    except Exception as e:
        print(f"[Error querying summary] {e}")
    finally:
        cur.close()
        conn.close()

def view_users():
    conn = get_connection()
    cur = conn.cursor()
    print("\n" + "=" * 90)
    print("  REGISTERED USERS TABLE (privacy accounts)")
    print("=" * 90)
    try:
        if USE_POSTGRES:
            cur.execute("SELECT id, name, email, age, gender, created_at FROM users ORDER BY id ASC;")
            rows = cur.fetchall()
            if not rows:
                print("  No registered users found in database.")
                return
            print(f"{'ID':<4} | {'Name':<22} | {'Email':<30} | {'Age/Sex':<10} | {'Created At'}")
            print("-" * 90)
            for r in rows:
                age_sex = f"{r[3] or '-'}/{r[4] or '-'}"
                print(f"{r[0]:<4} | {str(r[1])[:22]:<22} | {str(r[2])[:30]:<30} | {age_sex:<10} | {str(r[5])[:19]}")
        else:
            cur.execute("SELECT id, name, email, age, gender, created_at FROM users ORDER BY id ASC;")
            rows = cur.fetchall()
            if not rows:
                print("  No registered users found in database.")
                return
            print(f"{'ID':<4} | {'Name':<22} | {'Email':<30} | {'Age/Sex':<10} | {'Created At'}")
            print("-" * 90)
            for r in rows:
                age_sex = f"{r['age'] or '-'}/{r['gender'] or '-'}"
                print(f"{r['id']:<4} | {str(r['name'])[:22]:<22} | {str(r['email'])[:30]:<30} | {age_sex:<10} | {str(r['created_at'])[:19]}")
    finally:
        cur.close()
        conn.close()

def view_reports():
    conn = get_connection()
    cur = conn.cursor()
    print("\n" + "=" * 115)
    print("  SAVED MEDICAL REPORTS TABLE (All User Entries)")
    print("=" * 115)
    try:
        query = """
            SELECT id, user_id, patient_name, filename, upload_date, health_score, 
                   primary_condition, stage_name, total_biomarkers, abnormal_count
            FROM reports 
            ORDER BY id DESC;
        """
        cur.execute(query)
        rows = cur.fetchall()
        if not rows:
            print("  No medical reports have been saved in the database yet.")
            return

        print(f"{'ID':<4} | {'User':<5} | {'Patient Name':<20} | {'Filename':<22} | {'Score':<6} | {'Biomarkers':<10} | {'Primary Condition / Stage'}")
        print("-" * 115)
        for r in rows:
            if USE_POSTGRES:
                u_id = str(r[1]) if r[1] is not None else "GUEST"
                print(f"{r[0]:<4} | {u_id:<5} | {str(r[2])[:20]:<20} | {str(r[3])[:22]:<22} | {r[5]:<6} | {r[8]} tests   | {str(r[6])} ({str(r[7])[:30]})")
            else:
                u_id = str(r["user_id"]) if r["user_id"] is not None else "GUEST"
                print(f"{r['id']:<4} | {u_id:<5} | {str(r['patient_name'])[:20]:<20} | {str(r['filename'])[:22]:<22} | {r['health_score']:<6} | {r['total_biomarkers']} tests   | {str(r['primary_condition'])} ({str(r['stage_name'])[:30]})")
    finally:
        cur.close()
        conn.close()

def view_report_detail(report_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if USE_POSTGRES:
            cur.execute("SELECT * FROM reports WHERE id = %s;", (report_id,))
            r = cur.fetchone()
            if not r:
                print(f"Report ID {report_id} not found.")
                return
            print("\n" + "=" * 80)
            print(f"  DETAILED REPORT VIEW: ID #{r[0]} - {r[2]} ({r[5]})")
            print("=" * 80)
            print(f"Owner User ID:        {r[1]}")
            print(f"Upload Timestamp:     {r[6]}")
            print(f"Health Score:         {r[7]} / 100 ({r[8]})")
            print(f"Primary Condition:    {r[9]}")
            print(f"Clinical Stage:       {r[10]}")
            print("\nExtracted Biomarkers JSON:")
            vals = json.loads(r[14]) if isinstance(r[14], str) else r[14]
            for k, v in vals.items():
                print(f"  * {k}: {v}")
        else:
            cur.execute("SELECT * FROM reports WHERE id = ?;", (report_id,))
            r = cur.fetchone()
            if not r:
                print(f"Report ID {report_id} not found.")
                return
            print("\n" + "=" * 80)
            print(f"  DETAILED REPORT VIEW: ID #{r['id']} - {r['patient_name']} ({r['filename']})")
            print("=" * 80)
            print(f"Owner User ID:        {r['user_id']}")
            print(f"Upload Timestamp:     {r['upload_date']}")
            print(f"Health Score:         {r['health_score']} / 100 ({r['overall_severity']})")
            print(f"Primary Condition:    {r['primary_condition']}")
            print(f"Clinical Stage:       {r['stage_name']}")
            print("\nExtracted Biomarkers:")
            vals = json.loads(r["extracted_values_json"]) if isinstance(r["extracted_values_json"], str) else r["extracted_values_json"]
            for k, v in vals.items():
                print(f"  * {k}: {v}")
    finally:
        cur.close()
        conn.close()

def execute_custom_sql(sql_query):
    conn = get_connection()
    cur = conn.cursor()
    print("\n" + "=" * 80)
    print(f"  EXECUTING SQL: {sql_query}")
    print("=" * 80)
    try:
        cur.execute(sql_query)
        if sql_query.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            if not rows:
                print("  0 rows returned.")
                return
            if USE_POSTGRES:
                colnames = [desc[0] for desc in cur.description]
                print(" | ".join(colnames))
                print("-" * 80)
                for r in rows:
                    print(" | ".join(str(val) for val in r))
            else:
                colnames = rows[0].keys()
                print(" | ".join(colnames))
                print("-" * 80)
                for r in rows:
                    print(" | ".join(str(r[c]) for c in colnames))
        else:
            conn.commit()
            print(f"  Query executed successfully. Rows affected: {cur.rowcount}")
    except Exception as e:
        print(f"  [SQL Error]: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "users":
            view_users()
        elif cmd == "reports":
            view_reports()
        elif cmd == "report" and len(sys.argv) > 2:
            view_report_detail(int(sys.argv[2]))
        elif cmd == "sql" and len(sys.argv) > 2:
            execute_custom_sql(" ".join(sys.argv[2:]))
        else:
            print("Usage: python view_db.py [users|reports|report <id>|sql <query>]")
    else:
        view_summary()
        view_users()
        view_reports()
        print("\n" + "-" * 90)
        print("Tip: To view details of a specific report:  python view_db.py report <id>")
        print("Tip: To run custom SQL query:              python view_db.py sql \"SELECT * FROM users\"")
        print("Tip: To view visual GUI in MySQL style:     Open database/hexadisease.db in 'DB Browser for SQLite'")
        print("-" * 90)
