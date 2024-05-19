import pandas as pd
import streamlit as st


# CSS и JavaScript для стилизации и обработки событий
def apply_styles() -> None:
    st.set_page_config(layout="wide")
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )


# Функция для отображения данных в виде карточек
def display_card(person: pd.Series) -> None:
    duplicate_warning = (
        "<div class='duplicate-warning'>Возможно дубликат</div>"
        if person["Дублон ли"] == 1
        else "<div></div>"
    )
    st.markdown(
        f"""
    <div class="card">
        {duplicate_warning}
        <h3 style="color: #2c3e50;">{person['Имя']}</h3>
        <p style="color: #34495e;"><strong>Статус:</strong> {person['Статус']}</p>
        <p style="color: #34495e;"><strong>Диагноз:</strong> {person['Диагноз']}</p>
        <p style="color: #34495e;"><strong>Почта:</strong> {person['Почта']}</p>
        <p style="color: #34495e;"><strong>Заявка:</strong> {person['Тема заявки']}</p>
        <p style="color: #34495e;"><strong>Специалист:</strong> {person['Специалист']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
