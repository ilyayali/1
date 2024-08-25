from aiogram import Bot, Dispatcher

from src.config import BOT_TOKEN
from src.handlers import router

API_TOKEN = BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def on_startup(dp):
    print("Bot is online!")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True, on_startup=on_startup)
