# asyncio
import asyncio

# config
from src.config import TOKEN

# aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

# database
from src.db_manager import create_table_quotes

#handlers
import handlers


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=None))
dp = Dispatcher()


async def main():
    await create_table_quotes()

    dp.include_router(handlers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())