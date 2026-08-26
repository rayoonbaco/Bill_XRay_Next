@echo off
setlocal
cd /d "%~dp0"
echo ========================================================================
echo  BILL X-RAY NEXT - PASS 41.1 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
echo Runs FROM the main Bill_XRay_Next folder.
echo No patch folder. No sibling project dependency. No pytest requirement.
echo.
python SMOKE_TEST_PASS_41_1.py
if errorlevel 1 (
  echo.
  echo ========================================================================
  echo  NEEDS REVIEW - PASS 41.1 DID NOT CLEAR
  echo ========================================================================
) else (
  echo.
  echo ========================================================================
  echo  CLEAR - PASS 41.1 ENGINE PASSED - READ THE HUMAN GATES ABOVE
  echo ========================================================================
)
echo.
pause
endlocal
