# College system web application

### requirements to run the project:
        - python 3.0+
        - mysql

### steps to run the project in your system:
        1. open terminal
        2. git clone https://github.com/rajpipaliya048/college_system.git
        3. cd college_system
        4. create virtual environment
        5. pip install -r requirements.txt 
        6. cd college
        7. python3 manage.py runserver

### for celery tasks:
        1. open new terminal
        2. start redis server
        3. stat celery worker using this command
            - python3 -m celery -A college worker -l info
