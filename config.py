import os
import json
import logging

from google.cloud import storage
from google.cloud import kms_v1

# NOTE: resolve name with environment
# NOTE: may move name to config file
BUCKET_NAME="harambe-6-dev"
DEFAULTS_FILE="defaults.json"
SECRETS_FILE="secrets.json"
ENCRYPTED_SECRETS_FILE="secrets.json.encrypted"
ENVIRON = os.getenv('ENVIRON', None);

STATIC_CONFIG={}


def update_config(config_file):
    global STATIC_CONFIG
    try:
        conf = load_json_config(config_file)

        for key in conf:
            STATIC_CONFIG[key] = conf[key]
            
    except FileNotFoundError as e:
        logging.warn(f"Config file not found for environment: {ENVIRON}")

def update_encrypted_config(secrets_file=SECRETS_FILE, encrypted_secrets_file=ENCRYPTED_SECRETS_FILE):
    # load secrets file
    download_config_file(encrypted_secrets_file)
    # decrypt secrets file
    decrypt_secrets_file(encrypted_secrets_file, secrets_file)
    # load secrets into static config
    update_config(secrets_file)


def get_config_key(key):
    global STATIC_CONFIG

    if key in STATIC_CONFIG:
        return STATIC_CONFIG[key]
    else:
        # load defaults
        if key not in STATIC_CONFIG:
            update_config(DEFAULTS_FILE)

        # look in environ config
        if key not in STATIC_CONFIG:
            update_config(f"{ENVIRON}.json")

        # look in encrypted
        if key not in STATIC_CONFIG:
            update_encrypted_config()

        # Key error if not in config
        return STATIC_CONFIG[key]


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
        print(name)
        # Use the KMS API to decrypt the data.
        response = client.decrypt(name, ciphertext)

        plaintext = response.plaintext.decode("utf-8")

        with open(output_filename, "w") as output_file:
            output_file.write(plaintext)


def load_json_config(input_filename):
    with open(input_filename) as json_file:  
        return json.load(json_file)
