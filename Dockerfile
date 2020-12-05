FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt update && \
    pip install pipenv

WORKDIR /code
COPY . /code
RUN pipenv sync

CMD pipenv run python houseworkmanager/manage.py collectstatic --noinput && \
    pipenv run python houseworkmanager/manage.py migrate && \
    pipenv run python houseworkmanager/manage.py custom_createsuperuser --username $SUPERUSER_USERNAME --email $SUPERUSER_EMAIL --password $SUPERUSER_PASSWORD && \
    pipenv run uwsgi --chdir=/code/houseworkmanager --module houseworkmanager.wsgi --env DJANGO_SETTINGS_MODULE=houseworkmanager.settings --socket :8001