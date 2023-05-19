FROM python:3.11.3-buster

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

# System deps:
ENV TZ="Asia/Dhaka"
RUN apt-get install -yq tzdata
RUN ln -fs /usr/share/zoneinfo/Asia/Dhaka /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code
