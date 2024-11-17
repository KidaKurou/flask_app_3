# Этап сборки
FROM python:3.9-alpine as builder
WORKDIR /app
# Установка необходимых системных пакетов
RUN apk add --update --no-cache postgresql-dev gcc python3-dev musl-dev
# Устанавливаем зависимости
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Используем базовый образ Python
FROM python:3.9-alpine
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