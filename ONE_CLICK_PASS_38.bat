@echo off
setlocal
cd /d "%~dp0"
title Bill X-Ray Next - Pass 38

echo ========================================================================
echo  BILL X-RAY NEXT - PASS 38 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
echo Runs FROM the main Bill_XRay_Next folder.
echo No patch folder. No sibling project dependency. No pytest requirement.
echo.

python SMOKE_TEST_PASS_38.py
set RC=%ERRORLEVEL%

echo.
if "%RC%"=="0" (
  echo ========================================================================
  echo  CLEAR - PASS 38 PASSED
  echo ========================================================================
) else (
  echo ========================================================================
  echo  NEEDS REVIEW - PASS 38 DID NOT CLEAR
  echo ========================================================================
)
echo.
pause
exit /b %RC%
