from celery import shared_task

from parsing.common import CommonClass
from parsing.parsing_selenium import ParsingSelenium
from sitemain.settings import logger

from .serializers import ProductSerializer


@shared_task
def parsing_goods_selenium(count: int):
    products = ParsingSelenium(count).parsing_goods()
    addition = 0
    for product in products:
        try:
            serializer_product = ProductSerializer(data=product)
            serializer_product.is_valid(raise_exception=True)
            serializer_product.save()
            addition += 1
        except Exception as e:
            logger.error(f'{type(e)} - {e}')

    resp = CommonClass.send_message_tg(addition)
    if resp.status_code != 200:
        logger.error(f'Notofication in tg error - {resp.status_code}\n{resp.text}')
