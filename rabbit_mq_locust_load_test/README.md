# Distributed Jobs

This directory contains examples of queue implementations for distributing asynchronous tasks across multiple processing instances.

## Requirements

Before getting started, make sure the following are installed in your environment:

- **Docker**
- **Docker extension for VS Code**

## How to Run the Examples

1. Navigate to the module directory:

   ```sh
   cd distributed_jobs
````

2. Start the containers using Docker Compose:
   sh
   ```
   docker compose up -d
   ```
3. To stop the containers and remove associated volumes, run:
   sh
   ```
   docker compose down -v
   ```

### Available Endpoints

- Flower (Celery Monitoring): [http://localhost:5555](<http://localhost:5555>)
- RabbitMQ Management Interface: [http://localhost:15672](<http://localhost:15672>)
- Locust (Load Testing): [http://localhost:8089](<http://localhost:8089>)
- Main API: [http://localhost:8000](<http://localhost:8000>)
- API Documentation: [http://localhost:8000/docs](<http://localhost:8000/docs>)

If you cannot access an endpoint using `localhost`, try `127.0.0.1` instead.
