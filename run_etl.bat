@echo off
cd /d %~dp0
call venv\Scripts\activate.bat

echo Running Category loader...
python -m ETL.ETL_LoadD_Category

echo Running Date loader...
python -m ETL.ETL_LoadD_Time

echo Running Product loader...
python -m ETL.ETL_LoadMD_Product

echo Running Fact loader...
python -m ETL.ETL_LoadF_Expenses

deactivate
echo.
echo All done! Press any key to exit…
pause
