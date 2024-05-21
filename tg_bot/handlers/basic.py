from aiogram import Bot
from aiogram.types import Message

from tg_bot.other.db_connect import Request
from tg_bot.settings import settings


async def show_goods(message: Message, bot: Bot, request: Request):
    goods = await request.get_goods_db()
    message = make_message(goods)
    await bot.send_message(settings.bot.admin_id, message, parse_mode='html', disable_web_page_preview=True)


def make_message(goods):
    message = '<b>Список товаров:\n</b>'
    for i, item in enumerate(goods, 1):
        message += f'{i}. {item[0]} - {item[1]}\n'
    return message
