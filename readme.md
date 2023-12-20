# Django Based Web-Application

Django is very popular framework of python to build web applications.You can learn it form official [Documentation](https://docs.djangoproject.com/en/5.0/)

This project is based on selling the courses.

## Steps to Run the Project

>Open Terminal

>Make clone of project

```bash
  git clone https://github.com/rajpipaliya048/college_system.git
```

>Create a virtual environment in project directory

```bash
  python -m venv <name_of_virtual_environment>
```

>Install all the required packages in virtual environment

```bash
  pip install -r requirements.txt
```
> Migrate the models

```bash
  python manage.py migrate
```
> if you want to load data of database run the following command

```bash
  python manage.py loaddata data.sql
```

>Now, Yor're ready to run the project

```bash
  python manage.py runserver
```
> For frontend hit "127.0.0.1:8000" in browser's url

### For Celery Tasks

Celery is an asynchronous task queue/job system. It is focused on real-time operation, but supports scheduling as well. The execution units, called tasks, are executed concurrently on a single or more worker servers.([Documentation](https://docs.celeryq.dev/projects/django-celery/en/2.4/introduction.html#:~:text=django%2Dcelery%20%2D%20Celery%20Integration%20for%20Django,-Version%3A&text=Celery%20is%20a%20task%20queue,single%20or%20more%20worker%20servers.))

>Start redis server

```bash
  redis-server
```
>Start Celery Worker

```bash
  python -m celery -A college worker -l info
```

>If you want to test bulk mails should have mailctcher installed in your system. To start mailcatcher simpally run following command in Terminal

```bash
  mailcatcher
```
> To check emails hit "http://127.0.0.1:1080/" url in browser

## Dockerizing The Project

Docker is an open platform for developing, shipping, and running applications.([Documentation](https://docs.docker.com/guides/get-started/))

### To Dockerize Your Project First You Have to Installed Docker in Your System

>To check if docker is installed or not by running followning command.

```bash
docker -v
```

If docker is not installed then You can Install Docker On your system from their [official website](https://docs.docker.com/get-docker/)

## First We Need to Build Project’s Container Image

Firstly, We need a Dockerfile. A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image.

1. .Create a file named 'Dockerfile' in the same folder as the file manage.py with the following content.

```bash
FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/college
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
```
#### Note: Dockerfile does not have any extensions

2. Our project has multiple components so we need to create multiple containers.

>To create multiple container you should have installed docker-compose. To check if docker-compose is installed or not by running followning command.

```bash
docker-compose version
```

>If not you can install docker-compose using following commands:
- For Ubuntu and Debian, run:
```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

- For RPM-based distros, run:

```bash
sudo yum update
sudo yum install docker-compose-plugin
```
### Create Docker Compose File

1. In the same folder as manage.py create file called docker-compose.yaml.

2. In the Compose File the first line is always the version. Try to use the latest version.

```bash
version: "3.8"
```

### Define the app service

1. Redis service. we can oull image from docker too. container name will be shown as name of your container in docker

```bash
version: "3.8"
services:

# Redis
    redis:
        image: redis:5.0.14
        container_name: redis
```

2.  We can set ports too. The 'ports' configuration in Docker Compose facilitates mapping of the service's port number inside the Docker container to a port number on the host machine.

```bash
version: "3.8"
services:

# Redis
    redis:
        image: redis:5.0.14
        container_name: redis
        ports:
            - "6379:6379"
        entrypoint: redis-server --appendonly yes
```

3. let's create a container for mysql database. Also, we can set environment variables for database.

```bash
version: "3.8"
services:

# Redis
    redis:
        image: redis:5.0.14
        container_name: redis
        ports:
            - "6379:6379"
        entrypoint: redis-server --appendonly yes


# Database
    db:
        image: mysql:8.0
        container_name: college_db
        volumes:
          - ./data.sql:/docker-entrypoint-initdb.d/data.sql
        environment:
          MYSQL_DATABASE: mycollege
          MYSQL_ROOT_PASSWORD: 09888
```

4. The third service is of our maiin app's container. we can write commands in docker-compose file like Dockerfile. which are used to run our project.

```bash 
# Redis
    redis:
        image: redis:5.0.14
        container_name: redis
        ports:
            - "6379:6379"
        entrypoint: redis-server --appendonly yes


# Database
    db:
        image: mysql:8.0
        container_name: college_db
        volumes:
          - ./data.sql:/docker-entrypoint-initdb.d/data.sql
        environment:
          MYSQL_DATABASE: mycollege
          MYSQL_ROOT_PASSWORD: 09888

# Django Application
    django:
        build: .
        container_name: college
        command: python manage.py runserver 0.0.0.0:8000
        volumes:
            - .:/usr/src/college
        ports:
            - "8000:8000"
        depends_on:
            - db
```

5. Lastly, the last service is our celery container.

```bash
version: "3.8"
services:

# Redis
    redis:
        image: redis:5.0.14
        container_name: redis
        ports:
            - "6379:6379"
        entrypoint: redis-server --appendonly yes


# Database
    db:
        image: mysql:8.0
        container_name: college_db
        volumes:
          - ./data.sql:/docker-entrypoint-initdb.d/data.sql
        environment:
          MYSQL_DATABASE: mycollege
          MYSQL_ROOT_PASSWORD: 09888

# Django Application
    django:
        build: .
        container_name: college
        command: python manage.py runserver 0.0.0.0:8000
        volumes:
            - .:/usr/src/college
        ports:
            - "8000:8000"
        depends_on:
            - db

# Celery
    celery:
        restart: always
        build:
            context: .
        command: python3 -m celery -A college worker -l info
        volumes:
            - .:/usr/src/college
        container_name: celery
        depends_on:
            - db
            - redis
            - django
```
### Building and Starting the Docker Containers

1. First we have to build images using following command:

```bash
docker-compose build
```

2. After, building successfully we can run our project using following command:

```bash
docker-compose up
```

- To run project in background without watching logs use the following command:

```bash
docker-compose up -d
```

## Stopping the Docker container
If you want to stop running the project use the following command 
```bash
  docker-compose down
```
