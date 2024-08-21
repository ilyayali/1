from src.bot import bot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from src.config import DEFAULT_COMMANDS
from src.database import Database
from src.parcer import get_categorise


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
    if len(args) == 1:
        bot.reply_to(message, "Введите название категории")
        return
    category_name = args[1:]
    with Database('data.db') as db:
        category_name = " ".join(category_name)
        products = db.filter_product(category_name)
        text = [f'https://www.wildberries.ru/catalog/{data[0]}/detail.aspx' for data in products]
        bot.reply_to(message, f"Найдены товары с кэшбэком в категории {category_name}\n"+"\n".join(text))

categories = get_categorise()

# Обработчик команды /select_category
@bot.message_handler(commands=['select_category'])
def send_category_buttons(message):
    markup = InlineKeyboardMarkup()
    for category in categories.keys():
        button = InlineKeyboardButton(text=category, callback_data=f"category_{category}")
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def callback_inline(call):
    category = call.data.split('_')[1]
    subcategories = categories.get(category, [])
    markup = InlineKeyboardMarkup()
    if subcategories:
        for subcategory in subcategories:
            print(subcategory)
            button = InlineKeyboardButton(text=subcategory, callback_data=f"products_{subcategory}")
            markup.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите подкатегорию:", reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Подкатегории для категории {category} не найдены.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('products_'))
def callback_product(call):
    subcategory = call.data.split('_')[1]
    with Database('data.db') as db:
        products = db.filter_product(subcategory)
        text = [f'https://www.wildberries.ru/catalog/{data[0]}/detail.aspx' for data in products]
        bot.send_message(call.message.chat.id, f"Найдены товары с кэшбэком в категории {subcategory}\n" + "\n".join(text))

# Обработчик нажатий на подкатегории
@bot.callback_query_handler(func=lambda call: call.data.startswith('subcategory_'))
def callback_subcategory_inline(call):
    subcategory = call.data.split('_')[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Вы выбрали подкатегорию: {subcategory}")