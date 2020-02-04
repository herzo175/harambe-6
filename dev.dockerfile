FROM node:13.2-buster-slim

FROM python:3.6-slim-buster

WORKDIR /workspace

RUN apt-get update
RUN apt-get install docker.io -y
RUN apt-get install build-essential -y

RUN pip install --upgrade pip setuptools

ADD requirements requirements
RUN pip install -r requirements/ml_requirements.txt
RUN pip install -r requirements/requirements.txt
