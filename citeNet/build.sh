#!/usr/bin/env bash
set -o errexit  # Exit immediately if a command exits with a non-zero status

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Create a superuser if it doesn't exist
python manage.py createsuperuser --noinput --username raviteja --email ravi@gmail.com

# Set the superuser password
python manage.py set_superuser_password
