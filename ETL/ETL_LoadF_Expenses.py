"""THIS SCRIPT TRUNCATES AND THEN LOADS THE MAIN FACT TABLE F_EXPENSES"""

import os
import pathlib
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

from database_conn_func import get_engine
from ETL.ETL_LoadInitialData import return_df
from ETL.ETL_Taxonomy import returnTaxonomy

#Loading all source data into dataframe
df = return_df()

#Loading the engine for SQL
engine = get_engine()

#Loading the TAXONOMY for D_Category
category_map = returnTaxonomy()

#Adding month and year columns to df
df_withMonthYear = df.copy()
df_withMonthYear['MONTH'] = df_withMonthYear['sheet_name'].str[-2:]
df_withMonthYear['YEAR'] = df_withMonthYear['sheet_name'].str[:4]
df_withMonthYear.drop(columns={'sheet_name'}, inplace=True)

#Melting "unpivoting" the table
columnsToMelt = list(df_withMonthYear.columns)
columnsToMelt.remove("YEAR")
columnsToMelt.remove("MONTH")
columnsToMelt.remove("DAY")

df_melted = df_withMonthYear.melt(
    id_vars=['DAY', 'MONTH', 'YEAR'],
    value_vars=columnsToMelt,
    var_name='product_desc',
    value_name='spend'
)

df_melted.dropna(inplace=True)
df_melted.sort_values(by=['YEAR', 'MONTH', 'DAY'], ascending=True, inplace=True)

#Joining to the product names from MD_Product to get the product IDs into our dataframe
mdproduct_df = pd.read_sql("SELECT product_id, product_desc FROM md_product", engine)
df_joined = df_melted.merge(mdproduct_df, on='product_desc')
#Removing the product_desc column as we don't need it for the final table
df_joined.drop(columns={"product_desc"}, inplace=True)

#Merging all three date columns into one
df_withdate = df_joined.copy()
cols = df_withdate[['YEAR','MONTH','DAY']].astype(int).rename(
    columns={'YEAR':'year','MONTH':'month','DAY':'day'}
)
df_withdate['date_id'] = pd.to_datetime(cols).dt.date   # <- python date objects for safe static typing
#Removing the day, month and year columns as they will not exist in the final table in SQL
df_withdate.drop(columns={'DAY', 'MONTH', 'YEAR'}, inplace=True)

#Adding the id as the primary key for this table
df_final = df_withdate.copy()
df_final['id'] = range(1, len(df_final) + 1)

#Changing the order of the columns to match the one in the database
df_final = df_final.iloc[:, [3, 0, 2, 1]] #stole the code from here: https://www.geeksforgeeks.org/change-the-order-of-a-pandas-dataframe-columns-in-python/

#bulk-insert into database
with engine.begin() as conn:
    conn.execute(text("DELETE FROM dbo.f_expenses"))

    df_final.to_sql(
        "f_expenses",
        conn,
        if_exists="append",
        index=False,
        chunksize=2000
    )