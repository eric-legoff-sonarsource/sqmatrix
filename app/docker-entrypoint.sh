#!/bin/sh


echo "In entry point"
ls -la /opt/app


echo "Migrate the Database at startup of project"

# Wait for few minute and run db migraiton
while ! python manage.py makemigrations  2>&1; do
   echo "Migration is in progress status"
   sleep 3
done

# Wait for few minute and run db migraiton
while ! python manage.py migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 3
done

echo "Django docker is fully configured successfully."

python manage.py runserver 0.0.0.0:8000