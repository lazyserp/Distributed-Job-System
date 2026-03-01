import redis
import time
import json
from database import update_job_status # Use the fixed name

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def start_worker():
    print("Worker started. Looking for jobs in Redis...")
    while True:
        # Returns a tuple: (queue_name, data)
        result = r.brpop("job_queue", timeout=0)
        if result: # handling error for empty tuple
            _, job_data_raw = result
            job_data = json.loads(job_data_raw)

            try:           
                # 1. Update DB to Processing
                update_job_status(job_data['job_id'], 'Processing')
                
                # 2. Do the work
                time.sleep(job_data['duration'])
                
                # 3. Update DB to Completed
                update_job_status(job_data['job_id'], "Completed")

            except Exception as e:
                print(f"Error in {job_data['job_id']} : {e}")
                update_job_status(job_data['job_id'], "Failed")
        

if __name__ == "__main__":
    start_worker()