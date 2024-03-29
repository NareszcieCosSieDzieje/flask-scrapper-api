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

# PRODUCTION
FROM python:3.10.2-bullseye

RUN apt update
RUN apt install sqlite3 nano redis -y

# Setup venv
ENV VIRTUAL_ENV=/opt/venv
ENV PYTHON=python3.10
RUN $PYTHON -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV APP_DIR=/home/app/
RUN mkdir $APP_DIR
RUN mkdir -p $APP_DIR/database

COPY src $APP_DIR/src
ENV SRC_DIR=/home/app/src
WORKDIR $SRC_DIR

# install dependencies
COPY --from=builder /home/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

RUN groupadd -r app && \
    useradd app_user -r -g app

# Chown all the files to the app user
RUN chown -R app_user:app $APP_DIR
RUN chown -R app_user:app $VIRTUAL_ENV

# Set user
USER app_user
CMD python -m dramatiq tasks
