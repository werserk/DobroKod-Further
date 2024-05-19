# web_app/src/web/data_loader.py
import pandas as pd
import requests
import streamlit as st

API_URL = "http://common_api:5000"


@st.cache_data
def load_data() -> pd.DataFrame:
    response = requests.get(f"{API_URL}/get_all_tickets")
    data = response.json()
    return pd.DataFrame(data)


def filter_by_email(df: pd.DataFrame, search_query: str) -> pd.DataFrame:
    if search_query:
        return df[df["Почта"].str.contains(search_query, case=False, na=False)]
    return df


def filter_by_status(df: pd.DataFrame, status_filter: str) -> pd.DataFrame:
    if status_filter != "Все":
        return df[df["Статус"] == status_filter]
    return df


def filter_by_doctor(df: pd.DataFrame, doctor_filter: str) -> pd.DataFrame:
    if doctor_filter != "Все":
        return df[df["Специалист"] == doctor_filter]
    return df


def update_data(df: pd.DataFrame) -> None:
    # Update data through API
    pass
