# Django Based Web-Application

Django is very popular framework of python to build web applications.

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
>Now, Yor're ready to run the project

```bash
  python manage.py runserver
```
> For frontend hit "127.0.0.1:8000" in browser's url

### For Celery Tasks

>Start redis server

```bash
redis-server
```
>Start Celery Worker

```bash
python -m celery -A college worker -l info
```

>Also, start the mailcatcher service to get emails, To start mailcatcher simpally run following command in Terminal

```bash
mailcatcher
```
> To check emails hit "http://127.0.0.1:1080/" url in browser
