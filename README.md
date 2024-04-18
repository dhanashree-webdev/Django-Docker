Dockerfile
Dockerfile
Copy code
## Use an official Python runtime as a parent image
```bash
FROM python:3.9-slim
```

## Set environment variables
```bash
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
```

## Set the working directory in the container
```
WORKDIR /app
```

## Copy the dependencies file to the working directory
```
COPY requirements.txt /app/
```

## Install any needed packages specified in requirements.txt
```
RUN pip install --no-cache-dir -r requirements.txt
```
## Copy the rest of the application code to the working directory
```
COPY . /app/
```

## Run entrypoint.sh
```
CMD ["sh", "entrypoint.sh"]
```

Docker-compose file (docker-compose.yml)

```yaml
version: '3.8'

services:
  web:
    build: ./dcelery
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./dcelery/:/usr/src/app/
    ports:
      - 1337:8000
    environment:
      - DEBUG=1
      - SECRET_KEY=dbaa1_i7%*3r9-=z-+_mz4r-!qeed@(-a_r(g@k8jo8y3r27%m
      - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    depends_on:
      - redis
  redis:
    image: redis:alpine
  celery:
    build: ./dcelery
    command: celery -A dcelery worker -l info
    volumes:
      - ./dcelery/:/usr/src/app/
    environment:
      - DEBUG=1
      - SECRET_KEY=dbaa1_i7%*3r9-=z-+_mz4r-!qeed@(-a_r(g@k8jo8y3r27%m
      - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    depends_on:
      - redis
  celery-beat:
    build: ./dcelery
    command: celery -A dcelery beat -l info
    volumes:
      - ./dcelery/:/usr/src/app/
    environment:
      - DEBUG=1
      - SECRET_KEY=dbaa1_i7%*3r9-=z-+_mz4r-!qeed@(-a_r(g@k8jo8y3r27%m
      - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    depends_on:
      - redis    depends_on:
      - db
      - redis
    environment:
      - DJANGO_SETTINGS_MODULE=your_project.settings
      - DATABASE_URL=postgres://user:password@db:5432/db_name
      - CELERY_BROKER_URL=redis://redis:6379/0
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=db_name
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  redis:
    image: redis:latest
    command: ["redis-server", "--appendonly", "yes"]
```


entrypoint.sh
```bash
#!/bin/bash
```

## Apply database migrations
```
python manage.py migrate
```

## Start the Celery worker
```
celery -A your_project worker -l info --concurrency=4
```

## Start the Celery beat scheduler
```
celery -A your_project beat -l info
```

settings.py
```python
# Celery configuration
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
```
celery.py
```python
Copy code
from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
```

tasks.py
```python
from celery import shared_task

@shared_task
def your_task_name():
    # Task logic goes here
    pass
```

This repository contains the necessary files to Dockerize a Django project with Celery for performing scheduled tasks.

## Docker Components
- `Dockerfile`: Defines the Docker image for the Django application.
- `docker-compose.yml`: Orchestrates the Docker containers for Django, PostgreSQL, and Redis.
- `entrypoint.sh`: Defines the entrypoint script for running database migrations, Celery worker, and Celery beat scheduler.
- `settings.py`: Contains the Django settings including Celery configuration.
- `celery.py`: Configures Celery for the Django project.
- `tasks.py`: Defines Celery tasks to be executed.

## Getting Started
1. Clone this repository.
2. Customize the `settings.py` and `docker-compose.yml` files with your project settings and environment variables.
3. Run `docker-compose up --build` to build and start the Docker containers.
4. Access your Django application at `http://localhost:8000`.
