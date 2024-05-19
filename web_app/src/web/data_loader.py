import requests
import streamlit as st

API_URL = "http://common_api:5000"


@st.cache_resource
def load_tickets() -> list:
    response = requests.get(f"{API_URL}/get_all_tickets")
    response.raise_for_status()
    return response.json()


def filter_by_diagnosis(tickets: list, search_query: str) -> list:
    return [ticket for ticket in tickets if search_query.lower() in (ticket.get('diagnosis') or '').lower()]


def doctor_list() -> list:
    response = requests.get(f"{API_URL}/get_all_tickets")
    response.raise_for_status()
    tickets = response.json()
    unique_doctors = {ticket.get('expert') for ticket in tickets if ticket.get('expert')}
    return list(unique_doctors)


def filter_by_status(tickets: list, status: str) -> list:
    if status == "все":
        return tickets
    elif status == "активный":
        return [ticket for ticket in tickets if ticket.get('status').lower() == "активный"]
    elif status == "неактивный":
        return [ticket for ticket in tickets if ticket.get('status').lower() == "неактивный"]
    else:
        raise ValueError(f"Unknown status: {status}")


def filter_by_doctor(tickets: list, doctor: str) -> list:
    if doctor == "all" or not doctor:
        return tickets
    return [ticket for ticket in tickets if ticket.get('expert').lower() == doctor.lower()]
