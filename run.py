import asyncio
import redis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
redis_client = redis.Redis(host='localhost', port=6379, db=0)
storage = RedisStorage(redis_client)


async def main():
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
