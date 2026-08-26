@echo off
setlocal
cd /d "%~dp0"
title Bill X-Ray Next - Pass 37

echo ========================================================================
echo  BILL X-RAY NEXT - PASS 37 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
echo Runs FROM the main Bill_XRay_Next folder.
echo No patch folder. No sibling project dependency. No pytest requirement.
echo.

python SMOKE_TEST_PASS_37.py
set EXITCODE=%ERRORLEVEL%

echo.
if "%EXITCODE%"=="0" (
  echo ========================================================================
  echo  CLEAR - PASS 37 PASSED
  echo ========================================================================
) else (
  echo ========================================================================
  echo  NEEDS REVIEW - PASS 37 DID NOT CLEAR
  echo ========================================================================
)
echo.
pause
exit /b %EXITCODE%
