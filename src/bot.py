import telebot
from telebot import types
from config import TELEGRAM_BOT_TOKEN
from src.openai_service import get_ai_response
import time
from charity import CHARITY_ANSWERS
import threading

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Главное меню
main_menu_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons = [
    types.KeyboardButton("Хочу знать больше о раке груди"),
    types.KeyboardButton("Необходимо мнение врача"),
    types.KeyboardButton("Как получить лечение по ОМС бесплатно?"),
    types.KeyboardButton("Как получить помощь Фонда"),
    types.KeyboardButton("Психологическая поддержка"),
    types.KeyboardButton("Хочу оставить отзыв о работе Фонда"),
    types.KeyboardButton("Соедините меня с сотрудником Фонда"),
    types.KeyboardButton("Хочу помочь Фонду"),
]
main_menu_keyboard.add(*buttons)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Что вас интересует?", reply_markup=main_menu_keyboard
    )


def generate_submenu(options):
    submenu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(option) for option in options]
    buttons.append(types.KeyboardButton("Назад"))
    submenu.add(*buttons)
    return submenu


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if text == "назад":
        bot.send_message(
            message.chat.id, "Что вас интересует?", reply_markup=main_menu_keyboard
        )
        return

    responses = {
        "хочу знать больше о раке груди": generate_submenu(
            [
                "Как сохранить здоровье груди",
                "Как узнать свой риск",
                "Как рак груди лечится",
                "Навигатор для пациента",
                "Соедините меня с сотрудником Фонда",
            ]
        ),
        "необходимо мнение врача": generate_submenu(
            [
                "Подозрение на рак",
                "Вопрос онкологу",
                "Вопрос лимфологу",
                "Вопрос эндокринологу",
                "Вопрос диетологу",
                "Вопрос дерматологу",
                "Соедините меня с сотрудником Фонда",
            ]
        ),
        "как получить лечение по омс бесплатно?": generate_submenu(
            [
                "Как попасть к онкологу",
                "Где пройти обследования",
                "Где получить лечение",
                "Где пройти реабилитацию",
                "Где пройти контрольные обследования",
                "Соедините меня с сотрудником Фонда",
            ]
        ),
        "как получить помощь фонда": generate_submenu(
            [
                "Консультация психолога",
                "Консультация онколога",
                "Консультация медицинского юриста",
                "Бесплатное такси к месту лечения",
                "Другие вопросы",
                "Соедините меня с сотрудником Фонда",
                "Скачать пособие для пациентов",
            ]
        ),
        "психологическая поддержка": generate_submenu(
            [
                "Консультация психолога",
                "Группы поддержки",
                "Психологические тренинги",
                "Соедините меня с сотрудником Фонда",
            ]
        ),
        "хочу оставить отзыв о работе фонда": generate_submenu(
            [
                "Хочу поделиться своим опытом",
                "Написать руководителю",
                "Хочу оставить отзыв",
                "Оцените работу Фонда по шкале от 1 до 10",
            ]
        ),
        "хочу помочь фонду": generate_submenu(
            [
                "Юридическое лицо",
                "Частное лицо",
                "Отправить ссылку другу или в соц. сети",
                "Сделать пожертвование",
                "Помочь по-другому",
                "Связаться с руководителем",
            ]
        ),
    }

    if text in responses:
        response_markup = responses[text]
        if isinstance(response_markup, list):
            bot.send_message(message.chat.id, "Соединяем вас с сотрудником Фонда...")
        else:
            bot.send_message(
                message.chat.id,
                f'Вы выбрали "{message.text}". Пожалуйста, выберите:',
                reply_markup=response_markup,
            )
    elif text in CHARITY_ANSWERS:
        if CHARITY_ANSWERS[text].info_type == "link":
            bot.send_message(message.chat.id, CHARITY_ANSWERS[text].name)
        elif CHARITY_ANSWERS[text].info_type == "document":
            pdf_path = CHARITY_ANSWERS[text].file
            with open(pdf_path, "rb") as pdf_file:
                bot.send_document(message.chat.id, pdf_file)
    # elif text in TO_MAKE_TICKETS:
    #     make_ticket(message.chat.id, message.from_user.id)
    else:
        print("AI response")
        process_question(message)
        print("End of AI response")


def handle_ai_response(message, ai_message):
    dots = ""
    for _ in range(20):
        dots += "."
        if len(dots) > 3:
            dots = ""
        bot.edit_message_text(chat_id=message.chat.id, message_id=ai_message.message_id, text=f"Ищем ответ{dots}")
        time.sleep(0.5)


def process_question(message):
    user_question = message.text
    loading_message = bot.send_message(message.chat.id, "Ищем ответ")

    # Запускаем handle_ai_response в отдельном потоке
    thread = threading.Thread(target=handle_ai_response, args=(message, loading_message))
    thread.start()

    # Запрашиваем ответ у AI в основном потоке
    gpt_response = get_ai_response(user_question, message.chat.id)

    thread.join()

    # После получения ответа от AI, отправляем его пользователю
    bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text=gpt_response)


if __name__ == "__main__":
    bot.polling()
