# syntax=docker/dockerfile:1
FROM python:3.10.2-bullseye as builder

LABEL version="1.0"
LABEL author="Pawel.Kryczka"
LABEL email="kryczka.pawel.42@gmail.com"
LABEL description="A Python3.10.2 Dockerfile for running Dramatiq workers"

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
ENV REQUIREMENTS=tasks_requirements.txt
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
WORKDIR $APP_DIR

COPY src $APP_DIR/
# FIXME?

# install dependencies
COPY --from=builder /home/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

RUN groupadd -r app && \
    useradd app_user -r -g app

# chown all the files to the app user
RUN chown -R app_user:app $APP_DIR

USER app_user

# FIXME RUN
RUN dramatiq $APP_DIR/src.tasks
