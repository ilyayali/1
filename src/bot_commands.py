from src.bot import bot
from telebot.types import Message
from src.config import DEFAULT_COMMANDS
from src.database import Database


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))


@bot.message_handler(commands=["products"])
def bot_products(message: Message):
    args = message.text.split()
    if len(args) < 1:
        bot.reply_to(message, "Введите название категории")
        return
    category_name = args[1:]
    with Database('data.db') as db:
        category_name = " ".join(category_name)
        products = db.filter_product(category_name)
        text = [f'https://www.wildberries.ru/catalog/{data[0]}/detail.aspx' for data in products]
        bot.reply_to(message, f"Найдены товары с кэшбэком в категории {category_name}\n"+"\n".join(text))