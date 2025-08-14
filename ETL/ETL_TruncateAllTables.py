from sqlalchemy import create_engine, text
from database_conn_func import get_engine

engine = get_engine()

#Truncate all tables because of clear & replace data loading process
with engine.begin() as conn:
    #We use DELETE FROM and not TRUNCATE because of FK constraints in SQL server
    #We delete children first and then move up the hierarchy - in the batch file that runs the load procedures, the order is reversed
    conn.execute(text("DELETE FROM dbo.f_expenses;"
                      "DELETE FROM dbo.md_product;"
                      "DELETE FROM dbo.d_category;"
                      "DELETE FROM dbo.d_time;"))
