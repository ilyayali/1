from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command, CommandStart
from src.config import DEFAULT_COMMANDS
from src.database import Database
from src.parcer import get_categorise
import src.keyboards as kb

categories = get_categorise()

router = Router()


@router.message(CommandStart())
async def bot_start(message: types.Message):
    """Функция команды start"""
    await message.answer(f"Привет, {message.from_user.full_name}!")


@router.message(Command("help"))
async def bot_help(message: types.Message):
    """Функция команды help"""
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    await message.answer("\n".join(text))


@router.message(Command("products"))
async def bot_products(message: types.Message):
    """Функция вывода товаров с кэшбэком запрос в формате /products <Название категории>"""
    args = message.text.split()
    if len(args) == 1:
        await message.answer("Введите название категории")
        return
    category_name = " ".join(args[1:])
    with Database('data.db') as db:
        products = db.filter_product(category_name)
        text = [f'https://www.wildberries.ru/catalog/{data[0]}/detail.aspx' for data in products]
        await message.answer(f"Найдены товары с кэшбэком в категории {category_name}\n" + "\n".join(text))


@router.message(Command("select_category"))
async def send_category_buttons(message: types.Message):
    """Функция вывода кнопок с категориями"""
    await message.answer("Выберите категорию:", reply_markup=await kb.keyboard_catalog())

@router.callback_query(lambda call: call.data.startswith('category_'))
async def callback_inline(call: CallbackQuery):
    """Функция вывода кнопок с подкатегориями"""
    category = call.data.split('_')[1]
    print(category)
    subcategories = categories.get(category, [])
    if subcategories:
        await call.message.answer("Выберите подкатегорию:", reply_markup=await kb.sub_catalog_keyboard(category))
    else:
        await call.message.answer(f"Подкатегории для категории {category} не найдены.")

@router.callback_query(lambda call: call.data.startswith('subcat_'))
async def callback_product(call: types.CallbackQuery):
    """Функция вывода товаров с кэшбэком через кнопку"""
    subcategory = call.data.split('_')[1]
    with Database('data.db') as db:
        products = db.filter_product(subcategory)
        text = [f'https://www.wildberries.ru/catalog/{data[0]}/detail.aspx' for data in products]
        await call.message.answer(f"Найдены товары с кэшбэком в категории {subcategory}\n" + "\n".join(text))