from typing import Optional

import requests

API_URL = "http://common_api:5000"


def add_user(
        chat_id: int,
        user_id: int,
        thread_id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        surname: Optional[str] = None,
) -> dict:
    payload = {
        'chat_id': chat_id,
        'user_id': user_id,
        'thread_id': thread_id,
        'email': email,
        'name': name,
        'surname': surname
    }
    response = requests.post(f"{API_URL}/add_user", json=payload)
    response.raise_for_status()
    return response.json()


def add_ticket(
        user_id: int,
        diagnosis: str,
        doctor: str,
        status: str,
        request_subject: str,
        request_body: str,
) -> None:
    payload = {
        'user_id': user_id,
        'diagnosis': diagnosis,
        'expert': doctor,
        'status': status,
        'request_subject': request_subject,
        'request_body': request_body,
        'is_duplicate': 0,
    }
    response = requests.post(f"{API_URL}/add_ticket", json=payload)
    response.raise_for_status()


def update_ticket_status(ticket_id: int, status: str) -> None:
    payload = {'status': status}
    response = requests.put(f"{API_URL}/update_ticket_status/{ticket_id}", json=payload)
    response.raise_for_status()


def get_ticket_by_id(ticket_id: int) -> dict:
    response = requests.get(f"{API_URL}/get_ticket/{ticket_id}")
    response.raise_for_status()
    return response.json()


def get_user_by_id(user_id: int) -> dict:
    response = requests.get(f"{API_URL}/get_user/{user_id}")
    response.raise_for_status()
    return response.json()


def get_user_by_chat_id(chat_id: int) -> dict:
    response = requests.get(f"{API_URL}/get_user_by_chat_id/{chat_id}")
    response.raise_for_status()
    return response.json()


def get_user_by_email(email: str) -> dict:
    response = requests.get(f"{API_URL}/get_user_by_email/{email}")
    response.raise_for_status()
    return response.json()


def get_user_by_name(name: str) -> dict:
    response = requests.get(f"{API_URL}/get_user_by_name/{name}")
    response.raise_for_status()
    return response.json()


def update_user_thread_id(user_id: int, thread_id: str) -> None:
    payload = {'thread_id': thread_id}
    response = requests.put(f"{API_URL}/update_user_thread_id/{user_id}", json=payload)
    response.raise_for_status()


def get_all_tickets() -> list:
    response = requests.get(f"{API_URL}/get_all_tickets")
    response.raise_for_status()
    return response.json()


def get_all_users() -> list:
    response = requests.get(f"{API_URL}/get_all_users")
    response.raise_for_status()
    return response.json()
