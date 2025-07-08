FROM python:3.12-slim-bullseye

WORKDIR /bot

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libgomp1 \
    libatomic1 \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей и установка Python-зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование модели Vosk
COPY application/vosk-model-small-ru-0.22 /bot/application/vosk-model-small-ru-0.22

# Копирование исходного кода
COPY . .

ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
