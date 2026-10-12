FROM postgres:13

# Copies the initialization script into the container
COPY init.sql /docker-entrypoint-initdb.d/

# Exposes the default PostgreSQL port
EXPOSE 5432