import openai
from src.config import OPENAI_API_KEY

openai.apli_key = OPENAI_API_KEY


def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
