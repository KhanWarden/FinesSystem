import asyncio
import redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from app.handlers import calculator, admin
from app.config import API_TOKEN

redis_client = redis.Redis(host='localhost', port=6379, db=0)
storage = RedisStorage(redis_client)
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(calculator.router)


async def main():
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
