# web_app/Dockerfile
FROM python:3.12
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY web_app/src/web /app/web
COPY common_api/src/my_api /app/common_api
COPY ./data /app/data
COPY pyproject.toml poetry.lock /app/

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

CMD ["streamlit", "run", "web/app.py"]
