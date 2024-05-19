import os

import streamlit as st
import pandas as pd

data_path = 'src/web/table.xlsx'
df = pd.read_excel('src/web/table.xlsx')

# CSS и JavaScript для стилизации и обработки событий
st.markdown("""
    <style>
    .card {
        border: 1px solid #e6e6e6; 
        border-radius: 10px; 
        padding: 20px; 
        margin: 10px; 
        background-color: #f2f2f2; 
        position: relative;
    }
    .checkmark {
        position: absolute; 
        top: 10px; 
        right: 10px; 
        background: none; 
        border: none; 
        cursor: pointer;
    }
    .checkmark svg:hover {
        fill: limegreen;
    }
    .duplicate-warning {
        color: red;
        font-weight: bold;
    }
    </style>
    <script>
    function changeStatus(key) {
        const params = new URLSearchParams(window.location.search);
        params.set('change_status', key);
        window.location.search = params.toString();
    }
    </script>
""", unsafe_allow_html=True)

# Функция для отображения данных в виде карточек
def display_card(person, key):
    duplicate_warning = "<div class='duplicate-warning'>Возможно дубликат</div>" if person['Дублон ли'] == 1 else "<div></div>"
    st.markdown(f"""
    <div class="card">
        {duplicate_warning}
        <button class="checkmark" onclick="changeStatus('{key}')">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="green" style="transform: scaleY(-1);">
                <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 22c-5.514 0-10-4.486-10-10s4.486-10 10-10 10 4.486 10 10-4.486 10-10 10zm-2-15l-5 5 1.414 1.414 3.586-3.586 7.586 7.586 1.414-1.414-9-9z"/>
            </svg>
        </button>
        <h3 style="color: #2c3e50;">{person['Имя']}</h3>
        <p style="color: #34495e;"><strong>Статус:</strong> {person['Статус']}</p>
        <p style="color: #34495e;"><strong>Диагноз:</strong> {person['Диагноз']}</p>
        <p style="color: #34495e;"><strong>Почта:</strong> {person['Почта']}</p>
        <p style="color: #34495e;"><strong>Заявка:</strong> {person['Тема заявки']}</p>
        <p style="color: #34495e;"><strong>Специалист:</strong> {person['Специалист']}</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Меню с поисковой строкой и фильтрами
    st.sidebar.header("Фильтры")
    search_query = st.sidebar.text_input("Поиск по почте:")
    status_filter = st.sidebar.selectbox("Статус:", ["Все", "активный", "неактивный"])
    doctor_filter = st.sidebar.selectbox("Специалист:", ["Все"] + list(df['Специалист'].unique()))

    # Фильтрация данных
    filtered_df = df[
        (df['Почта'].str.contains(search_query, case=False, na=False)) &
        ((df['Статус'] == status_filter) if status_filter != "Все" else True) &
        ((df['Специалист'] == doctor_filter) if doctor_filter != "Все" else True)
        ]

    # Вывод данных
    st.markdown("<h1 style='text-align: center;'>Хуи и пёзды</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            display_card(row, key=idx)

    # Обработчик события для изменения статуса
    query_params = st.experimental_get_query_params()
    if 'change_status' in query_params:
        key = int(query_params['change_status'][0])
        person = df.loc[key]
        if person['Статус'] == "активный":
            df.loc[key, 'Статус'] = "неактивный"
        else:
            df.loc[key, 'Статус'] = "активный"
        df.to_excel(data_path, index=False)
        st.experimental_set_query_params()  # Очистить параметры
        st.experimental_rerun()

if __name__ == "__main__":
    main()
