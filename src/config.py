import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Файл .env не найден')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("products <Категория>", "Вывести все с кэшбэком товары в указанной категории"),
)