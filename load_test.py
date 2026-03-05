import time
from locust import HttpUser, task, between, events

test_start_time = None

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global test_start_time
    test_start_time = time.time()
    print(f"Load test started at : {test_start_time}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    end_time = time.time()
    total = end_time - test_start_time

    print(f"Test ended at : {end_time}")
    print(f"Test duration : {total}s")


class JobProcessingUser(HttpUser):
    host = "http://api:8000"
    wait_time = between(1,3)

    @task
    def submit_job(self):

        #duration: int parameter for post api
        self.client.post("/submit?duration=6")


    @task(3) #Rune 3x more often than submit_job
    def check_status(self):
        #In a real scenario, users check status more than they submit
        pass
