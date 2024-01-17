<p><a target="_blank" href="https://app.eraser.io/workspace/ZSIAOd9qx7MOGPlmxEgK" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

# Introduction & Pre-requisites


## Containerisation and Docker
Containers offer several benefits for software development, streamlining the development process and offering a more efficient and consistent environment for both development and deployment. Here are some of the key advantages:

1. **Consistency Across Environments**: Containers encapsulate an application and its environment. This means that they run the same regardless of where they are deployed, be it a developer's local machine, a test environment, or production. This consistency reduces the "it works on my machine" syndrome.
2. **Dependency Management**: Containers can include the specific versions of software dependencies that applications need to run. This prevents conflicts between different projects that may require different versions of the same dependency.
3. **Microservices Architecture**: Containers are well-suited for microservices architectures, where applications are broken down into smaller, independent services. This can improve the scalability and isolation of services.
4. **Efficient Use of Resources**: Containers share the host system's kernel, so they do not require an entire operating system to run. This makes them more lightweight and faster to start than virtual machines, which require a full OS for each instance.
5. **Isolation**: Containers isolate applications from each other on a shared system. This isolation helps in security by ensuring that applications do not interfere with each other and reduces the risk of cross-application attacks.
6. **Rapid Deployment and Scaling**: Containers can be started, stopped, or replicated in seconds. This rapid deployment capability is essential for high-availability applications and is beneficial during peak times when you need to scale out quickly.
7. **Development Productivity**: Developers can focus on writing code without worrying about the underlying system and deployment specifics. They can easily pull a pre-configured container image and start working on it.
8. **Continuous Integration and Continuous Deployment (CI/CD)**: Containers integrate well with CI/CD pipelines, allowing automated testing and deployment. This helps in ensuring that new code changes keep the existing system.
9. **Version Control for the Environment**: Container definitions can be version-controlled along with application code, which means that changes to the environment can be tracked and audited.
10. **Local Development Environments**: Developers can easily replicate production environments on their local machines without needing to manually configure their development environment.
11. **Cost-Effectiveness**: Since containers make more efficient use of hardware than traditional or virtual machine-based solutions, they can reduce infrastructure costs.
12. **Cloud-Native Compatibility**: Containers are often designed to be cloud-native, meaning they are optimized for cloud environments, which can provide additional scalability, resilience, and distribution benefits.
In summary, containers simplify the development process by creating a portable and consistent environment for applications to run in, which helps in reducing the time and effort required for dealing with environmental inconsistencies and dependency management. This allows teams to focus more.

---

Docker is a platform for developing, shipping and running applications using containerisation. It allows you to package your application and its dependencies into a standardised Docker container unit. Docker containers are lightweight, portable, and isolated, making running applications consistently across different environments easy.

Kubernetes (k8s) is an open-source container orchestration platform that automates containerised applications' deployment, scaling, and management. It provides features for deploying, maintaining, and scaling application containers across clusters of hosts, making it easier to manage large, complex applications.

Orchestration tools like Kubernetes help manage and automate application container deployment, scaling, and operation. They provide features for load balancing, service discovery, and rolling updates. Popular orchestration tools include Docker Swarm, Apache Mesos, and Amazon ECS.

Some commonly used Docker commands include:

- `docker run` : To run a container from an image.
- `docker build` : To build an image from a Dockerfile.
- `docker ps` : To list running containers.
- `docker exec` : To run a command inside a running container.
- `docker stop` : To stop a running container.


Certainly! Detaching and attaching to Docker containers are common tasks when managing multiple containers. Here's a guide on how to do it:

### Detaching from a Docker Container:
When you run a Docker container and want it to keep running in the background, you can start it in detached mode or detach from it after starting it in interactive mode.

**Starting a Container in Detached Mode:**

1. Use the `-d`  flag with `docker run`  to start a new container in detached mode: Replace `<image-name>`  with the name of your Docker image.docker run -d <image-name>
**Detaching from an Interactive Container:**

1. If you start a container in interactive mode using `-it`  flags:docker run -it <image-name>
2. You can detach from it and leave it running using the escape sequence `Ctrl+p`  followed by `Ctrl+q` .
### Attaching to a Running Docker Container:
To attach to a running container that is in detached mode, you can use the `docker attach` command:

1. First, find the container ID or name using:docker ps
2. Then attach to the container using: Replace `<container-id-or-name>`  with the actual ID or name of your container.docker attach <container-id-or-name>
### Running Multiple Containers in the Background:
You can run multiple containers in detached mode by issuing the `docker run -d <image-name>` command for each container you want to run.

Here's an example command to run three containers from the same image in detached mode:

```sh
docker run -d <image-name>
docker run -d <image-name>
docker run -d <image-name>
```
### Managing Containers:
- To list all running containers, use:docker ps
- To list all containers, including stopped ones, use:docker ps -a
### Stopping Containers:
When you want to stop a running container, use:

```sh
docker stop <container-id-or-name>
```
### Restarting Containers:
To restart a stopped container, use:

```sh
docker start <container-id-or-name>
```
Remember that you can always use Docker Compose to manage multiple containers as part of a single service stack, which can be more convenient for complex applications.

### Run Docker at the backend and attach it to the local host port
1. **Pull the Docker Image** (if you haven't already):
    1. Replace `<image-name>`  with the name of the Docker image you want to use. `docker pull <image-name>` 
2. **Run the Container in Detached Mode** with Port Mapping:
    1. `docker run -d -p <local-port>:<container-port> <image-name>` 
    2. `-d`  flag runs the container in detached mode.
    3. `-p`  flag maps a port on your local machine to a port in the container.
    4. `<local-port>`  is the port on your local machine you want to use.
    5. `<container-port>`  is the port inside the container that your application listens on.
    6. `<image-name>`  is the name of your Docker image.
For example, if you have an application inside your container that listens on port 5000, and you want to access it via port 8080 on your local machine, you would run:

```sh
docker run -d -p 8080:5000 <image-name>
```
After running this command, your Docker container will start in the background. You can access your application by going to `http://localhost:8080` in your web browser or using any other tool that makes HTTP requests.

Remember to replace `<image-name>` with the actual image you want to use and adjust the port numbers according to your specific needs.

## Running Database
I strongly recommend setting up a virtual Python environment.

- `pip3 install virtualenv` 
- `python3 -m venv my_venv` 
- `source my_venv/bin/activate` 
- `pip3 install -r requirements.txt` 


For dataset download, you can follow the Github link or use the download script; this download script will download the parquet file. 

- `python nyc_yellow_taxi_data_downloader.py --year=2021 --start_month=1 --end_month=1` 
- `python nyc_yellow_taxi_data_downloader.py -y=2021 -s=1 -e=1` 


Then you can run python scripts:

- Run database docker container: `./postgres.sh` 
- Run pgcli without enter password: .`/pgcli.sh` 
- Loading nyc_taxi dataset to database: `python3 dataset_to_postgres.py -f [file_path] -t [table_name]` 
    - For parquet: `python3 dataset_to_postgres.py -f='yellow_tripdata_2021-01.csv' -t='yellow_taxi_data'` 
    - For csv: `python3 dataset_to_postgres_parquet.py -f='yellow_tripdata_2021-01.csv' -t='yellow_taxi_data'`  
After loading the dataset, you can remove the csv files.








<!--- Eraser file: https://app.eraser.io/workspace/ZSIAOd9qx7MOGPlmxEgK --->