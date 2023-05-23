import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '../.env')
load_dotenv(dotenv_path)

API_QUESTION_REQUEST_PATH = "https://jservice.io/api/random?count="

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_PORT = (os.getenv("POSTGRES_PORT", '5432'))
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

DOCKER_HOST = 'berwise_db'
ENGINE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DOCKER_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

WEB_PORT = os.getenv("WEB_PORT", "8000")
