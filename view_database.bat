@echo off
title HexaDisease Database Inspector
echo ======================================================================
echo HexaDisease - Database Records Inspector (MySQL Workbench View)
echo ======================================================================
echo.

set "PY_BIN=python"
if exist "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python3.13.exe" (
    set "PY_BIN=C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python3.13.exe"
)

"%PY_BIN%" "%~dp0view_db.py"

echo.
pause
