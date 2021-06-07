# pull official base image
FROM python:3.8

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile

RUN useradd appuser && chown -R appuser /usr/src
USER appuser

# copy project python files
COPY . .