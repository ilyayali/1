from aiogram import Bot, Dispatcher, types
from src.handlers import router
from src.config import BOT_TOKEN
import asyncio
API_TOKEN = BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def on_startup(dp):
    print("Bot is online!")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True, on_startup=on_startup)

if __name__ == '__main__':
    asyncio.run(main())