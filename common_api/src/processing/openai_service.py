import os
import time

from dotenv import load_dotenv
from openai import OpenAI
from telebot import types

from ..my_api.utils import get_user_by_chat_id, update_user_thread_id, add_user

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_response(message: types.Message) -> str:
    chat_id = message.chat.id
    user_id = message.from_user.id
    current_user = get_user_by_chat_id(chat_id)
    if current_user is None:
        current_user = add_user(
            name=message.from_user.first_name,
            chat_id=chat_id,
            user_id=user_id,
        )
    if current_user.thread_id is None:
        thread = client.beta.threads.create()
        update_user_thread_id(user_id, thread.id)

    thread_id = current_user.thread_id

    client.beta.threads.messages.create(
        thread_id=thread_id, content=message.text, role="user"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        time.sleep(1)
    message_response = client.beta.threads.messages.list(thread_id=thread_id)
    latest_message = message_response.data[0]
    return latest_message.content[0].text.value
