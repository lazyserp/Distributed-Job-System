import sqlite3
import os

# Read from environment variable, default to 'jobs.db'
DB_NAME = os.getenv("DB_NAME", "jobs.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (job_id TEXT PRIMARY KEY, 
                  duration INTEGER, 
                  status TEXT, 
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def update_job_status(job_id, status):
    # Added timeout=10 to wait if the DB is busy
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status =  ? WHERE job_id = ?" , (status, job_id))
    conn.commit()
    conn.close()

def create_job_record(job_id, duration):
    # Added timeout=10
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (job_id, duration, status) VALUES (?,?,?)", (job_id, duration, "Pending"))
    conn.commit()
    conn.close()