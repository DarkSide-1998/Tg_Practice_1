import asyncio
import logging

from aiogram import Bot
from create_bot import bot, dp

from Routers import routers
from DB_Handlers import db_router

from DataBase import create_db, drop_db, session_maker
# from Middlewares import DataBaseSession


async def on_startup(bot: Bot):
    run_params = False  # Параметры в комм. строке при запуске бота из сервера
    if run_params:
        await drop_db()

    await create_db()


async def on_shutdown(bot: Bot):
    pass


async def main():
    # Прописываем вначале функцию старта бота а затем завершения
    dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    # Включаем все миддлвари тут
    # dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    
    # Здесь включаются роутеры!!
    dp.include_routers(*(*routers, db_router))

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Manual stopping bot.")
