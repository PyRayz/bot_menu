import asyncio

import logging

from aiogram import Bot, Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.handlers import router as user_router

from CONSTANTS import TOKEN

from app.utils.user_utils.update_data_utils import update_data
from app.utils.user_utils.database_utils import create_tables
from app.utils.admin_utils.dates.update_dates import update_dates

schedule = AsyncIOScheduler(timezone="Europe/Moscow")

schedule.add_job(update_data, trigger="cron", hour=0, minute=0)
schedule.add_job(update_dates, trigger="cron", hour=0, minute=1)

bot = Bot(token=TOKEN)

dp = Dispatcher()

logging.basicConfig(
    level=logging.INFO,  # Минимальный уровень логируемых сообщений
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',  # Файл для записи логов
    filemode='a'  # Режим записи ('a' - добавление в конец файла)
)


async def main():
    schedule.start()

    dp.include_router(user_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    create_tables()
    update_data()
    update_dates()

    asyncio.run(main())