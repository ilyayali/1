from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.parcer import get_categorise

CATALOG = get_categorise()


async def keyboard_catalog():
    keyboard = InlineKeyboardBuilder()
    for cat in CATALOG.keys():
        keyboard.add(InlineKeyboardButton(text=cat, callback_data=f"category_{cat}"))
    return keyboard.adjust(1).as_markup()


async def sub_catalog_keyboard(catalog_name: str):
    keyboard = InlineKeyboardBuilder()
    sub_catalog = CATALOG.get(catalog_name, [])
    for sub_cat in sub_catalog:
        keyboard.add(
            InlineKeyboardButton(text=sub_cat, callback_data=f"subcat_{sub_cat[:15]}")
        )
    return keyboard.adjust(2).as_markup()
