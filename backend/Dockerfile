  
FROM python:3.11.4

ARG BACKEND_ENV

ENV BACKEND_ENV=BACKEND_ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client && \
    pip install "poetry==1.5.1"

COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN POETRY_VIRTUALENVS_CREATE=false poetry install \
  && poetry install $(test "BACKEND_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /app