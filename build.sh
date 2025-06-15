#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python univote/manage.py collectstatic --no-input

echo "Running migrations..."
python univote/manage.py migrate

echo "Creating superuser if it doesn't exist..."
python univote/manage.py shell -c "
from authentication.models import User
if not User.objects.filter(email='admin@unphu.edu.do').exists():
    User.objects.create_superuser(
        email='admin@unphu.edu.do',
        password='admin1234',
        first_name='Administrador',
        last_name='Sistema',
        role='ADMIN'
    )
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
"

echo "Build completed successfully!"