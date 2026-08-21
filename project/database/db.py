import psycopg

conn = psycopg.connect(
    dbname="library_db",
    user="christopherbengen",
    password="5401",
    host="localhost",
    port=5432
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