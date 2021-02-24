## Runs on Python 3.8

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

## Need to set-up virtualenv

pip install virtualenv

## To Run the Application:

source venv/bin/activate
export READ_DOT_ENV_FILE=True
python manage.py runserver