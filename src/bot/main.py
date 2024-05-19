import json
import os
import threading
import time
from typing import List

import telebot
from dotenv import load_dotenv
from telebot import types

from src.bot.tickets import make_ticket
from src.processing.openai_service import get_ai_response

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Загрузка данных из JSON
with open("../../data/buttons_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

main_menu_buttons = data["main_menu_buttons"]
charity_answers = data["charity_answers"]
to_make_tickets = data["to_make_tickets"]

# Главное меню
main_menu_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons = [types.KeyboardButton(button["title"]) for button in main_menu_buttons]
main_menu_keyboard.add(*buttons)


@bot.message_handler(commands=["start"])
def send_welcome(message: types.Message) -> None:
    bot.send_message(
        message.chat.id, "Что вас интересует?", reply_markup=main_menu_keyboard
    )


def generate_submenu(options: List[str]) -> types.ReplyKeyboardMarkup:
    submenu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(option) for option in options]
    buttons.append(types.KeyboardButton("Назад"))
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
        make_ticket(message.chat.id, message.from_user.id)
        bot.send_message(
            message.chat.id, "Ваш запрос был зарегистрирован. Мы скоро с вами свяжемся."
        )
    else:
        process_question(message)


def handle_ai_response(message: types.Message, ai_message: types.Message) -> None:
    dots = ""
    for _ in range(20):
        dots += "."
        if len(dots) > 3:
            dots = ""
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=ai_message.message_id,
            text=f"Ищем ответ{dots}",
        )
        time.sleep(0.5)


def process_question(message: types.Message) -> None:
    user_question = message.text
    loading_message = bot.send_message(message.chat.id, "Ищем ответ")

    thread = threading.Thread(
        target=handle_ai_response, args=(message, loading_message)
    )
    thread.start()

    gpt_response = get_ai_response(user_question, message.chat.id)

    thread.join()

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=loading_message.message_id,
        text=gpt_response,
    )


if __name__ == "__main__":
    bot.polling()
