import os
from dotenv import load_dotenv

from app.repository.exceptions.repository_exceptions import DotEnvException


load_dotenv()

DEVICE_USERNAME = os.getenv('DEVICE_USERNAME')
if not DEVICE_USERNAME:
    raise DotEnvException('DEVICE_USERNAME not found in .env file')

DEVICE_PASSWORD = os.getenv('DEVICE_PASSWORD')
if not DEVICE_PASSWORD:
    raise DotEnvException('DEVICE_PASSWORD not found in .env file')
