import asyncio

from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery

import src.keyboards as kb
from src.config import DEFAULT_COMMANDS
from src.database import Database
from src.keyboards import CATALOG

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
    products = await asyncio.to_thread(fetch_products, category_name)
    if products:
        text = [
            f"https://www.wildberries.ru/catalog/{data[0]}/detail.aspx"
            for data in products
        ]
        await message.answer(
            f"Найдены товары с кэшбэком в категории {category_name}\n" + "\n".join(text)
        )


def fetch_products(category_name):
    with Database("src/data.db") as db:
        return db.filter_product(category_name)


@router.message(Command("select_category"))
async def send_category_buttons(message: types.Message):
    """Функция вывода кнопок с категориями"""
    await message.answer(
        "Выберите категорию:", reply_markup=await kb.keyboard_catalog()
    )


@router.callback_query(lambda call: call.data.startswith("category_"))
async def callback_inline(call: CallbackQuery):
    """Функция вывода кнопок с подкатегориями"""
    category = call.data.split("_")[1]
    subcategories = CATALOG.get(category, [])
    if subcategories:
        await call.message.answer(
            "Выберите подкатегорию:",
            reply_markup=await kb.sub_catalog_keyboard(category),
        )
    else:
        await call.message.answer(f"Подкатегории для категории {category} не найдены.")


@router.callback_query(lambda call: call.data.startswith("subcat_"))
async def callback_product(call: types.CallbackQuery):
    """Функция вывода товаров с кэшбэком через кнопку"""
    subcategory = call.data.split("_")[1]
    match = await search_single_match(CATALOG, subcategory)
    products = await asyncio.to_thread(fetch_products, match)
    if products:
        text = [
            f"https://www.wildberries.ru/catalog/{data[0]}/detail.aspx"
            for data in products
        ]
        await call.message.answer(
            f"Найдены товары с кэшбэком в категории {subcategory}\n" + "\n".join(text)
        )
    else:
        await call.message.answer("В данной категории нет товаров с кэшбэком.")


async def search_single_match(dictionary, substring):
    """
    Асинхронная функция поиска одного совпадения подстроки в словаре,
    где значениями являются списки строк.

    :param dictionary: Словарь, где значениями являются списки строк
    :param substring: Подстрока для поиска
    :return: Первая найденная строка или None
    """

    # Функция для поиска подстроки в списке строк
    def find_match(lst, substring):
        for item in lst:
            if substring in item:
                return item
        return None

    # Создаем задачи для поиска подстроки в каждом списке
    tasks = [
        asyncio.to_thread(find_match, values, substring)
        for values in dictionary.values()
    ]

    # Получаем результаты
    results = await asyncio.gather(*tasks)

    # Находим первое ненулевое совпадение
    for result in results:
        if result:
            return result

    return None
