import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from nova.settings import *
from nova_bot.models import *
import requests

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


@dp.message_handler(commands="start")
async def run(message: types.Message):
    if not Users.objects.filter(user_id=message.from_user.id):
        Users.objects.create(
            user_id=message.from_user.id,
            user_name=message.from_user.username
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        keyboard.add(button)
        await message.answer("Привет, а дай номер", reply_markup=keyboard)
    else:
        await message.answer("Кажется мы уже знакомы...")


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact(message: types.Message):
    current_user = Users.objects.get(user_id=message.from_user.id)
    current_user.phone = message.contact['phone_number']
    current_user.save()
    requests.post(url=NOVA_URL, data={"phone": message.contact["phone_number"], "login": message.from_user.username})


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    logging.warning('Bye!')


def start_bot():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
