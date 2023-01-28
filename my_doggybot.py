import os
import logging

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
URL = 'https://api.thedogapi.com/v1/images/search'
BACKUP_URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    format='%(asctime)s, %(name)s, %(levelname)s, %(message)s',
    level=logging.INFO,
)


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as exception:
        logging.error(f'Exception while request to main API {exception}')
        response = requests.get(BACKUP_URL)

    return response.json()[0].get('url')


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/new_dog']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Hello {name}, look what beautiful creature i found for you!',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('new_dog', new_dog))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
