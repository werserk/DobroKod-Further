FROM python:3.12
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы проекта
COPY common_api/src/my_api /app/my_api
COPY common_api/src/processing /app/processing
COPY pyproject.toml poetry.lock /app/

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Указываем команду по умолчанию для запуска контейнера
CMD ["python", "my_api/main.py"]
