from fastapi import FastAPI
import redis.asyncio as redis
import json
import uuid
import os
from database import init_db, create_job_record, get_job_status

app = FastAPI()

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/submit")
async def submit(duration: int):
    job_id = str(uuid.uuid4())
    
    # Use the database function
    create_job_record(job_id, duration)
    
    job_data = json.dumps({"job_id": job_id, "duration": duration})
    await r.lpush("job_queue", job_data)
    
    return {"job_id": job_id, "status": "Pending"}

@app.get("/status/{job_id}") 
async def get_status(job_id: str):
    # Call the new database function
    status = get_job_status(job_id)
    
    if status:
        return {"job_id": job_id, "status": status}
    else:
        return {"job_id": job_id, "status": "Not Found"}