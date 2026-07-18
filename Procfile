web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn cannelle_hill.wsgi --bind 0.0.0.0:$PORT
