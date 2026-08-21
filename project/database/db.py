import os
import psycopg

conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

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