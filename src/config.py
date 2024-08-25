import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Файл .env не найден")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("products <Категория>", "Вывести все с кэшбэком товары в указанной категории"),
    ("help", "Вывести справку"),
    ("select_category", "Выбрать категорию"),
)
