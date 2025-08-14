@echo off
cd /d %~dp0

rem —––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
rem Activate virtualenv
call venv\Scripts\activate.bat
if errorlevel 1 goto :onError

rem —––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
rem Run your ETL steps

echo Truncating all tables...
python -m ETL.ETL_TruncateAllTables
if errorlevel 1 goto :onError

echo Running Category loader...
python -m ETL.ETL_LoadD_Category
if errorlevel 1 goto :onError

echo Running Product loader...
python -m ETL.ETL_LoadMD_Product
if errorlevel 1 goto :onError

echo Running Date loader...
python -m ETL.ETL_LoadD_Time
if errorlevel 1 goto :onError

echo Running Fact loader...
python -m ETL.ETL_LoadF_Expenses
if errorlevel 1 goto :onError


rem —––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
rem Clean up and exit normally
deactivate
echo.
echo All done! Press any key to exit…
pause
exit /b 0

:onError
rem —––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
rem One of the steps failed; notify and pause
echo.
echo *** ERROR: A step has failed. Press any key to exit and check the logs. ***
pause
exit /b 1