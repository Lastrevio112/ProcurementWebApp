import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
import urllib

# ─── 1. CONFIGURATION ─────────────────────────────────────────────────────────
def get_engine():
    load_dotenv()

    DRIVER_NAME = os.environ["DRIVER_NAME"]
    SERVER_NAME = os.environ["SERVER_NAME"]
    DATABASE_NAME = os.environ["DATABASE_NAME"]
    DATABASE_USERNAME = os.environ["SQLSERVER_USERNAME"]
    DATABASE_PASSWORD = os.environ["SQLSERVER_PASSWORD"]

    params = urllib.parse.quote_plus(f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        UID={DATABASE_USERNAME};
        PWD={DATABASE_PASSWORD};
        Encrypt=yes;
        TrustServerCertificate=yes;
        """
    )

    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        fast_executemany=True,
        pool_pre_ping=True,
    )

    return engine