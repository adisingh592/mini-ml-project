@echo off
title HexaDisease 6-Disease Diagnostic Platform
echo ======================================================================
echo Starting HexaDisease AI Multi-Disease Platform
echo Core 6 Tabular Diseases:
echo   1. Diabetes Mellitus (Metabolic)
echo   2. Cerebrovascular Stroke (Vascular / Neurological)
echo   3. Heart Failure & Cardiac Risk (Cardiovascular)
echo   4. Chronic Kidney Disease (CKD) (Renal)
echo   5. Hypertension / Maternal Vascular Risk (Vascular)
echo   6. Clinical Anemia (Hematology / Oxygen Transport)
echo ======================================================================
echo.

set "PY_BIN=python"
if exist "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python3.13.exe" (
    set "PY_BIN=C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python3.13.exe"
)

echo [1/2] Starting Flask REST API on http://localhost:8000 ...
start "HexaDisease API" cmd /k "cd /d "%~dp0" && "%PY_BIN%" api.py"

timeout /t 3 >nul

echo [2/2] Starting React Frontend on http://localhost:5173 ...
start "HexaDisease Frontend" cmd /k "cd /d "%~dp0frontend" && pnpm run dev"

echo.
echo ======================================================================
echo HexaDisease servers are starting:
echo   REST API   -> http://localhost:8000
echo   Health API -> http://localhost:8000/api/health
echo   Web UI     -> http://localhost:5173
echo   Lab Page   -> http://localhost:5173/predict
echo ======================================================================
echo.
pause
