# web_app/src/web/my_api.py
import streamlit as st

from data_loader import (
    load_ticket,
    filter_by_diagnosis,
    filter_by_doctor,
    filter_by_status,
    doctor_list
)
from style_display import apply_styles, display_card

API_URL = "http://common_api:5000"


def main():
    apply_styles()
    tickets = load_ticket()
    st.sidebar.header("Фильтры")
    search_query = st.sidebar.text_input("Поиск по диагнозу:")
    status_filter = st.sidebar.selectbox("Статус:", ["Все", "активный", "неактивный"])

    doctor_filter = st.sidebar.selectbox(
        "Специалист:", ["Все"] + doctor_list()
    )

    # Фильтрация данных
    filtered_df = filter_by_diagnosis(tickets, search_query)
    filtered_df = filter_by_status(tickets, status_filter)
    filtered_df = filter_by_doctor(tickets, doctor_filter)

    # Вывод данных
    st.markdown("<h1 style='text-align: center;'>Тикеты</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for ticket in filtered_df:
            display_card(ticket)


if __name__ == "__main__":
    main()
