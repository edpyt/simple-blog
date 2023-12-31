FROM python:3.11.7-slim-bullseye

WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --with test

# add app
COPY ./src /app/src

# add tests
COPY ./tests /app/tests