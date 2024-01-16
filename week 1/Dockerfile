# docker file is case sensitive
# first line is always FROM, it is the base image
FROM python:3.9 

# RUN, it runs the command in the terminal
RUN pip install pandas

# WORKDIR, it is the working directory
WORKDIR /app

# COPY, it copies the files from the local machine to the docker image
COPY pipeline.py pipeline.py

# ENTRYPOINT is the command that is run when the docker image is run
ENTRYPOINT ["python3", "pipeline.py"]