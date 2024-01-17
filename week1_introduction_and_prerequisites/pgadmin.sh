#!/bin/bash

# pgadmin4 setup (https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html)
# once the container and server are running, go to http://localhost:8080
# login with the credentials below

# container running in detached mode

docker run -d -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --name pgadmin \
    dpage/pgadmin4  