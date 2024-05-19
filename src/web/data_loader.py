import pandas as pd
import streamlit as st

DATA_PATH = "./data/table.xlsx"


@st.cache_resource
def load_data():
    return pd.read_excel(DATA_PATH)


def filter_by_email(df, search_query):
    if search_query:
        return df[df["Почта"].str.contains(search_query, case=False, na=False)]
    return df


def filter_by_status(df, status_filter):
    if status_filter != "Все":
        return df[df["Статус"] == status_filter]
    return df


def filter_by_doctor(df, doctor_filter):
    if doctor_filter != "Все":
        return df[df["Специалист"] == doctor_filter]
    return df


def update_data(df):
    df.to_excel(DATA_PATH, index=False)
