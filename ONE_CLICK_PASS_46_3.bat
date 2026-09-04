@echo off
cd /d "%~dp0"
python SMOKE_TEST_PASS_46_3.py
if errorlevel 1 (
  echo.
  echo PASS 46.3 FAILED. Read the errors above.
  pause
  exit /b 1
)
echo.
echo PASS 46.3 PASSED. SB 1570 is current through P.A. 104-0395.
pause
