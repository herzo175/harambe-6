FROM python:3.6.0

ARG CONTAINER_PORT=8080
ENV PORT=${CONTAINER_PORT}

WORKDIR /app

RUN pip install --upgrade pip setuptools

ADD ml_requirements.txt .
RUN pip install -r ml_requirements.txt

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

EXPOSE ${CONTAINER_PORT}

# ENTRYPOINT $(echo python service.py $PORT)
ENTRYPOINT $(echo python server.py $PORT)
