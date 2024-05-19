import json
import os
import threading
import time

import requests
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
API_URL = "http://common_api:5000"

# Load data from JSON
with open("./data/buttons_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

main_menu_buttons = data["main_menu_buttons"]
charity_answers = data["charity_answers"]
to_make_tickets = data["to_make_tickets"]

# Main menu
main_menu_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons = [types.KeyboardButton(button["title"]) for button in main_menu_buttons]
main_menu_keyboard.add(*buttons)

USER_DATA = {}


@bot.message_handler(commands=["start"])
def send_welcome(message: types.Message) -> None:
    bot.send_message(
        message.chat.id, "Что вас интересует?", reply_markup=main_menu_keyboard
    )
    # response = requests.post(
    #     f"{API_URL}/add_user",
    #     json={
    #         "chat_id": message.chat.id,
    #         "user_id": message.from_user.id,
    #         "name": message.from_user.first_name,
    #     },
    # )
    # user_id = response.json().get("user_id")


def generate_submenu(options: list) -> types.ReplyKeyboardMarkup:
    submenu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(option) for option in options]
    buttons.append(types.KeyboardButton("Назад"))
    buttons.append(types.KeyboardButton("Оставить заявку"))
    submenu.add(*buttons)
    return submenu


@bot.message_handler(func=lambda message: True)
def handle_message(message: types.Message) -> None:
    text = message.text.lower()

    if text == "назад":
        bot.send_message(
            message.chat.id, "Что вас интересует?", reply_markup=main_menu_keyboard
        )
        return
    if (
            message.from_user.id in USER_DATA
            and USER_DATA[message.from_user.id].get('flag') == True
            and USER_DATA[message.from_user.id].get('status') == "заполнено"
    ):
        USER_DATA[message.from_user.id]['request'] = message.text
        USER_DATA[message.from_user.id]['flag'] = False
        USER_DATA[message.from_user.id]['status'] = "работаем"
        response = requests.post(
            f"{API_URL}/add_ticket",
            json={
                "user_id": message.from_user.id,
                "diagnosis": USER_DATA[message.from_user.id].get('diagnosis'),
                "doctor": USER_DATA[message.from_user.id].get('doctor'),
                "status": "активный",
                "request_subject": "",
                "request_body": USER_DATA[message.from_user.id].get('request'),
            },
        )
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("status") == "success":
                bot.send_message(
                    message.chat.id, "Спасибо за заявку, она принята и находится в работе"
                )
            else:
                bot.send_message(
                    message.chat.id, f"Ошибка: {response_json.get('error', 'Unknown error')}"
                )
        else:
            bot.send_message(
                message.chat.id, f"Ошибка при обработке запроса: {response.status_code}"
            )
        return

    if (
            message.from_user.id in USER_DATA
            and USER_DATA[message.from_user.id].get('flag') == True
            and USER_DATA[message.from_user.id].get('status') == "сбор данных"
    ):
        if USER_DATA[message.from_user.id].get('name') is None:
            USER_DATA[message.from_user.id]['name'] = message.text
            if USER_DATA[message.from_user.id].get('email') is None:
                bot.send_message(message.chat.id, "Напишите свой email")
            elif USER_DATA[message.from_user.id].get('diagnosis') is None:
                bot.send_message(
                    message.chat.id,
                    "Напишите свой диагноз или слово нет, при отсутствии",
                )
            elif USER_DATA[message.from_user.id].get('doctor') is None:
                bot.send_message(message.chat.id, "Напишите, кому адресован вопрос")
            else:
                USER_DATA[message.from_user.id]['status'] = "заполнено"
                bot.send_message(message.chat.id, "Напишите свой вопрос")
        elif USER_DATA[message.from_user.id].get('email') is None:
            USER_DATA[message.from_user.id]['email'] = message.text
            if USER_DATA[message.from_user.id].get('diagnosis') is None:
                bot.send_message(
                    message.chat.id,
                    "Напишите свой диагноз или слово нет, при отсутствии",
                )
            elif USER_DATA[message.from_user.id].get('doctor') is None:
                bot.send_message(message.chat.id, "Напишите, кому адресован вопрос")
            else:
                USER_DATA[message.from_user.id]['status'] = "заполнено"
                bot.send_message(message.chat.id, "Напишите свой вопрос")
        elif USER_DATA[message.from_user.id].get('diagnosis') is None:
            USER_DATA[message.from_user.id]['diagnosis'] = message.text
            if USER_DATA[message.from_user.id].get('doctor') is None:
                bot.send_message(message.chat.id, "Напишите, кому адресован вопрос")
            else:
                USER_DATA[message.from_user.id]['status'] = "заполнено"
                bot.send_message(message.chat.id, "Напишите свой вопрос")
        elif USER_DATA[message.from_user.id].get('doctor') is None:
            USER_DATA[message.from_user.id]['doctor'] = message.text
            USER_DATA[message.from_user.id]['status'] = "заполнено"
            bot.send_message(message.chat.id, "Напишите свой вопрос")

    if text == "оставить заявку":
        if message.from_user.id not in USER_DATA:
            USER_DATA[message.from_user.id] = {}
        USER_DATA[message.from_user.id]['flag'] = True
        if USER_DATA[message.from_user.id].get('name') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(message.chat.id, "Напишите ФИО")
        elif USER_DATA[message.from_user.id].get('email') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(message.chat.id, "Напишите свой email")
        elif USER_DATA[message.from_user.id].get('diagnosis') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(
                message.chat.id, "Напишите свой диагноз или слово нет, при отсутствии"
            )
        elif USER_DATA[message.from_user.id].get('doctor') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(message.chat.id, "Напишите, кому адресован вопрос")
        else:
            USER_DATA[message.from_user.id]['status'] = "заполнено"
            bot.send_message(message.chat.id, "Напишите свой вопрос")

    for button in main_menu_buttons:
        if text == button["title"].lower():
            if button["submenu"]:
                submenu = generate_submenu(button["submenu"])
                bot.send_message(
                    message.chat.id,
                    f'Вы выбрали "{message.text}". Пожалуйста, выберите:',
                    reply_markup=submenu,
                )
            else:
                bot.send_message(
                    message.chat.id, "Соединяем вас с сотрудником Фонда..."
                )
            return

    if text in charity_answers:
        answer = charity_answers[text]
        if answer["info_type"] == "link":
            bot.send_message(message.chat.id, answer["name"])
        elif answer["info_type"] == "document":
            pdf_path = answer["file"]
            with open(pdf_path, "rb") as pdf_file:
                bot.send_document(message.chat.id, pdf_file)
    elif text in to_make_tickets:
        if message.from_user.id not in USER_DATA:
            USER_DATA[message.from_user.id] = {}
        USER_DATA[message.from_user.id]['flag'] = True
        if USER_DATA[message.from_user.id].get('name') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(message.chat.id, "Напишите ФИО")
        elif USER_DATA[message.from_user.id].get('email') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(message.chat.id, "Напишите свой email")
        elif USER_DATA[message.from_user.id].get('diagnosis') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(
                message.chat.id, "Напишите свой диагноз или слово нет, при отсутствии"
            )
        elif USER_DATA[message.from_user.id].get('doctor') is None:
            USER_DATA[message.from_user.id]['status'] = "сбор данных"
            bot.send_message(message.chat.id, "Напишите, кому адресован вопрос")
        else:
            USER_DATA[message.from_user.id]['status'] = "заполнено"
            bot.send_message(message.chat.id, "Напишите свой вопрос")
        response = requests.post(
            f"{API_URL}/add_ticket",
            json={
                "user_id": message.from_user.id,
                "status": "new",
                "request_subject": "New Ticket",
                "request_body": text,
            },
        )
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("status") == "success":
                bot.send_message(
                    message.chat.id,
                    "Ваш запрос был зарегистрирован. Мы скоро с вами свяжемся.",
                )
            else:
                bot.send_message(
                    message.chat.id, f"Ошибка: {response_json.get('error', 'Unknown error')}"
                )
        else:
            bot.send_message(
                message.chat.id, f"Ошибка при обработке запроса: {response.status_code}"
            )
    else:
        if not USER_DATA[message.from_user.id].get('flag', False):
            process_question(message)


def handle_ai_response(message: types.Message, ai_message: types.Message) -> None:
    max_points_generated = 25
    max_points_inline = 3

    dots = ""
    for _ in range(max_points_generated):
        dots += "."
        if len(dots) > max_points_inline:
            dots = ""
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=ai_message.message_id,
            text=f"Ищем ответ{dots}",
        )
        time.sleep(0.5)


def process_question(message: types.Message) -> None:
    loading_message = bot.send_message(message.chat.id, "Ищем ответ")
    thread = threading.Thread(
        target=handle_ai_response, args=(message, loading_message)
    )
    thread.start()

    response = requests.post(
        f"{API_URL}/get_ai_response", json={"message": message.text}
    )
    gpt_response = response.json().get("response")

    thread.join()

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=loading_message.message_id,
        text=gpt_response,
    )


if __name__ == "__main__":
    print("[*] Bot is active")
    bot.polling()
