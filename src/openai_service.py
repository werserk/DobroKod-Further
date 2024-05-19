from openai import OpenAI
from src.config import OPENAI_API_KEY
import time

ASSISTANT_ID = "asst_LbBRPG5mUmBZeX47iY5gFH8p"

chats = {}

client = OpenAI(api_key=OPENAI_API_KEY)


def get_ai_response(message: str, chat_id: str):
    if chat_id not in chats:
        thread = client.beta.threads.create()
        chats[chat_id] = thread.id

    client.beta.threads.messages.create(
        thread_id=chats[chat_id], content=message, role="user"
    )

    run = client.beta.threads.runs.create(
        thread_id=chats[chat_id], assistant_id=ASSISTANT_ID
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=chats[chat_id], run_id=run.id)
        time.sleep(1)
    message_response = client.beta.threads.messages.list(thread_id=chats[chat_id])
    latest_message = message_response.data[0]
    return latest_message.content[0].text.value
