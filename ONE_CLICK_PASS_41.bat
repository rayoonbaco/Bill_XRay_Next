@echo off
setlocal
cd /d "%~dp0"
echo ========================================================================
echo  BILL X-RAY NEXT - PASS 41 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
echo Runs FROM the main Bill_XRay_Next folder.
echo No patch folder. No sibling project dependency. No pytest requirement.
echo.
python SMOKE_TEST_PASS_41.py
if errorlevel 1 (
  echo.
  echo ========================================================================
  echo  NEEDS REVIEW - PASS 41 DID NOT CLEAR
  echo ========================================================================
) else (
  echo.
  echo ========================================================================
  echo  CLEAR - PASS 41 ENGINE PASSED - READ THE HUMAN GATE ABOVE
  echo ========================================================================
)
echo.
pause
endlocal
