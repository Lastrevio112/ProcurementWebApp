# test_conn.py
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  # loads SUPABASE_* into os.environ

url = (
    f"postgresql+psycopg2://{os.environ['SUPABASE_USER']}:"
    f"{os.environ['SUPABASE_PW']}@{os.environ['SUPABASE_HOST']}:"
    f"{os.environ['SUPABASE_PORT']}/{os.environ['SUPABASE_DB']}"
)
engine = create_engine(url, echo=True)

with engine.begin() as conn:
    # wrap your SQL in sqlalchemy.text()
    version = conn.execute(text("SELECT version()")).scalar_one()
    print("🎉 Connected to:", version)
