"""THIS SCRIPT TRUNCATES THE D_TIME TABLE AND THEN POPULATES IT WITH DATE DATA BETWEEN A START TIME AND END TIME"""

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

from database_conn_func import get_engine
engine = get_engine()

#set start date and end date for D_Time table
start_date = "2020-01-01"
end_date = "2050-12-31"

# Generate the date dimension dataframe
dates = pd.date_range(start=start_date, end=end_date, freq='D')
df = pd.DataFrame({
    'date_id': dates,
    'year': dates.year,
    'month': dates.month,
    'month_text': dates.month_name(),
    'day': dates.day
})

# Bulk load via pandas to database
with engine.begin() as conn:
    #Truncate existing table:
    conn.execute(text("DELETE FROM d_time"))

    #Bulk load dates into database:
    df.to_sql(
        'd_time',
        conn,
        if_exists='append',  # table must exist already with proper schema
        index=False,
        chunksize=2000
    )