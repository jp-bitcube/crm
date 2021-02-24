## Runs on Python 3.8
## Install Dependencies
$ pip install -r requirement.txt

## Set-up .env file in crm folder within the project
DEBUG=True
SECRET_KEY=
DB_NAME=leadcrm
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
SENDGRID_API_KEY=

generate secret key https://djecrety.ir/

## Set-up DB PostgreSQL

$ createDB leadcrm
$ python manage.py makemigrations
$ python manage.py migrate

## Create a Super User Account

$ python manage.py createsuperuser

## Need to set-up virtualenv

$ pip install virtualenv

## To Run the Application:

$ source venv/bin/activate
$ export READ_DOT_ENV_FILE=True
$ python manage.py runserver

## Set-up Email Sendgrid

`If you are not using a SMPT from Sendgrid locally change the crm/settings.py variable`

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

`else when the SMPT is set-up you can leave this as is`

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'   