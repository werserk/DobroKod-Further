import json
import os
import threading
import time
from typing import List

import telebot
from dotenv import load_dotenv
from telebot import types

from src.bot.tickets import Ticket
from src.database.session import init_db
from src.database.utils import add_user, add_ticket
from src.processing.openai_service import get_ai_response

load_dotenv()

init_db()

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

USER_DATA = {}

@bot.message_handler(commands=["start"])
def send_welcome(message: types.Message) -> None:
    bot.send_message(
        message.chat.id, "Что вас интересует?", reply_markup=main_menu_keyboard
    )
    USER_DATA[message.from_user.id] = Ticket(message.from_user.id, message.chat.id)
    add_user(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        name=message.from_user.first_name,
    )


def generate_submenu(options: List[str]) -> types.ReplyKeyboardMarkup:
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
    if message.from_user.id in USER_DATA and USER_DATA[message.from_user.id].flag == True and USER_DATA[message.from_user.id].status == 'заполнено':
        USER_DATA[message.from_user.id].request = message.text
        USER_DATA[message.from_user.id].flag = False
        USER_DATA[message.from_user.id].status = 'работаем'
        add_ticket(
            message.from_user.id, USER_DATA[message.from_user.id].diagnosis,
            USER_DATA[message.from_user.id].doctor,
            'активный', '', USER_DATA[message.from_user.id].request
        )
        bot.send_message(message.chat.id, 'Спасибо за заявку, она принята и находится в работе')
        return

    if message.from_user.id in USER_DATA and USER_DATA[message.from_user.id].flag == True and USER_DATA[message.from_user.id].status == 'сбор данных':
        if  USER_DATA[message.from_user.id].name == None:
            USER_DATA[message.from_user.id].name = message.text
            if USER_DATA[message.from_user.id].email == None:
                bot.send_message(message.chat.id, 'Напишите свой email')
            elif USER_DATA[message.from_user.id].diagnosis == None:
                bot.send_message(message.chat.id, 'Напишите свой диагноз или слово нет, при отсутствии')
            elif USER_DATA[message.from_user.id].doctor == None:
                bot.send_message(message.chat.id, 'Напишите, кому адрессован вопрос')
            else:
                USER_DATA[message.from_user.id].status = 'заполнено'
                bot.send_message(message.chat.id, 'Напишите свой вопрос')
        elif USER_DATA[message.from_user.id].email == None:
            USER_DATA[message.from_user.id].email = message.text
            if USER_DATA[message.from_user.id].diagnosis == None:
                bot.send_message(message.chat.id, 'Напишите свой диагноз или слово нет, при отсутствии')
            elif USER_DATA[message.from_user.id].doctor == None:
                bot.send_message(message.chat.id, 'Напишите, кому адрессован вопрос')
            else:
                USER_DATA[message.from_user.id].status = 'заполнено'
                bot.send_message(message.chat.id, 'Напишите свой вопрос')
        elif USER_DATA[message.from_user.id].diagnosis == None:
            USER_DATA[message.from_user.id].diagnosis = message.text
            if USER_DATA[message.from_user.id].doctor == None:
                bot.send_message(message.chat.id, 'Напишите, кому адрессован вопрос')
            else:
                USER_DATA[message.from_user.id].status = 'заполнено'
                bot.send_message(message.chat.id, 'Напишите свой вопрос')
        elif USER_DATA[message.from_user.id].doctor == None:
            USER_DATA[message.from_user.id].doctor = message.text
            USER_DATA[message.from_user.id].status = 'заполнено'
            bot.send_message(message.chat.id, 'Напишите свой вопрос')


    if text == 'оставить заявку':
        if message.from_user.id not in USER_DATA:
            USER_DATA[message.from_user.id] = Ticket(message.from_user.id, message.chat.id)
        USER_DATA[message.from_user.id].flag = True
        if  USER_DATA[message.from_user.id].name == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите ФИО')
        elif USER_DATA[message.from_user.id].email == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите свой email')
        elif USER_DATA[message.from_user.id].diagnosis == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите свой диагноз или слово нет, при отсутствии')
        elif USER_DATA[message.from_user.id].doctor == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите, кому адрессован вопрос')
        else:
            USER_DATA[message.from_user.id].status = 'заполнено'
            bot.send_message(message.chat.id, 'Напишите свой вопрос')

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
            USER_DATA[message.from_user.id] = Ticket(message.from_user.id, message.chat.id)
        USER_DATA[message.from_user.id].flag = True
        if USER_DATA[message.from_user.id].name == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите ФИО')
        elif USER_DATA[message.from_user.id].email == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите свой email')
        elif USER_DATA[message.from_user.id].diagnosis == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите свой диагноз или слово нет, при отсутствии')
        elif USER_DATA[message.from_user.id].doctor == None:
            USER_DATA[message.from_user.id].status = 'сбор данных'
            bot.send_message(message.chat.id, 'Напишите, кому адрессован вопрос')
        else:
            USER_DATA[message.from_user.id].status = 'заполнено'
            bot.send_message(message.chat.id, 'Напишите свой вопрос')
    else:
        if USER_DATA[message.from_user.id].flag != True:
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

    gpt_response = get_ai_response(message)

    thread.join()

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=loading_message.message_id,
        text=gpt_response,
    )


if __name__ == "__main__":
    print("[*] Bot is active")
    bot.polling()
