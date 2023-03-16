from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import models
import os

url = os.getenv('URL_MYSQL')

if url:
    URL_MYSQL = url
else:
    load_dotenv()

    DB_NAME = os.getenv('DB_NAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST_TEST')
    DB_PORT = os.getenv('DB_PORT')

    URL_MYSQL = f"mysql+pymysql://root:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(URL_MYSQL, echo=True)
