web: python univote/manage.py migrate && python univote/manage.py collectstatic --noinput && gunicorn --chdir univote univote.wsgi:application --bind 0.0.0.0:$PORT
