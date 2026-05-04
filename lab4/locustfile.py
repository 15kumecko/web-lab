from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def complex_scenario(self):
        payload = {
            "id": 100,
            "author_id": 1,
            "title": "Load Test Article",
            "content": "Content"
        }
        
        response = self.client.post("/articles", json=payload)
        
        if response.status_code == 201:
            article_id = response.json().get("id")
            self.client.delete(f"/articles/{article_id}")
