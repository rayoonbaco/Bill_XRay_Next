@echo off
setlocal
cd /d "%~dp0"
title BILL X-RAY NEXT - PASS 40.1

echo ========================================================================
echo  BILL X-RAY NEXT - PASS 40.1 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
echo Runs FROM the main Bill_XRay_Next folder.
echo No patch folder. No sibling project dependency. No pytest requirement.
echo.
python SMOKE_TEST_PASS_40_1.py
if errorlevel 1 (
  echo.
  echo ========================================================================
  echo  NEEDS REVIEW - PASS 40.1 DID NOT CLEAR
  echo ========================================================================
  pause
  exit /b 1
)
echo.
echo ========================================================================
echo  CLEAR - PASS 40.1 PASSED - READ THE HUMAN VERDICT ABOVE
 echo ========================================================================
pause
