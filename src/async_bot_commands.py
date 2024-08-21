from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
from src.config import DEFAULT_COMMANDS
from src.database import Database
from src.parcer import get_categorise
from src.config import BOT_TOKEN
import asyncio
API_TOKEN = BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

categories = get_categorise()

@dp.message(Command("start"))
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message(Command("help"))
async def bot_help(message: types.Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    await message.answer("\n".join(text))

@dp.message(Command("products"))
async def bot_products(message: types.Message):
    args = message.text.split()
    if len(args) == 1:
        await message.answer("Введите название категории")
        return
    category_name = " ".join(args[1:])
    with Database('data.db') as db:
        products = db.filter_product(category_name)
        text = [f'https://www.wildberries.ru/catalog/{data[0]}/detail.aspx' for data in products]
        await message.answer(f"Найдены товары с кэшбэком в категории {category_name}\n" + "\n".join(text))

@dp.message(Command("select_category"))
async def send_category_buttons(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)  # Specify row_width if necessary
    for category in categories.keys():
        button = InlineKeyboardButton(text=category, callback_data=f"category_{category}")
        markup.add(button)
    await message.answer("Выберите категорию:", reply_markup=markup)

@dp.callback_query(lambda call: call.data.startswith('category_'))
async def callback_inline(call: types.CallbackQuery):
    category = call.data.split('_')[1]
    subcategories = categories.get(category, [])
    markup = InlineKeyboardMarkup(row_width=1)  # Specify row_width if necessary
    if subcategories:
        for subcategory in subcategories:
            button = InlineKeyboardButton(text=subcategory, callback_data=f"products_{subcategory}")
            markup.add(button)
        await call.message.edit_text("Выберите подкатегорию:", reply_markup=markup)
    else:
        await call.message.edit_text(f"Подкатегории для категории {category} не найдены.")

@dp.callback_query(lambda call: call.data.startswith('products_'))
async def callback_product(call: types.CallbackQuery):
    subcategory = call.data.split('_')[1]
    with Database('data.db') as db:
        products = db.filter_product(subcategory)
        text = [f'https://www.wildberries.ru/catalog/{data[0]}/detail.aspx' for data in products]
        await call.message.answer(f"Найдены товары с кэшбэком в категории {subcategory}\n" + "\n".join(text))

async def on_startup(dp):
    print("Bot is online!")
async def main():
    await dp.start_polling(bot, skip_updates=True, on_startup=on_startup)

if __name__ == '__main__':
    asyncio.run(main())