# Hujan.io

## Prerequisite
  - Python 3.6.x already installed on system or using virtualenv
  - virtualenv

## Development Setup
activate env
```
source env/bin/activate
```

```
$ pip install -r requirements.txt
```

Create your own settings and modify as your preference

```
$ cp hujan_ui/local_settings.py.sample hujan_ui/local_settings.py
```

Migrate database

```
$ python manage.py migrate
```

Collect Static

```
$ python manage.py collectstatic
```

Create superuser

```
$ python manage.py createsuperuser
Username (leave blank to use 'btech'):
Email address: contact@btech,id
Password:
Password (again):
Superuser created successfully.
```

Runing the service

```
python manage.py runserver
```

Then open your browser http://localhost:8000 and voila your web apps is already running !

Run app with specific port

```
$ python manage.py runserver 5000
```
Then open your browser http://localhost:5000.

## Server Installation And Configuration

### Pre-Installation

You need to install the following apps:

- python3.6
- Nginx
- virtualenv

### Application Setup


Clone the latest source code from the repository, and I assume you put it to `/var/www/html/`

```
$ cd /var/www/html/
$ git clone {repository}
$ cd hujan_ui
```

Then create virtualenv with python3

```
$ virtualenv --python=python3.6
$ source/env/bin/activate
$ pip install -r requirements.txt
$ pip install gunicorn
```

Then create a configuration file, just copy from sample file and modify as your preference

```
$ cp hujan_ui/local_settings.py.sample hujan_ui/local_settings.py
```

Then run the database migration

```
$ python manage.py migrate
```

Then create first superuser

```
$ python manage.py createsuperuser
Username (leave blank to use 'btech'):
Email address:
Password:
Password (again):
Superuser created successfully.
```

Then generate static files

```
$ python manage.py collectstatic
```

Create logs directory

```
$ mkdir logs
```
