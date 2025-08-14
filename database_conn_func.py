import os
import pypyodbc as odbc
from dotenv import load_dotenv

# ─── 1. CONFIGURATION ─────────────────────────────────────────────────────────
def connect():
    load_dotenv()

    DRIVER_NAME = os.environ["DRIVER_NAME"]
    SERVER_NAME = os.environ["SERVER_NAME"]
    DATABASE_NAME = os.environ["DATABASE_NAME"]
    DATABASE_USERNAME = os.environ["SQLSERVER_USERNAME"]
    DATABASE_PASSWORD = os.environ["SQLSERVER_PASSWORD"]

    connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        uid={DATABASE_USERNAME};
        pwd={DATABASE_PASSWORD};
        TrustServerCertificate=yes;
    """

    conn = odbc.connect(connection_string, autocommit=True)

    return conn

# ─── 2. CURSOR TO WRITE QUERIES ─────────────────────────────────────────────────────────
def return_cursor(connection):
    return connection.cursor()

