# docker file is case sensitive
# first line is always FROM, it is the base image
FROM python:3.9 

# RUN, it runs the command in the terminal
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install pandas sqlalchemy psycopg2

# WORKDIR, it is the working directory
WORKDIR /app


COPY dataset_to_postgres.py dataset_to_postgres.py
COPY download_transfer.sh download_transfer.sh
RUN chmod +x download_transfer.sh
RUN ./taxi_ingest 

# ENTRYPOINT is the command that is run when the docker image is run
ENTRYPOINT ["python3", "dataset_to_postgres.py"]