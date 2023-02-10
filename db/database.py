from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = 'root'
PASSWORD = 'admin_fernando'
PORT = '3306'
DB_NAME = 'fernando_responde'

SQL_ALCHEMY_DATABASE_URL = f'mysql+mysqldb://{USER}:{PASSWORD}@127.1.0.0/{DB_NAME}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()