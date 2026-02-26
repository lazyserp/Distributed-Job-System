import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def start_worker():
    print("👷 Worker started. Looking for jobs in Redis...")
    while True:
        # brpop returns (queue_name, data)
        _, job_data_raw = r.brpop("job_queue", timeout=0)
        
        job_data = json.loads(job_data_raw)
        job_id = job_data['job_id']
        duration = job_data['duration']

        # Update Redis status
        r.set(job_id, "Processing")
        print(f"Working on {job_id} for {duration}s")
        
        time.sleep(duration)

        # Update Redis status
        r.set(job_id, "Completed")
        print(f"Finished {job_id}")

if __name__ == "__main__":
    start_worker()