from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.parcer import get_categorise
from aiogram.utils.keyboard import InlineKeyboardBuilder

catalog = get_categorise()


async def keyboard_catalog():
    keyboard = InlineKeyboardBuilder()
    for cat in catalog.keys():
        keyboard.add(InlineKeyboardButton(text=cat, callback_data=f'category_{cat}'))
    return keyboard.adjust(1).as_markup()


async def sub_catalog_keyboard(catalog_name: str):
    keyboard = InlineKeyboardBuilder()
    sub_catalog = catalog.get(catalog_name, [])
    for sub_cat in sub_catalog:
        keyboard.add(InlineKeyboardButton(text=sub_cat, callback_data=f'subcat_{sub_cat}'))
    return keyboard.adjust(2).as_markup()

