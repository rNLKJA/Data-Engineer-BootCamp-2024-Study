#!/bin/bash

# create a Docker network
docker network create pg-network 2>/dev/null || true

# check if a container named 'pg-database' already exists and run it
if [ $(docker ps -aq -f name=^/pg-database$) ]; then
    echo "Running existing 'pg-database' container..."
    docker start pg-database
else
    # start the PostgreSQL database container
    echo "Running container pg-database"
    docker run -d -it \
        -e POSTGRES_USER="root" \
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="ny_taxi" \
        -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
        -p 5432:5432 \
        --network pg-network \
        --name pg-database \
        postgres:13
fi

# check if a container named 'pgadmin-2' already exists and run it
if [ $(docker ps -aq -f name=^/pgadmin-2$) ]; then
    echo "Running existing 'pgadmin-2' container..."
    docker start pgadmin-2
else
    echo "Running container pgadmin-2"
    # start the pgAdmin container
    docker run -d -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        --network pg-network \
        --name pgadmin-2 \
        dpage/pgadmin4
fi

echo "Containers initialised"
