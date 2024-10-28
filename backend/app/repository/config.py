import os
from dotenv import load_dotenv
from .exceptions.repository_exceptions import DotEnvException, URIException

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
if not DB_USERNAME:
    raise DotEnvException('DB_USERNAME not found in .env file')

DB_PASSWORD = os.getenv('DB_PASSWORD')
if not DB_PASSWORD:
    raise DotEnvException('DB_PASSWORD not found in .env file')

try:
    MONGODB_URI = os.getenv('MONGODB_URI').format(db_username=DB_USERNAME, db_password=DB_PASSWORD)
except AttributeError:
    raise DotEnvException('MONGODB_URI not found in .env file')
except KeyError:
    raise URIException('{db_username} or {db_password} not found in MONGODB_URI string')