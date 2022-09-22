from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config
from urllib import parse



DATABASE_CONFIG = Config.MariaDB
DATABASE_URL = f'mysql://{DATABASE_CONFIG["user"]}:{parse.quote(DATABASE_CONFIG["password"])}@{DATABASE_CONFIG["host"]}/{DATABASE_CONFIG["database"]}'

engine = create_engine(DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        yield session()
    except Exception as e:
        print(f"error {e}")
    finally:
        session.close_all()
