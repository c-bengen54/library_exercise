from pathlib import Path
from dotenv import load_dotenv
import psycopg, os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

conn = psycopg.connect(os.getenv("DATABASE_URL"))

"""
conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
"""

def _execute(query: str, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
    conn.commit()

def _fetch_all(query: str, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()
    
def _fetch_one(query:str, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchone()