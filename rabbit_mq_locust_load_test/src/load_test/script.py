from locust import HttpUser, task, between  # Imports the HttpUser base class and functions for defining load tests
import requests  # Imports the library for handling HTTP requests

class PerformanceTests(HttpUser):
    """
    Performance testing class using Locust.

    - Simulates users sending requests to the `/start-task` endpoint.
    - Defines a random wait interval between requests to simulate realistic user behavior.
    """

    # Defines a random wait time between 5 and 10 seconds between requests
    wait_time = between(5, 10)

    @task(1)
    def trigger_task(self):
        """
        Sends a POST request to the `/start-task` endpoint to start an asynchronous task.

        - Sets appropriate JSON headers.
        - Adds a 30-second timeout to prevent long blocking requests.
        - Implements exception handling for request failures.
        """
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = self.client.post("/start-task", headers=headers, timeout=30)
            response.raise_for_status()  # Raises an error if the response status code is not 2xx
        except requests.exceptions.Timeout:
            print("The request exceeded the 30-second timeout")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")