import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from settings import settings


SQLALCHEMY_DATABASE_URL = settings.DB_CONNECT

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)


Base = declarative_base()
