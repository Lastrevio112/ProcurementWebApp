This project displays two dashboards of my personal expenses. 
The first dashboard is an expense overview with line charts, bar charts and KPIs while the second one is a transaction data with a table of each transaction and filters on the right.

The source data can be found in the 'Data' folder. It is an Excel file where I record every single thing I buy. 
The Excel contains multiple sheets, each sheet representing a month-year combination. The first column of the sheet contains the day of the month (from 1 to 31) while the other columns represent products I buy.

A PosgreSQL database was created in supabase and tables were created there in a snowflake schema:
1. F_Expenses is the main fact table containing each transaction.
2. MD_Product is a dimension table referncing the fact table which contains each possible product I buy (the columns in the source data).
3. D_Category is a sub-dimension table that references MD_Product that classifies my expenses into four categories: food, transport, utilities and undefined.
4. D_Time is a calendar look-up dimension table containing all the dates between two intervals and the year, month, day and month_text of each particular date. It references F_Expenses.

The Python code connects to this database in database_conn_func.py and appends all of the sheets of the source data into a single dataframe which is then fed into the scripts in the ETL folder.

Each script in the ETL folder creates a dataframe representing each of the tables in the SQL database and then pushes it into the database directly through a _clear and replace_ data loading process.

The batch file run_etl.bat runs the ETL scripts in a certain order, updating the database with the new source data.

The file ProcurementSpendProject_PowerBIProject.pbix is the PowerBI project where I created all the dashboards.

The index.html loads this PBI project into a Web App.

Here are some screenshots from the final dashboard:
![image](https://github.com/user-attachments/assets/6500b205-1d6e-41f5-9aba-849490ccf3a8)
![image](https://github.com/user-attachments/assets/81eb41f9-52ca-4d46-8dfe-1614a885a6f3)
