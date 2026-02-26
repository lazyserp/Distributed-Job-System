from fastapi import FastAPI
import redis
import uuid
import json


app = FastAPI()

#Redis Local Host Server for single machine
r = redis.Redis(host='localhost',port=6379, decode_responses=True)

# Submit Api to submit a job 
@app.post("/submit")
def submit(duration:int):
    #Unique Job Id
    job_id = str(uuid.uuid4())

    #Makes job data as JSON , easy for storing multiple values
    job_data = json.dumps({"job_id": job_id, "duration":duration})

    #Set job_id status -> "Pending" in redis
    r.set(job_id, "Pending")

    #Pushing this new Job to the left of queue in Redis
    r.lpush("job_queue", job_data)

    #Return the JSON status to the user
    return {"job_id": job_id, "status": "Pending"}



#Get the status of the Job
@app.get("/status/{job_id}")
def get_status(job_id:str):
    #r.get() return the value of the key=job_id in redis
    status = r.get(job_id)
    return {"job_id": job_id, "status": status or "Not Found"}