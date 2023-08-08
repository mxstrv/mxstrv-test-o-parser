import os

import requests


def telegram_notify(number: int) -> None:
    """ Вспомогательная функция для отправки сообщения пользователю
    в телеграм, использующая Telegram HTTP API.

    :param number: Количество товаров, которые были запарсены
    :type number: int
    :return:
    """
    bot_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    message_text = (f"Привет, парсинг Ozon завершен!\n"
                    f"Добавлено {number} товаров")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    params = {
        'chat_id': telegram_chat_id,
        'text': message_text
    }
    requests.post(url, data=params)
