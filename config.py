import os
import json

from google.cloud import storage
from google.cloud import kms_v1

# NOTE: resolve name with environment
# NOTE: may move name to config file
BUCKET_NAME="harambe-6-dev"
SECRETS_FILE="secrets.json"
ENCRYPTED_SECRETS_FILE="secrets.json.encrypted"

STATIC_CONFIG={}


def update_encrypted_config(secrets_file=SECRETS_FILE, encrypted_secrets_file=ENCRYPTED_SECRETS_FILE):
    # load secrets file
    download_config_file(encrypted_secrets_file)
    # decrypt secrets file
    decrypt_secrets_file(encrypted_secrets_file, secrets_file)
    # load secrets into static config
    conf = load_json_config(secrets_file)

    for key in conf:
        STATIC_CONFIG[key] = conf[key]


def get_alphavantage_api_key():
    global STATIC_CONFIG
    alphavantage_api_key_id = "ALPHAVANTAGE_API_KEY" 

    if alphavantage_api_key_id not in STATIC_CONFIG:
        update_encrypted_config()

    return STATIC_CONFIG[alphavantage_api_key_id]


def download_config_file(filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(filename)

    blob.download_to_filename(filename)


def decrypt_secrets_file(input_filename, output_filename):
    with open(input_filename, "rb") as ciphertext_file:
        ciphertext = ciphertext_file.read()

        client = kms_v1.KeyManagementServiceClient()
        name = client.crypto_key_path_path(
            "harambe-6", "global", "harambe-6-dev", "harambe-6-dev-key")
        # Use the KMS API to decrypt the data.
        response = client.decrypt(name, ciphertext)

        plaintext = response.plaintext.decode("utf-8")

        with open(output_filename, "w") as output_file:
            output_file.write(plaintext)


def load_json_config(input_filename):
    with open(input_filename) as json_file:  
        return json.load(json_file)
