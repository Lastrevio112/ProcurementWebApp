import os
import pathlib
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ─── 1. CONFIGURATION ─────────────────────────────────────────────────────────
def connect():
    load_dotenv()  # reads SUPABASE_* into os.environ

    DB_USER = os.environ["SUPABASE_USER"]
    DB_PW   = os.environ["SUPABASE_PW"]
    DB_HOST = os.environ["SUPABASE_HOST"]
    DB_PORT = os.environ.get("SUPABASE_PORT", "5432")
    DB_NAME = os.environ["SUPABASE_DB"]

    CONN_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PW}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return CONN_URL

# ─── 2. ENGINE FACTORY ─────────────────────────────────────────────────────────
def get_engine(CONN_URL, echo: bool = False):
    """Return a SQLAlchemy engine connected to your Postgres."""
    return create_engine(CONN_URL, echo=echo)
