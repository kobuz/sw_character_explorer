FROM python:3.8.0

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=0

RUN apt-get update
RUN apt-get install -y postgresql-client

WORKDIR /app

RUN pip install poetry
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install

COPY . /app
