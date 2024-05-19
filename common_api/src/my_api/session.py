from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

SQLALCHEMY_DATABASE_URI = "sqlite:///tickets_lib.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
