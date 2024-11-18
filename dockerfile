# Этап сборки
FROM python:3.9-alpine AS builder
WORKDIR /app
# Установка необходимых системных пакетов
RUN apk add --update --no-cache postgresql-dev gcc python3-dev musl-dev
# Устанавливаем зависимости
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Этап тесирования
# FROM python:3.9-alpine AS tester
# WORKDIR /tests
# COPY requirements.txt .
# RUN pip install --no-cache-dir --no-deps -r requirements.txt
# COPY . .
# CMD ["pytest"]

# Используем базовый образ Python
FROM python:3.9-alpine AS prod
# Установка необходимых системных пакетов
RUN apk add --update --no-cache libpq curl
# Создаем непривилегированного пользователя
RUN adduser -D appuser
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файл зависимостей и устанавливаем их
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/* && rm -rf /wheels && rm -rf requirements.txt
# Копируем код приложения в контейнер
COPY . .
RUN chown -R appuser:appuser /app
# Переключаемся на непривилегированного пользователя
USER appuser
# Открываем порт 5000 для Flask
EXPOSE 5000
# Команда для запуска приложения с использованием Gunicorn для масштабирования приложения
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]