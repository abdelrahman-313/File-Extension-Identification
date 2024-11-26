# Django WebSocket File Extension Identification Service

This project is a Django-based WebSocket service that allows clients to send a file's metadata to the server and receive the file's extension in response. The application is containerized using Docker for easy development, deployment, and scalability.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)

## Project Overview

This Django WebSocket service allows clients to send metadata about a file (including the file's name) over a WebSocket connection. The server identifies the file extension and sends the result back to the client. This is particularly useful for handling file uploads in real-time applications, like file managers or web apps that need to process files.

## Prerequisites

Before you begin, ensure that you have the following tools installed on your machine:

- **Docker**: Docker is used to containerize the application and its dependencies. You can install Docker from [here](https://www.docker.com/get-started).
- **Docker Compose**: Docker Compose is optional but recommended if you need to manage multiple containers. [Installation guide](https://docs.docker.com/compose/install/).

## Installation

Follow these steps to set up the application using Docker.

### 1. **Clone the Repository**

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/django-websocket-file-extension.git
cd django-websocket-file-extension
```

### 2. **Build the Docker Image**

The Dockerfile in this project is responsible for setting up the environment. It installs Python, dependencies, and sets up the application. To build the image:

```bash
docker build -t websocket-file-extension .
```

### 3. **Run the Docker Container**

Once the image is built, you can run the container with the following command:

```bash
docker run -d -p 8000:8000 --name websocket-app --network host websocket-file-extension
```
This will run the Django application inside a Docker container and expose it on port 8000 of your host machine.


### 4. **Access the Application**

- **WebSocket**: ```ws://localhost:8000/ws/file/```
- **Django Admin**: ```http://localhost:8000/admin/```  (Login using the superuser credentials created during migration).
```bash
docker run -d -p 8000:8000 --name websocket-app --network host websocket-file-extension
```
This will run the Django application inside a Docker container and expose it on port 8000 of your host machine.


