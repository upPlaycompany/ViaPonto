FROM python:3.9
ENV PYTHONUNBUFFERED  1
RUN mkdir /code
WORKDIR /code
# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip install -U pip setuptools
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
ADD . /code/
# Django service
EXPOSE 80