FROM python:3.11.3-alpine3.18

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1 \
  POETRY_VIRTUALENVS_CREATE=false

RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry install

# Creating folders, and files for a project:
COPY . /app/
