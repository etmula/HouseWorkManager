FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt update && \
    pip install pipenv

WORKDIR /code
COPY Pipfile Pipfile.lock ./
RUN pipenv sync

COPY houseworkmanager/ houseworkmanager/
COPY docker/ docker/

CMD pipenv run python houseworkmanager/manage.py collectstatic  && \
    pipenv run python houseworkmanager/manage.py migrate && \
    pipenv run uwsgi --chdir=/code/houseworkmanager --module houseworkmanager.wsgi --env DJANGO_SETTINGS_MODULE=houseworkmanager.settings --socket :8001