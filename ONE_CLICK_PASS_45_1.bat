@echo off
setlocal
cd /d "%~dp0"
echo ========================================================================
echo  BILL X-RAY NEXT - PASS 45.1 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
python SMOKE_TEST_PASS_45_1.py
if errorlevel 1 (
  echo.
  echo ========================================================================
  echo  NEEDS REVIEW - PASS 45.1 DID NOT CLEAR
  echo ========================================================================
  pause
  exit /b 1
)
echo.
echo ========================================================================
echo  CLEAR - PASS 45.1 TRANSFORMATION LADDER PASSED
echo ========================================================================
pause
