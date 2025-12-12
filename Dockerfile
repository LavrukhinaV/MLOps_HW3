FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем зависимости
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY app/ .

# Значение версии модели по умолчанию
ENV MODEL_VERSION=v1.0.0

# Запуск сервиса
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
