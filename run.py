import asyncio
from aiogram import Bot, Dispatcher
from app.config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
