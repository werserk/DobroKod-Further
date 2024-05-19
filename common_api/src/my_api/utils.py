from typing import Optional

from models import User, Ticket
from session import SessionLocal


def add_user(
        chat_id: int,
        user_id: int,
        thread_id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        surname: Optional[str] = None,
) -> User:
    session = SessionLocal()
    user = User(
        surname=surname,
        name=name,
        email=email,
        chat_id=chat_id,
        user_id=user_id,
        thread_id=thread_id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def add_ticket(
        user_id: int, status: str, request_subject: str, request_body: str
) -> None:
    session = SessionLocal()
    ticket = Ticket(
        user_id=user_id,
        status=status,
        request_subject=request_subject,
        request_body=request_body,
    )
    session.add(ticket)
    session.commit()


def update_ticket_status(ticket_id: int, status: str) -> None:
    session = SessionLocal()
    ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
    ticket.status = status
    session.commit()
    session.refresh(ticket)


def get_ticket_by_id(ticket_id: int) -> Ticket:
    session = SessionLocal()
    ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
    return ticket


def get_user_by_id(user_id: int) -> User:
    session = SessionLocal()
    user = session.query(User).filter(User.user_id == user_id).first()
    return user


def get_user_by_chat_id(chat_id: int) -> User:
    session = SessionLocal()
    user = session.query(User).filter(User.chat_id == chat_id).first()
    return user


def get_user_by_email(email: str) -> User:
    session = SessionLocal()
    user = session.query(User).filter(User.email == email).first()
    return user


def get_user_by_name(name: str) -> User:
    session = SessionLocal()
    user = session.query(User).filter(User.name == name).first()
    return user


def update_user_thread_id(user_id: int, thread_id: str) -> None:
    session = SessionLocal()
    user = session.query(User).filter(User.user_id == user_id).first()
    user.thread_id = thread_id
    session.commit()
    session.refresh(user)


def get_all_tickets() -> list[Ticket]:
    session = SessionLocal()
    tickets = session.query(Ticket).all()
    return tickets


def get_all_users() -> list[User]:
    session = SessionLocal()
    users = session.query(User).all()
    return users
