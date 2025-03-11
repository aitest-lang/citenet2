#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create a superuser if it doesn't exist
python manage.py createsuperuser --noinput --username ravi --email ravi@gmail.com

# Set the superuser password
python manage.py set_superuser_password
