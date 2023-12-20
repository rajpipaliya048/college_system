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
