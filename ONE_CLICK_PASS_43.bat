@echo off
setlocal
cd /d "%~dp0"
echo ========================================================================
echo  BILL X-RAY NEXT - PASS 43 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
echo Runs FROM the main Bill_XRay_Next folder.
echo No patch folder. No sibling project dependency. No pytest requirement.
echo.
py -3 SMOKE_TEST_PASS_43.py 2>nul
if errorlevel 1 python SMOKE_TEST_PASS_43.py
if errorlevel 1 (
  echo.
  echo ========================================================================
  echo  NEEDS REVIEW - PASS 43 DID NOT CLEAR
  echo ========================================================================
  pause
  exit /b 1
)
echo.
echo ========================================================================
echo  CLEAR - PASS 43 ENGINE PASSED - RAY GENERALIZATION GATE REQUIRED
echo ========================================================================
pause
