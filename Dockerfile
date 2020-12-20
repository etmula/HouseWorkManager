FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt update && \
    pip install pipenv

WORKDIR /code
COPY ./houseworkmanager /code
COPY Pipfile /code
COPY Pipfile.lock /code
RUN pipenv install --system

CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py custom_createsuperuser --username $SUPERUSER_USERNAME --email $SUPERUSER_EMAIL --password $SUPERUSER_PASSWORD && \
    uwsgi --chdir=/code --module houseworkmanager.wsgi --env DJANGO_SETTINGS_MODULE=houseworkmanager.settings --socket :8001