@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo  BILL X-RAY - PASS 45.3 FOUR SYNTHESIS SIGNATURES
echo ========================================================
py -3 SMOKE_TEST_PASS_45_3.py
if errorlevel 1 goto :fail
echo.
echo PASS 45.3: CLEAR
echo Four laws. Four synthesis signatures. Same doctrine.
pause
exit /b 0
:fail
echo.
echo PASS 45.3: NOT CLEAR
pause
exit /b 1
