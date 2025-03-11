#!/usr/bin/env bash
set -o errexit  # Exit immediately if a command exits with a non-zero status

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Create a superuser if it doesn't exist


# Set the superuser password
