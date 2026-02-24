import threading
import queue
import time
from fastapi import FastAPI
import uuid
import uvicorn

app = FastAPI()

job_queue = queue.Queue()
results = {}
results_loc = threading.Lock()


def worker(worker_id ):
    print("Worker has started and waiting for jobs...")

    while True:
        job_id , job_duration = job_queue.get()

        print(f"Worker {worker_id} is processing a job for {job_duration} seconds.")
        with results_loc:
            results[job_id] = "Processing"

        time.sleep(job_duration)

        with results_loc:
            results[job_id] = "Completed"

        print(f"Worker {worker_id} has finished the job {job_id}")
        job_queue.task_done()


@app.on_event("startup")
def startup_event():
    for i in range(3):
        t = threading.Thread(target=worker,args=(i,),daemon=True)
        t.start()

    print("3 Workers are on standby")


@app.post("/submit")
def submit(duration:int):
    job_id = str(uuid.uuid4())

    with results_loc:
        results[job_id] = "Pending"

    job_queue.put((job_id,duration))

    return {"job_id":job_id,"status":"pending"}


@app.get("/status/{job_id}")
def get_status(job_id: str):

    with results_loc:
        status = results.get(job_id, "Not Found")
    return {"job_id": job_id, "status": status}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)