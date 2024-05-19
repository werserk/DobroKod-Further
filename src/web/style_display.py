import streamlit as st


# CSS и JavaScript для стилизации и обработки событий
def apply_styles():
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
def display_card(person, key):
    duplicate_warning = (
        "<div class='duplicate-warning'>Возможно дубликат</div>"
        if person["Дублон ли"] == 1
        else "<div></div>"
    )
    st.markdown(
        f"""
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
    """,
        unsafe_allow_html=True,
    )
