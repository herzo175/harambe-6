NAME=harambe-6
GIT_TAG=$(shell git rev-parse HEAD)
PROJECT_ID=$(shell gcloud config list --format 'value(core.project)')
CONTAINER_PORT=8080
HOST_PORT=50051
KEYRING=harambe-6-dev
KEY=harambe-6-dev-key
BUCKET=harambe-6-dev
CREDENTIALS_FILE=harambe-6-account.json
SECRETS_FILE=secrets.json
SECRETS_FILE_ENCRYPTED=secrets.json.encrypted

# gcloud config set project harambe-6
# gcloud projects add-iam-policy-binding harambe-6 --member serviceAccount:... --role roles/cloudkms.cryptoKeyDecrypter

proto_compile:
	python3 -m grpc_tools.protoc -I . \
		--python_out=. \
		--grpc_python_out=. \
		--descriptor_set_out=api_descriptor.pb \
		service.proto

build:
	docker build -t gcr.io/$(PROJECT_ID)/$(NAME):$(GIT_TAG) --build-arg CONTAINER_PORT=$(CONTAINER_PORT) .

run:
	docker run --rm -d --name $(NAME) \
		--env GOOGLE_APPLICATION_CREDENTIALS=$(CREDENTIALS_FILE) \
		-v $(shell pwd)/$(CREDENTIALS_FILE):/app/$(CREDENTIALS_FILE) \
		-p $(HOST_PORT):$(CONTAINER_PORT) \
		gcr.io/$(PROJECT_ID)/$(NAME):$(GIT_TAG)

deploy:
	gcloud auth configure-docker && docker push gcr.io/$(PROJECT_ID)/$(NAME):$(GIT_TAG)
	# kubectl run $(NAME) --image=gcr.io/$(PROJECT_ID)/$(NAME):$(GIT_TAG) --port 50051
	# kubectl expose deployment $(NAME) --type=LoadBalancer --port 50051 --target-port 50051
	# kubectl get service
	# gcloud app deploy --version $(GIT_TAG)
	# gcloud endpoints services deploy api_descriptor.pb api_config.yaml # NOTE: re-enable for grpc when endpoints is available on cloud run
	gcloud beta run deploy --image gcr.io/$(PROJECT_ID)/$(NAME):$(GIT_TAG) --memory 512Mi

upload_secrets:
	gcloud kms encrypt \
		--location global \
		--keyring $(KEYRING) \
		--key $(KEY) \
		--plaintext-file $(SECRETS_FILE) \
		--ciphertext-file $(SECRETS_FILE_ENCRYPTED)
	gsutil cp $(SECRETS_FILE_ENCRYPTED) gs://$(BUCKET)/

download_secrets:
	gsutil cp gs://$(BUCKET)/$(SECRETS_FILE_ENCRYPTED) $(SECRETS_FILE_ENCRYPTED)
	gcloud kms decrypt \
		--location global \
		--keyring $(KEYRING) \
		--key $(KEY) \
		--plaintext-file $(SECRETS_FILE) \
		--ciphertext-file $(SECRETS_FILE_ENCRYPTED)
