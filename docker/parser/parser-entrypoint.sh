#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

./manage.py makemigrations parser
./manage.py dumpdata > db.json

until ./manage.py makemigrations && ./manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

while true
do
    ./manage.py parsing && break
done