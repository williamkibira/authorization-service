# import os
# from decouple import config

# DEBUG = config('DEBUG', cast=bool, default=True)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATABASE_URL = config('DATABASE_URL', default='sqlite:///sample.db')
# RESOURCES_DIRECTORY = os.path.join(BASE_DIR, "resources")
# MIGRATIONS_FOLDER = os.path.join(RESOURCES_DIRECTORY, "migrations")
# STORAGE_HOST = config('STORAGE_BUCKET', default='')
# STORAGE_BUCKET = config('STORAGE_BUCKET', default='')
# STORAGE_KEY = config('STORAGE_KEY', default='')
# STORAGE_SECRET = config('STORAGE_SECRET', default='')
# STORAGE_REGION = config('STORAGE_REGION', default='')
#
# # SECURITY AUTHORIZATION PARAMETERS
# PRIVATE_RSA_KEY = os.path.join(RESOURCES_DIRECTORY, "keys/private-rsa-key.pem")
# PRIVATE_RSA_KEY_PASSWORD = config('RSA_KEY_PASSWORD', default='')
# ACCEPTED_AUDIENCE = config('ACCEPTED_AUDIENCE', default='')
from os import path

BASE_DIRECTORY = path.dirname(path.abspath(__file__))

RESOURCES_DIRECTORY = path.join(BASE_DIRECTORY, "../resources")

MIGRATIONS_FOLDER = path.join(RESOURCES_DIRECTORY, "migrations")
PRIVATE_RSA_KEY = path.join(RESOURCES_DIRECTORY, "keys/private-rsa-key.pem")
PUBLIC_RSA_KEY = path.join(RESOURCES_DIRECTORY, "keys/public-rsa-key.pem")
