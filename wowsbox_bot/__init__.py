import logging
from typing import Optional

from telegram.ext import Updater

from .commands import register_commands
from .database import get_persistence
from .env import env

TOKEN = env.str('TELEGRAM_TOKEN')

updater: Optional[Updater] = None


def init():
    logging.info('Initializing bot...')

    global updater
    updater = Updater(TOKEN, use_context=True,
                      persistence=get_persistence())

    register_commands(updater.dispatcher)

    logging.info('Bot initialized')


def run():
    if updater is None:
        raise RuntimeError('Please initialize the bot first.')
    updater.start_polling()
    updater.idle()
