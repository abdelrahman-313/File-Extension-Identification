# Step 1: Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Step 2: Install Python 3.10, pip, and other necessary dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    python3.10-venv \
    build-essential \
    curl \
    libmagic1 \ 
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set working directory
WORKDIR /app

# Step 4: Copy requirements.txt into the container
COPY requirements.txt /app/

# Step 5: Create a virtual environment in the container
RUN python3.10 -m venv /app/venv

# Step 6: Set the PATH environment variable to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Step 7: Upgrade pip and install dependencies inside the virtual environment
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Step 8: Copy the rest of your application code into the container
COPY . /app/

# Step 9: Run collectstatic using the virtual environment's Python
RUN python manage.py collectstatic --noinput

# Step 10: Expose the port your app will run on
EXPOSE 8000

# Step 11: Set the command to run your application with Uvicorn (or your preferred ASGI server)
CMD ["uvicorn", "websocket_project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]


