import os
import json
import logging

from google.cloud import storage
from google.cloud import kms_v1

class Config:
    def __init__(self):
        self.resolvers = {
            "IEX_KEY": lambda: os.getenv("IEX_KEY")
        }

    def get_value(self, key):
        resolver = self.resolvers[key]
        value = resolver()

        if value is not None:
            self.resolvers[key] = lambda: value

        return value

STATIC_CONFIG=Config()
