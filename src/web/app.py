import streamlit as st

from data_loader import (
    load_ticket,
    filter_by_diagnosis,
    filter_by_doctor,
    filter_by_status,
)
from style_display import apply_styles, display_card


def main():
    apply_styles()
    tickets = load_ticket()
    st.sidebar.header("Фильтры")
    search_query = st.sidebar.text_input("Поиск по диагнозу:")
    status_filter = st.sidebar.selectbox("Статус:", ["Все", "активный", "неактивный"])

    doctor_filter = st.sidebar.selectbox(
        "Специалист:", ["Все"] + list(df["Специалист"].unique())
    )

    # Фильтрация данных
    filtered_df = filter_by_email(load_user, search_query)
    filtered_df = filter_by_status(load_ticket, status_filter)
    filtered_df = filter_by_doctor(filtered_df, doctor_filter)

    # Вывод данных
    st.markdown("<h1 style='text-align: center;'>Тикеты</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            display_card(row)

    # Обработчик события для изменения статуса
    query_params = st.query_params
    if "change_status" in query_params:
        key = int(query_params["change_status"][0])
        person = df.loc[key]
        if person["Статус"] == "активный":
            df.loc[key, "Статус"] = "неактивный"
        else:
            df.loc[key, "Статус"] = "активный"
        update_data(df)
        st.experimental_set_query_params()
        st.experimental_rerun()


if __name__ == "__main__":
    main()
