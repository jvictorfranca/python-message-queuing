from celery import Celery
import os
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initializes the Celery instance with the name "tasks"
# The broker is the queue system (e.g., Redis or RabbitMQ) that manages tasks
# The backend stores task results (e.g., a database or Redis)
celery = Celery(
    "tasks",
    broker=os.environ[
        "CELERY_BROKER_URL"
    ],  # Retrieves the broker URL from environment variables
    backend=os.environ["CELERY_BACKEND_URL"],  # Retrieves the result backend URL
)

# Allows Celery to automatically discover tasks registered in the "app.celery.tasks" module
celery.autodiscover_tasks(["app.celery.tasks"])