FROM python:3.12-bullseye

WORKDIR /bot

# Копирование зависимостей и установка Python-зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копирование исходного кода
COPY . .

# Настройка прав и локали
RUN chmod 755 /bot
ENV TZ=Europe/Moscow

# Запуск бота с фиксацией на ядрах 0-1
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]