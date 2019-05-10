# Harambe 6

## Getting started

In order to resolve secret credentials, you will need to either have a Google
application credentials file at 'harambe-6-account.json' or override the config
keys with either a 'default.json' file or a 'local.json' file. Those will be
added to the docker container at build time.

Once you have credentials:

```bash
make set-project

make build
make run
```

## Deployment

This app uses GCP Cloud Run for deployment (TODO: CI/CD)

To deploy:

```bash
make run
```

There is code to support using gRPC instead of REST API calls to invoke the
predictor. The deployment should be changed once HTTP 2 is available for Cloud
Run
