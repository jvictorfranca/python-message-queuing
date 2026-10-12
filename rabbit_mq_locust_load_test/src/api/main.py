from fastapi import FastAPI
from celery.result import AsyncResult
from app.celery.worker import celery  # Imports the configured Celery instance
from app.celery.tasks import task_with_high_latency  # Imports the long-running task
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Defines an output model to represent the task status returned by the API
class CeleryTaskOutputDto(BaseModel):
    state: str  # Current task state (pending, running, completed, etc.)
    output: Optional[str] = None  # Task result, if available

# Initializes the FastAPI application
app = FastAPI()

@app.post("/start-task")
def start_task():
    """Starts an asynchronous Celery task and returns its ID."""
    task = task_with_high_latency.delay(enqueued_time=datetime.utcnow().isoformat())
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    """Retrieves the status and result (if available) of a Celery task by its ID."""
    task_result = AsyncResult(task_id, app=celery)
    return CeleryTaskOutputDto(state=task_result.state, output=task_result.info)