from locust import HttpUser, task, between


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
