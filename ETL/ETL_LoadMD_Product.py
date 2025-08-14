"""THIS SCRIPT TRUNCATES AND THEN LOADS DATA INTO MD_Product"""

import os
import pathlib
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from database_conn_func import get_engine
from ETL.ETL_LoadInitialData import return_df
from ETL.ETL_Taxonomy import returnTaxonomy

#Loading all source data into dataframe
df = return_df()

#Loading the engine for SQL
engine = get_engine()

#Loading the TAXONOMY for D_Category
category_map = returnTaxonomy()

# look up the category_id values from the d_category table once:
cat_df = pd.read_sql("SELECT category_id, category_desc FROM d_category", engine)
cat_lookup = cat_df.set_index('category_desc')['category_id'].to_dict()

#List of values in MD_Product_df
MD_values = list(df.columns)
MD_values = [x.strip() for x in MD_values] #This line fixes a bug where INTERNET was wrongly classified as Undefined because of a blank space

columns_to_remove = ['DAY', 'sheet_name']
for col in columns_to_remove:
    MD_values.remove(col)

MD_Product_df = pd.DataFrame()
MD_Product_df['product_id'] = pd.Series(range(1, len(MD_values) + 1))
MD_Product_df['product_desc'] = pd.Series(MD_values)
# add the category_id column
MD_Product_df['category_id'] = (
    MD_Product_df['product_desc']
    .map(category_map)                 # map to 'Food', 'Transport', etc.
    .map(cat_lookup)                   # map to the integer key
    .fillna(cat_lookup['Undefined'])  # optional: default “Undefined"
)

#bulk-insert into database
with engine.begin() as conn:
    MD_Product_df.to_sql(
        "md_product",
        conn,
        if_exists="append",
        index=False,
        chunksize=2000
    )