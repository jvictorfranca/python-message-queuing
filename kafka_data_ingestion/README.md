# Data Ingestion

This directory demonstrates the use of queues in data ingestion and processing pipelines.

## Requirements

Before getting started, make sure the following are installed in your environment:

- **Docker**
- **Docker extension for VS Code**

## How to Run the Examples

1. Navigate to the module directory:

   ```sh
   cd data_ingestion

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

- Kibana: [http://localhost:5601](<http://localhost:5601>)
- Kafka Control Center: [http://localhost:9021](<http://localhost:9021>)

If you cannot access an endpoint using `localhost`, try `0.0.0.0` or `127.0.0.1` instead.

### Accessing the PostgreSQL Database

To access the database inside the container, run:

sh
```
psql usuarios
```

```
