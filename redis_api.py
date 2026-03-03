from fastapi import FastAPI
import asyncio
import redis.asyncio as redis # Use async redis
import json
import uuid
import sqlite3
import os
from database import init_db, create_job_record, DB_NAME

app = FastAPI()

# Read host from environment variable
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/submit")
async def submit(duration: int):
    job_id = str(uuid.uuid4())
    create_job_record(job_id, duration)
    job_data = json.dumps({"job_id": job_id, "duration": duration})
    await r.lpush("job_queue", job_data)
    return {"job_id": job_id, "status": "Pending"}

@app.get("/status/{job_id}") 
async def get_status(job_id: str):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT status FROM jobs WHERE job_id = ?", (job_id,))
    result = c.fetchone()
    conn.close()
    return {"job_id": job_id, "status": result[0] if result else "Not Found"}