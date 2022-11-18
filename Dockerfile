FROM python:3.10.7-slim-buster@sha256:97c123c899c8c9ca46248f4002ec4173322e0a1086b386efefac163c64967ba2

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

