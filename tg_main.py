import asyncio

import aiomysql
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from sitemain.settings import logger
from tg_bot.handlers.basic import show_goods
from tg_bot.middleware.db_middleware import DbSession
from tg_bot.other.commands_bot import set_commands
from tg_bot.settings import settings


async def start_bot(bot: Bot):
    await set_commands(bot)
    logger.info('Бот запущен.')


async def stop_bot(bot: Bot):
    logger.info('Бот остановлен.')


async def create_pool(host, user, password, database, port):
    return await aiomysql.create_pool(host=host, user=user, password=password, db=database, port=int(port))


async def main():
    bot = Bot(settings.bot.bot_token)
    dp = Dispatcher()

    pooling = await create_pool(settings.database.host, settings.database.user, settings.database.password, settings.database.db_name, settings.database.port)

    dp.callback_query.middleware(DbSession(pooling))
    dp.message.middleware(DbSession(pooling))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # hanglers
    dp.message.register(show_goods, Command(commands=['start']))

    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
