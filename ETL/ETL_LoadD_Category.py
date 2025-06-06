"""THIS SCRIPT TRUNCATES AND THEN LOADS DATA INTO D_CATEGORY BASED ON THE TAXONOMY CREATED IN ETL_Taxonomy.py"""

from sqlalchemy import create_engine, text
import pandas as pd

from database_conn_func import connect, get_engine
from ETL.ETL_Taxonomy import returnTaxonomy

taxonomy = returnTaxonomy()

#Creating the dataframe
d_category_df = pd.DataFrame()
# Get unique category names in order of first appearance:
all_categories = list(taxonomy.values())
unique_categories = list(dict.fromkeys(all_categories))
d_category_df = pd.DataFrame({
    'category_id': range(1, len(unique_categories) + 1),
    'category_desc': unique_categories
})

#Adding the undefined row
d_category_df.loc[3] = [4] + ['Undefined']

#Insert into database
engine = get_engine(connect())
with engine.begin() as conn:
    conn.execute(text("TRUNCATE d_category CASCADE"))
    d_category_df.to_sql(
        "d_category",
        conn,
        if_exists="append",
        index=False,
        method="multi"
    )