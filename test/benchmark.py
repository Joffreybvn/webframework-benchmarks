# locust -f benchmark.py
from locust import HttpUser, between, task


class APIUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def home(self):
        self.client.post("/", json={"name": "Jean", "age": 12})
