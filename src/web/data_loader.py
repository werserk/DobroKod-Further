import pandas as pd
import streamlit as st
from src.database.utils import get_all_users, get_all_tickets
from src.database.models import User, Ticket


@st.cache_resource
def load_ticket() -> list[Ticket]:
    return get_all_tickets()

def filter_by_diagnosis(users: list[Ticket], search_query: str) -> list[Ticket]:
    return [user for user in users if search_query.lower() in (user.diagnosis or '').lower()]

def doctor_list():
    unique_doctors = session.query(Ticket.expert).distinct().all()
    return [doctor[0] for doctor in unique_doctors if doctor[0]]

def filter_by_status(tickets: list[Ticket], status: str) -> list[Ticket]:
    if status == "все":
        return tickets
    elif status == "активный":
        return [ticket for ticket in tickets if ticket.status.lower() == "активный"]
    elif status == "неактивный":
        return [ticket for ticket in tickets if ticket.status.lower() == "неактивный"]
    else:
        raise ValueError(f"Unknown status: {status}")



def filter_by_doctor(tickets: list[Ticket], doctor: str) -> list[Ticket]:
    if doctor == "all" or not doctor:
        return tickets
    return [ticket for ticket in tickets if ticket.expert.lower() == doctor.lower()]

