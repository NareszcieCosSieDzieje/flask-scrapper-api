# syntax=docker/dockerfile:1
FROM python:3.10.2-bullseye as builder

LABEL version="1.0"
LABEL author="Pawel.Kryczka"
LABEL email="kryczka.pawel.42@gmail.com"
LABEL description="A Python3.10.2 Dockerfile for running a Flask server"

# BUILD
RUN apt update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_DIR=/home/src/app
RUN mkdir -p $APP_DIR
ENV WHEEL_DIR=$APP_DIR/wheels
RUN mkdir -p $WHEEL_DIR

WORKDIR $APP_DIR

# install dependencies
ENV REQUIREMENTS=requirements.txt
COPY ./$REQUIREMENTS .
# build wheels for later re-use
RUN pip wheel --no-cache-dir --no-deps --wheel-dir $WHEEL_DIR -r $REQUIREMENTS

# PROD

FROM python:3.10.2-bullseye

RUN apt update
RUN apt install sqlite3 nano

# Setup venv
ENV VIRTUAL_ENV=/opt/venv
ENV PYTHON=python3.10
RUN $PYTHON -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV APP_DIR=/home/app/
RUN mkdir $APP_DIR
# FIXME STATICS
# RUN mkdir -p $APP_DIR/static # FIXME: THE named_volume ownership trick doesnt work (create dir inside Dockerfile and then mount named volume as root and access as non root)
RUN mkdir -p $APP_DIR/database # FIXME CO Z POZIOMEM CZY NIE NIZEJ NIE POWINNO BYC
WORKDIR $APP_DIR

COPY src/ $APP_DIR

# install dependencies
COPY --from=builder /home/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# FIXME: COPY STATIC FILES?
# RUN cp -r /opt/venv/lib/python3.10/site-packages/rest_framework/static/rest_framework $APP_DIR/static/
# RUN cp -r /opt/venv/lib/python3.10/site-packages/django/contrib/gis/static $APP_DIR/static/
# RUN cp -r /opt/venv/lib/python3.10/site-packages/django/contrib/admin/static $APP_DIR/static/

# RUN python ./manage.py makemigrations && \  # FIXME REMOVE!
#     python ./manage.py migrate

RUN groupadd -r app && \
    useradd app_user -r -g app

# chown all the files to the app user
RUN chown -R app_user:app $APP_DIR

# change to the app user
# USER app_user # FIXME: doesnt work because of the named_volume attached in the compose file
CMD python -m gunicorn server.wsgi:app --bind 0.0.0.0:8000
# FIXME APP CZY SERVER?
