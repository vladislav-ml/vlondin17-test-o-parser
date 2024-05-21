import os

import requests
from django.template.loader import render_to_string
from dotenv import dotenv_values
from requests.models import Response

from sitemain import settings

config = dotenv_values(settings.NAME_ENV_FILE)


class CommonClass:

    @classmethod
    def get_template(cls, file: str, context: dict) -> str:
        path_file = os.path.join(os.getcwd(), 'api', 'templates', file)
        return render_to_string(path_file, context)

    @classmethod
    def get_correct_phrase(cls, count: int) -> str:
        ending_good = cls.get_ending(count, ['товар', 'товара', 'товаров'])
        return f'{count} {ending_good}'

    @classmethod
    def send_message_tg(cls, count: int) -> Response:
        correct_phrase = cls.get_correct_phrase(count)
        message = cls.get_template('notification.txt', {'count': correct_phrase})
        url_tg = f'https://api.telegram.org/bot{config["TOKEN"]}/sendMessage'
        data = {
            'chat_id': config['ADMIN_ID'],
            'text': message,
        }
        response = requests.post(url_tg, data=data)
        return response

    @classmethod
    def get_ending(cls, number: int, ending_list: list[str]) -> str:
        number = number % 100
        if number >= 11 and number <= 19:
            ending = ending_list[2]
        else:
            i = number % 10
            if i == 1:
                ending = ending_list[0]
            elif i == 2 or i == 3 or i == 4:
                ending = ending_list[1]
            else:
                ending = ending_list[2]
        return ending
