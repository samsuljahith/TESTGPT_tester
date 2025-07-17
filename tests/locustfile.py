from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    @task
    def get_rockets(self):
        self.client.get("/rockets/123", host="http://localhost:4000")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000

class AssertStats:
    class Meta:
        stats = "stats.csv"

class UserWithAssert(TaskSet):
    @task
    def get_rockets(self):
        self.client.get("/rockets/123", host="http://localhost:4000")

    def on_start(self):
        self.stats.incr("requests")

class WebsiteUserWithAssert(HttpLocust):
    task_set = UserWithAssert
    min_wait = 5000
    max_wait = 9000
    stop_timeout = 0.1
    stop_max_duration = 600
    stop_on_assert = AssertStats()