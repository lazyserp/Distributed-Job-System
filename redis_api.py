from fastapi import FastAPI
import redis
import uuid
import json


app = FastAPI()

r = redis.Redis(host='localhost',port=6379, decode_responses=True)

@app.post("/submit")
def submit(duration:int):
    job_id = str(uuid.uuid4())

    job_data = json.dumps({"job_id": job_id, "duration":duration}
                          )
    r.set(job_id, "Pending")

    r.lpush("job_queue", job_data)

    return {"job_id": job_id, "status": "Pending"}



@app.get("/status/{job_id}")
def get_status(job_id:str):
    status = r.get(job_id)
    return {"job_id": job_id, "status": status or "Not Found"}