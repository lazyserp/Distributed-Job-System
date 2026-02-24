import threading
import queue
import random
import time



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


for i in range(3):
    t = threading.Thread(target=worker, args=(i,),daemon=True)
    t.start()

durations = [2, 5, 1, 4, 3, 2, 1, 2, 4, 2]

for i,duration in enumerate(durations):
    print(f" Producer adding a {i}s job to the queue.")
    job_queue.put((i,duration))


print("Main thread: Waiting for all jobs to finish...")
job_queue.join() 
print("All jobs are done!")


print(results)