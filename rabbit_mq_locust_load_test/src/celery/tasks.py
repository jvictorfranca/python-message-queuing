from app.celery.worker import celery, logger  # Imports the configured Celery instance and logger
import time
import random
import datetime

@celery.task(name="task_with_high_latency")
def task_with_high_latency(enqueued_time=None):
    """
    Simulates a long-running Celery task.

    - Calculates how long the task waited in the queue before execution started.
    - Waits for a random duration between 17 and 20 seconds to simulate a slow operation.
    - Logs the total execution time and the time spent waiting in the queue.
    """
    task_id = task_with_high_latency.request.id  # Retrieves the Celery task ID

    # If the enqueue timestamp was not provided, uses the current time as a reference
    if enqueued_time:
        enqueued_time = datetime.datetime.fromisoformat(enqueued_time)
    else:
        enqueued_time = datetime.datetime.utcnow()

    start_time = datetime.datetime.utcnow()  # Records when the task starts executing

    # Calculates how long the task waited in the queue before execution
    queue_wait_time = (start_time - enqueued_time).total_seconds()

    # Sets a random delay to simulate a long-running operation
    delay = random.uniform(17, 20)

    try:
        time.sleep(delay)  # Simulates processing time
        logger.info(
            f"Task {task_id} completed after {delay:.2f} seconds, having spent {queue_wait_time:.2f} seconds in the queue."
        )
        return f"Task {task_id} completed after {delay:.2f} seconds, having spent {queue_wait_time:.2f} seconds in the queue."
    except Exception as e:
        logger.error(f"Error in task {task_id}: {e}")
        raise e  # Re-raises the exception so Celery can handle it correctly