import os

import pandas as pd

DATA_PATH = "src/web/table.xlsx"


def add_patient_record(
    file_path: str,
    status: str,
    diagnosis: str,
    name: str,
    email: str,
    chat_id: int,
    user_id: int,
    request: str,
    doctor: str,
):
    # Проверим, существует ли файл
    if os.path.exists(file_path):
        # Загрузим существующие данные
        df = pd.read_excel(file_path)
    else:
        # Создадим новый DataFrame с заголовками
        df = pd.DataFrame(
            columns=[
                "Статус",
                "Диагноз",
                "Имя",
                "Почта",
                "chat_id",
                "user_id",
                "Заявка",
                "Врач",
            ]
        )

    # Создадим новую запись
    new_record = {
        "Статус": status,
        "Диагноз": diagnosis,
        "Имя": name,
        "Почта": email,
        "chat_id": chat_id,
        "user_id": user_id,
        "Заявка": request,
        "Врач": doctor,
    }

    # Добавим новую запись в DataFrame
    df = df.append(new_record, ignore_index=True)

    # Сохраним DataFrame в Excel файл
    df.to_excel(file_path, index=False)


def make_ticket(chat_id, user_id):
    # Здесь добавьте логику для создания заявки
    pass
