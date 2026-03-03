import psycopg2
import os
import time

# FIX: Reading the correct variables from .env
# We read POSTGRES_DB for the database name, not DB_NAME
DB_NAME = os.getenv("POSTGRES_DB", "jobs_db")
DB_USER = os.getenv("POSTGRES_USER", "myuser")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "mypassword")
DB_HOST = os.getenv("DB_HOST", "db")

def get_connection():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST
            )
            return conn
        except psycopg2.OperationalError:
            print("Database not ready yet... waiting 3 seconds...")
            time.sleep(3)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (job_id TEXT PRIMARY KEY, 
                  duration INTEGER, 
                  status TEXT, 
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
    print("Database initialized!")

def update_job_status(job_id, status):
    conn = get_connection()
    c = conn.cursor()
    # IMPORTANT: Postgres uses %s, not ?
    c.execute("UPDATE jobs SET status = %s WHERE job_id = %s", (status, job_id))
    conn.commit()
    conn.close()

def create_job_record(job_id, duration):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO jobs (job_id, duration, status) VALUES (%s, %s, %s)", 
              (job_id, duration, "Pending"))
    conn.commit()
    conn.close()

def get_job_status(job_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT status FROM jobs WHERE job_id = %s", (job_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None   