import pandas as pd
import streamlit as st

DATA_PATH = "./data/table.xlsx"


@st.cache_resource
def load_data() -> pd.DataFrame:
    return pd.read_excel(DATA_PATH)


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
    df.to_excel(DATA_PATH, index=False)
