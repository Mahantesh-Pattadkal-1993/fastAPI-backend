# fastAPI-backend

A FastAPI application with logging and Dockerized
==================================================

This is a template project that showcases how to create a FastAPI application with logging and containerize it using Docker.

## Features

* A fully functional FastAPI application with a basic endpoint
* Integrated logging framework for error handling and debugging
* A Dockerfile for containerization

## Quick Start

To get started, clone this repository and navigate to the project directory.

### Prerequisites

* Docker installed on your system
* Python 3.8 or higher
* pip installed

### Running the Application

1. Build the Docker image by running `docker build -t myapp .` (replace `myapp` with your desired image name)
2. Run the Docker container by running `docker run -p 8000:8000 myapp` (port 8000 is used by default, change it as needed)
3. Open a web browser and navigate to `http://localhost:8000` to access the FastAPI application

### Logging

The application logs are configured using the `loguru` library and can be viewed using the `docker logs` command. For example:
```bash
docker logs -f myapp
```
### Contributors

* [Mahantesh Pattadkal] (maintainer)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact

For any issues or feedback, please create an issue on the repository or reach out to mpattadkal@gmail.com
