.PHONY=build,run,clean,deploy

include .env

NAME=harambe-6
GIT_TAG=$(shell git rev-parse HEAD)
DOCKER_PROVIDER=jeremyaherzog
IMAGE=$(DOCKER_PROVIDER)/$(NAME)
CONTAINER_PORT=8080
HOST_PORT=50051

set-project:
	gcloud config set project $(NAME)

proto_compile:
	python3 -m grpc_tools.protoc -I src/api \
		--python_out=src/api \
		--grpc_python_out=src/api \
		--descriptor_set_out=src/api/api_descriptor.pb \
		src/api/service.proto

build:
	docker build -t $(IMAGE) --build-arg CONTAINER_PORT=$(CONTAINER_PORT) .

run:
	docker run -d --rm --name $(NAME) \
		--env-file=.env \
		-p $(HOST_PORT):$(CONTAINER_PORT) \
		$(IMAGE)

build-dev:
	docker build -f dev.dockerfile -t ${NAME}-dev-env .

run-dev:
	docker run --rm -it \
		--name ${NAME}-dev-env \
		-v $(shell pwd):/workspace \
		-v /var/run/docker.sock:/var/run/docker.sock \
		${NAME}-dev-env /bin/bash

clean:
	docker stop harambe-6 && docker rm harambe-6 && docker rmi $(IMAGE)

run-client:
	python3 src/client.py

push:
	docker tag ${IMAGE} ${IMAGE}:latest
	docker tag ${IMAGE} ${IMAGE}:${GIT_TAG}
	docker push ${IMAGE}:latest
	docker push ${IMAGE}:${GIT_TAG}

tf-init:
	terraform init \
		-backend-config "access_key=${TF_STATE_ACCESS_KEY}" \
		-backend-config "secret_key=${TF_STATE_SECRET_KEY}"

tf-deploy:
	terraform apply \
		-var "do_token=${DO_TOKEN}" \
		-var "version_tag"=${GIT_TAG} \
		-var "iex_key=${IEX_KEY}"
