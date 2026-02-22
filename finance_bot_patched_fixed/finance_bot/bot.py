from finance_bot.database_helpers import init_db
init_db()

import asyncio
from aiogram import Bot, Dispatcher
from finance_bot.config import TOKEN
from finance_bot.handlers import start_router, record_router, reports_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(record_router)
dp.include_router(reports_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
