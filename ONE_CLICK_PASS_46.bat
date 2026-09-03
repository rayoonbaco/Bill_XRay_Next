@echo off
cd /d "%~dp0"
python SMOKE_TEST_PASS_46.py
if errorlevel 1 (
  echo.
  echo PASS 46 FAILED. Read the errors above.
  pause
  exit /b 1
)
echo.
echo PASS 46 PASSED. SB 1570 is the fifth public case and its release checks passed.
pause
