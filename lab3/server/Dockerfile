# Используем официальный Python образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости, включая libglib2.0-0
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt /app/

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем серверное приложение
COPY main.py /app/

# Экспонируем порт
EXPOSE 8000

# По умолчанию запускаем серверное приложение с Gunicorn
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
