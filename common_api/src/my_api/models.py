# common_api/src/my_api/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    surname = Column(String)
    name = Column(String)
    email = Column(String)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    thread_id = Column(String, nullable=True)

    tickets = relationship("Ticket", back_populates="user")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String, nullable=False)
    diagnosis = Column(String)
    request_subject = Column(String, nullable=False)
    request_body = Column(String, nullable=False)
    expert = Column(String)
    is_duplicate = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tickets")
