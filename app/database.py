from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
from icecream import ic


# Format of connection string for sqlalchemt
# SQLALCHEMY_DATABASE_URL = "postgresql://<user>:<password>@<postgresserver-host>/<database name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{config('DB_PASSWORD')}@localhost/fastapi"
ic(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()