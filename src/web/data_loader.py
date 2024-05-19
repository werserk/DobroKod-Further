import pandas as pd
import streamlit as st

DATA_PATH = "src/web/table.xlsx"


@st.cache
def load_data():
    return pd.read_excel(DATA_PATH)


def update_data(df):
    df.to_excel(DATA_PATH, index=False)
