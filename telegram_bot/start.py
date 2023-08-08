import ast
import logging
import os

import redis
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

redis_client = redis.StrictRedis(
    host='redis',
    port=6379,
    db=0,
    charset='utf-8',
    decode_responses=True
)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def say_hello(message: types.Message):
    await message.answer('Привет, используй /products_list,'
                         ' чтобы получить результат последнего парсинга')


@dp.message_handler(commands=['products_list'])
async def receive_redis_data(message: types.Message):
    """ Функция берет из Redis данные по ключу 'parsing_results',
    форматирует их и отправляет.

    :return: Пронумерованный список товаров: № - Название(ссылка)
    """
    redis_data = redis_client.get('parsing results')

    if redis_data is None:
        await message.answer('Нет данных о последнем парсинге')

    processed_data = ast.literal_eval(redis_data)
    data_to_send = []

    for index, product in enumerate(processed_data, start=1):
        data_to_send.append((index, product['name'], f"https://ozon.ru/product/{product['product_id']}"))

    formatted_message = "\n".join([f"{index} - [{text}]({link})\n" for index, text, link in data_to_send])

    await message.answer(formatted_message, parse_mode=types.ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
