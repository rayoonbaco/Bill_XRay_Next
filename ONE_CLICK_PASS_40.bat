@echo off
setlocal
cd /d "%~dp0"
cls
echo ========================================================================
echo  BILL X-RAY NEXT - PASS 40 ONE-CLICK SMOKE CAST
echo ========================================================================
echo.
echo Runs FROM the main Bill_XRay_Next folder.
echo No patch folder. No sibling project dependency. No pytest requirement.
echo.
python SMOKE_TEST_PASS_40.py
if errorlevel 1 (
 echo.
 echo ========================================================================
 echo  NEEDS REVIEW - PASS 40 DID NOT CLEAR
 echo ========================================================================
 echo.
 pause
 exit /b 1
)
echo.
echo ========================================================================
echo  CLEAR - PASS 40 ENGINE PASSED - READ THE HUMAN VERDICT ABOVE
echo ========================================================================
echo.
pause
endlocal
