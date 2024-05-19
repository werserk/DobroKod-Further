# telegram_bot/Dockerfile
FROM python:3.12
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

WORKDIR /app

COPY telegram_bot/src/bot /app/bot
COPY pyproject.toml poetry.lock /app/

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

CMD ["python3", "bot/main.py"]
