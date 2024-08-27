# Используйте официальный образ Python в качестве базового
FROM python:3.10-slim

RUN apt-get update && apt-get -y install curl

# Установите Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Установите переменную окружения для Poetry
ENV PATH="/root/.local/bin:$PATH"

# Создайте рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта
COPY pyproject.toml poetry.lock ./

# Установите зависимости с помощью Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Скопируйте остальной код приложения
COPY . .

# Откройте порты, если нужно
# EXPOSE 8000




