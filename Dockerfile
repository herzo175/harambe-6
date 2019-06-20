FROM python:3.6.0

ARG CONTAINER_PORT=8080
ENV PORT=${CONTAINER_PORT}

WORKDIR /app

RUN pip install --upgrade pip setuptools

ADD requirements requirements
RUN pip install -r requirements/ml_requirements.txt
RUN pip install -r requirements/requirements.txt

ADD src .

EXPOSE ${CONTAINER_PORT}

ENTRYPOINT $(echo python service.py $PORT)
