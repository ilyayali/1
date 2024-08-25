# Используйте официальный образ Python в качестве базового
FROM python:3.10-slim

# Установите Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Установите переменную окружения для Poetry
ENV PATH="/root/.local/bin:$PATH"

# Создайте рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта
COPY pyproject.toml poetry.lock ./

# Установите зависимости с помощью Poetry
RUN poetry install --no-root

# Скопируйте остальной код приложения
COPY . .

# Откройте порты, если нужно
# EXPOSE 8000

# Запустите команду по умолчанию
CMD ["poetry", "run", "python", "main.py"]
