import telebot
from config import TELEGRAM_BOT_TOKEN
from handlers.faq_handler import handle_faq
from handlers.questionnaire import handle_questionnaire
from handlers.recommendation import handle_recommendation
from services.openai_service import get_openai_response
from prompts.get_prompt import load_prompt

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id, "Welcome to the support bot! How can I assist you today?"
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    response = (
        handle_faq(user_input)
        or handle_questionnaire(user_input)
        or handle_recommendation(user_input)
    )

    if not response:
        # Request description of who the person is
        bot.send_message(
            message.chat.id,
            "Can you please describe who you are? For example, 'I am the patient' or 'I am the parent'.",
        )
        bot.register_next_step_handler(message, process_description)
    else:
        bot.send_message(message.chat.id, response)


def process_description(message):
    description = message.text
    bot.send_message(message.chat.id, "Thank you. Now, please ask your question.")
    bot.register_next_step_handler(message, process_question, description)


def process_question(message, description):
    user_question = message.text
    basic_prompt = load_prompt("basic_prompt.txt")
    faq_prompt = load_prompt("faq_prompt.txt")

    full_prompt = f"{basic_prompt}\n\n{faq_prompt}\n\nUser: {user_question}\nUser Description: {description}"
    gpt_response = get_openai_response(full_prompt)

    bot.send_message(message.chat.id, gpt_response)


if __name__ == "__main__":
    bot.polling()
