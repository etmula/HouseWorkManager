FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt update && \
    pip install pipenv

RUN git clone https://github.com/etmula/HouseWorkManager.git code
WORKDIR /code
RUN pipenv sync

CMD pipenv run python houseworkmanager/manage.py collectstatic --noinput && \
    pipenv run python houseworkmanager/manage.py migrate && \
    pipenv run uwsgi --chdir=/code/houseworkmanager --module houseworkmanager.wsgi --env DJANGO_SETTINGS_MODULE=houseworkmanager.settings --socket :8001