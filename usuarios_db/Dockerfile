# Use the official PostgreSQL image as a base image
FROM postgres:13

# Copy the initialization script to the container
COPY init.sql /docker-entrypoint-initdb.d/

# Set necessary environment variables (optional here, as you can set them in docker-compose.yml)
ENV POSTGRES_USER=usuarios_ms
ENV POSTGRES_PASSWORD=rasi
ENV POSTGRES_DB=usuarios_db

# The default port for PostgreSQL is 5432
EXPOSE 5432

