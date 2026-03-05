import redis
import time
import json
import os
import socket
from database import update_job_status

# Read host from environment variable, default to localhost
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
WORKER_ID = socket.gethost()

def start_worker():
    
    print(f"Worker started. Connected to Redis at {redis_host}...")
    while True:
        result = r.brpop("job_queue", timeout=0)
        if result:
            _, job_data_raw = result
            job_data = json.loads(job_data_raw)

            try:           
                update_job_status(job_data['job_id'], 'Processing', WORKER_ID)
                time.sleep(job_data['duration'])
                update_job_status(job_data['job_id'], "Completed",WORKER_ID)

            except Exception as e:
                print(f"Error in {job_data['job_id']} : {e}")
                # retry logic or simple wait to avoid DB lock
                time.sleep(0.5) 
                update_job_status(job_data['job_id'], "Failed")

if __name__ == "__main__":
    start_worker()