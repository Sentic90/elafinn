#!/bin/bash

# Run Django migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Run the Django development server
echo "Starting the server..."
python manage.py runserver
